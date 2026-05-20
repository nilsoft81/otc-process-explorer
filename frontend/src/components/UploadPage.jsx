import React, { useState, useRef } from 'react'
import { Upload, CheckCircle, XCircle, ArrowLeft, FileSpreadsheet, AlertCircle } from 'lucide-react'

const API = 'https://otc-process-explorer.onrender.com'

const REQUIRED_COLUMNS = [
  { col: 'A',  name: 'AI Agent',                description: 'Flag for AI Agent steps (e.g. Y / Yes)' },
  { col: 'B',  name: 'System / Tool',            description: 'System or tool used in the step' },
  { col: 'C',  name: 'Level',                    description: 'Process level (L1, L2, L3, L4)' },
  { col: 'D',  name: 'Step Number / Seq',         description: 'Sequence number e.g. 1 / 1.1 / 1.1.1 / 1.1.1.1' },
  { col: 'E',  name: 'Step Name',                description: 'Name of the process step' },
  { col: 'F',  name: 'Description',              description: 'Detailed description of the step' },
  { col: 'G',  name: 'Step Type',                description: 'Process, Decision, Start, or Automated — Decisions include If yes/no routing' },
  { col: 'H',  name: 'Automated',                description: 'Whether the step is fully automated' },
  { col: 'Q',  name: 'RACI – Responsible',       description: 'Who is responsible for executing the step' },
  { col: 'R',  name: 'RACI – Accountable',       description: 'Who is ultimately accountable' },
  { col: 'S',  name: 'RACI – Contributing',      description: 'Who is consulted or contributes' },
  { col: 'X',  name: 'Critical Artefact',        description: 'Key document or deliverable produced' },
  { col: 'Y',  name: 'SLA',                      description: 'Service level agreement / time target' },
  { col: 'Z',  name: 'Key Data Points',          description: 'Key data fields and dimensionality' },
  { col: 'AB', name: 'Change Highlight',         description: 'To-Be process change or delta' },
]

