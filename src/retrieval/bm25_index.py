"""
Stage 6 — BM25 Keyword Indexing & Retrieval
Builds, serializes, and loads a rank_bm25 keyword index over scheme chunks
for exact matching of scheme titles, numbers, and specific eligibility terms.
"""

import os
import json
import pickle
import re
import logging
from pathlib import Path
from typing import List, Dict, Any, Tuple
from rank_bm25 import BM25Okapi

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

def tokenize(text: str) -> List[str]:
    """Tokenizes text by lowercasing and extracting alphanumeric terms."""
    clean_text = re.sub(r'[^a-zA-Z0-9\s]', ' ', text.lower())
    return [word for word in clean_text.split() if len(word) > 1]

class SchemeBM25Index:
    def __init__(self, index_file: str = None):
        base_dir = Path(__file__).resolve().parent.parent.parent
        if index_file is None:
            index_file = base_dir / "data" / "processed" / "bm25_index.pkl"
        else:
            index_file = Path(index_file)
            
        self.index_file = index_file
        self.bm25 = None
        self.chunks = []

    def build_and_save_index(self, chunks_file: str = None) -> int:
        """Reads chunk JSON, tokenizes texts, builds BM25 index, and serializes to disk."""
        base_dir = Path(__file__).resolve().parent.parent.parent
        if chunks_file is None:
            chunks_file = base_dir / "data" / "processed" / "chunks_with_metadata.json"
        else:
            chunks_file = Path(chunks_file)

        if not os.path.exists(chunks_file):
            raise FileNotFoundError(f"Chunks JSON file not found at {chunks_file}")

        with open(chunks_file, "r", encoding="utf-8") as f:
            self.chunks = json.load(f)

        if not self.chunks:
            logger.warning("No chunks available for BM25 indexing.")
            return 0

        logger.info(f"Tokenizing {len(self.chunks)} chunks for BM25 indexing...")
        corpus = [
            tokenize(f"{c['scheme_name']} {c['section_title']} {c['category']} {c['target_group']} {c['text']}")
            for c in self.chunks
        ]

        self.bm25 = BM25Okapi(corpus)

        # Save index and chunks mapping
        os.makedirs(self.index_file.parent, exist_ok=True)
        with open(self.index_file, "wb") as f:
            pickle.dump({"bm25": self.bm25, "chunks": self.chunks}, f)

        logger.info(f"BM25 index saved successfully to {self.index_file}")
        return len(self.chunks)

    def load_index(self) -> bool:
        """Loads serialized BM25 index from disk if available."""
        if not os.path.exists(self.index_file):
            logger.info(f"BM25 index file not found at {self.index_file}. Will build new index.")
            return False

        with open(self.index_file, "rb") as f:
            data = pickle.load(f)
            self.bm25 = data["bm25"]
            self.chunks = data["chunks"]

        logger.info(f"Loaded BM25 index from {self.index_file} ({len(self.chunks)} chunks).")
        return True

    def search(self, query: str, top_k: int = 10) -> List[Tuple[Dict[str, Any], float]]:
        """
        Executes BM25 search for query string and returns top_k chunks with scores.
        """
        if self.bm25 is None or not self.chunks:
            if not self.load_index():
                self.build_and_save_index()

        tokenized_query = tokenize(query)
        if not tokenized_query:
            return []

        scores = self.bm25.get_scores(tokenized_query)
        scored_chunks = list(zip(self.chunks, scores))
        # Sort descending by score
        scored_chunks.sort(key=lambda x: x[1], reverse=True)

        return [(chunk, score) for chunk, score in scored_chunks[:top_k] if score > 0.0]

if __name__ == "__main__":
    index = SchemeBM25Index()
    index.build_and_save_index()
    results = index.search("PMEGP subsidy for rural women", top_k=3)
    
    print("\n" + "="*70)
    print("             STAGE 6: BM25 INDEX VERIFICATION REPORT              ")
    print("="*70)
    print(f"Total Chunks Indexed : {len(index.chunks)}")
    print(f"Query: 'PMEGP subsidy for rural women'")
    print("-" * 70)
    for chunk, score in results:
        print(f" • Score: {score:.4f} | {chunk['scheme_name']} | {chunk['section_title']}")
    print("="*70 + "\n")
