import React, { useState } from 'react';
import { Sparkles } from 'lucide-react';

export default function EligibilityChecker({ onOpenChecklist }) {
  const [profile, setProfile] = useState({
    age: 26,
    business_stage: 'Idea Stage',
    applicant_category: 'Women Entrepreneur',
    scheme_type: 'All',
    state: 'All India'
  });

  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);

  const handleEvaluate = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const res = await fetch('/api/eligibility', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(profile)
      });
      const data = await res.json();
      setResults(data.schemes || []);
    } catch (err) {
      console.error("Eligibility check failed:", err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <div style={{ marginBottom: '24px' }}>
        <h1 style={{ fontSize: '1.6rem', fontWeight: '800', color: 'var(--primary-dark)', marginBottom: '4px' }}>
          📋 Scheme Eligibility Checker
        </h1>
        <p style={{ color: 'var(--text-muted)', fontSize: '0.92rem' }}>
          Fill out your profile details below to discover schemes you qualify for — no typing required!
        </p>
      </div>

      {/* Form Card */}
      <form onSubmit={handleEvaluate} style={{ background: 'var(--bg-card)', padding: '28px', borderRadius: '20px', border: '1px solid var(--border-color)', boxShadow: 'var(--shadow-sm)', marginBottom: '36px' }}>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))', gap: '20px', marginBottom: '24px' }}>
          <div>
            <label style={{ display: 'block', fontSize: '0.85rem', fontWeight: '700', color: 'var(--text-secondary)', marginBottom: '6px' }}>
              Your Age
            </label>
            <input
              type="number"
              min="18"
              max="75"
              style={{ width: '100%', padding: '10px 14px', borderRadius: '10px', border: '1px solid var(--border-color)', background: 'var(--bg-surface)', color: 'var(--text-main)', fontSize: '0.95rem' }}
              value={profile.age}
              onChange={(e) => setProfile({ ...profile, age: parseInt(e.target.value) || 18 })}
            />
          </div>

          <div>
            <label style={{ display: 'block', fontSize: '0.85rem', fontWeight: '700', color: 'var(--text-secondary)', marginBottom: '6px' }}>
              Business Stage
            </label>
            <select
              style={{ width: '100%', padding: '10px 14px', borderRadius: '10px', border: '1px solid var(--border-color)', background: 'var(--bg-surface)', color: 'var(--text-main)', fontSize: '0.95rem' }}
              value={profile.business_stage}
              onChange={(e) => setProfile({ ...profile, business_stage: e.target.value })}
            >
              <option value="Idea Stage">Idea Stage</option>
              <option value="Early Stage / Startup">Early Stage / Startup</option>
              <option value="Growth & Expansion">Growth & Expansion</option>
              <option value="Existing Business">Existing Business</option>
            </select>
          </div>

          <div>
            <label style={{ display: 'block', fontSize: '0.85rem', fontWeight: '700', color: 'var(--text-secondary)', marginBottom: '6px' }}>
              Applicant Category
            </label>
            <select
              style={{ width: '100%', padding: '10px 14px', borderRadius: '10px', border: '1px solid var(--border-color)', background: 'var(--bg-surface)', color: 'var(--text-main)', fontSize: '0.95rem' }}
              value={profile.applicant_category}
              onChange={(e) => setProfile({ ...profile, applicant_category: e.target.value })}
            >
              <option value="Women Entrepreneur">Women Entrepreneur</option>
              <option value="Women Entrepreneur (SC / ST)">Women Entrepreneur (SC / ST)</option>
              <option value="Rural Women Micro-business">Rural Women Micro-business</option>
              <option value="General Category">General Category</option>
            </select>
          </div>

          <div>
            <label style={{ display: 'block', fontSize: '0.85rem', fontWeight: '700', color: 'var(--text-secondary)', marginBottom: '6px' }}>
              Scheme Type Interest
            </label>
            <select
              style={{ width: '100%', padding: '10px 14px', borderRadius: '10px', border: '1px solid var(--border-color)', background: 'var(--bg-surface)', color: 'var(--text-main)', fontSize: '0.95rem' }}
              value={profile.scheme_type}
              onChange={(e) => setProfile({ ...profile, scheme_type: e.target.value })}
            >
              <option value="All">All Categories</option>
              <option value="Loans & Credit">Loans & Credit</option>
              <option value="Scholarships">Scholarships</option>
              <option value="Skill Training">Skill Training</option>
              <option value="Support Services">Support Services</option>
            </select>
          </div>

          <div>
            <label style={{ display: 'block', fontSize: '0.85rem', fontWeight: '700', color: 'var(--text-secondary)', marginBottom: '6px' }}>
              State / Location
            </label>
            <select
              style={{ width: '100%', padding: '10px 14px', borderRadius: '10px', border: '1px solid var(--border-color)', background: 'var(--bg-surface)', color: 'var(--text-main)', fontSize: '0.95rem' }}
              value={profile.state}
              onChange={(e) => setProfile({ ...profile, state: e.target.value })}
            >
              <option value="All India">All India / Central</option>
              <option value="Telangana">Telangana</option>
              <option value="Karnataka">Karnataka</option>
              <option value="Andhra Pradesh">Andhra Pradesh</option>
              <option value="Maharashtra">Maharashtra</option>
            </select>
          </div>
        </div>

        <button type="submit" className="btn-primary" disabled={loading} style={{ width: '100%', justifyContent: 'center', padding: '12px' }}>
          <Sparkles size={18} />
          <span>{loading ? 'Evaluating Profile...' : 'Evaluate Scheme Eligibility'}</span>
        </button>
      </form>

      {/* Matched Results */}
      {results && (
        <div>
          <h2 style={{ fontSize: '1.3rem', fontWeight: '800', color: 'var(--primary-dark)', marginBottom: '20px' }}>
            Matched Eligible Schemes ({results.length} found)
          </h2>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
            {results.map((item, idx) => (
              <div key={idx} className="scheme-card" style={{ flexDirection: 'row', gap: '20px', alignItems: 'center' }}>
                <div style={{ flex: 1 }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '8px' }}>
                    <h3 style={{ fontSize: '1.15rem', fontWeight: '700', color: 'var(--primary-dark)' }}>{item.scheme_name}</h3>
                    <span className="badge badge-loan">{item.score}% MATCH</span>
                  </div>

                  <p style={{ color: 'var(--primary-dark)', fontWeight: '700', fontSize: '0.9rem', marginBottom: '6px' }}>
                    💰 Limit: {item.max_loan_amount} | 🎁 Subsidy: {item.subsidy}
                  </p>

                  <div style={{ display: 'flex', gap: '12px', flexWrap: 'wrap', marginBottom: '10px' }}>
                    {item.match_reasons.map((reason, rIdx) => (
                      <span key={rIdx} style={{ fontSize: '0.8rem', background: 'var(--primary-light)', color: 'var(--primary-dark)', padding: '4px 10px', borderRadius: '6px', fontWeight: '600' }}>
                        ✓ {reason}
                      </span>
                    ))}
                  </div>

                  <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)', background: 'var(--bg-surface-subtle)', padding: '10px', borderRadius: '8px' }}>
                    <strong>Eligibility Snippet:</strong> {item.eligibility_snippet}
                  </p>
                </div>

                <button
                  className="btn-secondary"
                  style={{ alignSelf: 'center', whiteSpace: 'nowrap' }}
                  onClick={() => onOpenChecklist(item.scheme_name)}
                >
                  View Checklist
                </button>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
