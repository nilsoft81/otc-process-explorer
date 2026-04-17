import React, { useRef, useEffect, useState } from 'react'

const STAGE_ICONS = {
  Target: '🎯',
  FileText: '📄',
  Shield: '🛡️',
  Settings: '⚙️',
  Microscope: '🔬',
  Clock: '⏱️',
  Receipt: '🧾',
  Banknote: '💰',
  BarChart: '📊',
  Users: '👥',
}

const COLS = 5

function Arrow({ color = '#475569' }) {
  return (
    <div className="flex items-center flex-shrink-0 self-center" style={{ marginTop: '-8px' }}>
      <svg width="32" height="16" viewBox="0 0 32 16" fill="none">
        <path
          d="M0 8 H26"
          stroke={color}
          strokeWidth="2"
          strokeLinecap="round"
        />
        <path
          d="M22 3 L30 8 L22 13"
          stroke={color}
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
          fill="none"
        />
      </svg>
    </div>
  )
}

function RowWrapArrow({ color = '#475569' }) {
  return (
    <div className="flex justify-end pr-4 py-1">
      <svg width="32" height="28" viewBox="0 0 32 28" fill="none">
        <path
          d="M28 0 L28 14 Q28 20 22 20 L10 20 Q4 20 4 26"
          stroke={color}
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
          fill="none"
          strokeDasharray="4 3"
        />
        <path d="M0 22 L4 30 L8 22" stroke={color} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" fill="none" />
      </svg>
    </div>
  )
}

export default function ProcessFlow({ stages, selectedStageId, onSelectStage }) {
  const rows = []
  for (let i = 0; i < stages.length; i += COLS) {
    rows.push(stages.slice(i, i + COLS))
  }

  return (
    <div className="w-full h-full overflow-auto flex items-center justify-center p-6">
      <div className="flex flex-col gap-0 items-start">
        {rows.map((row, rowIdx) => {
          const isEven = rowIdx % 2 === 0
          const displayRow = isEven ? row : [...row].reverse()
          const isLast = rowIdx === rows.length - 1

          return (
            <div key={rowIdx} className="flex flex-col">
              {/* Stage nodes row */}
              <div className="flex items-stretch gap-0">
                {displayRow.map((stage, colIdx) => {
                  const isSelected = stage.id === selectedStageId
                  const icon = STAGE_ICONS[stage.icon] || '📋'
                  const isLastInRow = colIdx === displayRow.length - 1
                  const globalIdx = rowIdx * COLS + (isEven ? colIdx : row.length - 1 - colIdx)

                  return (
                    <React.Fragment key={stage.id}>
                      {/* Stage card */}
                      <button
                        onClick={() => onSelectStage(stage.id)}
                        className={`
                          relative flex flex-col items-center justify-center gap-1.5
                          w-36 min-h-[90px] px-3 py-4 rounded-xl border-2
                          text-center transition-all duration-200 flex-shrink-0
                          focus:outline-none
                          ${isSelected
                            ? 'scale-105 shadow-lg'
                            : 'hover:scale-102 hover:shadow-md'
                          }
                        `}
                        style={{
                          background: isSelected
                            ? `linear-gradient(135deg, ${stage.color}30, ${stage.color}50)`
                            : 'linear-gradient(135deg, #1e293b, #0f172a)',
                          borderColor: isSelected ? '#f59e0b' : stage.color + '80',
                          boxShadow: isSelected
                            ? `0 0 20px ${stage.color}40`
                            : undefined,
                        }}
                      >
                        <span className="text-2xl leading-none">{icon}</span>
                        {stage.seq && (
                          <span className="text-xs font-mono opacity-60" style={{ color: isSelected ? '#fde68a' : stage.color }}>
                            {stage.seq}
                          </span>
                        )}
                        <span
                          className="text-xs font-semibold leading-tight"
                          style={{ color: isSelected ? '#fde68a' : '#e2e8f0' }}
                        >
                          {stage.name}
                        </span>
                        {isSelected && (
                          <span
                            className="absolute -bottom-2 left-1/2 -translate-x-1/2 w-3 h-3 rotate-45 rounded-sm"
                            style={{ background: '#f59e0b' }}
                          />
                        )}
                      </button>

                      {/* Arrow between nodes (not after last in row) */}
                      {!isLastInRow && <Arrow />}
                    </React.Fragment>
                  )
                })}
              </div>

              {/* Row-wrap arrow between rows */}
              {!isLast && (
                <div
                  className="flex"
                  style={{ justifyContent: isEven ? 'flex-end' : 'flex-start', paddingLeft: isEven ? 0 : '16px', paddingRight: isEven ? '16px' : 0 }}
                >
                  <svg width="40" height="32" viewBox="0 0 40 32" fill="none">
                    <path
                      d={isEven
                        ? "M36 2 L36 16 Q36 22 30 22 L10 22 Q4 22 4 28"
                        : "M4 2 L4 16 Q4 22 10 22 L30 22 Q36 22 36 28"
                      }
                      stroke="#475569"
                      strokeWidth="2"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeDasharray="4 3"
                      fill="none"
                    />
                    <path
                      d={isEven ? "M0 24 L4 32 L8 24" : "M32 24 L36 32 L40 24"}
                      stroke="#475569"
                      strokeWidth="2"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      fill="none"
                    />
                  </svg>
                </div>
              )}
            </div>
          )
        })}
      </div>
    </div>
  )
}
