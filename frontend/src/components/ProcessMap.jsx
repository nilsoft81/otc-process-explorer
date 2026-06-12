import React, { useState, useMemo, useEffect, useRef, useCallback } from 'react'
import { ChevronDown, ChevronRight } from 'lucide-react'

// ── Inizio brand color palette ─────────────────────────────────────────────────
const INIZIO_COLORS = {
  'order-capture':            '#7C3AED',
  'demand-supply-planning':   '#0E7490',
  'service-delivery':         '#0891B2',
  'revenue-recognition':      '#16A34A',
  'invoicing-billing':        '#D97706',
  'collections':              '#2563EB',
  'project-close-reporting':  '#0F766E',
}
function procColor(proc) { return INIZIO_COLORS[proc.id] || proc.l1_color }

// ── Color helpers ──────────────────────────────────────────────────────────────
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

function bg(hex, level)     { return mixWhite(hex, OMBRE[level] ?? 0.5) }
function tc(level)          { return TEXT_ON[level] ?? '#1e293b' }
function mc(level)          { return MUTED[level]   ?? '#94a3b8' }
function darkBg(hex, level) { return mixWhite(hex, Math.max(0, (OMBRE[level] ?? 0.5) - 0.18)) }

// ── AI / Bot icon ──────────────────────────────────────────────────────────────
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

// ── NodeFooter (system + RACI) ─────────────────────────────────────────────────
function NodeFooter({ node, textC, mutedC }) {
  const { raci, system_tool, decision_outcomes } = node
  const anyRaci = raci && Object.values(raci).some(v => v && v !== 'NA')
  const hasSys  = system_tool && system_tool !== 'NA'
  const hasOuts = !!decision_outcomes
  if (!anyRaci && !hasSys && !hasOuts) return null

  const pill = (label, val) =>
    val && val !== 'NA' ? (
      <span key={label} style={{
        display:'inline-flex', alignItems:'flex-start', gap:3,
        padding:'2px 6px', borderRadius:4, fontSize:9, fontWeight:600,
        background:'rgba(0,0,0,0.18)', color:textC,
        border:'1px solid rgba(255,255,255,0.18)',
        flexWrap:'wrap', lineHeight:1.35,
      }}>
        <span style={{flexShrink:0}}>{label}</span>
        <span style={{fontWeight:400, opacity:0.9, wordBreak:'break-word'}}>{val}</span>
      </span>
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
        <div style={{display:'flex',flexDirection:'column',gap:2}}>
          {pill('R:', raci.r)}
          {pill('A:', raci.a)}
          {pill('C:', raci.c)}
          {pill('I:', raci.i)}
        </div>
      )}
      {hasOuts && decision_outcomes.split('|').map((o,idx)=>(
        <span key={idx} style={{fontSize:9,color:mutedC,display:'flex',gap:2,lineHeight:1.3}}>
          <span style={{color:textC}}>▸</span><span>{o.trim()}</span>
        </span>
      ))}
    </div>
  )
}

