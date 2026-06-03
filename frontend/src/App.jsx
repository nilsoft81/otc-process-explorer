import React, { useState, useEffect, useRef, useCallback } from 'react'
import ProcessMap from './components/ProcessMap'
import UploadPage from './components/UploadPage'
import { Activity, RefreshCw, Download, Image, Upload } from 'lucide-react'
import { downloadBPMN } from './utils/bpmnExport'
import html2canvas from 'html2canvas'

const API = 'https://otc-process-explorer.onrender.com'

const RACI_LEGEND = [
  { short: 'R', label: 'Responsible', dot: 'bg-emerald-400', text: 'text-emerald-300', ring: 'ring-emerald-600/40', bg: 'bg-emerald-900/30' },
  { short: 'A', label: 'Accountable', dot: 'bg-slate-400',   text: 'text-slate-300',   ring: 'ring-slate-600/40',   bg: 'bg-slate-800/60'   },
  { short: 'I', label: 'Informed',    dot: 'bg-slate-500',   text: 'text-slate-400',   ring: 'ring-slate-600/40',   bg: 'bg-slate-800/40'   },
]

export default function App() {
  const [processes, setProcesses] = useState(null)
  const [loading, setLoading]     = useState(true)
  const [error, setError]         = useState(null)
  const [page, setPage]           = useState('map') // 'map' | 'upload'
  const mapRef = useRef(null)

  const fetchProcesses = useCallback(() => {
    setLoading(true)
    setError(null)
    fetch(`${API}/api/processes`)
      .then(r => { if (!r.ok) throw new Error(`HTTP ${r.status}`); return r.json() })
      .then(json => { setProcesses(json); setLoading(false) })
      .catch(err => { setError(err.message); setLoading(false) })
  }, [])

  useEffect(() => { fetchProcesses() }, [fetchProcesses])

  function handleUploadSuccess() {
    setPage('map')
    fetchProcesses()
  }

  function downloadJSON() {
    const blob = new Blob(
      [JSON.stringify(processes, null, 2)],
      { type: 'application/json' }
    )
    const link = document.createElement('a')
    link.download = 'otc-process-map.json'
    link.href = URL.createObjectURL(blob)
    link.click()
    URL.revokeObjectURL(link.href)
  }

  async function downloadImage() {
    if (!mapRef.current) return
    try {
      const canvas = await html2canvas(mapRef.current, { backgroundColor: '#f8fafc', scale: 2 })
      const link = document.createElement('a')
      link.download = 'otc-process-map.png'
      link.href = canvas.toDataURL('image/png')
      link.click()
    } catch (e) {
      console.error('Image export failed:', e)
    }
  }

  // Upload page
  if (page === 'upload') {
    return (
      <UploadPage
        onBack={() => setPage('map')}
        onSuccess={handleUploadSuccess}
      />
    )
  }

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-slate-900">
        <div className="flex flex-col items-center gap-4 text-slate-400">
          <RefreshCw size={32} className="animate-spin text-teal-400" />
          <p className="text-sm">Loading process map…</p>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-slate-900">
        <div className="bg-red-900/30 border border-red-500/40 rounded-xl p-8 max-w-md text-center">
          <div className="text-4xl mb-3">⚠️</div>
          <h2 className="text-red-300 font-bold text-lg mb-2">Failed to load data</h2>
          <p className="text-slate-400 text-sm mb-1">Could not reach the backend API.</p>
          <code className="block mt-2 text-xs bg-slate-800 text-teal-300 rounded px-3 py-2">
            uvicorn main:app --reload
          </code>
          <p className="text-slate-600 text-xs mt-2">Error: {error}</p>
        </div>
      </div>
    )
  }

  return (
    <div className="h-screen flex flex-col bg-slate-900">

      {/* ── Header ─────────────────────────────────────────────────────────── */}
      <header className="flex-shrink-0 border-b border-slate-700/60 bg-slate-900/95 backdrop-blur px-6 py-3">
        <div className="flex items-center justify-between flex-wrap gap-3">

          {/* Title */}
          <div className="flex items-center gap-3">
            <div className="p-2 bg-teal-500/20 rounded-lg border border-teal-500/30">
              <Activity size={20} className="text-teal-400" />
            </div>
            <div>
              <h1 className="text-base font-bold text-white leading-tight">OTC Process Explorer</h1>
              <p className="text-xs text-slate-500">
                Expandable process map · L1 → L4 · RACI · Systems · Handoffs
              </p>
            </div>
          </div>

          <div className="flex items-center gap-3 flex-wrap">

            {/* Upload Data */}
            <button
              onClick={() => setPage('upload')}
              className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg border border-amber-500/40 bg-amber-500/10 text-amber-300 text-xs font-medium hover:bg-amber-500/20 transition-colors flex-shrink-0"
            >
              <Upload size={13} />
              Upload Data
            </button>

            {/* Download BPMN */}
            <button
              onClick={() => downloadBPMN(processes[0])}
              className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg border border-teal-500/40 bg-teal-500/10 text-teal-300 text-xs font-medium hover:bg-teal-500/20 transition-colors flex-shrink-0"
            >
              <Download size={13} />
              Download BPMN 2.0
            </button>

            {/* Download JSON */}
            <button
              onClick={downloadJSON}
              className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg border border-emerald-500/40 bg-emerald-500/10 text-emerald-300 text-xs font-medium hover:bg-emerald-500/20 transition-colors flex-shrink-0"
            >
              <Download size={13} />
              Download JSON
            </button>

            {/* Download Image */}
            <button
              onClick={downloadImage}
              className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg border border-violet-500/40 bg-violet-500/10 text-violet-300 text-xs font-medium hover:bg-violet-500/20 transition-colors flex-shrink-0"
            >
              <Image size={13} />
              Download Image
            </button>

            {/* RACI legend */}
            <div className="flex items-center gap-2 flex-wrap">
              {RACI_LEGEND.map(r => (
                <span
                  key={r.short}
                  className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-lg ring-1 text-xs ${r.bg} ${r.ring}`}
                >
                  <span className={`w-2 h-2 rounded-full flex-shrink-0 ${r.dot}`} />
                  <span className={`font-bold ${r.text}`}>{r.short}</span>
                  <span className="text-slate-400">{r.label}</span>
                </span>
              ))}
            </div>

            {/* Indicators legend */}
            <div className="flex items-center gap-2 flex-wrap pl-2 border-l border-slate-700">
              <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-lg ring-1 text-xs
                bg-violet-900/30 ring-violet-600/40">
                <span className="text-violet-300 font-bold">🤖</span>
                <span className="text-violet-300 font-bold">AI Agent</span>
                <span className="text-slate-400">AI-responsible step</span>
              </span>
              <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-lg ring-1 text-xs
                bg-slate-800/60 ring-slate-600/40">
                <svg width="14" height="14" viewBox="0 0 14 14" className="flex-shrink-0">
                  <rect x="2" y="2" width="10" height="10" transform="rotate(45 7 7)"
                    fill="none" stroke="#94a3b8" strokeWidth="1.4"/>
                </svg>
                <span className="text-slate-300 font-bold">Decision</span>
                <span className="text-slate-400">Gateway with Yes/No paths</span>
              </span>
            </div>
          </div>

        </div>
      </header>

      {/* ── Process Map ────────────────────────────────────────────────────── */}
      <main className="flex-1 overflow-hidden" ref={mapRef}>
        <ProcessMap processes={processes} />
      </main>

    </div>
  )
}
