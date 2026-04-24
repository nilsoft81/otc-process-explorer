import React, { useState, useMemo } from 'react'
import { ChevronDown, ChevronRight } from 'lucide-react'

// ── Ombre color helpers ───────────────────────────────────────────────────────
// Mix hex color toward white by `t` (0 = full color, 1 = white)
function mixWhite(hex, t) {
  const h = hex.replace('#', '')
  const r = parseInt(h.slice(0, 2), 16)
  const g = parseInt(h.slice(2, 4), 16)
  const b = parseInt(h.slice(4, 6), 16)
  const m = v => Math.round(v + (255 - v) * t)
  return `rgb(${m(r)},${m(g)},${m(b)})`
}

// Per-level ombre ratios: L1 darkest → L4 lightest
const OMBRE = { L1: 0.18, L2: 0.40, L3: 0.63, L4: 0.80 }
// Text colour on each level's background
const TEXT_ON = { L1: '#fff', L2: '#fff', L3: '#1e293b', L4: '#334155' }
const MUTED_ON = { L1: 'rgba(255,255,255,0.78)', L2: 'rgba(255,255,255,0.82)', L3: '#64748b', L4: '#94a3b8' }

function bg(hex, level) { return mixWhite(hex, OMBRE[level] ?? 0.5) }
function textColor(level) { return TEXT_ON[level] ?? '#1e293b' }
function mutedColor(level) { return MUTED_ON[level] ?? '#94a3b8' }
// Slightly deeper shade for shadows / seq badges
function darkBg(hex, level) { return mixWhite(hex, Math.max(0, (OMBRE[level] ?? 0.5) - 0.18)) }

// ── NodeFooter ────────────────────────────────────────────────────────────────
function NodeFooter({ node, tc, mc }) {
  const { raci, system_tool, key_data_points, change_highlight, decision_outcomes,
          critical_artefact, sla } = node
  const anyRaci    = raci && Object.values(raci).some(v => v && v !== 'NA')
  const hasSys     = system_tool && system_tool !== 'NA'
  const hasData    = key_data_points && key_data_points !== 'NA'
  const hasOuts    = !!decision_outcomes
  const hasChg     = !!change_highlight
  const hasArtef   = critical_artefact && critical_artefact !== 'NA' && critical_artefact !== ''
  const hasSla     = sla && sla !== 'NA' && sla !== ''
  if (!anyRaci && !hasSys && !hasData && !hasOuts && !hasChg && !hasArtef && !hasSla) return null

  const pill = (label, val, bg='rgba(0,0,0,0.18)', border='rgba(255,255,255,0.18)') =>
    val && val !== 'NA' ? (
      <span key={label} style={{
        display:'inline-flex', alignItems:'center', gap:3,
        padding:'1px 5px', borderRadius:4, fontSize:9, fontWeight:600,
        background:bg, color:tc, border:`1px solid ${border}`,
      }}>{label} <span style={{fontWeight:400,opacity:0.9}}>{val}</span></span>
    ) : null

  return (
    <div style={{ marginTop:6, paddingTop:6, borderTop:'1px solid rgba(255,255,255,0.18)',
      display:'flex', flexDirection:'column', gap:3 }}>
      {hasSys && (
        <div style={{display:'flex',flexWrap:'wrap',gap:2}}>
          {system_tool.split('/').map(s=>s.trim()).filter(Boolean).map(s=>(
            <span key={s} style={{fontSize:9,fontFamily:'monospace',padding:'1px 4px',borderRadius:3,
              background:'rgba(0,0,0,0.15)',color:tc}}>{s}</span>
          ))}
        </div>
      )}
      {anyRaci && (
        <div style={{display:'flex',flexWrap:'wrap',gap:2}}>
          {pill('R',raci.r)}{pill('A',raci.a)}{pill('C',raci.c)}
        </div>
      )}
      {(hasArtef || hasSla) && (
        <div style={{display:'flex',flexWrap:'wrap',gap:2}}>
          {hasArtef && pill('📎', critical_artefact, 'rgba(217,119,6,0.35)', 'rgba(217,119,6,0.5)')}
          {hasSla   && pill('⏱', sla,               'rgba(37,99,235,0.30)', 'rgba(37,99,235,0.45)')}
        </div>
      )}
      {hasOuts && decision_outcomes.split('|').map((o,i)=>(
        <span key={i} style={{fontSize:9,color:mc,display:'flex',gap:2,lineHeight:1.3}}>
          <span>▸</span><span>{o.trim()}</span>
        </span>
      ))}
      {hasData && <p style={{fontSize:9,color:mc,margin:0,lineHeight:1.3}}>
        <b>Data:</b> {key_data_points}</p>}
      {hasChg && <p style={{fontSize:9,color:mc,margin:0,fontStyle:'italic',lineHeight:1.3}}>
        <b>Δ</b> {change_highlight}</p>}
    </div>
  )
}

