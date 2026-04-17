import React, { useState } from 'react'
import { AlertTriangle, ArrowRight, Info } from 'lucide-react'

// ── RACI badge config ──────────────────────────────────────────────────────────
const RACI_CONFIG = {
  r: {
    label: 'R',
    title: 'Responsible',
    bg: 'bg-emerald-900/50',
    border: 'border-emerald-600/50',
    text: 'text-emerald-200',
    dot: 'bg-emerald-400',
  },
  a: {
    label: 'A',
    title: 'Accountable',
    bg: 'bg-amber-900/50',
    border: 'border-amber-600/50',
    text: 'text-amber-200',
    dot: 'bg-amber-400',
  },
  c: {
    label: 'C',
    title: 'Consulted',
    bg: 'bg-blue-900/50',
    border: 'border-blue-600/50',
    text: 'text-blue-200',
    dot: 'bg-blue-400',
  },
  i: {
    label: 'I',
    title: 'Informed',
    bg: 'bg-slate-700/50',
    border: 'border-slate-500/50',
    text: 'text-slate-300',
    dot: 'bg-slate-400',
  },
}

function RaciCell({ role, value }) {
  const cfg = RACI_CONFIG[role]
  if (!value || value === 'NA') {
    return <span className="text-slate-700 text-xs select-none">—</span>
  }
  return (
    <span
      className={`inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-xs font-medium border ${cfg.bg} ${cfg.border} ${cfg.text} whitespace-nowrap`}
      title={`${cfg.title}: ${value}`}
    >
      <span
        className={`w-1.5 h-1.5 rounded-full flex-shrink-0 ${cfg.dot}`}
      />
      {value}
    </span>
  )
}

// ── Step-type badge ────────────────────────────────────────────────────────────
function TypeBadge({ type }) {
  const isDecision = type.toLowerCase().includes('decision')
  const isAuto = type.toLowerCase().includes('automated')

  if (isDecision && isAuto) {
    return (
      <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded border bg-violet-900/40 border-violet-500/50 text-violet-200 text-xs whitespace-nowrap">
        ◇ Decision (Auto)
      </span>
    )
  }
  if (isDecision) {
    return (
      <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded border bg-amber-900/40 border-amber-500/50 text-amber-200 text-xs whitespace-nowrap">
        ◇ Decision
      </span>
    )
  }
  return (
    <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded border bg-slate-700/60 border-slate-500/50 text-slate-300 text-xs whitespace-nowrap">
      → Process
    </span>
  )
}

// ── System/Tool tag ────────────────────────────────────────────────────────────
function SystemTag({ value }) {
  if (!value || value === 'NA') {
    return <span className="text-slate-700 text-xs">—</span>
  }
  // may be multiple tools separated by "/"
  const parts = value.split('/').map(p => p.trim())
  return (
    <div className="flex flex-wrap gap-1">
      {parts.map(p => (
        <span
          key={p}
          className="inline-flex items-center px-2 py-0.5 rounded bg-slate-700 border border-slate-600 text-slate-200 text-xs whitespace-nowrap"
        >
          {p}
        </span>
      ))}
    </div>
  )
}

// ── Level badge ────────────────────────────────────────────────────────────────
function LevelBadge({ level, color }) {
  const isL4 = level === 'L4'
  return (
    <span
      className={`inline-flex items-center justify-center w-8 h-5 rounded text-xs font-bold flex-shrink-0 ${
        isL4
          ? 'bg-slate-700 text-slate-400 border border-slate-600'
          : 'border'
      }`}
      style={!isL4 ? { background: color + '30', color, borderColor: color + '60' } : {}}
    >
      {level}
    </span>
  )
}

// ── Decision Outcomes pill ─────────────────────────────────────────────────────
function OutcomesPill({ outcomes }) {
  if (!outcomes) return null
  const parts = outcomes.split('|').map(p => p.trim())
  return (
    <div className="flex flex-col gap-0.5 mt-1">
      {parts.map((p, i) => (
        <span key={i} className="inline-flex items-center gap-1 text-xs text-amber-300/80">
          <span className="text-amber-600">▸</span>
          {p}
        </span>
      ))}
    </div>
  )
}

// ── To-Be change indicator ─────────────────────────────────────────────────────
function ChangeBadge({ text }) {
  if (!text) return null
  return (
    <div className="flex items-start gap-1 mt-1.5">
      <span className="text-violet-400 text-xs mt-0.5 flex-shrink-0">Δ</span>
      <span className="text-xs text-violet-300/80 italic leading-relaxed">{text}</span>
    </div>
  )
}

