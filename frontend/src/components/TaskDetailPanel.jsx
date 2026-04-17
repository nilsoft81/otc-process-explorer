import React, { useState } from 'react'
import { Sparkles, ChevronDown, ChevronRight } from 'lucide-react'
import AutomationBadge, { BADGE_CONFIG } from './AutomationBadge'

function TaskRow({ task }) {
  const config = BADGE_CONFIG[task.automation_type] || BADGE_CONFIG.manual
  return (
    <div className={`rounded-lg border p-3 ${config.bg} ${config.border}`}>
      <div className="flex items-start justify-between gap-2 mb-1">
        <span className="text-xs font-semibold text-slate-100 leading-snug flex-1">
          {task.name}
        </span>
        <AutomationBadge type={task.automation_type} size="sm" />
      </div>
      {task.description && (
        <p className="text-xs text-slate-400 leading-relaxed mt-1">{task.description}</p>
      )}
      {task.ai_tool_examples && task.ai_tool_examples.length > 0 && (
        <div className="mt-2">
          <div className="flex items-center gap-1 mb-1">
            <Sparkles size={10} className={config.iconColor} />
            <span className={`text-xs font-medium ${config.text}`}>AI Tools / Approaches</span>
          </div>
          <div className="flex flex-wrap gap-1">
            {task.ai_tool_examples.map((tool, idx) => (
              <span
                key={idx}
                className={`text-xs px-1.5 py-0.5 rounded border ${config.border} bg-black/20 ${config.text} opacity-80`}
              >
                {tool}
              </span>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}

function TaskGroup({ group }) {
  const [open, setOpen] = useState(true)
  const config = BADGE_CONFIG[group.automation_type] || BADGE_CONFIG.manual

  return (
    <div className={`rounded-xl border-2 ${config.border} overflow-hidden`}>
      {/* L4 group header */}
      <button
        onClick={() => setOpen(o => !o)}
        className={`w-full flex items-center justify-between gap-3 px-4 py-3 text-left transition-colors ${config.bg} hover:brightness-110`}
      >
        <div className="flex items-center gap-2 flex-1 min-w-0">
          {open
            ? <ChevronDown size={14} className={config.iconColor} />
            : <ChevronRight size={14} className={config.iconColor} />
          }
          <span className={`text-sm font-bold leading-snug ${config.text}`}>
            {group.name}
          </span>
        </div>
        <div className="flex items-center gap-2 flex-shrink-0">
          <span className="text-xs text-slate-500">{group.tasks.length} tasks</span>
          <AutomationBadge type={group.automation_type} size="sm" />
        </div>
      </button>

      {/* L5 tasks */}
      {open && (
        <div className="px-3 pb-3 pt-2 grid gap-2 bg-slate-900/40">
          {group.tasks.map(task => (
            <TaskRow key={task.id} task={task} />
          ))}
        </div>
      )}
    </div>
  )
}

export default function TaskDetailPanel({ subProcess }) {
  return (
    <div className="h-full flex flex-col">
      <div className="mb-4">
        <h3 className="text-lg font-bold text-slate-100">{subProcess.name}</h3>
        <p className="text-sm text-slate-400 mt-1">{subProcess.description}</p>
      </div>

      <div className="grid grid-cols-1 gap-4 overflow-y-auto pr-1">
        {subProcess.task_groups.map(group => (
          <TaskGroup key={group.id} group={group} />
        ))}
      </div>
    </div>
  )
}