// ── NodeBox ───────────────────────────────────────────────────────────────────
function NodeBox({ node, baseColor, level, isSelected, childCount, onClick, expandDir='down' }) {
  const fill   = bg(baseColor, level)
  const dark   = darkBg(baseColor, level)
  const tc     = textColor(level)
  const mc     = mutedColor(level)
  const canClick = !!onClick
  const w = { L1:200, L2:185, L3:170, L4:160 }[level] ?? 170

  return (
    <div onClick={onClick} style={{
      position:'relative', flexShrink:0, width:w, padding:'9px 11px', borderRadius:8,
      background:fill,
      boxShadow: isSelected
        ? `0 0 0 2px ${dark}, 0 4px 16px rgba(0,0,0,0.2)`
        : '0 1px 4px rgba(0,0,0,0.14)',
      cursor: canClick ? 'pointer' : 'default',
      transition:'box-shadow 0.15s, transform 0.1s',
      transform: isSelected ? 'translateY(-1px)' : undefined,
      display:'flex', flexDirection:'column',
    }}>
      {/* Seq + decision badge */}
      <div style={{display:'flex',flexWrap:'wrap',alignItems:'center',gap:3,marginBottom:4}}>
        <span style={{fontSize:10,fontFamily:'monospace',fontWeight:700,
          padding:'1px 5px',borderRadius:3,background:'rgba(0,0,0,0.2)',color:tc}}>
          {node.seq}
        </span>
        {node.step_type?.toLowerCase().includes('decision') && (
          <span style={{fontSize:9,padding:'1px 4px',borderRadius:3,
            background:'rgba(0,0,0,0.2)',color:tc}}>◇ Decision</span>
        )}
      </div>

      {/* Name */}
      <p style={{fontSize:11,fontWeight:600,lineHeight:1.35,color:tc,margin:0}}>{node.name}</p>

      {/* Description — L1/L2 only, 2-line clamp */}
      {(level==='L1'||level==='L2') && node.description && (
        <p style={{fontSize:10,color:mc,margin:'3px 0 0',lineHeight:1.4,
          display:'-webkit-box',WebkitLineClamp:2,WebkitBoxOrient:'vertical',overflow:'hidden'}}>
          {node.description}
        </p>
      )}

      <NodeFooter node={node} tc={tc} mc={mc}/>

      {/* Expand count */}
      {childCount>0 && (
        <div style={{marginTop:5,display:'flex',alignItems:'center',gap:3,fontSize:10,color:mc}}>
          {isSelected ? <ChevronDown size={10} color={mc}/> : <ChevronRight size={10} color={mc}/>}
          <span>{childCount} {level==='L1'?'stages':level==='L2'?'steps':'tasks'}</span>
        </div>
      )}

      {/* Expand caret */}
      {isSelected && expandDir==='down' && (
        <div style={{position:'absolute',bottom:-8,left:'50%',transform:'translateX(-50%) rotate(45deg)',
          width:14,height:14,background:fill,borderRight:`2px solid ${dark}`,borderBottom:`2px solid ${dark}`,zIndex:2}}/>
      )}
      {isSelected && expandDir==='right' && (
        <div style={{position:'absolute',top:'50%',right:-8,transform:'translateY(-50%) rotate(45deg)',
          width:14,height:14,background:fill,borderTop:`2px solid ${dark}`,borderRight:`2px solid ${dark}`,zIndex:2}}/>
      )}
    </div>
  )
}

