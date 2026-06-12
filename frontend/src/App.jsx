import React, { useState, useEffect, useRef, useCallback } from 'react'
import ProcessMap from './components/ProcessMap'
import UploadPage from './components/UploadPage'
import { Activity, RefreshCw, Download, Image, Upload } from 'lucide-react'
import { downloadBPMN } from './utils/bpmnExport'
import html2canvas from 'html2canvas'
import { jsPDF } from 'jspdf'

const API = 'https://otc-process-explorer.onrender.com'

const RACI_LEGEND = [
  { short: 'R', label: 'Responsible',  dot: 'bg-emerald-400', text: 'text-emerald-300', ring: 'ring-emerald-600/40', bg: 'bg-emerald-900/30' },
  { short: 'A', label: 'Accountable',  dot: 'bg-slate-400',   text: 'text-slate-300',   ring: 'ring-slate-600/40',   bg: 'bg-slate-800/60'   },
  { short: 'C', label: 'Contributing', dot: 'bg-sky-400',     text: 'text-sky-300',     ring: 'ring-sky-600/40',     bg: 'bg-sky-900/30'     },
  { short: 'I', label: 'Informed',     dot: 'bg-slate-500',   text: 'text-slate-400',   ring: 'ring-slate-600/40',   bg: 'bg-slate-800/40'   },
]

// ── Tile-by-tile full-map capture ─────────────────────────────────────────────
// html2canvas only renders what the browser has painted on-screen.  For a large
// grid most columns/rows are outside the viewport and never painted, so a single
// html2canvas call produces an empty / partial image.
//
// The reliable fix: scroll the container to every tile position so the browser
// paints that region, capture the visible viewport, then stitch the tiles into a
// single master canvas.
//
// Sticky layout constants (must match ProcessMap.jsx):
const ROLE_W = 176  // sticky-left role label column width  (px)
const HEAD_H = 44   // sticky-top  header row height        (px)

// Dark-theme colours that need to be lightened so role labels are readable in exports
const DARK_BG_RGB  = 'rgb(30, 41, 59)'       // #1e293b — role labels / corner cell
const LIGHT_TEXTS  = new Set([
  'rgb(226, 232, 240)', 'rgb(148, 163, 184)',
  'rgb(100, 116, 139)', 'rgb(241, 245, 249)',
])

async function captureTiledCanvas(scrollEl, scale, onProgress, preCapture) {
  const fullW   = scrollEl.scrollWidth
  const fullH   = scrollEl.scrollHeight
  const vpW     = scrollEl.clientWidth    // visible viewport width  (no scrollbar)
  const vpH     = scrollEl.clientHeight   // visible viewport height
  const colStep = Math.max(vpW - ROLE_W, 1)
  const rowStep = Math.max(vpH - HEAD_H,  1)

  // Build deduplicated, sorted scroll-position lists that guarantee full coverage
  const makePositions = (full, vp, step) => {
    const set = new Set([0])
    for (let p = step; p < full - vp; p += step) set.add(p)
    if (full > vp) set.add(full - vp)   // always include last position
    return [...set].sort((a, b) => a - b)
  }
  const xs = makePositions(fullW, vpW, colStep)
  const ys = makePositions(fullH, vpH, rowStep)

  // Create master canvas pre-filled with the map background colour
  const master = document.createElement('canvas')
  master.width  = Math.round(fullW * scale)
  master.height = Math.round(fullH * scale)
  const ctx = master.getContext('2d')
  ctx.fillStyle = '#f1f5f9'
  ctx.fillRect(0, 0, master.width, master.height)

  const total = xs.length * ys.length
  let done = 0

  for (let ri = 0; ri < ys.length; ri++) {
    for (let ci = 0; ci < xs.length; ci++) {
      scrollEl.scrollLeft = xs[ci]
      scrollEl.scrollTop  = ys[ri]
      // Two rAF cycles so the browser finishes painting before we capture
      await new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r)))

      // Read back the ACTUAL scroll position (browser may clamp near edges)
      const sx = scrollEl.scrollLeft
      const sy = scrollEl.scrollTop

      // Re-apply any pre-capture DOM overrides (e.g. light-theme fixes) IMMEDIATELY
      // before html2canvas so React re-renders from onProgress cannot have reset them.
      if (preCapture) preCapture()

      const tile = await html2canvas(scrollEl, {
        backgroundColor: '#f1f5f9',
        scale,
        useCORS: true,
        logging: false,
      })

      const tW  = tile.width
      const tH  = tile.height
      const sRW = Math.round(ROLE_W * scale)   // role-label width in tile pixels
      const sHH = Math.round(HEAD_H * scale)   // header height in tile pixels
      const cW  = Math.max(0, tW - sRW)        // non-sticky content width
      const cH  = Math.max(0, tH - sHH)        // non-sticky content height

      // 1. Non-sticky content → master at (ROLE_W + sx, HEAD_H + sy)
      if (cW > 0 && cH > 0) {
        ctx.drawImage(tile, sRW, sHH, cW, cH,
          Math.round((ROLE_W + sx) * scale),
          Math.round((HEAD_H  + sy) * scale),
          cW, cH)
      }
      // 2. Role-label column (sticky left) — extract from every first-col tile
      if (ci === 0 && sRW > 0 && cH > 0) {
        ctx.drawImage(tile, 0, sHH, sRW, cH,
          0,
          Math.round((HEAD_H + sy) * scale),
          sRW, cH)
      }
      // 3. Header row (sticky top) — extract from every first-row tile
      if (ri === 0 && cW > 0 && sHH > 0) {
        ctx.drawImage(tile, sRW, 0, cW, sHH,
          Math.round((ROLE_W + sx) * scale),
          0,
          cW, sHH)
      }
      // 4. Corner cell — once, from tile (0, 0)
      if (ri === 0 && ci === 0 && sRW > 0 && sHH > 0) {
        ctx.drawImage(tile, 0, 0, sRW, sHH, 0, 0, sRW, sHH)
      }

      done++
      if (onProgress) onProgress(done, total)
    }
  }

  return master
}

