import React, { useState } from 'react';
import { Send, Sparkles, BookOpen, FileCheck } from 'lucide-react';

export default function AskQuestion({ language, plainLanguage, retrievalMode }) {
  const [question, setQuestion] = useState('');
  const [error, setError] = useState(null);

  const handleAsk = async (e) => {
    e.preventDefault();
    if (!question.trim()) return;

    setLoading(true);
    setError(null);
    try {
      const res = await fetch('/api/ask', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          query: question,
          language: language,
          plain_language: plainLanguage,
          mode: retrievalMode
        })
      });
      if (!res.ok) {
        throw new Error(`Server returned status ${res.status}`);
      }
      const data = await res.json();
      setResult(data);
    } catch (err) {
      console.error("Ask query failed:", err);
      setError("Unable to reach answer synthesis engine. Please try again in a moment.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: '900px' }}>
      <div style={{ marginBottom: '24px' }}>
        <h1 style={{ fontSize: '1.6rem', fontWeight: '800', color: 'var(--primary-dark)', marginBottom: '4px' }}>
          💬 Ask Nivra
        </h1>
        <p style={{ color: 'var(--text-muted)', fontSize: '0.92rem' }}>
          Ask questions in plain English, Telugu (తెలుగు), or Hindi (हिन्दी). Answers are strictly grounded in official documents.
        </p>
      </div>

      {/* Question Form */}
      <form onSubmit={handleAsk} style={{ marginBottom: '32px' }}>
        <div style={{ background: 'var(--bg-surface)', padding: '20px', borderRadius: '16px', border: '2px solid var(--border-color)', boxShadow: 'var(--shadow-sm)' }}>
          <textarea
            rows={3}
            className="search-box"
            style={{ border: 'none', resize: 'none', padding: '0', fontSize: '1.05rem', background: 'transparent' }}
            placeholder="Type your question (e.g. Can a woman starting a tailoring business get a loan without collateral?)..."
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
          />
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginTop: '16px', borderTop: '1px solid var(--border-color)', paddingTop: '12px' }}>
            <span style={{ fontSize: '0.82rem', color: 'var(--text-muted)' }}>
              🌐 Language: <strong>{language}</strong> | Mode: <strong>{retrievalMode}</strong>
            </span>
            <button type="submit" className="btn-primary" disabled={loading}>
              <Send size={16} />
              <span>{loading ? 'Synthesizing Answer...' : 'Ask Question'}</span>
            </button>
          </div>
        </div>
      </form>

      {/* Error Feedback Card */}
      {error && (
        <div style={{ background: '#FEF2F2', border: '1px solid #FCA5A5', color: '#991B1B', borderRadius: '16px', padding: '16px 20px', marginBottom: '24px', fontSize: '0.92rem' }}>
          ⚠️ {error}
        </div>
      )}

      {/* Answer Output */}
      {result && (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
          {/* Plain Language Summary Card */}
          {plainLanguage && (
            <div style={{ background: 'var(--primary-light)', border: '1px solid var(--border-color)', borderRadius: '16px', padding: '24px' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '10px', color: 'var(--primary-dark)', fontWeight: '700', fontSize: '1.05rem', marginBottom: '12px' }}>
                <Sparkles size={20} color="var(--primary)" />
                <span>Simplified Plain-Language Summary ({language})</span>
              </div>
              <div style={{ color: 'var(--text-main)', fontSize: '0.95rem', whiteSpace: 'pre-line', lineHeight: '1.6' }}>
                {result.translated_plain_answer}
              </div>
            </div>
          )}

          {/* Official Grounded Answer */}
          <div style={{ background: 'var(--bg-card)', border: '1px solid var(--border-color)', borderRadius: '16px', padding: '24px', boxShadow: 'var(--shadow-sm)' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px', color: 'var(--primary-dark)', fontWeight: '700', fontSize: '1.05rem', marginBottom: '12px' }}>
              <BookOpen size={20} color="var(--primary)" />
              <span>Official Wording & Citations</span>
            </div>
            <div style={{ color: 'var(--text-secondary)', fontSize: '0.94rem', whiteSpace: 'pre-line', lineHeight: '1.6' }}>
              {result.official_answer}
            </div>

            {/* Citations Footer */}
            <div style={{ marginTop: '20px', borderTop: '1px solid var(--border-color)', paddingTop: '16px' }}>
              <h4 style={{ fontSize: '0.85rem', color: 'var(--text-muted)', fontWeight: '700', marginBottom: '8px' }}>
                📍 Referenced Scheme Documents:
              </h4>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '6px' }}>
                {result.citations && result.citations.map((c, i) => (
                  <div key={i} style={{ fontSize: '0.82rem', color: 'var(--text-secondary)', display: 'flex', alignItems: 'center', gap: '6px' }}>
                    <FileCheck size={14} color="var(--primary)" />
                    <span><strong>{c.scheme_name}</strong> — {c.section_title} ({c.source_file})</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
