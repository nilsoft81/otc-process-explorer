import React, { useState, useMemo, useEffect, useRef, useCallback } from 'react'
import { ChevronDown, ChevronRight } from 'lucide-react'

// ── Color helpers ─────────────────────────────────────────────────────────────
function mixWhite(hex, t) {
  const h = hex.replace('#', '')
  const r = parseInt(h.slice(0,2), 16)
  const g = parseInt(h.slice(2,4), 16)
  const b = parseInt(h.slice(4,6), 16)
  const m = v => Math.round(v + (255 - v) * t)
  return `rgb(${m(r)},${m(g)},${m(b)})`
}
const OMBRE   = { L1:0.18, L2:0.40, L3:0.60, L4:0.75 }
const TEXT_ON = { L1:'#fff', L2:'#fff', L3:'#1e293b', L4:'#334155' }
const MUTED   = { L1:'rgba(255,255,255,0.78)', L2:'rgba(255,255,255,0.82)', L3:'#64748b', L4:'#94a3b8' }

function bg(hex, level)    { return mixWhite(hex, OMBRE[level] ?? 0.5) }
function tc(level)         { return TEXT_ON[level] ?? '#1e293b' }
function mc(level)         { return MUTED[level]   ?? '#94a3b8' }
function darkBg(hex, level){ return mixWhite(hex, Math.max(0, (OMBRE[level] ?? 0.5) - 0.18)) }

// ── AI / Bot icon ─────────────────────────────────────────────────────────────
function BotIcon({ color, size = 13 }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none"
         stroke={color} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <rect x="3" y="8" width="18" height="13" rx="2"/>
      <path d="M12 2v6"/>
      <circle cx="12" cy="2" r="1.5" fill={color} stroke="none"/>
      <circle cx="8.5" cy="14" r="1.5" fill={color} stroke="none"/>
      <circle cx="15.5" cy="14" r="1.5" fill={color} stroke="none"/>
      <line x1="8" y1="19" x2="16" y2="19" strokeWidth="1.5"/>
    </svg>
  )
}

// ── NodeFooter ────────────────────────────────────────────────────────────────
function NodeFooter({ node, textC, mutedC }) {
  const { raci, system_tool, key_data_points, change_highlight,
          decision_outcomes, critical_artefact, sla } = node
  const anyRaci  = raci  && Object.values(raci).some(v => v && v !== 'NA')
  const hasSys   = system_tool   && system_tool   !== 'NA'
  const hasData  = key_data_points && key_data_points !== 'NA'
  const hasOuts  = !!decision_outcomes
  const hasChg   = !!change_highlight
  const hasArt   = critical_artefact && critical_artefact !== '' && critical_artefact !== 'NA'
  const hasSla   = sla && sla !== '' && sla !== 'NA'
  if (!anyRaci && !hasSys && !hasData && !hasOuts && !hasChg && !hasArt && !hasSla) return null

  const pill = (label, val, pbg='rgba(0,0,0,0.18)', pbd='rgba(255,255,255,0.18)') =>
    val && val !== 'NA' ? (
      <span key={label} style={{
        display:'inline-flex', alignItems:'center', gap:3,
        padding:'1px 5px', borderRadius:4, fontSize:9, fontWeight:600,
        background:pbg, color:textC, border:`1px solid ${pbd}`,
      }}>{label} <span style={{fontWeight:400,opacity:0.9}}>{val}</span></span>
    ) : null

  return (
    <div style={{ marginTop:6, paddingTop:5, borderTop:'1px solid rgba(255,255,255,0.18)',
      display:'flex', flexDirection:'column', gap:3 }}>
      {hasSys && (
        <div style={{display:'flex',flexWrap:'wrap',gap:2}}>
          {system_tool.split('/').map(s=>s.trim()).filter(Boolean).map(s=>(
            <span key={s} style={{fontSize:9,fontFamily:'monospace',padding:'1px 4px',borderRadius:3,
              background:'rgba(0,0,0,0.15)',color:textC}}>{s}</span>
          ))}
        </div>
      )}
      {anyRaci && (
        <div style={{display:'flex',flexWrap:'wrap',gap:2}}>
          {pill('R',raci.r)}{pill('A',raci.a)}{pill('C',raci.c)}
        </div>
      )}
      {(hasArt || hasSla) && (
        <div style={{display:'flex',flexWrap:'wrap',gap:2}}>
          {hasArt && pill('📎', critical_artefact, 'rgba(217,119,6,0.35)', 'rgba(217,119,6,0.5)')}
          {hasSla && pill('⏱', sla,               'rgba(37,99,235,0.28)', 'rgba(37,99,235,0.42)')}
        </div>
      )}
      {hasOuts && decision_outcomes.split('|').map((o,i)=>(
        <span key={i} style={{fontSize:9,color:mutedC,display:'flex',gap:2,lineHeight:1.3}}>
          <span style={{color:textC}}>▸</span><span>{o.trim()}</span>
        </span>
      ))}
      {hasData && <p style={{fontSize:9,color:mutedC,margin:0,lineHeight:1.3}}>
        <b>Data:</b> {key_data_points}</p>}
      {hasChg && <p style={{fontSize:9,color:mutedC,margin:0,fontStyle:'italic',lineHeight:1.3}}>
        <b>Δ</b> {change_highlight}</p>}
    </div>
  )
}

