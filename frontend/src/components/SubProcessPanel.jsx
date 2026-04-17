import React from 'react'
import { Bot, Brain, User, ChevronRight } from 'lucide-react'
import AutomationBadge, { BADGE_CONFIG } from './AutomationBadge'

function getAutomationSummary(subProcess) {
  const counts = { agentic_ai: 0, classical_ml: 0, manual: 0 }
  subProcess.task_groups.forEach(tg => {
    tg.tasks.forEach(t => {
      if (counts[t.automation_type] !== undefined) counts[t.automation_type]++
    })
  })
  return counts
}

function totalTasks(subProcess) {
  return subProcess.task_groups.reduce((a, tg) => a + tg.tasks.length, 0)
}

function AutomationPill({ type, count }) {
  if (count === 0) return null
  const config = BADGE_CONFIG[type]
  const Icon = config.icon
  return (
    <span className={`inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-xs border ${config.bg} ${config.border} ${config.text}`}>
      <Icon size={10} className={config.iconColor} />
      {count}
    </span>
  )
}

export default function SubProcessPanel({ stage, selectedSubProcessId, onSelect }) {
  return (
    <div className="h-full flex flex-col">
      <div className="mb-4">
        <h2 className="text-lg font-bold text-slate-100 flex items-center gap-2">
          <span style={{ color: stage.color }}>◈</span>
          {stage.name}
        </h2>
        <p className="text-sm text-slate-400 mt-1">{stage.description}</p>
      </div>

      <div className="grid grid-cols-1 gap-3 overflow-y-auto pr-1">
        {stage.sub_processes.map(sp => {
          const counts = getAutomationSummary(sp)
          const isSelected = sp.id === selectedSubProcessId
          return (
            <button
              key={sp.id}
              onClick={() => onSelect(sp)}
              className={`
                text-left rounded-xl border-2 p-4 transition-all duration-150 group
                ${isSelected
                  ? 'border-amber-400/70 bg-amber-900/20 shadow-lg shadow-amber-500/10'
                  : 'border-slate-700 bg-slate-800/60 hover:border-slate-500 hover:bg-slate-800'
                }
              `}
            >
              <div className="flex items-start justify-between gap-2">
                <div className="flex-1 min-w-0">
                  <div className={`font-semibold text-sm leading-snug ${isSelected ? 'text-amber-200' : 'text-slate-200 group-hover:text-white'}`}>
                    {sp.name}
                  </div>
                  <div className="text-xs text-slate-400 mt-1 leading-relaxed line-clamp-2">
                    {sp.description}
                  </div>
                </div>
                <ChevronRight
                  size={16}
                  className={`flex-shrink-0 mt-0.5 transition-colors ${isSelected ? 'text-amber-400' : 'text-slate-600 group-hover:text-slate-400'}`}
                />
              </div>

              <div className="flex items-center gap-2 mt-3 flex-wrap">
                <span className="text-xs text-slate-500">{totalTasks(sp)} tasks</span>
                <span className="text-slate-700">·</span>
                <AutomationPill type="agentic_ai" count={counts.agentic_ai} />
                <AutomationPill type="classical_ml" count={counts.classical_ml} />
                <AutomationPill type="manual" count={counts.manual} />
              </div>
            </button>
          )
        })}
      </div>
    </div>
  )
}
