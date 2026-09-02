import React from 'react';
import { Globe, AlertTriangle, Sparkles, Sun, Moon } from 'lucide-react';

export default function Header({ language, setLanguage, plainLanguage, setPlainLanguage, theme, setTheme }) {
  const isDark = theme === 'dark';

  const toggleTheme = () => {
    setTheme(isDark ? 'light' : 'dark');
  };

  return (
    <div>
      <div className="disclaimer-banner">
        <AlertTriangle size={18} />
        <span>
          <strong>Official Disclaimer:</strong> Government scheme guidelines change periodically. Please verify final subvention terms on official portals before applying.
        </span>
      </div>

      <div className="top-bar">
        <div>
          <h2 style={{ fontSize: '1.25rem', fontWeight: '800', color: 'var(--primary-dark)' }}>
            Namaste, Entrepreneur 🌸
          </h2>
          <p style={{ fontSize: '0.88rem', color: 'var(--text-muted)' }}>
            Find government loans, scholarships, and grants in plain language.
          </p>
        </div>

        <div className="controls-group">
          {/* Day / Night Theme Toggle */}
          <button
            className="theme-toggle-btn"
            onClick={toggleTheme}
            title={isDark ? "Switch to Light Mode" : "Switch to Night Mode"}
          >
            {isDark ? <Sun size={17} color="#FDE047" /> : <Moon size={17} color="#7567B1" />}
            <span>{isDark ? 'Light' : 'Night'}</span>
          </button>

          <div className="toggle-switch">
            <Sparkles size={16} color="var(--primary)" />
            <span>Plain Language</span>
            <input
              type="checkbox"
              checked={plainLanguage}
              onChange={(e) => setPlainLanguage(e.target.checked)}
              style={{ accentColor: 'var(--primary)', width: '18px', height: '18px', cursor: 'pointer' }}
            />
          </div>

          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <Globe size={18} color="var(--primary)" />
            <select
              className="lang-select"
              value={language}
              onChange={(e) => setLanguage(e.target.value)}
            >
              <option value="English">English</option>
              <option value="Telugu">Telugu (తెలుగు)</option>
              <option value="Hindi">Hindi (हिन्दी)</option>
            </select>
          </div>
        </div>
      </div>
    </div>
  );
}
