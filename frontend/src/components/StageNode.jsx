import React from 'react'
import { Handle, Position } from '@xyflow/react'

export default function StageNode({ data, selected }) {
  const { label, description, color, icon, isSelected } = data

  return (
    <div
      className={`
        relative px-4 py-3 rounded-xl border-2 transition-all duration-200 cursor-pointer min-w-[130px] max-w-[150px] text-center
        ${isSelected
          ? 'border-amber-400 shadow-lg shadow-amber-500/30 scale-105'
          : 'border-slate-600 hover:border-slate-400 hover:shadow-md hover:shadow-slate-500/20'
        }
      `}
      style={{
        background: isSelected
          ? `linear-gradient(135deg, ${color}33, ${color}55)`
          : `linear-gradient(135deg, #1e293b, #0f172a)`,
        borderColor: isSelected ? '#f59e0b' : color + '80',
      }}
    >
      <Handle type="target" position={Position.Left} className="!bg-slate-500 !border-slate-400 !w-2 !h-2" />

      <div
        className="text-2xl mb-1 font-bold"
        style={{ color: isSelected ? '#f59e0b' : color }}
      >
        {icon}
      </div>
      <div
        className={`text-xs font-semibold leading-tight ${isSelected ? 'text-amber-200' : 'text-slate-200'}`}
      >
        {label}
      </div>
      {isSelected && (
        <div className="absolute -bottom-1.5 left-1/2 -translate-x-1/2 w-3 h-3 bg-amber-400 rotate-45 rounded-sm" />
      )}

      <Handle type="source" position={Position.Right} className="!bg-slate-500 !border-slate-400 !w-2 !h-2" />
    </div>
  )
}