export default function App() {
  const [processes, setProcesses] = useState(null)
  const [loading, setLoading]     = useState(true)
  const [error, setError]         = useState(null)
  const [page, setPage]           = useState('map') // 'map' | 'upload'
  const [exportStatus,   setExportStatus]   = useState('') // '' | 'pdf' | 'img'
  const [exportProgress, setExportProgress] = useState('') // e.g. '4 / 20 tiles'
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

  // ── Build per-tile light-theme fix functions ─────────────────────────────────
  // The tiling loop calls setExportProgress() which triggers React re-renders.
  // React re-renders reset any inline styles we set (e.g. role-label background).
  // Fix: scan dark elements ONCE, build fast applyLight / restoreLight functions,
  // then pass applyLight as preCapture so it runs just before each html2canvas call
  // (html2canvas reads the DOM synchronously, before any async React re-render).
  function buildDarkFixes(scrollEl) {
    const entries = []
    scrollEl.querySelectorAll('*').forEach(el => {
      if (window.getComputedStyle(el).backgroundColor === DARK_BG_RGB) {
        const children = []
        const origColors = []
        ;[el, ...el.querySelectorAll('*')].forEach(ch => {
          if (LIGHT_TEXTS.has(window.getComputedStyle(ch).color)) {
            children.push(ch)
            origColors.push(ch.style.color)
          }
        })
        entries.push({ el, origBg: el.style.background, children, origColors })
      }
    })
    const applyLight = () => entries.forEach(({ el, children }) => {
      el.style.background = '#dde3ed'
      children.forEach(ch => { ch.style.color = '#1e293b' })
    })
    const restoreDark = () => entries.forEach(({ el, origBg, children, origColors }) => {
      el.style.background = origBg
      children.forEach((ch, i) => { ch.style.color = origColors[i] })
    })
    return { applyLight, restoreDark }
  }

  async function downloadImage() {
    if (!mapRef.current) return
    setExportStatus('img')
    setExportProgress('0 / ?')
    // Wait for React to flush the status update re-render before we modify the DOM
    await new Promise(r => setTimeout(r, 60))
    const scrollEl  = mapRef.current.firstElementChild
    const savedLeft = scrollEl.scrollLeft
    const savedTop  = scrollEl.scrollTop
    const { applyLight, restoreDark } = buildDarkFixes(scrollEl)
    applyLight()
    try {
      const fullW = scrollEl.scrollWidth
      const fullH = scrollEl.scrollHeight
      const scale = Math.min(1.5, Math.sqrt(100_000_000 / Math.max(fullW * fullH, 1)))
      const master = await captureTiledCanvas(scrollEl, scale, (done, total) => {
        setExportProgress(`${done} / ${total} tiles`)
      }, applyLight)   // re-apply before each tile in case React reset the styles
      scrollEl.scrollLeft = savedLeft
      scrollEl.scrollTop  = savedTop
      const link = document.createElement('a')
      link.download = 'otc-process-map.png'
      link.href = master.toDataURL('image/png')
      link.click()
    } catch (e) {
      console.error('Image export failed:', e)
      alert('Image export failed.')
    } finally {
      scrollEl.scrollLeft = savedLeft
      scrollEl.scrollTop  = savedTop
      restoreDark()
      setExportStatus('')
      setExportProgress('')
    }
  }

  async function downloadPDF() {
    if (!mapRef.current) return
    setExportStatus('pdf')
    setExportProgress('0 / ?')
    // Wait for React to flush the status update re-render before we modify the DOM
    await new Promise(r => setTimeout(r, 60))
    const scrollEl  = mapRef.current.firstElementChild
    const savedLeft = scrollEl.scrollLeft
    const savedTop  = scrollEl.scrollTop
    const { applyLight, restoreDark } = buildDarkFixes(scrollEl)
    applyLight()
    try {
      const fullW = scrollEl.scrollWidth
      const fullH = scrollEl.scrollHeight

      // Use 150 M-pixel cap for better resolution than the old 100 M limit.
      const scale = Math.min(1.0, Math.sqrt(150_000_000 / Math.max(fullW * fullH, 1)))
      const master = await captureTiledCanvas(scrollEl, scale, (done, total) => {
        setExportProgress(`${done} / ${total} tiles`)
      }, applyLight)   // re-apply before each tile in case React reset the styles
      scrollEl.scrollLeft = savedLeft
      scrollEl.scrollTop  = savedTop

      const imgData = master.toDataURL('image/jpeg', 0.88)
      if (!imgData || imgData === 'data:,') throw new Error('Empty canvas')

      // PDF page dimensions: use the master canvas pixel size as PDF points (1 px = 1 pt).
      // This gives the maximum possible resolution within the canvas.
      // Cap both dimensions to 14 000 pt (just below the 14 400 pt PDF-spec hard limit)
      // so all viewers render the complete page without clipping.
      const MAX_PT   = 14000
      const rawPdfW  = master.width
      const rawPdfH  = master.height
      const shrink   = Math.min(1, MAX_PT / Math.max(rawPdfW, rawPdfH))
      const pdfW     = Math.round(rawPdfW * shrink)
      const pdfH     = Math.round(rawPdfH * shrink)
      const pdf = new jsPDF({ orientation: pdfW > pdfH ? 'l' : 'p', unit: 'pt', format: [pdfW, pdfH] })
      pdf.addImage(imgData, 'JPEG', 0, 0, pdfW, pdfH)
      pdf.save('otc-process-map.pdf')
    } catch (e) {
      console.error('PDF export failed:', e)
      alert('PDF export failed.')
    } finally {
      scrollEl.scrollLeft = savedLeft
      scrollEl.scrollTop  = savedTop
      restoreDark()
      setExportStatus('')
      setExportProgress('')
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
              <p className="text-xs text-teal-400/80 mt-0.5 font-semibold tracking-wide">SWIMLANES ARE SHOWN AT L3 LEVEL</p>
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
              disabled={!!exportStatus}
              className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg border border-violet-500/40 bg-violet-500/10 text-violet-300 text-xs font-medium hover:bg-violet-500/20 transition-colors flex-shrink-0 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {exportStatus === 'img'
                ? <><RefreshCw size={13} className="animate-spin" />{exportProgress || 'Capturing…'}</>
                : <><Image size={13} />Download Image</>}
            </button>

            {/* Download PDF */}
            <button
              onClick={downloadPDF}
              disabled={!!exportStatus}
              className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg border border-rose-500/40 bg-rose-500/10 text-rose-300 text-xs font-medium hover:bg-rose-500/20 transition-colors flex-shrink-0 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {exportStatus === 'pdf'
                ? <><RefreshCw size={13} className="animate-spin" />{exportProgress || 'Capturing…'}</>
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