// ── NodeBox (regular process steps) ───────────────────────────────────────────
function NodeBox({ node, baseColor, level, isSelected, childCount, onClick, expandDir='down', boxRef }) {
  const fill  = bg(baseColor, level)
  const dark  = darkBg(baseColor, level)
  const textC = tc(level)
  const mutedC= mc(level)
  const w     = { L1:200, L2:185, L3:170, L4:160 }[level] ?? 170
  const isAI  = node.is_ai ?? node.raci?.r?.toUpperCase().includes('AI')

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
      </div>
      <p style={{fontSize:11,fontWeight:600,lineHeight:1.35,color:textC,margin:0}}>
        {node.name}
      </p>
      {node.description && (
        <p style={{fontSize:10,color:mutedC,margin:'3px 0 0',lineHeight:1.4}}>
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

// ── DiamondBox (decision nodes) ────────────────────────────────────────────────
const DIAG  = 164
const SIDE  = Math.round(DIAG / Math.SQRT2)
const INSET = Math.round((DIAG - SIDE) / 2)

function DiamondBox({ node, baseColor, level, isSelected, onClick, boxRef }) {
  const fill  = bg(baseColor, level)
  const dark  = darkBg(baseColor, level)
  const textC = tc(level)
  const mutedC= mc(level)
  const isAI  = node.is_ai ?? node.raci?.r?.toUpperCase().includes('AI')

  // Scale name font so long labels shrink to fit inside the diamond
  const nameLen = node.name?.length || 0
  const nameFontSize = nameLen < 18 ? 10 : nameLen < 28 ? 9 : nameLen < 40 ? 8 : 7

  // Clip-path that exactly matches the rotated inner square's diamond outline,
  // so no content can bleed into the transparent corner triangles.
  const clipDiamond =
    `polygon(50% ${(INSET/DIAG*100).toFixed(1)}%, ` +
    `${((DIAG-INSET)/DIAG*100).toFixed(1)}% 50%, ` +
    `50% ${((DIAG-INSET)/DIAG*100).toFixed(1)}%, ` +
    `${(INSET/DIAG*100).toFixed(1)}% 50%)`

  return (
    <div
      ref={boxRef}
      onClick={onClick}
      data-diamond="true"
      style={{ position:'relative', flexShrink:0, width:DIAG, height:DIAG,
        cursor: onClick ? 'pointer' : 'default', overflow:'visible' }}
    >
      {/* Rotated square = diamond */}
      <div style={{
        position:'absolute', top:INSET, left:INSET, width:SIDE, height:SIDE,
        transform:'rotate(45deg)', background:fill, border:`2px solid ${dark}`,
        boxShadow: isSelected
          ? `0 0 0 2px ${dark}, 0 4px 14px rgba(0,0,0,0.18)`
          : '0 1px 5px rgba(0,0,0,0.13)',
      }}/>

      {/* Content clipped to diamond shape — nothing can bleed outside */}
      <div style={{
        position:'absolute', inset:0,
        display:'flex', flexDirection:'column', alignItems:'center', justifyContent:'center',
        padding:`10px ${INSET+10}px`, textAlign:'center', gap:1,
        overflow:'hidden', clipPath: clipDiamond,
      }}>
        <div style={{display:'flex',alignItems:'center',gap:3,flexWrap:'wrap',justifyContent:'center'}}>
          <span style={{fontSize:9,fontFamily:'monospace',fontWeight:700,
            padding:'1px 4px',borderRadius:3,background:'rgba(0,0,0,0.22)',color:textC}}>
            {node.seq}
          </span>
          {isAI && <BotIcon color={textC} size={14}/>}
        </div>
        <p style={{fontSize:nameFontSize, fontWeight:700, color:textC, margin:0,
          lineHeight:1.2, wordBreak:'break-word', width:'100%'}}>
          {node.name}
        </p>
        {node.raci?.r && node.raci.r !== 'NA' && (
          <span style={{fontSize:7,color:mutedC,lineHeight:1.2,wordBreak:'break-word',width:'100%'}}>
            R: {node.raci.r}
          </span>
        )}
        {node.raci?.a && node.raci.a !== 'NA' && (
          <span style={{fontSize:7,color:mutedC,lineHeight:1.2,wordBreak:'break-word',width:'100%'}}>
            A: {node.raci.a}
          </span>
        )}
        {node.raci?.c && node.raci.c !== 'NA' && (
          <span style={{fontSize:7,color:mutedC,lineHeight:1.2,wordBreak:'break-word',width:'100%'}}>
            C: {node.raci.c}
          </span>
        )}
        {node.raci?.i && node.raci.i !== 'NA' && (
          <span style={{fontSize:7,color:mutedC,lineHeight:1.2,wordBreak:'break-word',width:'100%'}}>
            I: {node.raci.i}
          </span>
        )}
      </div>

    </div>
  )
}

// ── Down-arrow connector ───────────────────────────────────────────────────────
function DownArrow({ color, centerX, large = false }) {
  const pl = centerX !== undefined ? Math.max(0, centerX - 5) : 20
  const margin = large ? '14px 0' : '8px 0'
  return (
    <div style={{display:'flex',alignItems:'center',paddingLeft:pl,margin}}>
      <svg width="10" height="18" viewBox="0 0 10 18" fill="none">
        <line x1="5" y1="0" x2="5" y2="11" stroke={color} strokeWidth="1.5" strokeLinecap="round"/>
        <path d="M1 8l4 10 4-10" fill={color}/>
      </svg>
    </div>
  )
}

// ── Right-arrow connector ──────────────────────────────────────────────────────
function RightArrow({ color }) {
  return (
    <svg width="28" height="12" viewBox="0 0 28 12" fill="none" style={{flexShrink:0}}>
      <line x1="0" y1="6" x2="19" y2="6" stroke={color} strokeWidth="1.5" strokeLinecap="round"/>
      <path d="M16 2l12 4-12 4" fill={color}/>
    </svg>
  )
}

// ── Utilities ──────────────────────────────────────────────────────────────────
function getRole(node) {
  const r = node?.raci?.r
  return (r && r !== 'NA') ? r : 'Unassigned'
}

function buildRoleOrder(processes) {
  const order = new Map()
  const add = r => { if (r && !order.has(r)) order.set(r, order.size) }
  processes.forEach(proc => {
    proc.stages.forEach(st => {
      add(getRole(st))
      // Only L3 steps drive swimlane rows. L4 children's roles are shown inside
      // their process box but do NOT create separate swimlane rows.
      st.steps.forEach(s => { add(getRole(s)) })
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

// ── Main component ─────────────────────────────────────────────────────────────
export default function ProcessMap({ processes }) {
  const [expL1, setExpL1] = useState(new Set())
  const [expL2, setExpL2] = useState(new Set())
  const [expL3, setExpL3] = useState(new Set())

  const roleOrder = useMemo(() => buildRoleOrder(processes), [processes])

  function togL1(id) {
    const was = expL1.has(id)
    const proc = processes.find(p => p.id === id)
    setExpL1(p => { const n = new Set(p); was ? n.delete(id) : n.add(id); return n })
    if (proc) {
      if (was) {
        // Collapsing: remove all L2 stages and L3 steps under this L1
        setExpL2(p => { const n = new Set(p); proc.stages.forEach(s => n.delete(s.id)); return n })
        setExpL3(p => { const n = new Set(p); proc.stages.flatMap(s => s.steps).forEach(s => n.delete(s.seq)); return n })
      } else {
        // Expanding: also expand all L2 stages and L3 steps (including L4 children) under this L1
        setExpL2(p => { const n = new Set(p); proc.stages.forEach(s => n.add(s.id)); return n })
        setExpL3(p => { const n = new Set(p); proc.stages.flatMap(s => s.steps).forEach(s => n.add(s.seq)); return n })
      }
    }
  }
  function togL2(id) {
    const was = expL2.has(id)
    setExpL2(p => { const n = new Set(p); was ? n.delete(id) : n.add(id); return n })
    for (const proc of processes) {
      const st = proc.stages.find(s => s.id === id)
      if (st) {
        if (was) {
          // Collapsing: remove all L3 steps under this L2
          setExpL3(p => { const n = new Set(p); st.steps.forEach(s => n.delete(s.seq)); return n })
        } else {
          // Expanding: also expand all L3 steps (showing L4 children) under this L2
          setExpL3(p => { const n = new Set(p); st.steps.forEach(s => n.add(s.seq)); return n })
        }
        break
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
      system_tool: proc.system_tool, raci: proc.raci, step_type: null,
    }))
    return m
  }, [processes])

  // ── Column array ─────────────────────────────────────────────────────────────
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
                prevRole: si > 0             ? segs[si-1].role : null,
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

  function getCellItems(col, role) {
    const base = procColor(col.proc)
    const items = []

    if (col.type === 'L1') return items

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
      if (col.type==='L1') { /* collapsed */ }
      else if (col.type==='L2') { seen.add(getRole(col.stage)) }
      else {
        seen.add(getRole(col.stage))
        seen.add(col.seg.role)
        // L4 child roles are intentionally excluded — they appear inside their
        // L3 cell and their RACI is shown in the process box, not as swimlane rows.
      }
    })
    return Array.from(roleOrder.keys()).filter(r => seen.has(r))
  }, [columns, expL3, roleOrder, l1Nodes])

  // ── Arrow overlay refs ────────────────────────────────────────────────────────
  const scrollRef    = useRef(null)
  const gridRef      = useRef(null)
  const cellRefs     = useRef({})
  const boxFirstRefs = useRef({})
  const boxLastRefs  = useRef({})
  const seqBoxRefs   = useRef({})
  const [svgArrows, setSvgArrows] = useState([])
  const [svgSize,   setSvgSize]   = useState({ w: 2000, h: 2000 })

  const computeArrows = useCallback(() => {
    const scroll = scrollRef.current
    if (!scroll) return

    const scrollRect = scroll.getBoundingClientRect()
    const sl = scroll.scrollLeft
    const st = scroll.scrollTop

    const toC = rect => ({
      top:    rect.top    - scrollRect.top  + st,
      bottom: rect.bottom - scrollRect.top  + st,
      left:   rect.left   - scrollRect.left + sl,
      right:  rect.right  - scrollRect.left + sl,
      cy:     rect.top    - scrollRect.top  + st + rect.height / 2,
    })

    const arrs = []
    const decisionCols = new Set()

    // ── Pass 1: decision YES / NO outgoing arrows ────────────────────────────
    columns.forEach((col, ci) => {
      if (col.type !== 'SEG') return
      const steps = col.seg.steps
      if (!steps.length) return
      const col_color = procColor(col.proc)

      // Draw arrows from a decision node (L3 or L4)
      //   YES (oi=0): target below → exit BOTTOM → arrive top-center (straight down)
      //   NO  (oi=1): target right → exit RIGHT → route via column right edge → no box crossing
      //   Long-distance right-exit: arch ABOVE the row
      function drawDecisionArrows(decNode) {
        const fromEl = seqBoxRefs.current[decNode.seq]
        if (!fromEl) return false
        const fr = toC(fromEl.getBoundingClientRect())
        let anyDrawn = false

        // Source cell geometry for routing lanes
        const srcCellEl = cellRefs.current[`${ci}_${col.seg.role}`]
        const srcCellRect = srcCellEl ? toC(srcCellEl.getBoundingClientRect()) : null
        const srcCellTop   = srcCellRect ? srcCellRect.top   : fr.top
        const srcCellRight = srcCellRect ? srcCellRect.right : fr.right + 20
        const srcCellLeft  = srcCellRect ? srcCellRect.left  : fr.left - 20

        // Parse all targets first so we can compare positions
        const targets = decNode.decision_outcomes.split('|').map(o => o.trim()).map((out, oi) => {
          const m = out.match(/proceed to\s+(.+)/i)
          if (!m) return null
          const targetSeq = m[1].trim()
          const toEl = seqBoxRefs.current[targetSeq]
          if (!toEl) return null
          return { oi, out, targetSeq, toEl, tr: toC(toEl.getBoundingClientRect()) }
        }).filter(Boolean)

        const srcCellBottom = srcCellRect ? srcCellRect.bottom : fr.bottom + 20

        // checkBackward: target is left of diamond OR same column but above diamond
        const checkBackward = (tr) =>
          tr.left < fr.left - 5 ||
          (Math.abs(tr.left - fr.left) < DIAG && tr.top < fr.top - 5)

        // seqAfter: is targetSeq numerically later than sourceSeq?
        const seqAfter = (tSeq, sSeq) => {
          const t = tSeq.split('.').map(Number), s = sSeq.split('.').map(Number)
          for (let i = 0; i < Math.min(t.length, s.length); i++) {
            if (t[i] !== s[i]) return t[i] > s[i]
          }
          return t.length > s.length
        }

        targets.forEach((t, ti) => {
          const { oi, out, tr } = t
          const isYes = out.trim().toLowerCase().startsWith('yes')
          const isBackward = checkBackward(tr)
          const fromBottom = isYes && !isBackward

          let x1 = fromBottom ? fr.left + DIAG / 2 : fr.right
          let y1 = fromBottom ? fr.bottom           : fr.cy
          let usesBottomExit = fromBottom

          let x2, y2, isArch, aboveY, belowY, forwardBelowY, routeRight, routeLeft, arrowDir

          // Separate routing corridors for YES vs NO so their paths never overlap.
          // YES travels OUTSIDE the source cell (in the inter-column gap):
          //   rightCorridor = srcCellRight + 8  (in adjacent cell's left padding)
          //   leftCorridor  = srcCellLeft  - 6  (in adjacent cell's right padding)
          // NO travels INSIDE the source cell's own padding (between cell edge and diamond):
          //   rightCorridor = srcCellRight - 5  (in source cell's right padding, fr.right+5)
          //   leftCorridor  = srcCellLeft  + 4  (in source cell's left padding, fr.left-6)
          // Both zones are free of box content so neither path can cut through a box.
          const rRight = isYes ? srcCellRight + 8  : srcCellRight - 5
          const rLeft  = isYes ? srcCellLeft  - 6  : srcCellLeft  + 4
          // YES side-exits start 8px above the diamond vertex so YES and NO never share
          // an identical start point when both are routed to the same side.
          const sideY  = isYes ? fr.cy - 8 : fr.cy

          if (fromBottom) {
            const isL3Dec = decNode.seq.split('.').length === 3
            const crossesRow = isL3Dec && srcCellRect != null &&
              (tr.top > srcCellBottom + 5 || tr.bottom < srcCellTop - 5)
            if (tr.left > fr.right) {
              x1 = fr.right; y1 = sideY; usesBottomExit = false
              x2 = tr.left; y2 = tr.cy; arrowDir = 'right'
              if (tr.left > srcCellRight + 40) {
                const candAY = Math.min(srcCellTop, tr.top) - 8
                if (candAY >= 54) { // 54 = headerH(44)+10: safe above header
                  isArch = true; aboveY = candAY
                } else { // arch would be hidden under sticky header — route below cells
                  forwardBelowY = Math.max(srcCellBottom, tr.bottom) + 8
                }
              }
            } else if (crossesRow) {
              x1 = fr.left; y1 = sideY; usesBottomExit = false
              x2 = tr.left; y2 = tr.cy
              routeLeft = rLeft; arrowDir = 'right'
            } else {
              x2 = tr.right; y2 = tr.cy
              routeRight = rRight; arrowDir = 'left'
            }
          } else if (isBackward) {
            const sameColBackward = Math.abs(tr.left - fr.left) < DIAG
            if (sameColBackward) {
              const otherTarget = targets.find((_, i) => i !== ti)
              const otherFarRight = otherTarget && otherTarget.tr.left > fr.right
              if (otherFarRight || seqAfter(t.targetSeq, decNode.seq)) {
                x1 = fr.left; y1 = sideY
                x2 = tr.left; y2 = tr.cy
                routeLeft = rLeft; arrowDir = 'right'
              } else {
                x1 = fr.right; y1 = sideY
                x2 = tr.right; y2 = tr.cy
                routeRight = rRight; arrowDir = 'left'
              }
            } else {
              // Target is in a different column to the LEFT.
              // Exit LEFT vertex so the arrow's first move visually points backward,
              // not rightward off-screen (which confused users into thinking it was a
              // forward route going out of view).
              x1 = fr.left; y1 = sideY
              x2 = tr.right; y2 = tr.cy
              belowY = isYes
                ? Math.max(srcCellBottom, tr.bottom) + 6
                : Math.max(srcCellBottom, tr.bottom) + 10
              routeLeft = rLeft; arrowDir = 'left'
            }
          } else if (tr.left > fr.right) {
            x2 = tr.left; y2 = tr.cy; arrowDir = 'right'
            if (tr.left > srcCellRight + 40) {
              const candAY = Math.min(srcCellTop, tr.top) - 22
              if (candAY >= 54) {
                isArch = true; aboveY = candAY
              } else {
                forwardBelowY = Math.max(srcCellBottom, tr.bottom) + 12
              }
            }
          } else if (tr.top > fr.bottom) {
            const isL4Dec = decNode.seq.split('.').length === 4
            if (isL4Dec) {
              x1 = fr.left; y1 = fr.cy
              x2 = tr.left; y2 = tr.cy
              routeLeft = rLeft; arrowDir = 'right'
            } else {
              x2 = tr.right; y2 = tr.cy
              routeRight = rRight; arrowDir = 'left'
            }
          } else {
            x2 = tr.right; y2 = tr.cy
            routeRight = rRight; arrowDir = 'left'
          }

          arrs.push({ x1, y1, x2, y2, midX: (x1 + x2) / 2, color: col_color,
            id: `dec_${decNode.seq}_${oi}`,
            label: isYes ? 'YES' : 'NO',
            fromBottom: usesBottomExit, arch: isArch, aboveY, belowY, forwardBelowY, routeRight, routeLeft, arrowDir })
          anyDrawn = true
        })
        return anyDrawn
      }

      // L3 decisions: any step in the SEG column, not just the last
      steps.forEach(step => {
        if (step.step_type === 'Decision' && step.decision_outcomes
            && !(expL3.has(step.seq) && step.children?.length)) {
          if (drawDecisionArrows(step)) decisionCols.add(ci)
        }
      })

      // L4 decisions: inside expanded L3 steps
      steps.forEach(step => {
        if (!expL3.has(step.seq) || !step.children) return
        step.children.forEach(child => {
          if (child.step_type === 'Decision' && child.decision_outcomes) {
            drawDecisionArrows(child)
          }
        })
      })
    })

    // ── Pass 2: regular column-to-column flow arrows ─────────────────────────
    columns.forEach((col, ci) => {
      if (col.type === 'L1') return
      if (decisionCols.has(ci)) return

      const nextCol = columns[ci + 1]
      if (!nextCol || nextCol.type === 'L1') return
      if (col.proc.id !== nextCol.proc.id) return

      const fromRole = col.type === 'L2' ? getRole(col.stage) : col.seg.role
      const toRole   = nextCol.type === 'L2' ? getRole(nextCol.stage) : nextCol.seg.role

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

      // If target is a decision diamond, connect to its TOP point
      const toDiamond = toEl.dataset?.diamond === 'true'
      const x1   = fr.right
      const y1   = fr.cy
      const x2   = toDiamond ? (tr.left + tr.right) / 2 : tr.left
      const y2   = toDiamond ? tr.top                    : tr.cy

      arrs.push({ x1, y1, x2, y2, midX: (x1 + x2) / 2,
        color: procColor(col.proc),
        id: `${col.id}_to_${ci+1}`,
        arrowDir: toDiamond ? 'down' : 'right' })
    })

    const grid = gridRef.current
    if (grid) setSvgSize({ w: grid.scrollWidth, h: grid.scrollHeight })
    setSvgArrows(arrs)
  }, [columns, expL3])

  useEffect(() => {
    const raf = requestAnimationFrame(() => computeArrows())
    return () => cancelAnimationFrame(raf)
  }, [computeArrows, expL1, expL2, expL3, visibleRoles])

  const gtc = `${ROLE_W}px ${columns.map(()=>'max-content').join(' ')}`

  return (
    <div ref={scrollRef}
      style={{ height:'100%', overflow:'auto', background:'#f1f5f9', position:'relative' }}>

      {/* ── Grid ──────────────────────────────────────────────────────────────── */}
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
                          const prevIsDecision = ii > 0 && items[ii-1]?.node.step_type?.toLowerCase() === 'decision'
                          const BoxComp = isDecision ? DiamondBox : NodeBox
                          const cellKey = `${ci}_${role}`
                          const isFirstBox = ii === 0
                          const isLastBox  = ii === items.length - 1
                          return (
                            <React.Fragment key={`${item.node.seq??item.node.id}_${ii}`}>
                              {ii > 0 && !prevIsDecision && (
                                <DownArrow
                                  color={mixWhite(item.base, 0.22)}
                                  centerX={isDecision ? DIAG/2 : undefined}
                                  large={isDecision}
                                />
                              )}
                              {ii > 0 && prevIsDecision && (
                                <div style={{height: 20}} />
                              )}
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
                                  seqBoxRefs.current[item.node.seq] = el
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

      {/* ── SVG arrow overlay ─────────────────────────────────────────────────── */}
      <svg
        style={{
          position:'absolute', top:0, left:0,
          width: svgSize.w, height: svgSize.h,
          pointerEvents:'none', overflow:'visible', zIndex:20,
        }}
        width={svgSize.w} height={svgSize.h}>
        {svgArrows.map(a => {
          const arrowColor = mixWhite(a.color, 0.15)
          const AH = 5
          let d, labelX, labelY

          if (a.forwardBelowY != null) {
            // Forward-right path going BELOW all cells — used when the above-arch would
            // travel through the sticky header row and be hidden behind it (z-index:30).
            // Route: exit right of diamond → down past all rows → right to target → up to target.
            const bY = a.forwardBelowY
            d = `M${a.x1},${a.y1} L${a.x1+16},${a.y1} L${a.x1+16},${bY} L${a.x2-15},${bY} L${a.x2-15},${a.y2} L${a.x2},${a.y2}`
            labelX = a.midX
            labelY = bY + 10
          } else if (a.arch) {
            // Long right-exit: arch above the row, arrive at left side with horizontal approach
            const ay = a.aboveY ?? Math.min(a.y1, a.y2) - 12
            const approachX = a.x2 - 15  // 15px horizontal run before arrowhead
            d = `M${a.x1},${a.y1} L${a.x1},${ay} L${approachX},${ay} L${approachX},${a.y2} L${a.x2},${a.y2}`
            labelX = (a.x1 + approachX) / 2
            labelY = ay - 4
          } else if (a.fromBottom) {
            if (a.routeRight != null) {
              // YES exits bottom → routes down right column gap → arrives at target right edge.
              // This guarantees no intermediate boxes are crossed regardless of how many
              // steps sit between the diamond and its YES target.
              d = `M${a.x1},${a.y1} L${a.routeRight},${a.y1} L${a.routeRight},${a.y2} L${a.x2},${a.y2}`
              labelX = (a.x1 + a.routeRight) / 2
              labelY = a.y1 + 14
            } else {
              // Fallback straight-down (only reached if fromBottom is set via an override path)
              const dx = Math.abs(a.x2 - a.x1)
              if (dx < 15) {
                d = `M${a.x1},${a.y1} L${a.x2},${a.y2}`
              } else {
                const midY = (a.y1 + a.y2) / 2
                d = `M${a.x1},${a.y1} L${a.x1},${midY} L${a.x2},${midY} L${a.x2},${a.y2}`
              }
              labelX = (a.x1 + a.x2) / 2
              labelY = a.y1 + 16
            }
          } else if (a.belowY != null) {
            // Backward-to-left-column: exit left (or right) → drop below all rows → left to target → up → arrive right side
            // routeLeft is preferred (exits LEFT vertex, arrow direction is visually "going backward")
            // routeRight is the legacy fallback
            const approachX = a.x2 + 15
            const corridor = a.routeLeft != null ? a.routeLeft : a.routeRight
            d = `M${a.x1},${a.y1} L${corridor},${a.y1} L${corridor},${a.belowY} L${approachX},${a.belowY} L${approachX},${a.y2} L${a.x2},${a.y2}`
            labelX = (a.x1 + corridor) / 2
            labelY = a.y1 - 6
          } else if (a.routeRight != null) {
            // Same-column right-exit: right to gap → down → left to target right side
            d = `M${a.x1},${a.y1} L${a.routeRight},${a.y1} L${a.routeRight},${a.y2} L${a.x2},${a.y2}`
            labelX = (a.x1 + a.routeRight) / 2
            labelY = a.y1 - 6
          } else if (a.routeLeft != null) {
            // Left-exit: exit left vertex → outside left margin → down → right to target left face
            d = `M${a.x1},${a.y1} L${a.routeLeft},${a.y1} L${a.routeLeft},${a.y2} L${a.x2},${a.y2}`
            labelX = (a.x1 + a.routeLeft) / 2
            labelY = a.y1 - 6
          } else {
            // Regular flow arrow: L-shape through midpoint gap between columns
            d = `M${a.x1},${a.y1} L${a.midX},${a.y1} L${a.midX},${a.y2} L${a.x2},${a.y2}`
            labelX = a.midX
            labelY = Math.min(a.y1, a.y2) - 4
          }

          // Arrowhead direction
          let ah
          if (a.arrowDir === 'down') {
            ah = `M${a.x2-AH},${a.y2-AH} L${a.x2},${a.y2} L${a.x2+AH},${a.y2-AH}`
          } else if (a.arrowDir === 'left') {
            ah = `M${a.x2+AH},${a.y2-AH} L${a.x2},${a.y2} L${a.x2+AH},${a.y2+AH}`
          } else {  // 'right'
            ah = `M${a.x2-AH},${a.y2-AH} L${a.x2},${a.y2} L${a.x2-AH},${a.y2+AH}`
          }

          return (
            <g key={a.id}>
              <path d={d} fill="none" stroke="rgba(255,255,255,0.7)" strokeWidth="3.5"
                strokeLinecap="square" strokeLinejoin="miter"/>
              <path d={d} fill="none" stroke={arrowColor} strokeWidth="1.5"
                strokeLinecap="square" strokeLinejoin="miter"/>
              <path d={ah} fill="none" stroke={arrowColor} strokeWidth="1.5"
                strokeLinecap="round" strokeLinejoin="round"/>
              {a.label && (
                <text x={labelX} y={labelY} fontSize="8" fill={arrowColor}
                  textAnchor="middle" fontWeight="700"
                  style={{fontFamily:'system-ui,sans-serif'}}>{a.label}</text>
              )}
            </g>
          )
        })}
      </svg>
    </div>
  )
}