export default function UploadPage({ onBack, onSuccess }) {
  const [status, setStatus]   = useState(null) // null | 'uploading' | 'success' | 'error'
  const [result, setResult]   = useState(null)
  const [dragOver, setDragOver] = useState(false)
  const [fileName, setFileName] = useState(null)
  const fileRef = useRef(null)

  async function handleFile(file) {
    if (!file) return
    if (!file.name.match(/\.(xlsx|xls)$/i)) {
      setStatus('error')
      setResult({ error: 'Please upload an Excel file (.xlsx or .xls)', missing_columns: [] })
      return
    }

    setFileName(file.name)
    setStatus('uploading')
    setResult(null)

    const form = new FormData()
    form.append('file', file)

    try {
      const res = await fetch(`${API}/api/upload`, { method: 'POST', body: form })
      const data = await res.json()
      setResult(data)
      setStatus(data.success ? 'success' : 'error')
    } catch (e) {
      setStatus('error')
      setResult({ error: `Network error: ${e.message}`, missing_columns: [] })
    }
  }

  function handleDrop(e) {
    e.preventDefault()
    setDragOver(false)
    handleFile(e.dataTransfer.files[0])
  }

  return (
    <div className="min-h-screen bg-slate-900 flex flex-col">

      {/* Header */}
      <header className="flex-shrink-0 border-b border-slate-700/60 bg-slate-900/95 backdrop-blur px-6 py-3">
        <div className="flex items-center gap-4">
          <button
            onClick={onBack}
            className="flex items-center gap-2 text-slate-400 hover:text-white text-sm transition-colors"
          >
            <ArrowLeft size={16} />
            Back to Process Map
          </button>
          <span className="text-slate-600">|</span>
          <span className="text-white font-semibold text-sm">Upload Process Data</span>
        </div>
      </header>

      {/* Main content */}
      <main className="flex-1 overflow-y-auto">
        <div className="max-w-4xl mx-auto px-8 py-10 w-full">

          {/* Page title */}
          <div className="mb-8">
            <h1 className="text-2xl font-bold text-white mb-2">Upload Process Data</h1>
            <p className="text-slate-400 text-sm leading-relaxed">
              Upload a new Excel file to update the process map. The file must contain a{' '}
              <code className="text-teal-300 bg-slate-800 px-1.5 py-0.5 rounded text-xs">Process Design</code>{' '}
              tab with headers in <strong className="text-slate-300">row 4</strong> and data starting from row 5.
              All 15 columns listed below must be present.
            </p>
          </div>

          {/* Drop zone */}
          <div
            onDragOver={e => { e.preventDefault(); setDragOver(true) }}
            onDragLeave={() => setDragOver(false)}
            onDrop={handleDrop}
            onClick={() => fileRef.current?.click()}
            className={`rounded-xl border-2 border-dashed p-12 text-center cursor-pointer transition-all mb-8 ${
              dragOver
                ? 'border-teal-400 bg-teal-500/10 scale-[1.01]'
                : 'border-slate-600 hover:border-slate-500 hover:bg-slate-800/30 bg-slate-800/20'
            }`}
          >
            <FileSpreadsheet size={48} className="mx-auto mb-4 text-teal-400 opacity-70" />
            <p className="text-white font-semibold text-lg mb-1">
              {dragOver ? 'Drop it here' : 'Drop your Excel file here'}
            </p>
            <p className="text-slate-400 text-sm mb-4">or click to browse your files</p>
            <span className="inline-block text-xs text-slate-500 bg-slate-800 border border-slate-700 rounded-lg px-3 py-1.5">
              Accepts .xlsx and .xls files
            </span>
            <input
              ref={fileRef}
              type="file"
              accept=".xlsx,.xls"
              className="hidden"
              onChange={e => handleFile(e.target.files[0])}
            />
          </div>

          {/* Status banners */}
          {status === 'uploading' && (
            <div className="mb-8 p-4 rounded-xl bg-slate-800 border border-slate-700 flex items-center gap-3">
              <div className="w-5 h-5 border-2 border-teal-400 border-t-transparent rounded-full animate-spin flex-shrink-0" />
              <div>
                <p className="text-slate-200 font-medium text-sm">Validating and processing…</p>
                <p className="text-slate-500 text-xs mt-0.5">{fileName}</p>
              </div>
            </div>
          )}

          {status === 'success' && result && (
            <div className="mb-8 p-5 rounded-xl bg-emerald-900/25 border border-emerald-500/40">
              <div className="flex items-start gap-3">
                <CheckCircle size={20} className="text-emerald-400 flex-shrink-0 mt-0.5" />
                <div className="flex-1 min-w-0">
                  <p className="text-emerald-300 font-semibold">Upload Successful</p>
                  <p className="text-slate-300 text-sm mt-1">{result.message}</p>
                  {result.git_committed && (
                    <p className="text-slate-500 text-xs mt-1">Changes committed to git repository.</p>
                  )}
                  <div className="flex items-center gap-3 mt-4">
                    <button
                      onClick={onSuccess}
                      className="px-4 py-2 bg-emerald-600 hover:bg-emerald-500 text-white text-sm font-medium rounded-lg transition-colors"
                    >
                      View Updated Process Map
                    </button>
                    <button
                      onClick={() => { setStatus(null); setResult(null); setFileName(null) }}
                      className="px-4 py-2 text-slate-400 hover:text-slate-200 text-sm transition-colors"
                    >
                      Upload Another File
                    </button>
                  </div>
                </div>
              </div>
            </div>
          )}

          {status === 'error' && result && (
            <div className="mb-8 p-5 rounded-xl bg-red-900/25 border border-red-500/40">
              <div className="flex items-start gap-3">
                <XCircle size={20} className="text-red-400 flex-shrink-0 mt-0.5" />
                <div className="flex-1 min-w-0">
                  <p className="text-red-300 font-semibold">Upload Failed</p>
                  <p className="text-slate-300 text-sm mt-1">{result.error}</p>

                  {result.missing_columns?.length > 0 && (
                    <div className="mt-4">
                      <p className="text-slate-300 text-sm font-medium mb-2 flex items-center gap-1.5">
                        <AlertCircle size={14} className="text-amber-400" />
                        Missing columns ({result.missing_columns.length}):
                      </p>
                      <ul className="space-y-1.5">
                        {result.missing_columns.map(col => (
                          <li key={col} className="flex items-center gap-2 text-sm">
                            <span className="w-1.5 h-1.5 rounded-full bg-red-400 flex-shrink-0" />
                            <span className="text-red-300">{col}</span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}

                  <p className="text-slate-500 text-xs mt-4">
                    The existing process map remains unchanged. Please fix the file and try again.
                  </p>
                  <button
                    onClick={() => { setStatus(null); setResult(null); setFileName(null) }}
                    className="mt-3 px-4 py-2 text-slate-400 hover:text-slate-200 text-sm border border-slate-600 hover:border-slate-500 rounded-lg transition-colors"
                  >
                    Try Again
                  </button>
                </div>
              </div>
            </div>
          )}

          {/* Required columns table */}
          <div className="rounded-xl border border-slate-700 overflow-hidden">
            <div className="px-5 py-4 bg-slate-800/60 border-b border-slate-700">
              <h2 className="text-white font-semibold">Required Columns</h2>
              <p className="text-slate-400 text-sm mt-1">
                Your Excel must have a{' '}
                <code className="text-teal-300 bg-slate-700/60 px-1 rounded">Process Design</code>{' '}
                tab with all 15 columns below. Headers must be in <strong className="text-slate-300">row 4</strong>.
                Columns I–P, AA, and AC onward are not read.
              </p>
            </div>
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead>
                  <tr className="border-b border-slate-700 bg-slate-800/30">
                    <th className="text-left px-5 py-3 text-slate-400 font-medium w-20">Column</th>
                    <th className="text-left px-5 py-3 text-slate-400 font-medium w-56">Field</th>
                    <th className="text-left px-5 py-3 text-slate-400 font-medium">Description</th>
                  </tr>
                </thead>
                <tbody>
                  {REQUIRED_COLUMNS.map((c, i) => (
                    <tr
                      key={c.col}
                      className={`border-b border-slate-700/50 ${i % 2 === 0 ? 'bg-slate-900/20' : ''}`}
                    >
                      <td className="px-5 py-3">
                        <span className="inline-flex items-center justify-center min-w-[2rem] h-6 px-1.5 rounded bg-teal-500/15 border border-teal-500/30 text-teal-300 font-mono font-bold text-xs">
                          {c.col}
                        </span>
                      </td>
                      <td className="px-5 py-3 text-white font-medium">{c.name}</td>
                      <td className="px-5 py-3 text-slate-400">{c.description}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

        </div>
      </main>
    </div>
  )
}