// ── Down-arrow connector between stacked items ────────────────────────────────
function DownArrow({ color }) {
  return (
    <div style={{display:'flex',alignItems:'center',paddingLeft:18,margin:'2px 0'}}>
      <svg width="10" height="16" viewBox="0 0 10 16" fill="none">
        <line x1="5" y1="0" x2="5" y2="10" stroke={color} strokeWidth="1.5" strokeLinecap="round"/>
        <path d="M2 8l3 8 3-8" fill={color}/>
      </svg>
    </div>
  )
}

// ── Right-arrow connector between adjacent cells ──────────────────────────────
function RightArrow({ color }) {
  return (
    <svg width="28" height="12" viewBox="0 0 28 12" fill="none" style={{flexShrink:0}}>
      <line x1="0" y1="6" x2="20" y2="6" stroke={color} strokeWidth="1.5" strokeLinecap="round"/>
      <path d="M17 3l11 3-11 3" fill={color}/>
    </svg>
  )
}

// ── Handoff connector pill (cross-swimlane) ───────────────────────────────────
function HandoffPill({ label, direction, color }) {
  const isOut = direction === 'out'
  return (
    <div style={{
      display:'inline-flex', alignItems:'center', gap:4, marginTop: isOut ? 6 : 0, marginBottom: isOut ? 0 : 6,
      padding:'3px 8px', borderRadius:20, fontSize:10, fontWeight:500,
      background: mixWhite(color, 0.82), border:`1px dashed ${mixWhite(color, 0.35)}`,
      color: mixWhite(color, 0.1),
    }}>
      {!isOut && <span>↳</span>}
      <span>{label}</span>
      {isOut && <span>↱</span>}
    </div>
  )
}

// ── Utilities ─────────────────────────────────────────────────────────────────
function getRole(node) {
  const r = node?.raci?.r
  return (r && r !== 'NA') ? r : 'Unassigned'
}

function buildRoleOrder(processes) {
  const order = new Map()
  const add = r => { if (r && r !== 'NA' && !order.has(r)) order.set(r, order.size) }
  processes.forEach(proc => {
    add(proc.raci?.r)
    proc.stages.forEach(st => {
      add(st.raci?.r)
      st.steps.forEach(function walk(s) { add(s.raci?.r); s.children?.forEach(walk) })
    })
  })
  return order
}

// Group steps into consecutive same-role segments
function segments(steps) {
  const segs = []
  steps.forEach(s => {
    const role = getRole(s)
    const last = segs[segs.length - 1]
    if (last && last.role === role) last.steps.push(s)
    else segs.push({ role, steps: [s] })
  })
  return segs
}

const ROLE_W = 176

