import React from 'react';
import { Bookmark, FileText, Trash2 } from 'lucide-react';

export default function SavedSchemes({ savedSchemes, onOpenChecklist, onRemoveScheme }) {
  const schemeList = Array.from(savedSchemes);

  return (
    <div style={{ maxWidth: '900px' }}>
      <div style={{ marginBottom: '24px' }}>
        <h1 style={{ fontSize: '1.6rem', fontWeight: '800', color: 'var(--primary-dark)', marginBottom: '4px' }}>
          🔖 My Saved Schemes
        </h1>
        <p style={{ color: 'var(--text-muted)', fontSize: '0.92rem' }}>
          Keep track of schemes you are preparing applications for.
        </p>
      </div>

      {schemeList.length === 0 ? (
        <div style={{ background: 'var(--bg-card)', padding: '40px', borderRadius: '20px', textAlign: 'center', border: '1px dashed var(--border-color)' }}>
          <Bookmark size={40} color="var(--text-muted)" style={{ marginBottom: '12px' }} />
          <h3 style={{ fontSize: '1.1rem', color: 'var(--text-main)', fontWeight: '700' }}>No Saved Schemes Yet</h3>
          <p style={{ fontSize: '0.88rem', color: 'var(--text-muted)', marginTop: '4px' }}>
            Bookmark schemes from the Dashboard Home or Eligibility Checker to save them here.
          </p>
        </div>
      ) : (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
          {schemeList.map((schemeName, idx) => (
            <div key={idx} className="scheme-card" style={{ flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center' }}>
              <div>
                <h3 style={{ fontSize: '1.1rem', fontWeight: '700', color: 'var(--primary-dark)', marginBottom: '4px' }}>
                  {schemeName}
                </h3>
                <span style={{ fontSize: '0.82rem', color: 'var(--text-muted)' }}>
                  Saved on 02 Sep 2026 • Ready for Document Preparation
                </span>
              </div>

              <div style={{ display: 'flex', gap: '10px' }}>
                <button
                  className="btn-primary"
                  style={{ padding: '8px 14px', fontSize: '0.85rem' }}
                  onClick={() => onOpenChecklist(schemeName)}
                >
                  <FileText size={16} />
                  <span>Required Documents</span>
                </button>
                <button
                  onClick={() => onRemoveScheme(schemeName)}
                  style={{ padding: '8px 12px', background: '#FEF2F2', color: '#DC2626', border: '1px solid #FECACA', borderRadius: '10px', cursor: 'pointer' }}
                >
                  <Trash2 size={16} />
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
