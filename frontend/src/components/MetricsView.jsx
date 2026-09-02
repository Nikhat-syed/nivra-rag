import React, { useState, useEffect } from 'react';
import { TrendingUp, Layers, CheckCircle } from 'lucide-react';

export default function MetricsView() {
  const [metrics, setMetrics] = useState([]);

  useEffect(() => {
    fetch('/api/metrics')
      .then(res => res.json())
      .then(data => setMetrics(data.metrics || []))
      .catch(err => console.error("Metrics fetch failed:", err));
  }, []);

  return (
    <div style={{ maxWidth: '960px' }}>
      <div style={{ marginBottom: '28px' }}>
        <h1 style={{ fontSize: '1.6rem', fontWeight: '800', color: 'var(--primary-dark)', marginBottom: '4px' }}>
          ⚙️ RAG System Architecture & Evaluation Metrics
        </h1>
        <p style={{ color: 'var(--text-muted)', fontSize: '0.92rem' }}>
          Comparative evaluation results across 20 ground-truth QA benchmark test items.
        </p>
      </div>

      {/* Metrics Cards Grid */}
      <div className="grid-3" style={{ gridTemplateColumns: 'repeat(auto-fill, minmax(220px, 1fr))', marginBottom: '36px' }}>
        {metrics.map((m, i) => (
          <div key={i} style={{ background: 'var(--bg-card)', border: '1px solid var(--border-color)', borderRadius: '16px', padding: '20px', boxShadow: 'var(--shadow-sm)' }}>
            <span style={{ fontSize: '0.82rem', fontWeight: '700', color: 'var(--text-muted)', display: 'block', marginBottom: '8px' }}>
              {m.name}
            </span>
            <div style={{ fontSize: '1.8rem', fontWeight: '800', color: 'var(--primary-dark)', marginBottom: '4px' }}>
              {m.hybrid_rrf}
            </div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '4px', fontSize: '0.82rem', color: '#047857', fontWeight: '700' }}>
              <TrendingUp size={14} />
              <span>{m.improvement} vs. Semantic</span>
            </div>
          </div>
        ))}
      </div>

      {/* Technical Stack Description */}
      <div style={{ background: 'var(--bg-card)', border: '1px solid var(--border-color)', borderRadius: '20px', padding: '28px' }}>
        <h3 style={{ fontSize: '1.1rem', fontWeight: '800', color: 'var(--primary-dark)', marginBottom: '16px', display: 'flex', alignItems: 'center', gap: '8px' }}>
          <Layers size={20} color="var(--primary)" />
          <span>Complete Technical RAG Architecture</span>
        </h3>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '16px' }}>
          {[
            { title: 'Docling Ingestion Engine', desc: 'Extracts structured markdown & preserves tables from raw government PDFs.' },
            { title: 'Semantic Section Chunking', desc: 'Header-aware logical section splitting with rich metadata tags (category, state, target group).' },
            { title: 'Qdrant Vector Engine', desc: '384-dimensional dense vector embeddings using SentenceTransformers (all-MiniLM-L6-v2).' },
            { title: 'BM25 Sparse Keyword Index', desc: 'Rank_bm25 serialized index ensuring exact match for scheme acronyms and numerical limits.' },
            { title: 'Reciprocal Rank Fusion (RRF)', desc: 'Blends dense semantic rankings and sparse BM25 rankings (k=60) for maximum precision.' },
            { title: 'Groq Grounded Generator', desc: 'Strict context prompt grounding (Llama-3.3-70b) with deep-translator Telugu & Hindi support.' }
          ].map((item, idx) => (
            <div key={idx} style={{ background: 'var(--bg-surface-subtle)', padding: '14px', borderRadius: '12px', display: 'flex', gap: '10px', border: '1px solid var(--border-color)' }}>
              <CheckCircle size={18} color="var(--primary)" style={{ flexShrink: 0, marginTop: '2px' }} />
              <div>
                <strong style={{ fontSize: '0.88rem', color: 'var(--primary-dark)', display: 'block', marginBottom: '2px' }}>{item.title}</strong>
                <span style={{ fontSize: '0.82rem', color: 'var(--text-muted)' }}>{item.desc}</span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
