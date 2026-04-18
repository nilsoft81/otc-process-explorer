import React, { useState, useEffect, useRef } from 'react'
import ProcessMap from './components/ProcessMap'
import { Activity, RefreshCw, Download, Image } from 'lucide-react'
import { downloadBPMN } from './utils/bpmnExport'
import html2canvas from 'html2canvas'

const RACI_LEGEND = [
  { short: 'R', label: 'Responsible', dot: 'bg-emerald-400', text: 'text-emerald-300', ring: 'ring-emerald-600/40', bg: 'bg-emerald-900/30' },
  { short: 'A', label: 'Accountable', dot: 'bg-amber-400',   text: 'text-amber-300',   ring: 'ring-amber-600/40',   bg: 'bg-amber-900/30'   },
  { short: 'C', label: 'Consulted',   dot: 'bg-blue-400',    text: 'text-blue-300',    ring: 'ring-blue-600/40',    bg: 'bg-blue-900/30'    },
]

export default function App() {
  const [processes, setProcesses] = useState(null)
  const [loading, setLoading]     = useState(true)
  const [error, setError]         = useState(null)
  const mapRef = useRef(null)

  useEffect(() => {
    fetch('https://otc-process-explorer.onrender.com/api/processes')
      .then(r => { if (!r.ok) throw new Error(`HTTP ${r.status}`); return r.json() })
      .then(json => { setProcesses(json); setLoading(false) })
      .catch(err => { setError(err.message); setLoading(false) })
  }, [])

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
    <div className="min-h-screen flex flex-col bg-slate-900">

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
              <span className="text-xs text-slate-600 ml-1 pl-2 border-l border-slate-700">
                <span className="text-violet-400 font-bold">Δ</span> = To-Be change &nbsp;
                <span className="text-amber-400">◇</span> = Decision
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
