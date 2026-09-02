import React, { useState, useEffect } from 'react';
import { X, CheckSquare, Square, Copy, Check } from 'lucide-react';

export default function DocumentChecklistModal({ schemeName, onClose }) {
  const [checklistData, setChecklistData] = useState(null);
  const [checkedItems, setCheckedItems] = useState({});
  const [copied, setCopied] = useState(false);

  useEffect(() => {
    if (schemeName) {
      fetch(`/api/checklist?scheme_name=${encodeURIComponent(schemeName)}`)
        .then(res => res.json())
        .then(data => setChecklistData(data))
        .catch(err => console.error("Checklist fetch failed:", err));
    }
  }, [schemeName]);

  const toggleCheck = (item) => {
    setCheckedItems(prev => ({ ...prev, [item]: !prev[item] }));
  };

  const copyChecklist = () => {
    if (!checklistData) return;
    let text = `Document Checklist for ${checklistData.scheme_name}:\n\n`;
    for (const [cat, items] of Object.entries(checklistData.categories)) {
      text += `${cat}:\n`;
      items.forEach(item => {
        text += `- ${item}\n`;
      });
      text += '\n';
    }
    navigator.clipboard.writeText(text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  if (!schemeName) return null;

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px', borderBottom: '1px solid var(--border-color)', paddingBottom: '16px' }}>
          <div>
            <h2 style={{ fontSize: '1.25rem', fontWeight: '800', color: 'var(--primary-dark)' }}>
              📋 Application Document Checklist
            </h2>
            <p style={{ fontSize: '0.88rem', color: 'var(--text-muted)' }}>
              {schemeName}
            </p>
          </div>
          <button onClick={onClose} style={{ background: 'none', border: 'none', cursor: 'pointer', color: 'var(--text-muted)' }}>
            <X size={24} />
          </button>
        </div>

        {checklistData ? (
          <div>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
              <span style={{ fontSize: '0.85rem', color: 'var(--text-muted)', fontWeight: '600' }}>
                Check off documents as you gather them:
              </span>
              <button className="btn-secondary" onClick={copyChecklist} style={{ padding: '6px 12px', fontSize: '0.82rem' }}>
                {copied ? <Check size={14} color="#047857" /> : <Copy size={14} />}
                <span>{copied ? 'Copied!' : 'Copy Checklist'}</span>
              </button>
            </div>

            <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
              {Object.entries(checklistData.categories).map(([catTitle, docs], i) => (
                <div key={i} style={{ background: 'var(--bg-surface-subtle)', padding: '16px', borderRadius: '14px', border: '1px solid var(--border-color)' }}>
                  <h3 style={{ fontSize: '0.95rem', fontWeight: '700', color: 'var(--primary-dark)', marginBottom: '10px' }}>
                    {catTitle}
                  </h3>
                  <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
                    {docs.map((doc, dIdx) => {
                      const isChecked = !!checkedItems[doc];
                      return (
                        <div
                          key={dIdx}
                          onClick={() => toggleCheck(doc)}
                          style={{ display: 'flex', alignItems: 'center', gap: '10px', fontSize: '0.88rem', color: isChecked ? 'var(--text-muted)' : 'var(--text-main)', cursor: 'pointer', textDecoration: isChecked ? 'line-through' : 'none' }}
                        >
                          {isChecked ? <CheckSquare size={18} color="var(--primary)" /> : <Square size={18} color="var(--text-muted)" />}
                          <span>{doc}</span>
                        </div>
                      );
                    })}
                  </div>
                </div>
              ))}
            </div>
          </div>
        ) : (
          <p style={{ color: 'var(--text-muted)' }}>Loading document checklist...</p>
        )}
      </div>
    </div>
  );
}