// ── Main step row ──────────────────────────────────────────────────────────────
function StepRow({ step, stageColor, isEven }) {
  const [expanded, setExpanded] = useState(false)
  const isL4 = step.level === 'L4'
  const hasNotes = !!step.notes
  const hasOutcomes = !!step.decision_outcomes
  const hasChange = !!step.change_highlight

  return (
    <tr
      className={`border-b border-slate-700/40 transition-colors ${
        isL4
          ? isEven ? 'bg-slate-800/20' : 'bg-slate-800/10'
          : isEven ? 'bg-slate-800/60' : 'bg-slate-800/40'
      } hover:bg-slate-700/30`}
    >
      {/* Level */}
      <td className="px-3 py-2.5 align-top">
        <LevelBadge level={step.level} color={stageColor} />
      </td>

      {/* Seq # */}
      <td className="px-3 py-2.5 align-top">
        <span className="text-xs font-mono text-slate-500 whitespace-nowrap">{step.seq}</span>
      </td>

      {/* Step Name + description + change */}
      <td className="px-3 py-2.5 align-top min-w-[200px]">
        <div className={`${isL4 ? 'pl-3' : ''}`}>
          {isL4 && <span className="text-slate-600 mr-1 text-xs">↳</span>}
          <span className={`font-semibold text-xs leading-snug ${isL4 ? 'text-slate-300' : 'text-slate-100'}`}>
            {step.name}
          </span>
          {step.description && (
            <p className="text-xs text-slate-500 mt-0.5 leading-relaxed">
              {step.description}
            </p>
          )}
          {hasOutcomes && <OutcomesPill outcomes={step.decision_outcomes} />}
          {hasChange && <ChangeBadge text={step.change_highlight} />}
          {hasNotes && (
            <div className="flex items-start gap-1 mt-1">
              <Info size={10} className="text-slate-500 mt-0.5 flex-shrink-0" />
              <span className="text-xs text-slate-500 italic">{step.notes}</span>
            </div>
          )}
        </div>
      </td>

      {/* Step type */}
      <td className="px-3 py-2.5 align-top">
        <TypeBadge type={step.step_type} />
      </td>

      {/* RACI — Responsible */}
      <td className="px-3 py-2.5 align-top text-center">
        <RaciCell role="r" value={step.raci.r} />
      </td>

      {/* RACI — Accountable */}
      <td className="px-3 py-2.5 align-top text-center">
        <RaciCell role="a" value={step.raci.a} />
      </td>

      {/* RACI — Consulted */}
      <td className="px-3 py-2.5 align-top text-center">
        <RaciCell role="c" value={step.raci.c} />
      </td>

      {/* RACI — Informed */}
      <td className="px-3 py-2.5 align-top text-center">
        <RaciCell role="i" value={step.raci.i} />
      </td>

      {/* System / Tool */}
      <td className="px-3 py-2.5 align-top">
        <SystemTag value={step.system_tool} />
      </td>

      {/* Key Data Points */}
      <td className="px-3 py-2.5 align-top text-xs text-slate-400 leading-relaxed min-w-[180px]">
        {step.key_data_points && step.key_data_points !== 'NA'
          ? step.key_data_points
          : <span className="text-slate-700">—</span>
        }
      </td>
    </tr>
  )
}

