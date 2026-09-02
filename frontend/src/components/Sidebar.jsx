import React from 'react';
import { Home, MessageSquare, ClipboardCheck, Bookmark, BarChart3, Flower2, Layers } from 'lucide-react';

export default function Sidebar({ activeTab, setActiveTab, retrievalMode, setRetrievalMode }) {
  const menuItems = [
    { id: 'home', label: 'Dashboard Home', icon: Home },
    { id: 'ask', label: 'Ask Nivra', icon: MessageSquare },
    { id: 'eligibility', label: 'Eligibility Checker', icon: ClipboardCheck },
    { id: 'saved', label: 'My Saved Schemes', icon: Bookmark },
    { id: 'metrics', label: 'Retrieval Settings', icon: BarChart3 },
  ];

  return (
    <aside className="sidebar">
      <div>
        <div className="brand-header">
          <div className="brand-logo">
            <Flower2 size={26} color="var(--primary)" />
          </div>
          <div>
            <h1 className="brand-title">Nivra</h1>
            <p className="brand-subtitle">Empowering Women Entrepreneurs</p>
          </div>
        </div>

        <ul className="nav-list">
          {menuItems.map((item) => {
            const Icon = item.icon;
            const isActive = activeTab === item.id;
            return (
              <li
                key={item.id}
                className={`nav-item ${isActive ? 'active' : ''}`}
                onClick={() => setActiveTab(item.id)}
              >
                <Icon size={20} />
                <span>{item.label}</span>
              </li>
            );
          })}
        </ul>
      </div>

      <div style={{ background: 'var(--bg-surface-subtle)', padding: '16px', borderRadius: '14px', marginTop: '24px', border: '1px solid var(--border-color)' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '8px', color: 'var(--primary-dark)', fontWeight: '700', fontSize: '0.85rem' }}>
          <Layers size={16} />
          <span>RAG Retrieval Engine</span>
        </div>
        <select
          value={retrievalMode}
          onChange={(e) => setRetrievalMode(e.target.value)}
          style={{ width: '100%', padding: '6px 10px', borderRadius: '8px', border: '1px solid var(--border-color)', background: 'var(--bg-surface)', fontFamily: 'inherit', fontSize: '0.82rem', fontWeight: '600', color: 'var(--text-main)' }}
        >
          <option value="hybrid">Hybrid (Dense + BM25 RRF)</option>
          <option value="semantic_only">Semantic Vector Only</option>
        </select>
        <p style={{ fontSize: '0.74rem', color: 'var(--text-muted)', marginTop: '6px' }}>
          Compare exact keyword + dense search against vector-only search.
        </p>
      </div>
    </aside>
  );
}
