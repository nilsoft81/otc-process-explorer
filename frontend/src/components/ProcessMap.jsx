import React, { useState, useMemo, useEffect, useRef, useCallback } from 'react'
import { ChevronDown, ChevronRight } from 'lucide-react'

// ── Inizio brand color palette (L1 override) ──────────────────────────────────
const INIZIO_COLORS = {
  'order-capture':            '#7C3AED',  // Inizio Violet (primary)
  'demand-supply-planning':   '#0E7490',  // Inizio Teal Dark
  'service-delivery':         '#0891B2',  // Inizio Teal
  'revenue-recognition':      '#16A34A',  // Forest Green
  'invoicing-billing':        '#D97706',  // Amber
  'collections':              '#2563EB',  // Inizio Blue
  'project-close-reporting':  '#0F766E',  // Emerald - Project Close & Reporting
}
function procColor(proc) { return INIZIO_COLORS[proc.id] || proc.l1_color }

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
function BotIcon({ color, size = 18 }) {
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

// ── NodeBox (regular process steps) ──────────────────────────────────────────
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
      <div style={{display:'flex',flexWrap:'wrap',alignItems:'center',gap:4,marginBottom:4}}>
        <span style={{fontSize:10,fontFamily:'monospace',fontWeight:700,
          padding:'1px 5px',borderRadius:3,background:'rgba(0,0,0,0.2)',color:textC}}>
          {node.seq}
        </span>
        {isAI && (
          <span style={{display:'inline-flex',alignItems:'center',gap:3,
            padding:'2px 6px',borderRadius:4,background:'rgba(99,102,241,0.40)',color:textC,
            fontSize:10,fontWeight:700}}>
            <BotIcon color={textC} size={18}/> AI Agent
          </span>
        )}
        {node.step_type?.toLowerCase().includes('decision') && (
          <span style={{fontSize:9,padding:'1px 4px',borderRadius:3,
            background:'rgba(0,0,0,0.2)',color:textC}}>◇ Decision</span>
        )}
      </div>
      <p style={{fontSize:11,fontWeight:600,lineHeight:1.35,color:textC,margin:0}}>{node.name}</p>
      {node.description && (
        <p style={{fontSize:10,color:mutedC,margin:'3px 0 0',lineHeight:1.4,
          ...(level==='L1'||level==='L2' ? {
            display:'-webkit-box',WebkitLineClamp:2,WebkitBoxOrient:'vertical',overflow:'hidden'
          } : {})}}>
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
const DIAG  = 164
const SIDE  = Math.round(DIAG / Math.SQRT2)   // ≈ 116px inner square
const INSET = Math.round((DIAG - SIDE) / 2)   // ≈ 24px

// Map first word of outcome to short direction label
function outcomeShort(txt) {
  const w = txt.split(/[\s–—-]/)[0]
  const M = { Yes:'YES', No:'NO', Approved:'OK', Rejected:'BACK',
              Aligned:'OK', Discrepancy:'REWORK', Query:'QUERY',
              Dispute:'DISPUTE', Chase:'CHASE' }
  return M[w] || w.slice(0, 7).toUpperCase()
}

function DiamondBox({ node, baseColor, level, isSelected, onClick, boxRef }) {
  const fill  = bg(baseColor, level)
  const dark  = darkBg(baseColor, level)
  const textC = tc(level)
  const mutedC= mc(level)
  const isAI  = node.raci?.r?.toUpperCase().includes('AI')

  const outcomes = node.decision_outcomes
    ? node.decision_outcomes.split('|').map(o => o.trim()).slice(0, 3)
    : []

  const isPos = t => /yes|proceed|approv|align/i.test(t)
  const isNeg = t => /no\b|reject|discrepan|dispute|query|chase|return/i.test(t)
  const outColor = () => dark

  const STUB = 24  // exit stub length (px)
  const HD   = 5   // arrowhead half-size

  // Right, bottom, left exit geometry for up to 3 outcomes
  const exits = [
    { // → right (typically "Yes / forward")
      lx1: DIAG,   ly1: DIAG/2,
      lx2: DIAG+STUB, ly2: DIAG/2,
      hd: `M${DIAG+STUB-HD},${DIAG/2-HD} L${DIAG+STUB+HD},${DIAG/2} L${DIAG+STUB-HD},${DIAG/2+HD}`,
      tx: DIAG+STUB+HD+3, ty: DIAG/2+3, ta: 'start',
    },
    { // ↓ bottom (typically "No / back")
      lx1: DIAG/2,   ly1: DIAG,
      lx2: DIAG/2,   ly2: DIAG+STUB,
      hd: `M${DIAG/2-HD},${DIAG+STUB-HD} L${DIAG/2},${DIAG+STUB+HD} L${DIAG/2+HD},${DIAG+STUB-HD}`,
      tx: DIAG/2, ty: DIAG+STUB+HD+10, ta: 'middle',
    },
    { // ← left (third outcome if present)
      lx1: 0,    ly1: DIAG/2,
      lx2: -STUB, ly2: DIAG/2,
      hd: `M${-STUB+HD},${DIAG/2-HD} L${-STUB-HD},${DIAG/2} L${-STUB+HD},${DIAG/2+HD}`,
      tx: -STUB-HD-3, ty: DIAG/2+3, ta: 'end',
    },
  ]

  return (
    <div ref={boxRef} onClick={onClick}
      style={{ position:'relative', flexShrink:0, width:DIAG, height:DIAG,
        cursor: onClick ? 'pointer' : 'default', overflow:'visible' }}>

      {/* Rotated square = diamond shape */}
      <div style={{
        position:'absolute', top:INSET, left:INSET, width:SIDE, height:SIDE,
        transform:'rotate(45deg)', background:fill, border:`2px solid ${dark}`,
        boxShadow: isSelected
          ? `0 0 0 2px ${dark}, 0 4px 14px rgba(0,0,0,0.18)`
          : '0 1px 5px rgba(0,0,0,0.13)',
      }}/>

      {/* Content — centered, stays horizontal */}
      <div style={{
        position:'absolute', inset:0,
        display:'flex', flexDirection:'column', alignItems:'center', justifyContent:'center',
        padding:`12px ${INSET+12}px`, textAlign:'center', gap:2,
      }}>
        <div style={{display:'flex',alignItems:'center',gap:3,flexWrap:'wrap',justifyContent:'center'}}>
          <span style={{fontSize:9,fontFamily:'monospace',fontWeight:700,
            padding:'1px 4px',borderRadius:3,background:'rgba(0,0,0,0.22)',color:textC}}>
            {node.seq}
          </span>
          {isAI && <BotIcon color={textC} size={16}/>}
        </div>
        <p style={{fontSize:10,fontWeight:700,color:textC,margin:0,lineHeight:1.25,
          maxWidth:SIDE-8, wordBreak:'break-word'}}>
          {node.name}
        </p>
        {node.raci?.r && node.raci.r !== 'NA' && (
          <span style={{fontSize:8,color:mutedC,lineHeight:1}}>R: {node.raci.r}</span>
        )}
        {node.sla && node.sla !== '' && node.sla !== 'NA' && (
          <span style={{fontSize:8,color:mutedC}}>⏱ {node.sla}</span>
        )}
      </div>

      {/* Decision exit arrows — exiting from diamond points */}
      {outcomes.length > 0 && (
        <svg style={{position:'absolute',top:0,left:0,overflow:'visible',
                     pointerEvents:'none',zIndex:6}}
             width={DIAG} height={DIAG}>
          {outcomes.map((out, i) => {
            if (i >= exits.length) return null
            const e = exits[i]
            const col = outColor(out)
            const lbl = outcomeShort(out)
            return (
              <g key={i}>
                {/* Stub line */}
                <line x1={e.lx1} y1={e.ly1} x2={e.lx2} y2={e.ly2}
                  stroke={col} strokeWidth="1.5" strokeLinecap="round"/>
                {/* Arrowhead */}
                <path d={e.hd} fill={col}/>
                {/* Short label */}
                <text x={e.tx} y={e.ty} fontSize="8" fill={col}
                  textAnchor={e.ta} fontWeight="700"
                  style={{fontFamily:'system-ui,sans-serif'}}>{lbl}</text>
              </g>
            )
          })}
        </svg>
      )}
    </div>
  )
}

// ── Down-arrow connector (within-cell, between stacked items) ─────────────────
function DownArrow({ color }) {
  return (
    <div style={{display:'flex',alignItems:'center',paddingLeft:20,margin:'3px 0'}}>
      <svg width="10" height="18" viewBox="0 0 10 18" fill="none">
        <line x1="5" y1="0" x2="5" y2="11" stroke={color} strokeWidth="1.5" strokeLinecap="round"/>
        <path d="M1 8l4 10 4-10" fill={color}/>
      </svg>
    </div>
  )
}

// ── Right-arrow connector (same role, consecutive segments) ───────────────────
function RightArrow({ color }) {
  return (
    <svg width="28" height="12" viewBox="0 0 28 12" fill="none" style={{flexShrink:0}}>
      <line x1="0" y1="6" x2="19" y2="6" stroke={color} strokeWidth="1.5" strokeLinecap="round"/>
      <path d="M16 2l12 4-12 4" fill={color}/>
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
    const base = procColor(col.proc)
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
  const scrollRef     = useRef(null)
  const gridRef       = useRef(null)
  const cellRefs      = useRef({})   // ci_role → cell div (fallback)
  const boxFirstRefs  = useRef({})   // ci_role → first NodeBox/DiamondBox in cell
  const boxLastRefs   = useRef({})   // ci_role → last  NodeBox/DiamondBox in cell
  const [svgArrows, setSvgArrows] = useState([])
  const [svgSize,   setSvgSize]   = useState({ w: 2000, h: 2000 })

  const computeArrows = useCallback(() => {
    const scroll = scrollRef.current
    if (!scroll) return

    const scrollRect = scroll.getBoundingClientRect()
    const sl = scroll.scrollLeft
    const st = scroll.scrollTop

    // Viewport → scroll-content coordinates
    const toC = rect => ({
      top:    rect.top    - scrollRect.top  + st,
      bottom: rect.bottom - scrollRect.top  + st,
      left:   rect.left   - scrollRect.left + sl,
      right:  rect.right  - scrollRect.left + sl,
      cy:     rect.top    - scrollRect.top  + st + rect.height / 2,
    })

    const arrs = []

    columns.forEach((col, ci) => {
      if (col.type === 'L1') return
      const nextCol = columns[ci + 1]
      if (!nextCol || nextCol.type === 'L1') return
      if (col.proc.id !== nextCol.proc.id) return

      const fromRole = col.type === 'L2' ? getRole(col.stage) : col.seg.role
      const toRole   = nextCol.type === 'L2' ? getRole(nextCol.stage) : nextCol.seg.role

      // Skip if same role and an inline right-arrow already handles this transition
      const inlineHandled = fromRole === toRole && (
        (col.type === 'SEG' && col.hasNext) || col.type === 'L2'
      )
      if (inlineHandled) return

      const fromKey = `${ci}_${fromRole}`
      const toKey   = `${ci+1}_${toRole}`
      const fromEl  = boxLastRefs.current[fromKey]
      const toEl    = boxFirstRefs.current[toKey]
      if (!fromEl || !toEl) return

      const fr = toC(fromEl.getBoundingClientRect())
      const tr = toC(toEl.getBoundingClientRect())

      const x1 = fr.right
      const y1 = fr.cy
      const x2 = tr.left
      const y2 = tr.cy
      const midX = (x1 + x2) / 2

      arrs.push({ x1, y1, x2, y2, midX, color: procColor(col.proc),
        id: `${col.id}_to_${ci+1}` })
    })

    const grid = gridRef.current
    if (grid) setSvgSize({ w: grid.scrollWidth, h: grid.scrollHeight })
    setSvgArrows(arrs)
  }, [columns])

  useEffect(() => {
    const raf = requestAnimationFrame(() => computeArrows())
    return () => cancelAnimationFrame(raf)
  }, [computeArrows, expL1, expL2, expL3, visibleRoles])

  const gtc = `${ROLE_W}px ${columns.map(()=>'max-content').join(' ')}`

  return (
    <div ref={scrollRef}
      style={{ height:'100%', overflow:'auto', background:'#f1f5f9', position:'relative' }}>

      {/* ── Grid ──────────────────────────────────────────────────────────── */}
      <div ref={gridRef}
        style={{ display:'grid', gridTemplateColumns:gtc, alignItems:'start' }}>

        {/* Corner cell */}
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
          const base = procColor(g.proc)
          const fill = bg(base, 'L1')
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
                const base     = procColor(col.proc)
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
                          const cellKey = `${ci}_${role}`
                          const isFirstBox = ii === 0
                          const isLastBox  = ii === items.length - 1
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
                                boxRef={el => {
                                  if (isFirstBox) boxFirstRefs.current[cellKey] = el
                                  if (isLastBox)  boxLastRefs.current[cellKey]  = el
                                }}
                              />
                            </React.Fragment>
                          )
                        })}

                        {/* Same-role continuation arrow */}
                        {(showRight || showL2Right) && (
                          <div style={{
                            position:'absolute', right:-16, top:'50%',
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
          {/* Small, clean arrowhead */}
          <marker id="swHead" markerWidth="7" markerHeight="7"
            refX="6" refY="3.5" orient="auto" markerUnits="strokeWidth">
            <path d="M0,0.5 L6,3.5 L0,6.5" fill="none"
              stroke="#475569" strokeWidth="1.2" strokeLinecap="round" strokeLinejoin="round"/>
          </marker>
          <marker id="swHeadColor" markerWidth="7" markerHeight="7"
            refX="6" refY="3.5" orient="auto" markerUnits="strokeWidth">
            <path d="M0,0.5 L6,3.5 L0,6.5" fill="none"
              stroke="inherit" strokeWidth="1.2" strokeLinecap="round" strokeLinejoin="round"/>
          </marker>
        </defs>
        {svgArrows.map(a => {
          const arrowColor = mixWhite(a.color, 0.15)
          const d  = `M${a.x1},${a.y1} L${a.midX},${a.y1} L${a.midX},${a.y2} L${a.x2},${a.y2}`
          const AH = 5
          const ah = `M${a.x2-AH},${a.y2-AH} L${a.x2},${a.y2} L${a.x2-AH},${a.y2+AH}`
          return (
            <g key={a.id}>
              <path d={d} fill="none" stroke="rgba(255,255,255,0.7)" strokeWidth="3.5"
                strokeLinecap="square" strokeLinejoin="miter"/>
              <path d={d} fill="none" stroke={arrowColor} strokeWidth="1.5"
                strokeLinecap="square" strokeLinejoin="miter"/>
              <path d={ah} fill="none" stroke={arrowColor} strokeWidth="1.5"
                strokeLinecap="round" strokeLinejoin="round"/>
            </g>
          )
        })}
      </svg>
    </div>
  )
}
