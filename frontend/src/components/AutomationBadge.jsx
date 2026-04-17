import React from 'react'
import { Bot, Brain, User } from 'lucide-react'

const BADGE_CONFIG = {
  agentic_ai: {
    label: 'Agentic AI',
    icon: Bot,
    bg: 'bg-purple-900/60',
    border: 'border-purple-500/60',
    text: 'text-purple-200',
    dot: 'bg-purple-400',
    iconColor: 'text-purple-400',
  },
  classical_ml: {
    label: 'Classical AI / ML',
    icon: Brain,
    bg: 'bg-blue-900/60',
    border: 'border-blue-500/60',
    text: 'text-blue-200',
    dot: 'bg-blue-400',
    iconColor: 'text-blue-400',
  },
  manual: {
    label: 'Manual',
    icon: User,
    bg: 'bg-slate-700/60',
    border: 'border-slate-500/60',
    text: 'text-slate-300',
    dot: 'bg-slate-400',
    iconColor: 'text-slate-400',
  },
}

export default function AutomationBadge({ type, size = 'md' }) {
  const config = BADGE_CONFIG[type] || BADGE_CONFIG.manual
  const Icon = config.icon

  if (size === 'sm') {
    return (
      <span className={`inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-xs font-medium border ${config.bg} ${config.border} ${config.text}`}>
        <Icon size={10} className={config.iconColor} />
        {config.label}
      </span>
    )
  }

  return (
    <span className={`inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-sm font-semibold border ${config.bg} ${config.border} ${config.text}`}>
      <Icon size={13} className={config.iconColor} />
      {config.label}
    </span>
  )
}

export { BADGE_CONFIG }
