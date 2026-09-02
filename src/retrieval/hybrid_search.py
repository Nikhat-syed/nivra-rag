"""
Stage 7 — Hybrid Retrieval Engine (Qdrant Dense + BM25 Sparse + Reciprocal Rank Fusion)
Combines semantic vector search with keyword matching using RRF rank fusion
and supports metadata pre-filtering (category, target_group, state_or_central).
"""

import logging
from typing import List, Dict, Any, Optional
from pathlib import Path

from src.retrieval.embed_store import SchemeVectorStore, COLLECTION_NAME
from src.retrieval.bm25_index import SchemeBM25Index

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

class HybridRetriever:
    def __init__(self, rrf_k: int = 60):
        self.rrf_k = rrf_k
        self.vector_store = SchemeVectorStore()
        self.bm25_index = SchemeBM25Index()

    def filter_chunk_by_metadata(self, chunk: Dict[str, Any], metadata_filter: Dict[str, Any]) -> bool:
        """Helper to match chunk metadata against filter dict."""
        if not metadata_filter:
            return True
        for key, val in metadata_filter.items():
            if not val:
                continue
            chunk_val = chunk.get(key, "").lower()
            target_val = str(val).lower()
            if key == "category" and chunk_val != target_val:
                return False
            elif key == "target_group" and target_val not in chunk_val and chunk_val not in target_val:
                return False
            elif key == "state_or_central" and target_val not in chunk_val and chunk_val != "national":
                return False
        return True

    def semantic_search(
        self, query: str, top_k: int = 20, metadata_filter: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """Runs vector semantic search on Qdrant."""
        try:
            query_vector = self.vector_store.encoder.encode([query])[0]
            search_results = self.vector_store.client.query_points(
                collection_name=COLLECTION_NAME,
                query=query_vector,
                limit=top_k * 2
            ).points

            results = []
            for item in search_results:
                payload = item.payload
                if self.filter_chunk_by_metadata(payload, metadata_filter):
                    payload_copy = payload.copy()
                    payload_copy["vector_score"] = float(item.score)
                    results.append(payload_copy)
                    if len(results) >= top_k:
                        break
            return results
        except Exception as e:
            logger.warning(f"Dense vector search failed: {e}. Falling back to empty results.")
            return []

    def bm25_search(
        self, query: str, top_k: int = 20, metadata_filter: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """Runs sparse keyword search using BM25."""
        raw_results = self.bm25_index.search(query, top_k=top_k * 2)
        results = []
        for chunk, score in raw_results:
            if self.filter_chunk_by_metadata(chunk, metadata_filter):
                chunk_copy = chunk.copy()
                chunk_copy["bm25_score"] = float(score)
                results.append(chunk_copy)
                if len(results) >= top_k:
                    break
        return results

    def hybrid_search(
        self, query: str, top_k: int = 5, metadata_filter: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Executes parallel Semantic and BM25 search, fusing results via RRF.
        RRF Score(d) = sum(1 / (k + rank_m(d)))
        """
        dense_results = self.semantic_search(query, top_k=20, metadata_filter=metadata_filter)
        bm25_results = self.bm25_search(query, top_k=20, metadata_filter=metadata_filter)

        rrf_scores: Dict[str, float] = {}
        chunk_map: Dict[str, Dict[str, Any]] = {}

        # Process dense ranks
        for rank, chunk in enumerate(dense_results, start=1):
            cid = chunk["chunk_id"]
            chunk_map[cid] = chunk
            rrf_scores[cid] = rrf_scores.get(cid, 0.0) + (1.0 / (self.rrf_k + rank))

        # Process BM25 ranks
        for rank, chunk in enumerate(bm25_results, start=1):
            cid = chunk["chunk_id"]
            chunk_map[cid] = chunk
            rrf_scores[cid] = rrf_scores.get(cid, 0.0) + (1.0 / (self.rrf_k + rank))

        # Sort chunks by fused RRF score descending
        sorted_cids = sorted(rrf_scores.keys(), key=lambda cid: rrf_scores[cid], reverse=True)

        final_chunks = []
        for cid in sorted_cids[:top_k]:
            chunk = chunk_map[cid].copy()
            chunk["rrf_score"] = rrf_scores[cid]
            final_chunks.append(chunk)

        return final_chunks

if __name__ == "__main__":
    retriever = HybridRetriever()
    test_query = "What business loan schemes offer subsidies for rural women entrepreneurs?"
    test_filter = {"category": "loan"}
    
    results = retriever.hybrid_search(test_query, top_k=5, metadata_filter=test_filter)

    print("\n" + "="*70)
    print("             STAGE 7: HYBRID SEARCH VERIFICATION REPORT            ")
    print("="*70)
    print(f"Query           : '{test_query}'")
    print(f"Metadata Filter : {test_filter}")
    print("-" * 70)
    for i, c in enumerate(results, start=1):
        print(f" {i}. [{c['scheme_name']}] (RRF Score: {c['rrf_score']:.5f})")
        print(f"    Section : {c['section_title']} | Target: {c['target_group']} | State: {c['state_or_central']}")
        print(f"    Subsidy : {c.get('subsidy', 'N/A')} | Max Loan: {c.get('max_loan_amount', 'N/A')}")
        print(f"    Snippet : {c['text'][:140]}...")
        print("-" * 70)
    print("="*70 + "\n")
