import React, { useState, useEffect } from 'react';
import universityData from './data/rankings.json';
import { getUNIVrank } from './utils/calcRank';
import AdmissionEvaluator from './components/AdmissionEvaluator';
import { 
  Search, Globe, Building2, Users, GraduationCap, 
  Trophy, BookOpen, ExternalLink, Filter, TrendingUp, 
  Leaf, FlaskConical, Award, Briefcase, ChevronRight, Calculator
} from 'lucide-react';

const App = () => {
  const [data, setData] = useState([]);
  const [filteredData, setFilteredData] = useState([]);
  const [search, setSearch] = useState('');
  const [regionFilter, setRegionFilter] = useState('All');
  const [typeFilter, setTypeFilter] = useState('All');
  const [compareList, setCompareList] = useState([]);
  const [view, setView] = useState('rankings');

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch('http://localhost:8000/rankings');
        if (response.ok) {
          const apiData = await response.json();
          processAndSetData(apiData);
        } else {
          processAndSetData(universityData);
        }
      } catch (err) {
        console.log("API not reachable, using local data");
        processAndSetData(universityData);
      }
    };

    const processAndSetData = (raw) => {
      const processed = raw.map(u => ({
        ...u,
        univrank: getUNIVrank(u)
      })).sort((a, b) => a.univrank - b.univrank);
      
      // Assign dense display rank
      let currentRank = 1;
      for (let i = 0; i < processed.length; i++) {
          if (i > 0 && processed[i].univrank > processed[i-1].univrank) {
              currentRank = i + 1;
          }
          processed[i].displayRank = currentRank;
      }
      setData(processed);
      setFilteredData(processed);
    };

    fetchData();
  }, []);

  useEffect(() => {
    let result = data;
    if (search) {
      result = result.filter(u => u.university_name.toLowerCase().includes(search.toLowerCase()) || u.country.toLowerCase().includes(search.toLowerCase()));
    }
    if (regionFilter !== 'All') {
      result = result.filter(u => u.region === regionFilter);
    }
    if (typeFilter !== 'All') {
      result = result.filter(u => u.university_type === typeFilter);
    }
    setFilteredData(result);
  }, [search, regionFilter, typeFilter, data]);

  const toggleCompare = (u) => {
    if (compareList.find(item => item.university_id === u.university_id)) {
      setCompareList(compareList.filter(item => item.university_id !== u.university_id));
    } else if (compareList.length < 3) {
      setCompareList([...compareList, u]);
    }
  };

  const regions = ['All', ...new Set(universityData.map(u => u.region))];
  const types = ['All', ...new Set(universityData.map(u => u.university_type))];

  return (
    <div className="app">
      <header>
        <div className="container" style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center'}}>
          <div className="logo" onClick={() => setView('rankings')} style={{cursor: 'pointer'}}>
            UNIV<span>rank</span>
          </div>
          <nav style={{display: 'flex', gap: '2rem', alignItems: 'center'}}>
            <a href="#" className="metric-label" onClick={() => setView('rankings')}>Rankings Index</a>
            <a href="#" className="metric-label" onClick={() => setView('compare')}>Compare Tools ({compareList.length})</a>
            <a href="#" className="metric-label" onClick={() => setView('admission')} style={{display: 'flex', alignItems: 'center', gap: '0.5rem'}}>
              <Calculator size={16} /> Admission Evaluator
            </a>
            <button className="btn btn-primary" style={{borderRadius: '12px'}} onClick={() => setView('compare')}>
              Open Comparison
            </button>
          </nav>
        </div>
      </header>

      <main className="container">
        {view === 'rankings' ? (
          <div className="animate-in">
            <section className="hero-v2">
              <span className="badge">World University Rankings 2026</span>
              <h1 style={{fontSize: '3.5rem', fontWeight: 800, color: 'var(--primary)', marginBottom: '1.5rem'}}>
                Global Performance Index
              </h1>
              <p style={{fontSize: '1.2rem', color: 'var(--text-light)', maxWidth: '900px', margin: '0 auto'}}>
                Aggregating the world's most trusted data from <strong>QS, THE, and ARWU</strong>. 
                Our bias-reduced UNIVrank algorithm ensures a balanced assessment of academic excellence, 
                research impact, and global outlook.
              </p>
            </section>

            <div className="filters-container">
              <div className="search-wrapper">
                <Search size={20} style={{position: 'absolute', left: '15px', top: '50%', transform: 'translateY(-50%)', color: '#999'}} />
                <input 
                  type="text" 
                  className="input-styled" 
                  style={{paddingLeft: '3rem'}}
                  placeholder="Search by university name or country..." 
                  value={search}
                  onChange={(e) => setSearch(e.target.value)}
                />
              </div>
              <select className="select-styled" value={regionFilter} onChange={(e) => setRegionFilter(e.target.value)}>
                {regions.map(r => <option key={r} value={r}>{r}</option>)}
              </select>
              <select className="select-styled" value={typeFilter} onChange={(e) => setTypeFilter(e.target.value)}>
                {types.map(t => <option key={t} value={t}>{t}</option>)}
              </select>
            </div>

            <div className="ranking-grid">
              {filteredData.map((u, i) => (
                <div key={u.university_id} className="univ-row">
                  <div className="rank-number">#{u.displayRank}</div>
                  <div className="univ-info">
                    <h3>{u.university_name}</h3>
                    <div className="univ-meta">
                      <span><Globe size={14} /> {u.country}</span>
                      <span><Building2 size={14} /> {u.university_type}</span>
                      <span><BookOpen size={14} /> Founded {u.founding_year}</span>
                    </div>
                  </div>
                  <div className="score-vibrant">
                    <TrendingUp size={16} /> UNIVrank: {u.univrank}
                  </div>
                  <div className="metric-box">
                    <div className="metric-label">Students</div>
                    <div className="metric-value">{u.student_population?.toLocaleString()}</div>
                  </div>
                  <div className="metric-box">
                    <div className="metric-label">ARWU Rank</div>
                    <div className="metric-value">{u.arwu_rank || 'N/A'}</div>
                  </div>
                  <div className="metric-box">
                    <div className="metric-label">Research</div>
                    <div className="metric-value">{u.research_impact_score}%</div>
                  </div>
                  <div>
                    <button 
                      className={`btn ${compareList.find(c => c.university_id === u.university_id) ? 'btn-primary' : ''}`}
                      style={{borderRadius: '10px', fontSize: '0.85rem'}}
                      onClick={() => toggleCompare(u)}
                    >
                      {compareList.find(c => c.university_id === u.university_id) ? 'Selected' : 'Compare'}
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </div>
        ) : view === 'compare' ? (
          <div className="animate-in" style={{paddingTop: '2rem'}}>
            <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '3rem'}}>
              <h2>Performance Comparison Dashboard</h2>
              <button className="btn btn-primary" onClick={() => setView('rankings')}>Back to Index</button>
            </div>

            {compareList.length === 0 ? (
              <div className="card" style={{textAlign: 'center', padding: '5rem'}}>
                <GraduationCap size={48} color="#ddd" style={{marginBottom: '1rem'}} />
                <p>Select universities from the main index to compare performance metrics.</p>
              </div>
            ) : (
              <div className="comparison-grid">
                {compareList.map(u => (
                  <div key={u.university_id} className="comparison-card">
                    <div style={{marginBottom: '2rem'}}>
                      <h3 style={{fontSize: '1.8rem', color: 'var(--primary)', lineHeight: 1.2}}>{u.university_name}</h3>
                      <div className="univ-meta" style={{marginTop: '0.5rem'}}>
                        <Globe size={16} /> {u.country} | {u.region}
                      </div>
                    </div>

                    <div style={{background: '#f8f9fa', padding: '1.5rem', borderRadius: '16px', marginBottom: '2rem'}}>
                      <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center'}}>
                        <span style={{fontWeight: 800, fontSize: '1.2rem'}}>UNIVrank Index</span>
                        <span className="rank-badge" style={{padding: '0.5rem 1rem', background: 'var(--primary)', color: 'white', borderRadius: '8px'}}>#{u.univrank}</span>
                      </div>
                    </div>

                    <div className="comparison-sections">
                      <h4 style={{fontSize: '0.8rem', textTransform: 'uppercase', color: 'var(--text-light)', letterSpacing: '1px', marginBottom: '1rem', display: 'flex', alignItems: 'center', gap: '0.5rem'}}>
                        <Trophy size={14} /> Core Platform Rankings
                      </h4>
                      <div className="metric-row">
                        <span className="metric-label">QS World (2026)</span>
                        <span className="metric-value">{u.qs_rank}</span>
                      </div>
                      <div className="metric-row">
                        <span className="metric-label">Times Higher Ed</span>
                        <span className="metric-value">{u.the_rank}</span>
                      </div>
                      <div className="metric-row">
                        <span className="metric-label">ARWU Academic</span>
                        <span className="metric-value">{u.arwu_rank || 'N/A'}</span>
                      </div>

                      <h4 style={{fontSize: '0.8rem', textTransform: 'uppercase', color: 'var(--text-light)', letterSpacing: '1px', marginTop: '2rem', marginBottom: '1rem', display: 'flex', alignItems: 'center', gap: '0.5rem'}}>
                        <Award size={14} /> Excellence Metrics
                      </h4>
                      <div className="metric-row">
                        <span className="metric-label"><Leaf size={14} style={{color: 'green'}} /> Sustainability</span>
                        <span className="metric-value">{u.sustainability_score}%</span>
                      </div>
                      <div className="metric-row">
                        <span className="metric-label"><FlaskConical size={14} style={{color: 'blue'}} /> Research Quality</span>
                        <span className="metric-value">{u.research_impact_score}%</span>
                      </div>
                      <div className="metric-row">
                        <span className="metric-label"><Briefcase size={14} style={{color: '#d4af37'}} /> Employer Reputation</span>
                        <span className="metric-value">{u.employer_reputation_score}%</span>
                      </div>
                      <div className="metric-row">
                        <span className="metric-label"><Users size={14} style={{color: '#007bff'}} /> Student Outlook</span>
                        <span className="metric-value">{u.international_outlook_score}%</span>
                      </div>

                      <h4 style={{fontSize: '0.8rem', textTransform: 'uppercase', color: 'var(--text-light)', letterSpacing: '1px', marginTop: '2rem', marginBottom: '1rem'}}>
                         Student Data
                      </h4>
                      <div className="metric-row">
                        <span className="metric-label">Nobel Laureates</span>
                        <span className="metric-value">{u.nobel_laureates}</span>
                      </div>
                      <div className="metric-row">
                        <span className="metric-label">Tuition Range</span>
                        <span className="metric-value" style={{fontSize: '0.8rem'}}>{u.tuition_fee_range}</span>
                      </div>

                      <div style={{marginTop: '2rem'}}>
                        <a 
                          href={u.website_url} 
                          target="_blank" 
                          rel="noreferrer"
                          className="btn" 
                          style={{display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '0.5rem', background: '#eee', color: 'var(--primary)', width: '100%'}}
                        >
                          Visit Institution <ExternalLink size={14} />
                        </a>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        ) : view === 'admission' ? (
          <AdmissionEvaluator />
        ) : null}
      </main>

      <footer style={{margin: '6rem 0 3rem 0', textAlign: 'center', opacity: 0.6, fontSize: '0.9rem'}}>
        <div className="container" style={{borderTop: '1px solid #ddd', paddingTop: '2rem'}}>
          <p>© 2026 UNIVrank Intelligence. Data sourced from world university ranking providers.</p>
          <div style={{marginTop: '1rem', display: 'flex', gap: '1rem', justifyContent: 'center'}}>
            <span>QS World</span> • <span>Times Higher Ed</span> • <span>ARWU</span>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default App;
