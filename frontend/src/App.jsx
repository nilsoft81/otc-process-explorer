import React, { useState, useEffect, useRef, useCallback } from 'react'
import ProcessMap from './components/ProcessMap'
import UploadPage from './components/UploadPage'
import { Activity, RefreshCw, Download, Image, Upload } from 'lucide-react'
import { downloadBPMN } from './utils/bpmnExport'
import html2canvas from 'html2canvas'
import { jsPDF } from 'jspdf'

const API = 'https://otc-process-explorer.onrender.com'

const RACI_LEGEND = [
  { short: 'R', label: 'Responsible', dot: 'bg-emerald-400', text: 'text-emerald-300', ring: 'ring-emerald-600/40', bg: 'bg-emerald-900/30' },
  { short: 'A', label: 'Accountable', dot: 'bg-slate-400',   text: 'text-slate-300',   ring: 'ring-slate-600/40',   bg: 'bg-slate-800/60'   },
  { short: 'I', label: 'Informed',    dot: 'bg-slate-500',   text: 'text-slate-400',   ring: 'ring-slate-600/40',   bg: 'bg-slate-800/40'   },
  { short: 'C', label: 'Consulted',   dot: 'bg-sky-400',     text: 'text-sky-300',     ring: 'ring-sky-600/40',     bg: 'bg-sky-900/30'     },
]

export default function App() {
  const [processes, setProcesses] = useState(null)
  const [loading, setLoading]     = useState(true)
  const [error, setError]         = useState(null)
  const [page, setPage]           = useState('map') // 'map' | 'upload'
  const [pdfLoading, setPdfLoading] = useState(false)
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

  async function downloadPDF() {
    if (!mapRef.current) return
    setPdfLoading(true)
    try {
      const scrollEl = mapRef.current.firstElementChild
      const fullW = scrollEl.scrollWidth
      const fullH = scrollEl.scrollHeight

      // Dynamically scale down so the canvas never exceeds ~120 million pixels,
      // which is a safe threshold across all modern browsers. Large expanded maps
      // would otherwise exceed the browser canvas memory limit and produce a
      // corrupted/empty PDF.
      const TARGET_PX = 120_000_000
      const scale = fullW * fullH > 0
        ? Math.min(1.5, Math.sqrt(TARGET_PX / (fullW * fullH)))
        : 1.5

      const canvas = await html2canvas(scrollEl, {
        backgroundColor: '#f8fafc',
        scale,
        width: fullW,
        height: fullH,
        windowWidth: fullW,
        windowHeight: fullH,
        useCORS: true,
        logging: false,
      })

      const imgData = canvas.toDataURL('image/jpeg', scale < 1.0 ? 0.80 : 0.88)
      if (!imgData || imgData === 'data:,') throw new Error('Canvas capture was empty')

      const pxToPt = 72 / 96
      const pdfW = fullW * pxToPt
      const pdfH = fullH * pxToPt
      const pdf = new jsPDF({
        orientation: pdfW > pdfH ? 'l' : 'p',
        unit: 'pt',
        format: [pdfW, pdfH],
      })
      pdf.addImage(imgData, 'JPEG', 0, 0, pdfW, pdfH)
      pdf.save('otc-process-map.pdf')
    } catch (e) {
      console.error('PDF export failed:', e)
      alert('PDF export failed. If all processes are expanded the map may be too large — try collapsing some sections first, then export again.')
    } finally {
      setPdfLoading(false)
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
              <p className="text-xs text-teal-400/80 mt-0.5">Swimlanes are at L3 level</p>
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

            {/* Download PDF */}
            <button
              onClick={downloadPDF}
              disabled={pdfLoading}
              className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg border border-rose-500/40 bg-rose-500/10 text-rose-300 text-xs font-medium hover:bg-rose-500/20 transition-colors flex-shrink-0 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {pdfLoading
                ? <><RefreshCw size={13} className="animate-spin" />Generating…</>
                : <><Download size={13} />Download PDF</>}
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
                <span className="text-slate-400">AI involvement step</span>
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
