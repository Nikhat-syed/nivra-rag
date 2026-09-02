import React, { useState } from 'react';
import { Search, DollarSign, Users, FileText, BookmarkPlus, Check } from 'lucide-react';

export default function DashboardHome({ onOpenChecklist, retrievalMode, onSaveScheme, savedSchemes }) {
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [searchResults, setSearchResults] = useState([]);
  const [isSearching, setIsSearching] = useState(false);

  const categories = [
    { id: 'all', label: 'All Schemes' },
    { id: 'loan', label: 'Loans & Credit' },
    { id: 'scholarship', label: 'Scholarships' },
    { id: 'training', label: 'Skill Training' },
    { id: 'support-service', label: 'Incubation & Support' },
  ];

  const featuredSchemes = [
    {
      name: 'Stand-Up India Scheme',
      category: 'loan',
      limit: 'Rs. 10 Lakhs - Rs. 1 Crore',
      target: 'SC / ST & Women Entrepreneurs',
      subsidy: '10-15% Margin Money Convergence',
      desc: 'Bank loans for setting up greenfield manufacturing, trading, or service enterprises with 7-year repayment.'
    },
    {
      name: 'Pradhan Mantri Mudra Yojana (PMMY)',
      category: 'loan',
      limit: 'Up to Rs. 10 Lakhs',
      target: 'Micro-entrepreneurs & Small Businesses',
      subsidy: 'Collateral-free credit guarantee',
      desc: 'Three tiers: Shishu (up to 50k), Kishore (50k - 5L), and Tarun (5L - 10L) for non-farm business expansion.'
    },
    {
      name: 'PMEGP MSME Subsidy',
      category: 'loan',
      limit: 'Up to Rs. 50 Lakhs',
      target: 'Rural & Urban Women (Special Category)',
      subsidy: '15% - 35% Margin Money Subsidy',
      desc: 'Credit-linked subsidy scheme offering 35% rural subsidy for female applicants setting up micro-units.'
    },
    {
      name: 'Pragati Scholarship for Girl Students',
      category: 'scholarship',
      limit: 'Rs. 50,000 / year',
      target: 'Women Students (Degree/Diploma)',
      subsidy: '100% Educational Aid',
      desc: 'AICTE financial aid for young women pursuing technical degree or diploma courses across India.'
    },
    {
      name: 'WE Hub Telangana Prototype Grant',
      category: 'support-service',
      limit: 'Rs. 5 Lakhs Grant',
      target: 'Telangana Female Founders',
      subsidy: 'Seed Grant & Incubation',
      desc: "India's first state-led incubator providing validation seed grants and market linkage for female founders."
    },
    {
      name: 'Udyogini Scheme for Women',
      category: 'loan',
      limit: 'Up to Rs. 3 Lakhs',
      target: 'Low Income / SC-ST Women',
      subsidy: '30% Subsidized Capital Grant',
      desc: 'Low-interest loans for women engaged in small trades and retail businesses to avoid private moneylenders.'
    }
  ];

  const handleSearch = async (e) => {
    e.preventDefault();
    if (!searchQuery.trim()) return;

    setIsSearching(true);
    try {
      const response = await fetch('/api/search', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          query: searchQuery,
          category: selectedCategory === 'all' ? null : selectedCategory,
          mode: retrievalMode,
          top_k: 6
        })
      });
      const data = await response.json();
      setSearchResults(data.results || []);
    } catch (err) {
      console.error("Search failed:", err);
    } finally {
      setIsSearching(false);
    }
  };

  return (
    <div>
      {/* Hero Search Section */}
      <div style={{ background: 'var(--primary-gradient)', padding: '40px', borderRadius: '24px', color: '#FFFFFF', marginBottom: '32px', boxShadow: 'var(--shadow-md)' }}>
        <h1 style={{ fontSize: '2rem', fontWeight: '800', marginBottom: '8px', letterSpacing: '-0.02em' }}>
          Find Government Schemes Made for You 🌸
        </h1>
        <p style={{ fontSize: '1rem', color: 'rgba(255,255,255,0.9)', marginBottom: '24px', maxWidth: '700px' }}>
          Search across verified government schemes by scheme name, business type, loan amount, or location.
        </p>

        <form onSubmit={handleSearch} style={{ display: 'flex', gap: '12px', maxWidth: '750px' }}>
          <div style={{ position: 'relative', flex: 1 }}>
            <Search style={{ position: 'absolute', left: '18px', top: '16px', color: '#7567B1' }} size={20} />
            <input
              type="text"
              className="search-box"
              style={{ paddingLeft: '50px', background: '#FFFFFF', color: '#27233A' }}
              placeholder="Search scheme name (e.g. Stand-Up India, Mudra, PMEGP subsidy, WE Hub)..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
            />
          </div>
          <button type="submit" className="btn-primary" style={{ padding: '0 28px', background: '#FFFFFF', color: '#7567B1', fontWeight: '700' }}>
            {isSearching ? 'Searching...' : 'Search'}
          </button>
        </form>

        {/* Category Pills */}
        <div style={{ display: 'flex', gap: '10px', marginTop: '20px', flexWrap: 'wrap' }}>
          {categories.map((cat) => (
            <button
              key={cat.id}
              onClick={() => setSelectedCategory(cat.id)}
              style={{
                background: selectedCategory === cat.id ? '#FFFFFF' : 'rgba(255, 255, 255, 0.2)',
                color: selectedCategory === cat.id ? '#7567B1' : '#FFFFFF',
                border: 'none',
                padding: '6px 16px',
                borderRadius: '20px',
                fontSize: '0.84rem',
                fontWeight: '700',
                cursor: 'pointer',
                transition: 'all 0.2s ease'
              }}
            >
              {cat.label}
            </button>
          ))}
        </div>
      </div>

      {/* Search Results Display */}
      {searchResults.length > 0 && (
        <div style={{ marginBottom: '40px' }}>
          <h2 style={{ fontSize: '1.3rem', fontWeight: '700', color: 'var(--primary-dark)', marginBottom: '16px' }}>
            Search Results for "{searchQuery}" ({searchResults.length} items found)
          </h2>
          <div className="grid-3">
            {searchResults.map((res, i) => (
              <div key={i} className="scheme-card">
                <div>
                  <div className="card-header">
                    <h3 className="scheme-title">{res.scheme_name}</h3>
                    <span className={`badge badge-${res.category || 'loan'}`}>
                      {(res.category || 'loan').toUpperCase()}
                    </span>
                  </div>
                  <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)', marginBottom: '8px' }}>
                    <strong>Section:</strong> {res.section_title} | <strong>Scope:</strong> {res.state_or_central}
                  </p>
                  <p style={{ fontSize: '0.88rem', color: 'var(--text-secondary)', lineHeight: '1.45' }}>
                    {res.text.slice(0, 220)}...
                  </p>
                </div>
                <div style={{ marginTop: '16px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <button
                    className="btn-secondary"
                    onClick={() => onOpenChecklist(res.scheme_name)}
                  >
                    <FileText size={15} />
                    <span>Checklist</span>
                  </button>
                  <button
                    onClick={() => onSaveScheme(res.scheme_name)}
                    style={{ background: 'none', border: 'none', cursor: 'pointer', color: savedSchemes.has(res.scheme_name) ? 'var(--primary)' : 'var(--text-muted)' }}
                  >
                    {savedSchemes.has(res.scheme_name) ? <Check size={20} /> : <BookmarkPlus size={20} />}
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Featured Recommended Schemes Grid */}
      <div>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
          <h2 style={{ fontSize: '1.35rem', fontWeight: '800', color: 'var(--primary-dark)' }}>
            Recommended Government Schemes 🌟
          </h2>
          <span style={{ fontSize: '0.85rem', color: 'var(--text-muted)', fontWeight: '500' }}>Verified Official Guidelines</span>
        </div>

        <div className="grid-3">
          {featuredSchemes
            .filter(s => selectedCategory === 'all' || s.category === selectedCategory)
            .map((sch, i) => {
              const isSaved = savedSchemes.has(sch.name);
              return (
                <div key={i} className="scheme-card">
                  <div>
                    <div className="card-header">
                      <h3 className="scheme-title">{sch.name}</h3>
                      <span className={`badge badge-${sch.category}`}>
                        {sch.category.replace('-service', '').toUpperCase()}
                      </span>
                    </div>

                    <div style={{ display: 'flex', flexDirection: 'column', gap: '6px', margin: '12px 0' }}>
                      <div style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '0.86rem', color: 'var(--primary-dark)', fontWeight: '700' }}>
                        <DollarSign size={16} />
                        <span>Limit: {sch.limit}</span>
                      </div>
                      <div style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '0.84rem', color: 'var(--text-muted)' }}>
                        <Users size={15} />
                        <span>{sch.target}</span>
                      </div>
                    </div>

                    <p style={{ fontSize: '0.88rem', color: 'var(--text-secondary)', lineHeight: '1.45' }}>
                      {sch.desc}
                    </p>
                  </div>

                  <div style={{ marginTop: '20px', display: 'flex', gap: '10px', alignItems: 'center' }}>
                    <button
                      className="btn-primary"
                      style={{ flex: 1, padding: '8px 12px', fontSize: '0.85rem' }}
                      onClick={() => onOpenChecklist(sch.name)}
                    >
                      <FileText size={16} />
                      <span>Required Documents</span>
                    </button>
                    <button
                      onClick={() => onSaveScheme(sch.name)}
                      style={{ padding: '8px', borderRadius: '8px', border: '1px solid var(--border-color)', background: isSaved ? 'var(--primary-light)' : 'var(--bg-surface)', cursor: 'pointer' }}
                    >
                      {isSaved ? <Check size={18} color="var(--primary)" /> : <BookmarkPlus size={18} color="var(--text-muted)" />}
                    </button>
                  </div>
                </div>
              );
            })}
        </div>
      </div>
    </div>
  );
}