// ── NodeBox (regular: process steps) ─────────────────────────────────────────
function NodeBox({ node, baseColor, level, isSelected, childCount, onClick, expandDir='down', boxRef }) {
  const fill  = bg(baseColor, level)
  const dark  = darkBg(baseColor, level)
  const textC = tc(level)
  const mutedC= mc(level)
  const w     = { L1:200, L2:185, L3:170, L4:160 }[level] ?? 170
  const isAI  = node.raci?.r?.toUpperCase().includes('AI')

  return (
    <div ref={boxRef} onClick={onClick} style={{
      position:'relative', flexShrink:0, width:w, padding:'9px 11px', borderRadius:8,
      background:fill,
      boxShadow: isSelected
        ? `0 0 0 2px ${dark}, 0 4px 16px rgba(0,0,0,0.18)`
        : '0 1px 5px rgba(0,0,0,0.13)',
      cursor: onClick ? 'pointer' : 'default',
      transition:'box-shadow 0.15s, transform 0.1s',
      transform: isSelected ? 'translateY(-1px)' : undefined,
      display:'flex', flexDirection:'column',
    }}>
      {/* Header row: seq badge + AI icon + decision badge */}
      <div style={{display:'flex',flexWrap:'wrap',alignItems:'center',gap:3,marginBottom:4}}>
        <span style={{fontSize:10,fontFamily:'monospace',fontWeight:700,
          padding:'1px 5px',borderRadius:3,background:'rgba(0,0,0,0.2)',color:textC}}>
          {node.seq}
        </span>
        {isAI && (
          <span style={{display:'inline-flex',alignItems:'center',gap:2,
            padding:'1px 5px',borderRadius:3,background:'rgba(99,102,241,0.35)',color:textC,
            fontSize:9,fontWeight:600}}>
            <BotIcon color={textC} size={11}/> AI
          </span>
        )}
        {node.step_type?.toLowerCase().includes('decision') && (
          <span style={{fontSize:9,padding:'1px 4px',borderRadius:3,
            background:'rgba(0,0,0,0.2)',color:textC}}>◇ Decision</span>
        )}
      </div>
      <p style={{fontSize:11,fontWeight:600,lineHeight:1.35,color:textC,margin:0}}>{node.name}</p>
      {(level==='L1'||level==='L2') && node.description && (
        <p style={{fontSize:10,color:mutedC,margin:'3px 0 0',lineHeight:1.4,
          display:'-webkit-box',WebkitLineClamp:2,WebkitBoxOrient:'vertical',overflow:'hidden'}}>
          {node.description}
        </p>
      )}
      <NodeFooter node={node} textC={textC} mutedC={mutedC}/>
      {childCount > 0 && (
        <div style={{marginTop:5,display:'flex',alignItems:'center',gap:3,fontSize:10,color:mutedC}}>
          {isSelected ? <ChevronDown size={10} color={mutedC}/> : <ChevronRight size={10} color={mutedC}/>}
          <span>{childCount} {level==='L1'?'stages':level==='L2'?'steps':'tasks'}</span>
        </div>
      )}
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

// ── DiamondBox (decision nodes) ───────────────────────────────────────────────
// Uses a rotated square that exactly inscribes a diamond within the outer bounding box.
// DIAG = visual width/height of the diamond point-to-point.
const DIAG = 164
const SIDE = Math.round(DIAG / Math.SQRT2)  // inner square side ≈ 116px
const INSET = Math.round((DIAG - SIDE) / 2) // offset from outer edge ≈ 24px

function DiamondBox({ node, baseColor, level, isSelected, onClick, boxRef }) {
  const fill  = bg(baseColor, level)
  const dark  = darkBg(baseColor, level)
  const textC = tc(level)
  const mutedC= mc(level)
  const isAI  = node.raci?.r?.toUpperCase().includes('AI')

  return (
    <div ref={boxRef} style={{ position:'relative', flexShrink:0, width:DIAG, height:DIAG,
      cursor: onClick ? 'pointer' : 'default' }}
      onClick={onClick}>
      {/* Rotated square = diamond */}
      <div style={{
        position:'absolute',
        top:INSET, left:INSET,
        width:SIDE, height:SIDE,
        transform:'rotate(45deg)',
        background:fill,
        border:`2px solid ${dark}`,
        boxShadow: isSelected
          ? `0 0 0 2px ${dark}, 0 4px 14px rgba(0,0,0,0.18)`
          : '0 1px 5px rgba(0,0,0,0.13)',
      }}/>
      {/* Content — centered, counter-rotated stays horizontal */}
      <div style={{
        position:'absolute', inset:0,
        display:'flex', flexDirection:'column', alignItems:'center', justifyContent:'center',
        padding:`12px ${INSET + 12}px`,
        textAlign:'center', gap:2,
      }}>
        <div style={{display:'flex',alignItems:'center',gap:3,flexWrap:'wrap',justifyContent:'center'}}>
          <span style={{fontSize:9,fontFamily:'monospace',fontWeight:700,
            padding:'1px 4px',borderRadius:3,background:'rgba(0,0,0,0.22)',color:textC}}>
            {node.seq}
          </span>
          {isAI && <BotIcon color={textC} size={10}/>}
        </div>
        <p style={{fontSize:10,fontWeight:700,color:textC,margin:0,lineHeight:1.25,
          maxWidth:SIDE-8,wordBreak:'break-word'}}>
          {node.name}
        </p>
        {node.raci?.r && node.raci.r !== 'NA' && (
          <span style={{fontSize:8,color:mutedC,lineHeight:1}}>R: {node.raci.r}</span>
        )}
        {node.sla && node.sla !== '' && (
          <span style={{fontSize:8,color:mutedC}}>⏱ {node.sla}</span>
        )}
        {/* Yes / No outcome branches */}
        {node.decision_outcomes && (
          <div style={{display:'flex',flexDirection:'column',gap:1,marginTop:1}}>
            {node.decision_outcomes.split('|').map((o,i) => {
              const txt = o.trim()
              const isYes = /^yes/i.test(txt)
              const isNo  = /^no/i.test(txt)
              return (
                <span key={i} style={{
                  fontSize:8, fontWeight:600, lineHeight:1.2,
                  color: isYes ? '#16a34a' : isNo ? '#dc2626' : textC,
                }}>
                  {isYes ? '✓' : isNo ? '✗' : '▸'} {txt}
                </span>
              )
            })}
          </div>
        )}
      </div>
    </div>
  )
}

// ── Down-arrow connector (within a cell, between stacked items) ───────────────
function DownArrow({ color }) {
  return (
    <div style={{display:'flex',alignItems:'center',paddingLeft:20,margin:'3px 0'}}>
      <svg width="12" height="20" viewBox="0 0 12 20" fill="none">
        <line x1="6" y1="0" x2="6" y2="13" stroke={color} strokeWidth="2" strokeLinecap="round"/>
        <path d="M2 10l4 10 4-10" fill={color}/>
      </svg>
    </div>
  )
}

// ── Right-arrow connector (same role, consecutive segments) ───────────────────
function RightArrow({ color }) {
  return (
    <svg width="32" height="14" viewBox="0 0 32 14" fill="none" style={{flexShrink:0}}>
      <line x1="0" y1="7" x2="22" y2="7" stroke={color} strokeWidth="2" strokeLinecap="round"/>
      <path d="M19 3l13 4-13 4" fill={color}/>
    </svg>
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

  const l1Nodes = useMemo(() => {
    const m = new Map()
    processes.forEach(proc => m.set(proc.id, {
      seq: `L${proc.l1_seq}`, name: proc.l1_name, description: proc.l1_description,
      system_tool: proc.system_tool, raci: proc.raci,
      key_data_points: proc.key_data_points, step_type: null,
      critical_artefact: proc.critical_artefact || '', sla: proc.sla || '',
    }))
    return m
  }, [processes])

  // ── Column array ──────────────────────────────────────────────────────────
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
                isFirst:  si === 0,
                prevRole: si > 0            ? segs[si-1].role : null,
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

  // L1 group header spans
  const l1Groups = useMemo(() => {
    const groups = []
    columns.forEach((c, i) => {
      const col = i + 2
      const last = groups[groups.length-1]
      if (last && last.proc.id === c.proc.id) last.span++
      else groups.push({ proc:c.proc, startCol:col, span:1 })
    })
    return groups
  }, [columns])

  // Cell items for (col, role)
  function getCellItems(col, role) {
    const base = col.proc.l1_color
    const items = []

    if (col.type === 'L1') {
      const node = l1Nodes.get(col.proc.id)
      if (node && getRole(node) === role)
        items.push({ node, level:'L1', base,
          isSelected:false, childCount:col.proc.stages.length,
          onClick:()=>togL1(col.proc.id), expandDir:'right' })
      return items
    }

    if (col.type === 'L2') {
      if (getRole(col.stage) === role)
        items.push({ node:col.stage, level:'L2', base,
          isSelected:false, childCount:col.stage.steps.length,
          onClick:()=>togL2(col.stage.id), expandDir:'down' })
      return items
    }

    const { seg, stage, isFirst } = col
    if (isFirst && getRole(stage) === role)
      items.push({ node:stage, level:'L2', base,
        isSelected:true, childCount:0,
        onClick:()=>togL2(stage.id), expandDir:'down' })

    if (seg.role === role) {
      seg.steps.forEach(step => {
        const hasKids = !!step.children?.length
        const l3Exp   = hasKids && expL3.has(step.seq)
        items.push({ node:step, level:'L3', base,
          isSelected:l3Exp, childCount:step.children?.length||0,
          onClick: hasKids ? ()=>togL3(step.seq) : undefined, expandDir:'down' })
        if (l3Exp) {
          step.children.forEach(child =>
            items.push({ node:child, level:'L4', base,
              isSelected:false, childCount:0, onClick:undefined, expandDir:'down' }))
        }
      })
    }
    return items
  }

  const visibleRoles = useMemo(() => {
    const seen = new Set()
    columns.forEach(col => {
      if (col.type==='L1') { const n=l1Nodes.get(col.proc.id); if(n) seen.add(getRole(n)) }
      else if (col.type==='L2') { seen.add(getRole(col.stage)) }
      else {
        seen.add(getRole(col.stage))
        seen.add(col.seg.role)
        col.seg.steps.forEach(s => {
          if (expL3.has(s.seq)) s.children?.forEach(c=>seen.add(getRole(c)))
        })
      }
    })
    return Array.from(roleOrder.keys()).filter(r => seen.has(r))
  }, [columns, expL3, roleOrder, l1Nodes])

  // ── Refs for SVG arrow overlay ────────────────────────────────────────────
  const scrollRef = useRef(null)
  const gridRef   = useRef(null)
  const cellRefs  = useRef({})   // key: `${ci}_${role}` → DOM element
  const nodeRefs  = useRef({})   // key: `${ci}_${role}_last` / `_first` → NodeBox DOM element
  const [svgArrows, setSvgArrows] = useState([])
  const [svgSize,   setSvgSize]   = useState({ w: 2000, h: 2000 })

  const computeArrows = useCallback(() => {
    const scroll = scrollRef.current
    if (!scroll) return

    const scrollRect = scroll.getBoundingClientRect()
    const sl = scroll.scrollLeft
    const st = scroll.scrollTop

    // Convert viewport rect → scroll-content coordinates
    const toC = rect => ({
      top:    rect.top    - scrollRect.top  + st,
      bottom: rect.bottom - scrollRect.top  + st,
      left:   rect.left   - scrollRect.left + sl,
      right:  rect.right  - scrollRect.left + sl,
      cx:     rect.left   - scrollRect.left + sl + rect.width  / 2,
      cy:     rect.top    - scrollRect.top  + st + rect.height / 2,
      w:      rect.width,
      h:      rect.height,
    })

    const arrs = []

    columns.forEach((col, ci) => {
      if (col.type !== 'SEG' || !col.hasNext) return
      if (col.seg.role === col.nextRole) return  // same lane → right-arrow already shown

      const fromKey = `${ci}_${col.seg.role}`
      const toKey   = `${ci+1}_${col.nextRole}`
      const fromEl  = cellRefs.current[fromKey]
      const toEl    = cellRefs.current[toKey]
      if (!fromEl || !toEl) return

      const fr = toC(fromEl.getBoundingClientRect())
      const tr = toC(toEl.getBoundingClientRect())

      // From right-center of source cell → left-center of target cell
      const x1 = fr.right
      const y1 = fr.cy
      const x2 = tr.left
      const y2 = tr.cy

      // Midpoint X for the bend
      const midX = (x1 + x2) / 2

      arrs.push({ x1, y1, x2, y2, midX, color: col.proc.l1_color,
        id: `${col.id}_${col.nextRole}` })
    })

    // Also draw within-column arrows: consecutive steps in SAME expanded L2
    // that are in DIFFERENT swimlane rows (same column position, different roles)
    // These appear when an L2 has multiple consecutive same-role steps but then
    // a role change within the same column (not possible with segment splitting,
    // so these are already covered by the SEG->SEG case above).

    const grid = gridRef.current
    if (grid) {
      setSvgSize({ w: grid.scrollWidth, h: grid.scrollHeight })
    }
    setSvgArrows(arrs)
  }, [columns])

  useEffect(() => {
    const raf = requestAnimationFrame(() => computeArrows())
    return () => cancelAnimationFrame(raf)
  }, [computeArrows, expL1, expL2, expL3, visibleRoles])

  // Re-compute on scroll (arrows need to stay fixed relative to content, not viewport)
  // They are in content-space so no recompute needed on scroll — they scroll with the grid.

  const gtc = `${ROLE_W}px ${columns.map(()=>'max-content').join(' ')}`

  return (
    <div ref={scrollRef}
      style={{ height:'100%', overflow:'auto', background:'#f1f5f9', position:'relative' }}>

      {/* ── Grid ──────────────────────────────────────────────────────────── */}
      <div ref={gridRef}
        style={{ display:'grid', gridTemplateColumns:gtc, alignItems:'start' }}>

        {/* Corner */}
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

        {/* L1 group headers */}
        {l1Groups.map(g => {
          const fill = bg(g.proc.l1_color, 'L1')
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
              }}>
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

        {/* Swimlane rows */}
        {visibleRoles.map((role, ri) => {
          const rowNum = ri + 2
          const rowBg  = ri % 2 === 0 ? '#f8fafc' : '#f1f5f9'

          return (
            <React.Fragment key={role}>
              {/* Role label */}
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
                const items    = getCellItems(col, role)
                const base     = col.proc.l1_color
                const isActive = items.length > 0
                const isSeg    = col.type === 'SEG'

                const showRight = isActive && isSeg && col.hasNext
                  && col.seg.role === role && col.nextRole === role
                const showL2Right = isActive && col.type==='L2' && (() => {
                  const ni = ci+1; if(ni>=columns.length) return false
                  return columns[ni].proc.id === col.proc.id
                })()

                return (
                  <div key={col.id+'_'+role}
                    ref={el => { cellRefs.current[`${ci}_${role}`] = el }}
                    style={{
                      gridRow:rowNum, gridColumn:ci+2,
                      background:rowBg,
                      borderRight:'1px solid #e2e8f0',
                      borderBottom:'1px solid #e2e8f0',
                      padding:'12px 10px',
                      position:'relative',
                    }}>
                    {isActive ? (
                      <div style={{display:'flex',flexDirection:'column',alignItems:'flex-start'}}>
                        {items.map((item, ii) => {
                          const isDecision = item.node.step_type?.toLowerCase() === 'decision'
                            || item.node.step_type?.toLowerCase() === 'decision (automated)'
                          const BoxComp = isDecision ? DiamondBox : NodeBox
                          return (
                            <React.Fragment key={`${item.node.seq??item.node.id}_${ii}`}>
                              {ii > 0 && <DownArrow color={mixWhite(item.base, 0.22)}/>}
                              <BoxComp
                                node={item.node}
                                baseColor={item.base}
                                level={item.level}
                                isSelected={item.isSelected}
                                childCount={item.childCount}
                                onClick={item.onClick}
                                expandDir={item.expandDir}
                              />
                            </React.Fragment>
                          )
                        })}

                        {/* Same-role continuation arrow */}
                        {(showRight || showL2Right) && (
                          <div style={{
                            position:'absolute', right:-18, top:'50%',
                            transform:'translateY(-50%)', zIndex:5,
                          }}>
                            <RightArrow color={mixWhite(base, 0.2)}/>
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

      {/* ── SVG cross-swimlane arrow overlay ──────────────────────────────── */}
      <svg
        style={{
          position:'absolute', top:0, left:0,
          width: svgSize.w, height: svgSize.h,
          pointerEvents:'none', overflow:'visible', zIndex:20,
        }}
        width={svgSize.w} height={svgSize.h}>
        <defs>
          <marker id="swHead" markerWidth="9" markerHeight="9"
            refX="8" refY="3" orient="auto">
            <path d="M0,0 L9,3 L0,6 Z" fill="#475569"/>
          </marker>
          <marker id="swHeadColor" markerWidth="9" markerHeight="9"
            refX="8" refY="3" orient="auto">
            <path d="M0,0 L9,3 L0,6 Z" fill="#334155"/>
          </marker>
        </defs>
        {svgArrows.map(a => {
          const arrowColor = mixWhite(a.color, 0.15)
          // Cubic bezier: right side of source → left side of target, bending via midX
          const d = `M${a.x1},${a.y1} C${a.midX},${a.y1} ${a.midX},${a.y2} ${a.x2},${a.y2}`
          return (
            <g key={a.id}>
              {/* Shadow for visibility */}
              <path d={d} fill="none" stroke="rgba(255,255,255,0.6)" strokeWidth="4.5"
                strokeLinecap="round"/>
              {/* Main arrow */}
              <path d={d} fill="none" stroke={arrowColor} strokeWidth="2.5"
                strokeLinecap="round" markerEnd="url(#swHead)"/>
            </g>
          )
        })}
      </svg>
    </div>
  )
}
