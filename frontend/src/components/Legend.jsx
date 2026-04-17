import React from 'react'

const items = [
  { dot: 'bg-emerald-400', label: 'R', desc: 'Responsible', text: 'text-emerald-300', bg: 'bg-emerald-900/30', border: 'border-emerald-700/40' },
  { dot: 'bg-amber-400',   label: 'A', desc: 'Accountable', text: 'text-amber-300',   bg: 'bg-amber-900/30',   border: 'border-amber-700/40'   },
  { dot: 'bg-blue-400',    label: 'C', desc: 'Consulted',   text: 'text-blue-300',    bg: 'bg-blue-900/30',    border: 'border-blue-700/40'    },
  { dot: 'bg-slate-400',   label: 'I', desc: 'Informed',    text: 'text-slate-300',   bg: 'bg-slate-700/30',   border: 'border-slate-600/40'   },
]

export default function Legend() {
  return (
    <div className="flex items-center gap-2 flex-wrap">
      {items.map(item => (
        <div
          key={item.label}
          className={`flex items-center gap-1.5 px-2.5 py-1 rounded-lg border ${item.bg} ${item.border}`}
        >
          <span className={`w-2 h-2 rounded-full flex-shrink-0 ${item.dot}`} />
          <span className={`text-xs font-bold ${item.text}`}>{item.label}</span>
          <span className="text-xs text-slate-400">{item.desc}</span>
        </div>
      ))}
    </div>
  )
}
