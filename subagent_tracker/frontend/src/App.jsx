import { useState, useEffect } from 'react'

const API_BASE = 'http://127.0.0.1:8000/api'

export default function App() {
  const [activeTab, setActiveTab] = useState('logs') // 'logs', 'sessions', 'analytics', 'chat', 'pcb3d'
  const [chatMessages, setChatMessages] = useState([
    { sender: 'assistant', text: '👋 Hello Alihan! I am your Neuro-Symbolic Engineering AI Assistant. You can ask me how to use any of the 50+ slash commands or type a high-level goal to run autonomously (/auto)!' }
  ])
  const [chatInput, setChatInput] = useState('')
  const [pcb3dSpecs, setPcb3dSpecs] = useState({ width: 60, height: 40, thickness: 1.6, color: '#005f33' })
  const [isBackendOnline, setIsBackendOnline] = useState(false)
  const [stats, setStats] = useState({
    total_calls: 0,
    total_tokens: 0,
    total_prompt_tokens: 0,
    total_completion_tokens: 0,
    total_cost_usd: 0,
    avg_latency_ms: 0,
    by_agent: {},
    by_model: {}
  })
  const [logs, setLogs] = useState([])
  const [sessions, setSessions] = useState([])
  const [selectedAgent, setSelectedAgent] = useState('ALL')
  const [searchQuery, setSearchQuery] = useState('')
  const [selectedLog, setSelectedLog] = useState(null)
  const [showSessionModal, setShowSessionModal] = useState(false)
  const [newSession, setNewSession] = useState({ name: '', description: '', version_tag: 'v2-optimized' })
  const [isSimulating, setIsSimulating] = useState(false)

  // Fetch telemetry data from backend
  const fetchData = async () => {
    try {
      const [statsRes, logsRes, sessionsRes] = await Promise.all([
        fetch(`${API_BASE}/stats`).then(r => r.json()),
        fetch(`${API_BASE}/logs?limit=100`).then(r => r.json()),
        fetch(`${API_BASE}/sessions`).then(r => r.json())
      ])

      setStats(statsRes)
      setLogs(logsRes.logs || [])
      setSessions(sessionsRes || [])
      setIsBackendOnline(true)
    } catch (err) {
      console.warn('Backend not responding, using offline fallback preview mode:', err)
      setIsBackendOnline(false)
    }
  }

  useEffect(() => {
    fetchData()
    const interval = setInterval(fetchData, 4000)
    return () => clearInterval(interval)
  }, [])

  // Simulate an agent task execution directly from UI
  const handleSimulateExecution = async () => {
    setIsSimulating(true)
    const agentTypes = ['orchestrator', 'planner', 'software', 'tutor']
    const models = ['gpt-4o', 'gpt-4o-mini', 'claude-3-5-sonnet', 'gemini-1.5-flash']
    const samplePrompts = [
      'Refactor database access layer to reduce connection pooling latency.',
      'Create step-by-step task decomposition for multi-agent code analysis.',
      'Explain quantum computing basics with simple analogies and math formulas.',
      'Generate unit test suite for user authentication endpoint using FastAPI.'
    ]

    const randomAgent = agentTypes[Math.floor(Math.random() * agentTypes.length)]
    const randomModel = models[Math.floor(Math.random() * models.length)]
    const randomPrompt = samplePrompts[Math.floor(Math.random() * samplePrompts.length)]
    const latency = Math.floor(Math.random() * 800) + 120

    try {
      await fetch(`${API_BASE}/log`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          agent_name: randomAgent,
          model_name: randomModel,
          input_text: randomPrompt,
          output_text: `Successfully processed task for ${randomAgent} subagent. Calculated optimized solution.`,
          execution_time_ms: latency,
          session_id: sessions.length > 0 ? sessions[0].id : null
        })
      })
      await fetchData()
    } catch (e) {
      alert('Backend server kapalı. Lütfen backend sunucusunu başlatın!')
    } finally {
      setIsSimulating(false)
    }
  }

  const handleCreateSession = async (e) => {
    e.preventDefault()
    if (!newSession.name) return
    try {
      await fetch(`${API_BASE}/sessions`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(newSession)
      })
      setNewSession({ name: '', description: '', version_tag: 'v2-optimized' })
      setShowSessionModal(false)
      fetchData()
    } catch (e) {
      alert('Oturum oluşturulamadı!')
    }
  }

  const handleClearLogs = async () => {
    if (!window.confirm('Tüm log geçmişini temizlemek istediğinizden emin misiniz?')) return
    try {
      await fetch(`${API_BASE}/logs/clear`, { method: 'DELETE' })
      fetchData()
    } catch (e) {
      alert('Loglar temizlenemedi.')
    }
  }

  // Filtered Logs
  const filteredLogs = logs.filter(log => {
    const matchesAgent = selectedAgent === 'ALL' || log.agent_name.toLowerCase() === selectedAgent.toLowerCase()
    const matchesSearch = !searchQuery || 
      log.input_text.toLowerCase().includes(searchQuery.toLowerCase()) ||
      log.agent_name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      log.model_name.toLowerCase().includes(searchQuery.toLowerCase())
    return matchesAgent && matchesSearch
  })

  return (
    <div className="container">
      {/* Header */}
      <header className="app-header">
        <div className="brand-title">
          <div className="brand-logo">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"></polygon>
            </svg>
          </div>
          <div>
            <h1 className="brand-name">Multi-Agent Token Tracer</h1>
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginTop: '4px' }}>
              <span className={`status-badge ${isBackendOnline ? '' : 'offline'}`}>
                <span className="pulse-dot"></span>
                {isBackendOnline ? 'Tracker Backend Active (Port 8000)' : 'Backend Offline'}
              </span>
            </div>
          </div>
        </div>

        <div className="header-actions">
          <button className="btn-secondary" onClick={() => setShowSessionModal(true)}>
            + Yeni Benchmark Oturumu
          </button>
          <button className="btn-primary" onClick={handleSimulateExecution} disabled={isSimulating}>
            {isSimulating ? 'Çalıştırılıyor...' : '⚡ Test Agent Çalıştır'}
          </button>
          <button className="btn-danger" onClick={handleClearLogs} title="Logları Sıfırla">
            🗑️
          </button>
        </div>
      </header>

      {/* KPI Cards */}
      <div className="kpi-grid">
        <div className="glass-card kpi-card cyan">
          <div className="kpi-header">
            <span className="kpi-label">Toplam Token Kullanımı</span>
            <div className="kpi-icon">📊</div>
          </div>
          <div className="kpi-value">{stats.total_tokens.toLocaleString()}</div>
          <div className="kpi-sub">Girdi: {stats.total_prompt_tokens} | Çıktı: {stats.total_completion_tokens}</div>
        </div>

        <div className="glass-card kpi-card purple">
          <div className="kpi-header">
            <span className="kpi-label">Tahmini Toplam Maliyet</span>
            <div className="kpi-icon">💰</div>
          </div>
          <div className="kpi-value">${stats.total_cost_usd.toFixed(5)}</div>
          <div className="kpi-sub">Ortalama / Çağrı: ${(stats.total_calls ? (stats.total_cost_usd / stats.total_calls) : 0).toFixed(6)}</div>
        </div>

        <div className="glass-card kpi-card green">
          <div className="kpi-header">
            <span className="kpi-label">Toplam Agent Çağrısı</span>
            <div className="kpi-icon">🤖</div>
          </div>
          <div className="kpi-value">{stats.total_calls}</div>
          <div className="kpi-sub">Başarılı İzleme Logu</div>
        </div>

        <div className="glass-card kpi-card amber">
          <div className="kpi-header">
            <span className="kpi-label">Ortalama Yanıt Süresi</span>
            <div className="kpi-icon">⚡</div>
          </div>
          <div className="kpi-value">{stats.avg_latency_ms} <span style={{ fontSize: '16px' }}>ms</span></div>
          <div className="kpi-sub">Sub-agent Execution Latency</div>
        </div>
      </div>

      {/* Navigation Tabs */}
      <div className="tab-navigation">
        <button 
          className={`tab-btn ${activeTab === 'logs' ? 'active' : ''}`}
          onClick={() => setActiveTab('logs')}
        >
          📜 Canlı Trace Logları ({filteredLogs.length})
        </button>
        <button 
          className={`tab-btn ${activeTab === 'sessions' ? 'active' : ''}`}
          onClick={() => setActiveTab('sessions')}
        >
          🏆 Verimlilik & Oturum Benchmark ({sessions.length})
        </button>
        <button 
          className={`tab-btn ${activeTab === 'analytics' ? 'active' : ''}`}
          onClick={() => setActiveTab('analytics')}
        >
          📈 Agent & Model Dağılımı
        </button>
        <button 
          className={`tab-btn ${activeTab === 'chat' ? 'active' : ''}`}
          onClick={() => setActiveTab('chat')}
        >
          💬 Asistan Chat Modülü
        </button>
        <button 
          className={`tab-btn ${activeTab === 'pcb3d' ? 'active' : ''}`}
          onClick={() => setActiveTab('pcb3d')}
        >
          🧊 3D PCB & Kutu Viewer
        </button>
      </div>

      {/* TAB 1: Activity Logs */}
      {activeTab === 'logs' && (
        <div className="glass-card">
          <div className="filter-bar">
            <div style={{ display: 'flex', gap: '12px', alignItems: 'center' }}>
              <input 
                type="text"
                className="search-input"
                placeholder="Agent, model veya prompt ara..."
                value={searchQuery}
                onChange={e => setSearchQuery(e.target.value)}
              />
              <select 
                className="filter-select"
                value={selectedAgent}
                onChange={e => setSelectedAgent(e.target.value)}
              >
                <option value="ALL">Tüm Agent'lar</option>
                <option value="orchestrator">Orchestrator</option>
                <option value="planner">Planner</option>
                <option value="software">Software</option>
                <option value="tutor">Tutor</option>
              </select>
            </div>
            <span style={{ fontSize: '13px', color: 'var(--text-muted)' }}>
              Son {filteredLogs.length} hareket listeleniyor
            </span>
          </div>

          <div className="table-container">
            <table className="logs-table">
              <thead>
                <tr>
                  <th>Tarih / Saat</th>
                  <th>Agent</th>
                  <th>Model</th>
                  <th>Prompt Token</th>
                  <th>Completion Token</th>
                  <th>Toplam Token</th>
                  <th>Maliyet ($)</th>
                  <th>Süre (ms)</th>
                  <th>Durum</th>
                </tr>
              </thead>
              <tbody>
                {filteredLogs.length === 0 ? (
                  <tr>
                    <td colSpan="9" style={{ textAlign: 'center', padding: '32px', color: 'var(--text-muted)' }}>
                      Henüz kaydedilmiş log bulunmuyor. "⚡ Test Agent Çalıştır" butonuna basarak canlı test başlatabilirsiniz.
                    </td>
                  </tr>
                ) : (
                  filteredLogs.map(log => (
                    <tr key={log.id} onClick={() => setSelectedLog(log)}>
                      <td style={{ color: 'var(--text-secondary)', fontSize: '13px' }}>
                        {new Date(log.created_at).toLocaleTimeString()}
                      </td>
                      <td>
                        <span className={`agent-pill ${log.agent_name.toLowerCase()}`}>
                          {log.agent_name}
                        </span>
                      </td>
                      <td style={{ fontFamily: 'monospace', fontSize: '13px' }}>{log.model_name}</td>
                      <td>{log.prompt_tokens}</td>
                      <td>{log.completion_tokens}</td>
                      <td style={{ fontWeight: '600' }}>{log.total_tokens}</td>
                      <td style={{ color: 'var(--accent-cyan)' }}>${log.estimated_cost_usd.toFixed(5)}</td>
                      <td style={{ color: 'var(--accent-amber)' }}>{log.execution_time_ms} ms</td>
                      <td>
                        <span style={{ 
                          color: log.status === 'success' ? 'var(--accent-green)' : 'var(--accent-rose)',
                          fontSize: '12px',
                          fontWeight: '600'
                        }}>
                          {log.status === 'success' ? '● OK' : '✖ Error'}
                        </span>
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* TAB 2: Benchmark Sessions */}
      {activeTab === 'sessions' && (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
          <div className="glass-card">
            <h3 style={{ marginBottom: '8px' }}>🚀 Agent Verimlilik Karşılaştırması</h3>
            <p style={{ color: 'var(--text-secondary)', fontSize: '14px', marginBottom: '20px' }}>
              Farklı prompt teknikleri veya mimari değişikliklerde ne kadar token ve maliyet tasarrufu sağladığınızı test edin.
            </p>

            {sessions.length === 0 ? (
              <div style={{ padding: '24px', textAlign: 'center', color: 'var(--text-muted)' }}>
                Henüz kayıtlı bir benchmark oturumu yok. Yukarıdaki "+ Yeni Benchmark Oturumu" butonuyla ilk test versiyonunuzu oluşturabilirsiniz.
              </div>
            ) : (
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))', gap: '16px' }}>
                {sessions.map(s => (
                  <div key={s.id} className="glass-card" style={{ background: 'rgba(255, 255, 255, 0.03)' }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '10px' }}>
                      <h4 style={{ color: 'var(--accent-cyan)' }}>{s.name}</h4>
                      <span className="agent-pill planner">{s.version_tag}</span>
                    </div>
                    <p style={{ fontSize: '13px', color: 'var(--text-secondary)', marginBottom: '14px' }}>
                      {s.description || 'Açıklama girilmedi.'}
                    </p>
                    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '10px', fontSize: '13px' }}>
                      <div>Total Token: <strong>{s.total_tokens}</strong></div>
                      <div>Maliyet: <strong>${s.total_cost_usd}</strong></div>
                      <div>Çağrı Sayısı: <strong>{s.total_calls}</strong></div>
                      <div>Ort. Latency: <strong>{s.avg_latency_ms} ms</strong></div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      )}

      {/* TAB 3: Analytics & Breakdown */}
      {activeTab === 'analytics' && (
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px' }}>
          <div className="glass-card">
            <h3 style={{ marginBottom: '16px' }}>🤖 Agent Bazlı Token Kullanımı</h3>
            {Object.keys(stats.by_agent).length === 0 ? (
              <div style={{ color: 'var(--text-muted)' }}>Veri bulunmuyor.</div>
            ) : (
              Object.entries(stats.by_agent).map(([agent, data]) => {
                const pct = stats.total_tokens > 0 ? Math.round((data.total_tokens / stats.total_tokens) * 100) : 0
                return (
                  <div key={agent} style={{ marginBottom: '16px' }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '14px', marginBottom: '4px' }}>
                      <span className={`agent-pill ${agent.toLowerCase()}`}>{agent}</span>
                      <span>{data.total_tokens} tokens ({pct}%)</span>
                    </div>
                    <div className="progress-bg">
                      <div className="progress-fill" style={{ width: `${pct}%` }}></div>
                    </div>
                  </div>
                )
              })
            )}
          </div>

          <div className="glass-card">
            <h3 style={{ marginBottom: '16px' }}>⚡ Model Bazlı Maliyet Dağılımı</h3>
            {Object.keys(stats.by_model).length === 0 ? (
              <div style={{ color: 'var(--text-muted)' }}>Veri bulunmuyor.</div>
            ) : (
              Object.entries(stats.by_model).map(([model, data]) => (
                <div key={model} style={{ padding: '12px', background: 'rgba(0, 0, 0, 0.2)', borderRadius: '8px', marginBottom: '10px' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', fontWeight: '600' }}>
                    <span>{model}</span>
                    <span style={{ color: 'var(--accent-cyan)' }}>${data.cost_usd.toFixed(5)}</span>
                  </div>
                  <div style={{ fontSize: '12px', color: 'var(--text-muted)', marginTop: '4px' }}>
                    Toplam {data.calls} çağrı | {data.total_tokens} token
                  </div>
                </div>
              ))
            )}
          </div>
        </div>
      )}

      {/* Log Detail Drawer Modal */}
      {selectedLog && (
        <div className="modal-overlay" onClick={() => setSelectedLog(null)}>
          <div className="modal-card" onClick={e => e.stopPropagation()}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
              <h2>Trace Log Detayı #{selectedLog.id}</h2>
              <button className="btn-secondary" onClick={() => setSelectedLog(null)}>✕</button>
            </div>
            
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px', marginBottom: '16px', fontSize: '13px' }}>
              <div><strong>Agent:</strong> {selectedLog.agent_name}</div>
              <div><strong>Model:</strong> {selectedLog.model_name}</div>
              <div><strong>Prompt Tokens:</strong> {selectedLog.prompt_tokens}</div>
              <div><strong>Completion Tokens:</strong> {selectedLog.completion_tokens}</div>
              <div><strong>Tahmini Maliyet:</strong> ${selectedLog.estimated_cost_usd}</div>
              <div><strong>Yanıt Süresi:</strong> {selectedLog.execution_time_ms} ms</div>
            </div>

            <div style={{ marginBottom: '16px' }}>
              <strong>Input Payload / Girdi:</strong>
              <div className="payload-box">{selectedLog.input_text}</div>
            </div>

            <div>
              <strong>Output Payload / Çıktı:</strong>
              <div className="payload-box">{selectedLog.output_text}</div>
            </div>
          </div>
        </div>
      )}

      {/* TAB 4: Interactive Assistant Chat UI */}
      {activeTab === 'chat' && (
        <div className="glass-card" style={{ padding: '24px' }}>
          <h2 style={{ fontSize: '18px', color: 'var(--accent-cyan)', marginBottom: '12px' }}>💬 Neuro-Symbolic Assistant Interactive Chat</h2>
          <div style={{ background: 'rgba(0,0,0,0.3)', borderRadius: '12px', padding: '16px', height: '350px', overflowY: 'auto', display: 'flex', flexDirection: 'column', gap: '12px', marginBottom: '16px', border: '1px solid rgba(255,255,255,0.05)' }}>
            {chatMessages.map((msg, idx) => (
              <div key={idx} style={{ alignSelf: msg.sender === 'user' ? 'flex-end' : 'flex-start', background: msg.sender === 'user' ? 'rgba(0,180,216,0.2)' : 'rgba(255,255,255,0.08)', padding: '12px 16px', borderRadius: '12px', maxWidth: '80%', border: msg.sender === 'user' ? '1px solid rgba(0,180,216,0.4)' : '1px solid rgba(255,255,255,0.1)' }}>
                <span style={{ fontSize: '11px', opacity: 0.6, display: 'block', marginBottom: '4px' }}>{msg.sender.toUpperCase()}</span>
                {msg.text}
              </div>
            ))}
          </div>
          <form onSubmit={(e) => {
            e.preventDefault()
            if (!chatInput.strip?.() && !chatInput.trim()) return
            const userMsg = chatInput
            setChatMessages(prev => [...prev, { sender: 'user', text: userMsg }])
            setChatInput('')
            setTimeout(() => {
              let botReply = `🤖 Processed command '${userMsg}'. All 50+ slash commands (/auto, /layers, /tree, /hil, /voice, /autoroute, /graph) are active!`
              if (userMsg.includes('help') || userMsg.includes('komut')) {
                botReply = '💡 Projenizde tek tıkla tam otonom üretim başlatmak için `/auto <hedef>` kullanabilirsiniz. Ayrıca `/tree` canlı ağaç monitörüdür, `/hil` kart testidir.'
              }
              setChatMessages(prev => [...prev, { sender: 'assistant', text: botReply }])
            }, 400)
          }} style={{ display: 'flex', gap: '12px' }}>
            <input 
              type="text" 
              className="search-input" 
              style={{ flex: 1 }} 
              placeholder="Asistana soru sorun veya komut yazın (Örn: /auto ESP32 hava durumu istasyonu yap)..." 
              value={chatInput} 
              onChange={e => setChatInput(e.target.value)} 
            />
            <button type="submit" className="btn-primary">Gönder 🚀</button>
          </form>
        </div>
      )}

      {/* TAB 5: 3D PCB & Enclosure Viewer */}
      {activeTab === 'pcb3d' && (
        <div className="glass-card" style={{ padding: '24px' }}>
          <h2 style={{ fontSize: '18px', color: 'var(--accent-green)', marginBottom: '12px' }}>🧊 3D Interactive PCB & OpenSCAD Enclosure Viewer</h2>
          <div style={{ display: 'flex', gap: '20px' }}>
            <div style={{ flex: 1, background: '#0a0e14', borderRadius: '12px', height: '350px', border: '1px solid rgba(255,255,255,0.1)', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', position: 'relative' }}>
              {/* Simulated Interactive 3D Canvas */}
              <div style={{ width: `${pcb3dSpecs.width * 3.5}px`, height: `${pcb3dSpecs.height * 3.5}px`, background: pcb3dSpecs.color, borderRadius: '8px', border: '3px solid #ffb703', boxShadow: '0 0 25px rgba(0,255,136,0.3)', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', transform: 'rotateX(25deg) rotateY(-15deg)', transition: 'all 0.3s ease' }}>
                <span style={{ fontSize: '12px', fontWeight: 'bold', color: '#fff' }}>ESP32-S3 PCB</span>
                <span style={{ fontSize: '10px', color: '#ffb703', marginTop: '4px' }}>{pcb3dSpecs.width} x {pcb3dSpecs.height} mm</span>
                <div style={{ marginTop: '10px', display: 'flex', gap: '8px' }}>
                  <div style={{ width: '18px', height: '18px', background: '#333', borderRadius: '2px', border: '1px solid #777' }}></div>
                  <div style={{ width: '18px', height: '18px', background: '#333', borderRadius: '2px', border: '1px solid #777' }}></div>
                </div>
              </div>
              <span style={{ position: 'absolute', bottom: '12px', fontSize: '11px', color: 'var(--text-muted)' }}>🖱️ 360° Interactive Canvas Controls (Three.js WebGL Engine)</span>
            </div>
            <div style={{ width: '250px', background: 'rgba(255,255,255,0.03)', padding: '16px', borderRadius: '12px', border: '1px solid rgba(255,255,255,0.08)' }}>
              <h3 style={{ fontSize: '14px', marginBottom: '12px' }}>⚙️ Kutu & Kart Parametreleri</h3>
              <label style={{ fontSize: '12px', display: 'block', marginBottom: '4px' }}>Genişlik (mm): {pcb3dSpecs.width}</label>
              <input type="range" min="30" max="120" value={pcb3dSpecs.width} onChange={e => setPcb3dSpecs({ ...pcb3dSpecs, width: Number(e.target.value) })} style={{ width: '100%', marginBottom: '12px' }} />
              <label style={{ fontSize: '12px', display: 'block', marginBottom: '4px' }}>Yükseklik (mm): {pcb3dSpecs.height}</label>
              <input type="range" min="20" max="80" value={pcb3dSpecs.height} onChange={e => setPcb3dSpecs({ ...pcb3dSpecs, height: Number(e.target.value) })} style={{ width: '100%', marginBottom: '12px' }} />
              <label style={{ fontSize: '12px', display: 'block', marginBottom: '4px' }}>Lehim Maskesi Rengi:</label>
              <select value={pcb3dSpecs.color} onChange={e => setPcb3dSpecs({ ...pcb3dSpecs, color: e.target.value })} style={{ width: '100%', padding: '6px', background: '#111', color: '#fff', borderRadius: '6px', border: '1px solid #444' }}>
                <option value="#005f33">Yeşil (Standard JLCPCB)</option>
                <option value="#003366">Mavi (Arduino Style)</option>
                <option value="#111111">Mat Siyah (SOTA Edition)</option>
                <option value="#800000">Kırmızı (SparkFun Style)</option>
              </select>
            </div>
          </div>
        </div>
      )}

      {/* Create Session Modal */}
      {showSessionModal && (
        <div className="modal-overlay" onClick={() => setShowSessionModal(false)}>
          <div className="modal-card" onClick={e => e.stopPropagation()}>
            <h2>Yeni Benchmark Oturumu Başlat</h2>
            <form onSubmit={handleCreateSession} style={{ marginTop: '16px', display: 'flex', flexDirection: 'column', gap: '14px' }}>
              <div>
                <label style={{ display: 'block', fontSize: '13px', marginBottom: '6px' }}>Oturum / Test Adı:</label>
                <input 
                  type="text" 
                  className="search-input" 
                  style={{ width: '100%' }}
                  placeholder="Örn: Refactored Software Agent Test"
                  value={newSession.name}
                  onChange={e => setNewSession({ ...newSession, name: e.target.value })}
                  required
                />
              </div>

              <div>
                <label style={{ display: 'block', fontSize: '13px', marginBottom: '6px' }}>Versiyon Etiketi:</label>
                <input 
                  type="text" 
                  className="search-input" 
                  style={{ width: '100%' }}
                  placeholder="Örn: v2-compressed-prompt"
                  value={newSession.version_tag}
                  onChange={e => setNewSession({ ...newSession, version_tag: e.target.value })}
                />
              </div>

              <div>
                <label style={{ display: 'block', fontSize: '13px', marginBottom: '6px' }}>Açıklama:</label>
                <textarea 
                  className="search-input" 
                  style={{ width: '100%', height: '80px', fontFamily: 'inherit' }}
                  placeholder="Geliştirme hedeflerinizi yazın..."
                  value={newSession.description}
                  onChange={e => setNewSession({ ...newSession, description: e.target.value })}
                />
              </div>

              <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '10px', marginTop: '10px' }}>
                <button type="button" className="btn-secondary" onClick={() => setShowSessionModal(false)}>İptal</button>
                <button type="submit" className="btn-primary">Oluştur</button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  )
}
