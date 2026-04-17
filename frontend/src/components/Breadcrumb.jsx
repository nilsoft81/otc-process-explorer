import React from 'react'
import { ChevronRight, Home } from 'lucide-react'

export default function Breadcrumb({ stage, subProcess, onHome, onStage }) {
  return (
    <nav className="flex items-center gap-1 text-sm text-slate-400 flex-wrap">
      <button
        onClick={onHome}
        className="flex items-center gap-1 hover:text-teal-400 transition-colors font-medium"
      >
        <Home size={14} />
        <span>OTC Overview</span>
      </button>

      {stage && (
        <>
          <ChevronRight size={14} className="text-slate-600" />
          <button
            onClick={onStage}
            className={`hover:text-teal-400 transition-colors font-medium ${!subProcess ? 'text-slate-200' : ''}`}
          >
            {stage.name}
          </button>
        </>
      )}

      {subProcess && (
        <>
          <ChevronRight size={14} className="text-slate-600" />
          <span className="text-slate-200 font-medium">{subProcess.name}</span>
        </>
      )}
    </nav>
  )
}
