import React, { useState, useEffect } from 'react';
import Sidebar from './components/Sidebar';
import Header from './components/Header';
import DashboardHome from './components/DashboardHome';
import AskQuestion from './components/AskQuestion';
import EligibilityChecker from './components/EligibilityChecker';
import SavedSchemes from './components/SavedSchemes';
import MetricsView from './components/MetricsView';
import DocumentChecklistModal from './components/DocumentChecklistModal';

export default function App() {
  const [activeTab, setActiveTab] = useState('home');
  const [language, setLanguage] = useState('English');
  const [plainLanguage, setPlainLanguage] = useState(true);
  const [retrievalMode, setRetrievalMode] = useState('hybrid');
  const [theme, setTheme] = useState('light');
  
  const [checklistScheme, setChecklistScheme] = useState(null);
  const [savedSchemes, setSavedSchemes] = useState(new Set());

  // Fetch saved schemes from Supabase database API on mount
  useEffect(() => {
    fetch('/api/supabase/saved_schemes')
      .then(res => res.json())
      .then(data => {
        if (data.saved_schemes) {
          setSavedSchemes(new Set(data.saved_schemes));
        }
      })
      .catch(err => console.error("Failed to fetch saved schemes from Supabase:", err));
  }, []);

  // Sync data-theme attribute on <html> element
  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme);
  }, [theme]);

  const handleSaveScheme = async (schemeName) => {
    const isCurrentlySaved = savedSchemes.has(schemeName);

    // Optimistic UI update
    setSavedSchemes((prev) => {
      const next = new Set(prev);
      if (isCurrentlySaved) {
        next.delete(schemeName);
      } else {
        next.add(schemeName);
      }
      return next;
    });

    // Sync to Supabase database via API
    try {
      if (isCurrentlySaved) {
        await fetch('/api/supabase/save_scheme', {
          method: 'DELETE',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ scheme_name: schemeName })
        });
      } else {
        await fetch('/api/supabase/save_scheme', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ scheme_name: schemeName })
        });
      }
    } catch (err) {
      console.error("Supabase bookmark sync error:", err);
    }
  };

  const handleRemoveScheme = async (schemeName) => {
    setSavedSchemes((prev) => {
      const next = new Set(prev);
      next.delete(schemeName);
      return next;
    });

    try {
      await fetch('/api/supabase/save_scheme', {
        method: 'DELETE',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ scheme_name: schemeName })
      });
    } catch (err) {
      console.error("Supabase remove bookmark error:", err);
    }
  };

  return (
    <div className="app-container">
      {/* Sidebar Navigation */}
      <Sidebar
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        retrievalMode={retrievalMode}
        setRetrievalMode={setRetrievalMode}
      />

      {/* Main Content Area */}
      <main className="main-content">
        <Header
          language={language}
          setLanguage={setLanguage}
          plainLanguage={plainLanguage}
          setPlainLanguage={setPlainLanguage}
          theme={theme}
          setTheme={setTheme}
          setActiveTab={setActiveTab}
        />

        {/* Dynamic View Rendering with Smooth Transition */}
        <div key={activeTab} className="page-transition-view">
          {activeTab === 'home' && (
            <DashboardHome
              onOpenChecklist={(sName) => setChecklistScheme(sName)}
              retrievalMode={retrievalMode}
              onSaveScheme={handleSaveScheme}
              savedSchemes={savedSchemes}
            />
          )}

          {activeTab === 'ask' && (
            <AskQuestion
              language={language}
              plainLanguage={plainLanguage}
              retrievalMode={retrievalMode}
            />
          )}

          {activeTab === 'eligibility' && (
            <EligibilityChecker
              onOpenChecklist={(sName) => setChecklistScheme(sName)}
            />
          )}

          {activeTab === 'saved' && (
            <SavedSchemes
              savedSchemes={savedSchemes}
              onOpenChecklist={(sName) => setChecklistScheme(sName)}
              onRemoveScheme={handleRemoveScheme}
            />
          )}

          {activeTab === 'metrics' && (
            <MetricsView />
          )}
        </div>
      </main>

      {/* Document Checklist Modal */}
      {checklistScheme && (
        <DocumentChecklistModal
          schemeName={checklistScheme}
          onClose={() => setChecklistScheme(null)}
        />
      )}
    </div>
  );
}