// ── Main component ────────────────────────────────────────────────────────────
export default function ProcessMap({ processes }) {
  const [expL1, setExpL1] = useState(new Set())
  const [expL2, setExpL2] = useState(new Set())
  const [expL3, setExpL3] = useState(new Set())

  const roleOrder = useMemo(() => buildRoleOrder(processes), [processes])

  function togL1(id) {
    const was = expL1.has(id)
    setExpL1(p => { const n=new Set(p); was?n.delete(id):n.add(id); return n })
    if (was) {
      const proc = processes.find(p=>p.id===id)
      if (proc) {
        setExpL2(p => { const n=new Set(p); proc.stages.forEach(s=>n.delete(s.id)); return n })
        setExpL3(p => { const n=new Set(p); proc.stages.flatMap(s=>s.steps).forEach(s=>n.delete(s.seq)); return n })
      }
    }
  }
  function togL2(id) {
    const was = expL2.has(id)
    setExpL2(p => { const n=new Set(p); was?n.delete(id):n.add(id); return n })
    if (was) {
      for (const proc of processes) {
        const st = proc.stages.find(s=>s.id===id)
        if (st) { setExpL3(p => { const n=new Set(p); st.steps.forEach(s=>n.delete(s.seq)); return n }); break }
      }
    }
  }
  function togL3(seq) {
    setExpL3(p => { const n=new Set(p); n.has(seq)?n.delete(seq):n.add(seq); return n })
  }

  // Normalized L1 display nodes
  const l1Nodes = useMemo(() => {
    const m = new Map()
    processes.forEach(proc => m.set(proc.id, {
      seq: `L${proc.l1_seq}`, name: proc.l1_name, description: proc.l1_description,
      system_tool: proc.system_tool, raci: proc.raci,
      key_data_points: proc.key_data_points, step_type: null,
    }))
    return m
  }, [processes])

  // ── Column array ─────────────────────────────────────────────────────────────
  // Each column = one CSS grid column.
  //   type:'L1'  → unexpanded L1 process
  //   type:'L2'  → expanded L1, unexpanded stage
  //   type:'SEG' → expanded stage; one column per consecutive same-role segment
  //                si = segment index within this stage
  //                isFirst = si===0 (L2 header shown here)
  //                prevRole / nextRole = neighbouring segment roles
  const columns = useMemo(() => {
    const cols = []
    processes.forEach(proc => {
      if (!expL1.has(proc.id)) {
        cols.push({ type:'L1', id:`l1-${proc.id}`, proc })
      } else {
        proc.stages.forEach(stage => {
          if (!expL2.has(stage.id)) {
            cols.push({ type:'L2', id:`l2-${stage.id}`, stage, proc })
          } else {
            const segs = segments(stage.steps)
            segs.forEach((seg, si) => {
              cols.push({
                type:'SEG', id:`seg-${stage.id}-${si}`,
                seg, stage, proc, si,
                isFirst: si === 0,
                prevRole: si > 0 ? segs[si-1].role : null,
                nextRole: si < segs.length-1 ? segs[si+1].role : null,
                hasNext:  si < segs.length-1,
              })
            })
          }
        })
      }
    })
    return cols
  }, [processes, expL1, expL2])

  // L1 group header spans (for sticky row 1)
  const l1Groups = useMemo(() => {
    const groups = []
    columns.forEach((c, i) => {
      const col = i + 2 // grid column (1=role-label, 2+=data)
      const last = groups[groups.length-1]
      if (last && last.proc.id === c.proc.id) last.span++
      else groups.push({ proc:c.proc, startCol:col, span:1 })
    })
    return groups
  }, [columns])

  // ── Get items to render in cell (col, role) ───────────────────────────────────
  function getCellItems(col, role) {
    const base = col.proc.l1_color
    const items = []

    // ── Unexpanded L1 ──────────────────────────────────────────────────────────
    if (col.type === 'L1') {
      const node = l1Nodes.get(col.proc.id)
      if (node && getRole(node) === role) {
        items.push({ node, level:'L1', base,
          isSelected: false, childCount: col.proc.stages.length,
          onClick: ()=>togL1(col.proc.id), expandDir:'right' })
      }
      return items
    }

    // ── Unexpanded L2 stage ────────────────────────────────────────────────────
    if (col.type === 'L2') {
      if (getRole(col.stage) === role) {
        items.push({ node:col.stage, level:'L2', base,
          isSelected: false, childCount: col.stage.steps.length,
          onClick: ()=>togL2(col.stage.id), expandDir:'down' })
      }
      return items
    }

    // ── Segment column ─────────────────────────────────────────────────────────
    const { seg, stage, isFirst } = col

    // First segment column: show the L2 parent box in L2-owner's row (collapsed button)
    if (isFirst && getRole(stage) === role) {
      items.push({ node:stage, level:'L2', base,
        isSelected: true, // expanded state
        childCount: 0,    // don't show count while expanded
        onClick: ()=>togL2(stage.id), expandDir:'down' })
    }

    // Show this segment's L3 steps in the matching role row
    if (seg.role === role) {
      seg.steps.forEach(step => {
        const hasKids  = !!step.children?.length
        const l3Exp    = hasKids && expL3.has(step.seq)
        items.push({ node:step, level:'L3', base,
          isSelected: l3Exp, childCount: step.children?.length || 0,
          onClick: hasKids ? ()=>togL3(step.seq) : undefined, expandDir:'down' })
        if (l3Exp) {
          step.children.forEach(child => {
            items.push({ node:child, level:'L4', base,
              isSelected:false, childCount:0, onClick:undefined, expandDir:'down' })
          })
        }
      })
    }

    return items
  }

  // Visible roles: only those present in current column set
  const visibleRoles = useMemo(() => {
    const seen = new Set()
    columns.forEach(col => {
      if (col.type==='L1') { const n=l1Nodes.get(col.proc.id); if(n) seen.add(getRole(n)) }
      else if (col.type==='L2') { seen.add(getRole(col.stage)) }
      else {
        seen.add(getRole(col.stage)) // L2 owner always present
        seen.add(col.seg.role)
        col.seg.steps.forEach(s => {
          if (expL3.has(s.seq)) s.children?.forEach(c=>seen.add(getRole(c)))
        })
      }
    })
    return Array.from(roleOrder.keys()).filter(r => seen.has(r))
  }, [columns, expL3, roleOrder, l1Nodes])

  // ── Grid template: col 1 = role labels, cols 2…N+1 = one per column ──────────
  const gtc = `${ROLE_W}px ${columns.map(()=>'max-content').join(' ')}`

  return (
    <div style={{ height:'100%', overflow:'auto', background:'#f1f5f9',
      display:'grid', gridTemplateColumns:gtc, alignItems:'start' }}>

      {/* ── Corner (spans only row 1) ─────────────────────────────────── */}
      <div style={{
        gridRow:1, gridColumn:1,
        position:'sticky', top:0, left:0, zIndex:40,
        background:'#1e293b', minHeight:44,
        borderRight:'1px solid #334155', borderBottom:'2px solid #0f172a',
        display:'flex', alignItems:'center', gap:8, padding:'0 16px',
      }}>
        <span style={{width:8,height:8,borderRadius:'50%',background:'#34d399',flexShrink:0}}/>
        <span style={{fontSize:11,fontWeight:700,color:'#94a3b8',
          textTransform:'uppercase',letterSpacing:'0.07em'}}>Responsible</span>
      </div>

      {/* ── L1 group headers (row 1, sticky top) ──────────────────────── */}
      {l1Groups.map(g => {
        const c = g.proc.l1_color
        const fill = bg(c,'L1')
        return (
          <div key={g.proc.id+'_gh'}
            onClick={()=>togL1(g.proc.id)}
            style={{
              gridRow:1, gridColumn:`${g.startCol} / span ${g.span}`,
              position:'sticky', top:0, zIndex:30,
              background:fill, minHeight:44,
              borderRight:'2px solid rgba(255,255,255,0.15)',
              borderBottom:'2px solid rgba(0,0,0,0.1)',
              display:'flex', alignItems:'center', gap:8, padding:'0 14px',
              cursor:'pointer',
            }}
          >
            <span style={{fontSize:11,fontFamily:'monospace',fontWeight:700,
              padding:'2px 7px',borderRadius:4,background:'rgba(0,0,0,0.22)',color:'#fff',flexShrink:0}}>
              L{g.proc.l1_seq}
            </span>
            {expL1.has(g.proc.id)
              ? <ChevronDown size={13} color="rgba(255,255,255,0.85)"/>
              : <ChevronRight size={13} color="rgba(255,255,255,0.85)"/>}
            <span style={{fontSize:12,fontWeight:600,color:'#fff',whiteSpace:'nowrap'}}>
              {g.proc.l1_name}
            </span>
          </div>
        )
      })}

      {/* ── Swimlane rows ──────────────────────────────────────────────── */}
      {visibleRoles.map((role, ri) => {
        const rowNum = ri + 2   // row 1 = L1 headers; data starts at row 2
        const rowBg  = ri % 2 === 0 ? '#f8fafc' : '#f1f5f9'

        return (
          <React.Fragment key={role}>

            {/* Sticky role label */}
            <div style={{
              gridRow:rowNum, gridColumn:1,
              position:'sticky', left:0, zIndex:10,
              background:'#1e293b',
              borderRight:'1px solid #334155', borderBottom:'1px solid #1e293b',
              display:'flex', alignItems:'center', gap:8, padding:'14px 16px',
              minHeight:60,
            }}>
              <span style={{width:8,height:8,borderRadius:'50%',background:'#34d399',flexShrink:0}}/>
              <span style={{fontSize:12,fontWeight:600,color:'#e2e8f0',lineHeight:1.3}}>{role}</span>
            </div>

            {/* Data cells */}
            {columns.map((col, ci) => {
              const items   = getCellItems(col, role)
              const base    = col.proc.l1_color
              const isActive = items.length > 0

              // Connector logic (SEG columns only)
              const isSeg  = col.type === 'SEG'
              // Right arrow: shown when next column in same stage exists and this cell is active
              const showRight = isActive && isSeg && col.hasNext && col.seg.role === role && col.nextRole === role
              // Handoff out: this role's last step here, next segment is different role
              const handoffOut = isActive && isSeg && col.hasNext && col.seg.role === role && col.nextRole !== role
                ? col.nextRole : null
              // Handoff in: this is the destination role, previous segment was different role
              const handoffIn = isActive && isSeg && col.prevRole && col.prevRole !== role && col.seg.role === role
                ? col.prevRole : null
              // Also right arrow between consecutive same-role L2 columns
              const showL2Right = isActive && col.type==='L2' && (() => {
                const ni = ci+1; if(ni>=columns.length) return false
                return columns[ni].proc.id === col.proc.id
              })()

              return (
                <div key={col.id+'_'+role}
                  style={{
                    gridRow:rowNum, gridColumn:ci+2,
                    background:rowBg,
                    borderRight:'1px solid #e2e8f0',
                    borderBottom:'1px solid #e2e8f0',
                    padding:'12px 10px',
                    position:'relative',
                  }}
                >
                  {isActive ? (
                    <div style={{display:'flex',flexDirection:'column',alignItems:'flex-start'}}>

                      {/* Handoff-in pill */}
                      {handoffIn && (
                        <HandoffPill label={`← from ${handoffIn}`} direction="in" color={base}/>
                      )}

                      {/* Stacked node items */}
                      {items.map((item, ii) => (
                        <React.Fragment key={`${item.node.seq??item.node._id}_${ii}`}>
                          {ii > 0 && <DownArrow color={mixWhite(item.base, 0.28)}/>}
                          <NodeBox
                            node={item.node}
                            baseColor={item.base}
                            level={item.level}
                            isSelected={item.isSelected}
                            childCount={item.childCount}
                            onClick={item.onClick}
                            expandDir={item.expandDir}
                          />
                        </React.Fragment>
                      ))}

                      {/* Handoff-out pill */}
                      {handoffOut && (
                        <HandoffPill label={`→ ${handoffOut}`} direction="out" color={base}/>
                      )}

                      {/* Right-flow arrow (same role continues in next segment) */}
                      {(showRight || showL2Right) && (
                        <div style={{
                          position:'absolute', right:-16, top:'50%',
                          transform:'translateY(-50%)', zIndex:5,
                        }}>
                          <RightArrow color={mixWhite(base, 0.25)}/>
                        </div>
                      )}
                    </div>
                  ) : (
                    <div style={{
                      minHeight:56, borderRadius:4,
                      backgroundImage:'repeating-linear-gradient(135deg,transparent,transparent 5px,rgba(148,163,184,0.06) 5px,rgba(148,163,184,0.06) 10px)',
                    }}/>
                  )}
                </div>
              )
            })}

          </React.Fragment>
        )
      })}
    </div>
  )
}
