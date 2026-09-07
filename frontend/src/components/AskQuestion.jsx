import React, { useState } from 'react';
import { Send, Sparkles, BookOpen, FileCheck, Bot, ShieldCheck, Zap, HelpCircle, ArrowRight } from 'lucide-react';

export default function AskQuestion({ language, plainLanguage, retrievalMode }) {
  const [activeBot, setActiveBot] = useState('scheme'); // 'scheme' or 'universal'
  const [question, setQuestion] = useState('');
  const [loading, setLoading] = useState(false);
  const [schemeResult, setSchemeResult] = useState(null);
  const [universalResult, setUniversalResult] = useState(null);
  const [error, setError] = useState(null);

  const samplePrompts = [
    "How do I price my handmade garments or products?",
    "Give me a 30-day Instagram marketing plan for my boutique",
    "How to manage cash flow and budgeting for a small business?",
    "Tips for pitching my business idea to local banks and customers"
  ];

  const handleAskScheme = async (queryText) => {
    const q = queryText || question;
    if (!q.trim()) return;

    setLoading(true);
    setError(null);
    try {
      const res = await fetch('/api/ask', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          query: q,
          language: language,
          plain_language: plainLanguage,
          mode: retrievalMode
        })
      });
      if (!res.ok) throw new Error(`Server returned status ${res.status}`);
      const data = await res.json();
      setSchemeResult(data);
    } catch (err) {
      console.error("Scheme query failed:", err);
      setError("Unable to reach Nivra Scheme Engine. Please try again in a moment.");
    } finally {
      setLoading(false);
    }
  };

  const handleAskUniversal = async (queryText) => {
    const q = queryText || question;
    if (!q.trim()) return;

    setLoading(true);
    setError(null);
    try {
      const res = await fetch('/api/ask', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          query: q,
          language: language,
          mode: 'universal'
        })
      });
      if (!res.ok) throw new Error(`Server returned status ${res.status}`);
      const data = await res.json();
      setUniversalResult(data);
    } catch (err) {
      console.error("Universal query failed:", err);
      setError("Unable to reach OpenAI Universal Assistant. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (activeBot === 'scheme') {
      handleAskScheme();
    } else {
      handleAskUniversal();
    }
  };

  const handleSampleClick = (prompt) => {
    setQuestion(prompt);
    if (activeBot === 'scheme') {
      handleAskScheme(prompt);
    } else {
      handleAskUniversal(prompt);
    }
  };

  return (
    <div style={{ maxWidth: '920px', margin: '0 auto' }}>
      {/* Page Header */}
      <div style={{ marginBottom: '24px' }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '12px' }}>
          <div>
            <h1 style={{ fontSize: '1.75rem', fontWeight: '800', color: 'var(--primary-dark)', marginBottom: '4px', display: 'flex', alignItems: 'center', gap: '10px' }}>
              <span>💬 Ask Nivra AI</span>
            </h1>
            <p style={{ color: 'var(--text-muted)', fontSize: '0.94rem' }}>
              Choose your specialized AI assistant: Grounded Scheme Advisor or OpenAI Universal Bot for everything else.
            </p>
          </div>
        </div>
      </div>

      {/* Bot Switcher Tabs */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: '1fr 1fr',
        gap: '12px',
        marginBottom: '24px',
        background: 'var(--bg-surface)',
        padding: '6px',
        borderRadius: '16px',
        border: '1px solid var(--border-color)'
      }}>
        <button
          type="button"
          onClick={() => setActiveBot('scheme')}
          style={{
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            gap: '10px',
            padding: '14px 18px',
            borderRadius: '12px',
            border: 'none',
            fontWeight: '700',
            fontSize: '0.95rem',
            cursor: 'pointer',
            transition: 'all 0.2s ease',
            background: activeBot === 'scheme' ? 'var(--primary-dark)' : 'transparent',
            color: activeBot === 'scheme' ? '#ffffff' : 'var(--text-muted)',
            boxShadow: activeBot === 'scheme' ? '0 4px 12px rgba(136, 14, 79, 0.25)' : 'none'
          }}
        >
          <ShieldCheck size={20} />
          <span>🏛️ Scheme RAG Bot</span>
          <span style={{
            fontSize: '0.72rem',
            padding: '2px 8px',
            borderRadius: '20px',
            background: activeBot === 'scheme' ? 'rgba(255,255,255,0.2)' : 'var(--border-color)',
            color: activeBot === 'scheme' ? '#ffffff' : 'var(--text-main)'
          }}>Grounded</span>
        </button>

        <button
          type="button"
          onClick={() => setActiveBot('universal')}
          style={{
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            gap: '10px',
            padding: '14px 18px',
            borderRadius: '12px',
            border: 'none',
            fontWeight: '700',
            fontSize: '0.95rem',
            cursor: 'pointer',
            transition: 'all 0.2s ease',
            background: activeBot === 'universal' ? 'linear-gradient(135deg, #7C3AED 0%, #C026D3 100%)' : 'transparent',
            color: activeBot === 'universal' ? '#ffffff' : 'var(--text-muted)',
            boxShadow: activeBot === 'universal' ? '0 4px 14px rgba(124, 58, 237, 0.3)' : 'none'
          }}
        >
          <Zap size={20} />
          <span>✨ Nivra Universal AI</span>
          <span style={{
            fontSize: '0.72rem',
            padding: '2px 8px',
            borderRadius: '20px',
            background: activeBot === 'universal' ? 'rgba(255,255,255,0.25)' : 'var(--border-color)',
            color: activeBot === 'universal' ? '#ffffff' : 'var(--text-main)'
          }}>OpenAI</span>
        </button>
      </div>

      {/* Description Card depending on active bot */}
      <div style={{
        background: activeBot === 'scheme' ? 'var(--primary-light)' : '#F3E8FF',
        border: `1px solid ${activeBot === 'scheme' ? 'var(--border-color)' : '#DDD6FE'}`,
        borderRadius: '14px',
        padding: '14px 20px',
        marginBottom: '20px',
        fontSize: '0.88rem',
        color: activeBot === 'scheme' ? 'var(--primary-dark)' : '#5B21B6',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between'
      }}>
        <div>
          {activeBot === 'scheme' ? (
            <span><strong>Scheme RAG Mode:</strong> Ask specific questions about Indian government schemes, loans, subsidies, and eligibility. Strictly grounded with official document citations.</span>
          ) : (
            <span><strong>Universal AI Mode (OpenAI):</strong> Ask ANY question under the sun — business plans, marketing strategies, budgeting, ideas, or daily guidance for women entrepreneurs.</span>
          )}
        </div>
      </div>

      {/* Quick Prompts for Universal Mode */}
      {activeBot === 'universal' && (
        <div style={{ marginBottom: '20px' }}>
          <div style={{ fontSize: '0.82rem', fontWeight: '700', color: 'var(--text-muted)', marginBottom: '8px', display: 'flex', alignItems: 'center', gap: '6px' }}>
            <HelpCircle size={14} />
            <span>Click any example to ask Universal AI instantly:</span>
          </div>
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px' }}>
            {samplePrompts.map((prompt, idx) => (
              <button
                key={idx}
                type="button"
                onClick={() => handleSampleClick(prompt)}
                style={{
                  background: 'var(--bg-surface)',
                  border: '1px solid var(--border-color)',
                  borderRadius: '20px',
                  padding: '8px 14px',
                  fontSize: '0.82rem',
                  color: 'var(--text-main)',
                  cursor: 'pointer',
                  textAlign: 'left',
                  transition: 'all 0.15s ease',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '6px'
                }}
              >
                <span>{prompt}</span>
                <ArrowRight size={12} color="var(--primary)" />
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Input Form */}
      <form onSubmit={handleSubmit} style={{ marginBottom: '28px' }}>
        <div style={{
          background: 'var(--bg-surface)',
          padding: '20px',
          borderRadius: '16px',
          border: `2px solid ${activeBot === 'scheme' ? 'var(--primary-dark)' : '#9333EA'}`,
          boxShadow: 'var(--shadow-sm)'
        }}>
          <textarea
            rows={3}
            className="search-box"
            style={{ border: 'none', resize: 'none', padding: '0', fontSize: '1.05rem', background: 'transparent', width: '100%' }}
            placeholder={
              activeBot === 'scheme'
                ? "Ask about schemes (e.g. Can a woman starting a tailoring shop get a collateral-free loan?)..."
                : "Ask ANYTHING (e.g. How to market my tailoring shop on Instagram and deal with pricing?)..."
            }
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
          />
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginTop: '16px', borderTop: '1px solid var(--border-color)', paddingTop: '12px' }}>
            <span style={{ fontSize: '0.82rem', color: 'var(--text-muted)' }}>
              🌐 Language: <strong>{language}</strong> | Bot: <strong>{activeBot === 'scheme' ? 'Nivra Scheme RAG' : 'Nivra Universal OpenAI'}</strong>
            </span>
            <button
              type="submit"
              className="btn-primary"
              disabled={loading}
              style={{
                background: activeBot === 'universal' ? 'linear-gradient(135deg, #7C3AED 0%, #C026D3 100%)' : undefined,
                borderColor: activeBot === 'universal' ? '#7C3AED' : undefined
              }}
            >
              <Send size={16} />
              <span>{loading ? 'Thinking & Synthesizing...' : (activeBot === 'scheme' ? 'Ask Scheme Advisor' : 'Ask Universal AI')}</span>
            </button>
          </div>
        </div>
      </form>

      {/* Error Card */}
      {error && (
        <div style={{ background: '#FEF2F2', border: '1px solid #FCA5A5', color: '#991B1B', borderRadius: '16px', padding: '16px 20px', marginBottom: '24px', fontSize: '0.92rem' }}>
          ⚠️ {error}
        </div>
      )}

      {/* Output Results - Scheme Bot */}
      {activeBot === 'scheme' && schemeResult && (
        <div className="ai-response-card" style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
          {/* Plain Language Summary */}
          {plainLanguage && (
            <div style={{ background: 'var(--primary-light)', border: '1px solid var(--border-color)', borderRadius: '16px', padding: '24px' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '10px', color: 'var(--primary-dark)', fontWeight: '700', fontSize: '1.05rem', marginBottom: '12px' }}>
                <Sparkles size={20} color="var(--primary)" />
                <span>Simplified Plain-Language Summary ({language})</span>
              </div>
              <div style={{ color: 'var(--text-main)', fontSize: '0.95rem', whiteSpace: 'pre-line', lineHeight: '1.6' }}>
                {schemeResult.translated_plain_answer}
              </div>
            </div>
          )}

          {/* Official Grounded Answer */}
          <div style={{ background: 'var(--bg-card)', border: '1px solid var(--border-color)', borderRadius: '16px', padding: '24px', boxShadow: 'var(--shadow-sm)' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px', color: 'var(--primary-dark)', fontWeight: '700', fontSize: '1.05rem', marginBottom: '12px' }}>
              <BookOpen size={20} color="var(--primary)" />
              <span>Official Scheme Wording & Citations</span>
            </div>
            <div style={{ color: 'var(--text-secondary)', fontSize: '0.94rem', whiteSpace: 'pre-line', lineHeight: '1.6' }}>
              {schemeResult.official_answer}
            </div>

            {/* Citations Footer */}
            {schemeResult.citations && schemeResult.citations.length > 0 && (
              <div style={{ marginTop: '20px', borderTop: '1px solid var(--border-color)', paddingTop: '16px' }}>
                <h4 style={{ fontSize: '0.85rem', color: 'var(--text-muted)', fontWeight: '700', marginBottom: '8px' }}>
                  📍 Referenced Scheme Documents:
                </h4>
                <div style={{ display: 'flex', flexDirection: 'column', gap: '6px' }}>
                  {schemeResult.citations.map((c, i) => (
                    <div key={i} style={{ fontSize: '0.82rem', color: 'var(--text-secondary)', display: 'flex', alignItems: 'center', gap: '6px' }}>
                      <FileCheck size={14} color="var(--primary)" />
                      <span><strong>{c.scheme_name}</strong> — {c.section_title} ({c.source_file})</span>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Output Results - Universal OpenAI Bot */}
      {activeBot === 'universal' && universalResult && (
        <div className="ai-response-card" style={{ background: 'var(--bg-card)', border: '1px solid var(--border-color)', borderRadius: '16px', padding: '24px', boxShadow: 'var(--shadow-md)' }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '16px', pb: '12px', borderBottom: '1px solid var(--border-color)' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px', color: 'var(--primary-dark)', fontWeight: '700', fontSize: '1.08rem' }}>
              <Zap size={22} color="var(--primary)" />
              <span>Nivra Universal AI Response</span>
            </div>
            <span style={{ fontSize: '0.78rem', background: 'var(--primary-light)', color: 'var(--primary-dark)', padding: '4px 12px', borderRadius: '20px', fontWeight: '600' }}>
              ⚡ {universalResult.provider || 'OpenAI GPT-4o-mini'}
            </span>
          </div>

          <div style={{ color: 'var(--text-main)', fontSize: '0.96rem', whiteSpace: 'pre-line', lineHeight: '1.75' }}>
            {universalResult.answer}
          </div>
        </div>
      )}
    </div>
  );
}