// ── Table header ───────────────────────────────────────────────────────────────
function TableHeader() {
  return (
    <thead className="sticky top-0 z-10">
      <tr className="bg-slate-800 border-b-2 border-slate-600">
        <th className="px-3 py-2.5 text-left text-slate-400 font-semibold text-xs w-12 whitespace-nowrap">Lvl</th>
        <th className="px-3 py-2.5 text-left text-slate-400 font-semibold text-xs w-20 whitespace-nowrap">Seq #</th>
        <th className="px-3 py-2.5 text-left text-slate-400 font-semibold text-xs min-w-[220px]">Step Name / Description</th>
        <th className="px-3 py-2.5 text-left text-slate-400 font-semibold text-xs w-28 whitespace-nowrap">Type</th>
        {/* RACI group header */}
        <th colSpan={4} className="px-3 py-2 text-center text-slate-300 font-bold text-xs border-l border-r border-slate-600/50 bg-slate-800">
          RACI
        </th>
        <th className="px-3 py-2.5 text-left text-slate-400 font-semibold text-xs w-36 whitespace-nowrap">System / Tool</th>
        <th className="px-3 py-2.5 text-left text-slate-400 font-semibold text-xs min-w-[200px]">Key Data Points & Dimensionality</th>
      </tr>
      {/* Sub-header for RACI columns */}
      <tr className="bg-slate-800/80 border-b border-slate-600/60">
        <th colSpan={4} className="px-3 py-1" />
        <th className="px-3 py-1 text-center text-emerald-400 font-semibold text-xs w-28 border-l border-slate-600/50 whitespace-nowrap">
          <span className="inline-flex items-center gap-1">
            <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 inline-block" />
            Responsible (R)
          </span>
        </th>
        <th className="px-3 py-1 text-center text-amber-400 font-semibold text-xs w-28 whitespace-nowrap">
          <span className="inline-flex items-center gap-1">
            <span className="w-1.5 h-1.5 rounded-full bg-amber-400 inline-block" />
            Accountable (A)
          </span>
        </th>
        <th className="px-3 py-1 text-center text-blue-400 font-semibold text-xs w-28 whitespace-nowrap">
          <span className="inline-flex items-center gap-1">
            <span className="w-1.5 h-1.5 rounded-full bg-blue-400 inline-block" />
            Consulted (C)
          </span>
        </th>
        <th className="px-3 py-1 text-center text-slate-400 font-semibold text-xs w-24 border-r border-slate-600/50 whitespace-nowrap">
          <span className="inline-flex items-center gap-1">
            <span className="w-1.5 h-1.5 rounded-full bg-slate-400 inline-block" />
            Informed (I)
          </span>
        </th>
        <th colSpan={2} className="px-3 py-1" />
      </tr>
    </thead>
  )
}

// ── Main export ────────────────────────────────────────────────────────────────
export default function ProcessTable({ stage }) {
  const l3Count = stage.steps.filter(s => s.level === 'L3').length
  const l4Count = stage.steps.filter(s => s.level === 'L4').length

  return (
    <div className="h-full flex flex-col">
      {/* Stage detail header */}
      <div className="flex-shrink-0 mb-3 flex items-start justify-between gap-4 flex-wrap">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <span
              className="text-xs font-mono px-2 py-0.5 rounded border"
              style={{ color: stage.color, borderColor: stage.color + '50', background: stage.color + '15' }}
            >
              {stage.seq}
            </span>
            <h2 className="text-base font-bold text-slate-100">{stage.name}</h2>
          </div>
          <p className="text-xs text-slate-400 leading-relaxed max-w-2xl">{stage.description}</p>
          {stage.change_highlight && (
            <div className="flex items-center gap-1 mt-1.5">
              <span className="text-violet-400 text-xs">Δ</span>
              <span className="text-xs text-violet-300/80 italic">{stage.change_highlight}</span>
            </div>
          )}
          {stage.key_question && (
            <div className="flex items-start gap-1.5 mt-1.5 bg-amber-900/20 border border-amber-700/30 rounded px-2 py-1">
              <AlertTriangle size={11} className="text-amber-400 mt-0.5 flex-shrink-0" />
              <span className="text-xs text-amber-300/90 italic">{stage.key_question}</span>
            </div>
          )}
        </div>
        <div className="flex items-center gap-3 flex-shrink-0">
          <div className="text-center">
            <div className="text-sm font-bold" style={{ color: stage.color }}>{l3Count}</div>
            <div className="text-xs text-slate-500">L3 Steps</div>
          </div>
          <div className="text-center">
            <div className="text-sm font-bold text-slate-400">{l4Count}</div>
            <div className="text-xs text-slate-500">L4 Tasks</div>
          </div>
        </div>
      </div>

      {/* Scrollable table */}
      <div className="flex-1 overflow-auto rounded-xl border border-slate-700/60">
        <table className="border-collapse text-xs" style={{ minWidth: '1100px', width: '100%' }}>
          <TableHeader />
          <tbody>
            {stage.steps.map((step, idx) => (
              <StepRow
                key={step.seq}
                step={step}
                stageColor={stage.color}
                isEven={idx % 2 === 0}
              />
            ))}
          </tbody>
        </table>
      </div>

      {/* Legend row */}
      <div className="flex-shrink-0 mt-2 flex items-center gap-4 flex-wrap px-1">
        <span className="text-xs text-slate-600">Legend:</span>
        <span className="text-xs text-slate-500">◇ Decision = gateway / branch point</span>
        <span className="text-xs text-slate-500">↳ = L4 sub-task of the L3 above</span>
        <span className="text-xs text-violet-400/70">Δ = As-Is → To-Be change</span>
        <span className="text-xs text-slate-500">— = not applicable / data unavailable</span>
      </div>
    </div>
  )
}
