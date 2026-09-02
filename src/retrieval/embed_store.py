"""
Stage 5 — Embeddings Generation & Qdrant Vector Store
Generates dense vector embeddings using SentenceTransformers (all-MiniLM-L6-v2)
or robust Hashing/TFIDF vectorizer fallback.
Stores vectors with full metadata payload in a local Qdrant collection.
Auto-initializes and populates embeddings if collection is empty.
"""

import os
import json
import logging
from pathlib import Path
from typing import List, Dict, Any

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

COLLECTION_NAME = "scheme_chunks"
_QDRANT_SINGLETON_CLIENT = None

class SchemeVectorEncoder:
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        self.use_st = False
        self.st_model = None
        
        try:
            from sentence_transformers import SentenceTransformer
            logger.info(f"Loading SentenceTransformer model: {model_name}...")
            self.st_model = SentenceTransformer(model_name)
            self.dim = self.st_model.get_embedding_dimension() if hasattr(self.st_model, "get_embedding_dimension") else self.st_model.get_sentence_embedding_dimension()
            self.use_st = True
            logger.info(f"SentenceTransformer loaded successfully (Dim: {self.dim}).")
        except Exception as e:
            logger.warning(f"SentenceTransformer fallback mode active: {e}.")
            from sklearn.feature_extraction.text import HashingVectorizer
            self.dim = 384
            self.vectorizer = HashingVectorizer(n_features=384, norm='l2', alternate_sign=False)

    def encode(self, texts: List[str], normalize_embeddings: bool = True) -> List[List[float]]:
        if self.use_st and self.st_model is not None:
            embeddings = self.st_model.encode(texts, show_progress_bar=False, normalize_embeddings=normalize_embeddings)
            return embeddings.tolist()
        else:
            sparse_matrix = self.vectorizer.transform(texts)
            return sparse_matrix.toarray().tolist()

class SchemeVectorStore:
    def __init__(self, db_path: str = None):
        global _QDRANT_SINGLETON_CLIENT
        base_dir = Path(__file__).resolve().parent.parent.parent
        if db_path is None:
            db_path = str(base_dir / "data" / "qdrant_db")
            
        self.db_path = db_path
        os.makedirs(db_path, exist_ok=True)
        
        if _QDRANT_SINGLETON_CLIENT is not None:
            self.client = _QDRANT_SINGLETON_CLIENT
        else:
            try:
                logger.info(f"Initializing Qdrant client at local path: {db_path}")
                self.client = QdrantClient(path=db_path)
                _QDRANT_SINGLETON_CLIENT = self.client
            except Exception as e:
                logger.warning(f"Local file storage lock active ({e}). Initializing Qdrant in-memory client.")
                self.client = QdrantClient(location=":memory:")
                _QDRANT_SINGLETON_CLIENT = self.client

        self.encoder = SchemeVectorEncoder()
        self.vector_dim = self.encoder.dim
        
        # Ensure collection exists and is populated
        self.ensure_collection_ready()

    def ensure_collection_ready(self):
        """Auto-builds embeddings if collection is missing or empty."""
        try:
            collections = [c.name for c in self.client.get_collections().collections]
            if COLLECTION_NAME not in collections or self.client.get_collection(COLLECTION_NAME).points_count == 0:
                self.build_and_store_embeddings()
        except Exception as e:
            logger.warning(f"Auto-populating collection: {e}")
            self.build_and_store_embeddings()

    def init_collection(self, force_recreate: bool = True):
        """Initializes or recreates Qdrant collection with cosine distance."""
        try:
            collections = [c.name for c in self.client.get_collections().collections]
            if COLLECTION_NAME in collections:
                if force_recreate:
                    logger.info(f"Recreating collection '{COLLECTION_NAME}'...")
                    self.client.delete_collection(COLLECTION_NAME)
                    self.client.create_collection(
                        collection_name=COLLECTION_NAME,
                        vectors_config=VectorParams(size=self.vector_dim, distance=Distance.COSINE)
                    )
            else:
                logger.info(f"Creating new collection '{COLLECTION_NAME}'...")
                self.client.create_collection(
                    collection_name=COLLECTION_NAME,
                    vectors_config=VectorParams(size=self.vector_dim, distance=Distance.COSINE)
                )
        except Exception as e:
            logger.warning(f"Collection init exception handled: {e}")

    def build_and_store_embeddings(self, chunks_file: str = None, batch_size: int = 32) -> int:
        """
        Embeds chunks in batches and upserts vectors + metadata into Qdrant.
        """
        base_dir = Path(__file__).resolve().parent.parent.parent
        if chunks_file is None:
            chunks_file = base_dir / "data" / "processed" / "chunks_with_metadata.json"
        else:
            chunks_file = Path(chunks_file)

        if not os.path.exists(chunks_file):
            logger.warning(f"Chunks JSON not found at {chunks_file}. Cannot auto-embed.")
            return 0

        with open(chunks_file, "r", encoding="utf-8") as f:
            chunks: List[Dict[str, Any]] = json.load(f)

        if not chunks:
            logger.warning("No chunks found to embed.")
            return 0

        self.init_collection(force_recreate=True)
        logger.info(f"Generating embeddings for {len(chunks)} chunks in batches of {batch_size}...")

        points = []
        for i in range(0, len(chunks), batch_size):
            batch = chunks[i:i + batch_size]
            texts_to_embed = [
                f"Scheme: {c['scheme_name']}. Section: {c['section_title']}. Content: {c['text']}"
                for c in batch
            ]
            embeddings = self.encoder.encode(texts_to_embed)

            for idx, (chunk, vector) in enumerate(zip(batch, embeddings)):
                point_id = i + idx + 1
                points.append(
                    PointStruct(
                        id=point_id,
                        vector=vector,
                        payload=chunk
                    )
                )

        logger.info(f"Upserting {len(points)} vector points into Qdrant collection '{COLLECTION_NAME}'...")
        self.client.upsert(collection_name=COLLECTION_NAME, points=points)
        logger.info("Upsert completed successfully.")
        return len(points)

    def test_qdrant_storage(self) -> dict:
        """
        Verifies vector store stats and performs a test similarity search.
        """
        collection_info = self.client.get_collection(COLLECTION_NAME)
        points_count = collection_info.points_count
        
        # Test Search Query
        test_query = "What is the loan limit for Stand-Up India scheme for women?"
        query_vector = self.encoder.encode([test_query])[0]
        
        search_results = self.client.query_points(
            collection_name=COLLECTION_NAME,
            query=query_vector,
            limit=3
        ).points

        print("\n" + "="*70)
        print("          STAGE 5: VECTOR STORE VERIFICATION REPORT               ")
        print("="*70)
        print(f"Qdrant Collection      : {COLLECTION_NAME}")
        print(f"Total Stored Vectors   : {points_count}")
        print(f"Vector Dimension       : {self.vector_dim}")
        print("-" * 70)
        print(f"Test Query: '{test_query}'")
        print("Top Matches Returned:")
        for res in search_results:
            payload = res.payload
            print(f" • Score: {res.score:.4f} | {payload.get('scheme_name')} | {payload.get('section_title')}")
        print("="*70 + "\n")

        return {
            "collection": COLLECTION_NAME,
            "points_count": points_count,
            "top_test_matches": len(search_results)
        }

if __name__ == "__main__":
    store = SchemeVectorStore()
    stored_count = store.build_and_store_embeddings()
    store.test_qdrant_storage()
