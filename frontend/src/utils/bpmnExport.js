// ── BPMN 2.0 XML export ───────────────────────────────────────────────────────
// Produces a valid BPMN 2.0 XML file with:
//   • One pool / process per L1
//   • One horizontal lane per L2 stage
//   • L3 steps as bpmn:task / bpmn:exclusiveGateway / bpmn:subProcess
//   • L4 children nested inside collapsed bpmn:subProcess
//   • RACI, system/tool and key data encoded in bpmn:documentation
//   • BPMNDiagram section with approximate layout coordinates

// ── helpers ───────────────────────────────────────────────────────────────────
function esc(s) {
  if (s == null) return ''
  return String(s)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&apos;')
}

function sid(seq) {
  // "1.1.4" → "1_1_4"
  return String(seq).replace(/\./g, '_')
}

function stepTag(step) {
  if (step.children?.length > 0)             return 'subProcess'
  if (step.step_type?.toLowerCase().includes('decision')) return 'exclusiveGateway'
  return 'task'
}

function elemId(step) {
  const tag = stepTag(step)
  if (tag === 'subProcess')        return `Sub_${sid(step.seq)}`
  if (tag === 'exclusiveGateway')  return `Gw_${sid(step.seq)}`
  return `Task_${sid(step.seq)}`
}

function docText(step) {
  const parts = []
  if (step.description)                        parts.push(step.description)
  if (step.system_tool && step.system_tool !== 'NA')
    parts.push(`System/Tool: ${step.system_tool}`)
  if (step.raci) {
    const { r, a, c, i } = step.raci
    const raci = [
      r && r !== 'NA' ? `R:${r}` : null,
      a && a !== 'NA' ? `A:${a}` : null,
      c && c !== 'NA' ? `C:${c}` : null,
      i && i !== 'NA' ? `I:${i}` : null,
    ].filter(Boolean)
    if (raci.length) parts.push(`RACI [${raci.join(', ')}]`)
  }
  if (step.key_data_points && step.key_data_points !== 'NA')
    parts.push(`Data: ${step.key_data_points}`)
  if (step.change_highlight)
    parts.push(`Change: ${step.change_highlight}`)
  return parts.join(' | ')
}

// ── layout constants ──────────────────────────────────────────────────────────
const TASK_W   = 100
const TASK_H   = 80
const GW_SIZE  = 50
const EVT_SIZE = 36
const SUB_W    = 120
const SUB_H    = 80
const H_GAP    = 50   // gap between elements
const LANE_H   = 180
const MARGIN_X = 60   // left margin inside lane (after lane label)
const MARGIN_Y = 20   // top margin inside lane

function elemDims(step) {
  if (!step) return { w: EVT_SIZE, h: EVT_SIZE }  // start/end event
  const tag = stepTag(step)
  if (tag === 'exclusiveGateway') return { w: GW_SIZE, h: GW_SIZE }
  if (tag === 'subProcess')       return { w: SUB_W,   h: SUB_H   }
  return { w: TASK_W, h: TASK_H }
}

// ── core generator ────────────────────────────────────────────────────────────
export function generateBPMN(data) {
  const L = []          // XML lines
  const diShapes = []   // BPMNDiagram shapes
  const diEdges  = []   // BPMNDiagram edges

  const processId = `Proc_${esc(data.l1_name).replace(/\W+/g, '_')}`

  // ── Definitions header ────────────────────────────────────
  L.push('<?xml version="1.0" encoding="UTF-8"?>')
  L.push('<bpmn:definitions')
  L.push('  xmlns:bpmn="http://www.omg.org/spec/BPMN/20100524/MODEL"')
  L.push('  xmlns:bpmndi="http://www.omg.org/spec/BPMN/20100524/DI"')
  L.push('  xmlns:dc="http://www.omg.org/spec/DD/20100524/DC"')
  L.push('  xmlns:di="http://www.omg.org/spec/DD/20100524/DI"')
  L.push('  id="Definitions_OTC"')
  L.push('  targetNamespace="http://inzio.com/bpmn/otc-process"')
  L.push('  exporter="Inzio OTC Process Explorer">')
  L.push('')

  // ── Process ───────────────────────────────────────────────
  L.push(`  <bpmn:process id="${processId}" name="${esc(data.l1_name)}" isExecutable="false">`)
  L.push('')

  // ── LaneSet ───────────────────────────────────────────────
  L.push('    <bpmn:laneSet id="LaneSet_1">')
  data.stages.forEach(stage => {
    const laneId = `Lane_${stage.id.replace(/-/g, '_')}`
    L.push(`      <bpmn:lane id="${laneId}" name="${esc(stage.name)}">`)
    L.push(`        <bpmn:flowNodeRef>Start_${stage.id.replace(/-/g, '_')}</bpmn:flowNodeRef>`)
    stage.steps.forEach(step => L.push(`        <bpmn:flowNodeRef>${elemId(step)}</bpmn:flowNodeRef>`))
    L.push(`        <bpmn:flowNodeRef>End_${stage.id.replace(/-/g, '_')}</bpmn:flowNodeRef>`)
    L.push(`      </bpmn:lane>`)
  })
  L.push('    </bpmn:laneSet>')
  L.push('')

  // ── Per-stage flow elements + sequence flows ──────────────
  // Pass 1: calculate max total width so all lanes are the same width
  let maxLaneContentW = 0
  data.stages.forEach(stage => {
    let x = MARGIN_X
    x += EVT_SIZE + H_GAP  // start event
    stage.steps.forEach(step => {
      const { w } = elemDims(step)
      x += w + H_GAP
    })
    x += EVT_SIZE  // end event
    if (x > maxLaneContentW) maxLaneContentW = x
  })
  const LANE_W = maxLaneContentW + 40  // padding

  data.stages.forEach((stage, stageIdx) => {
    const stId     = stage.id.replace(/-/g, '_')
    const startId  = `Start_${stId}`
    const endId    = `End_${stId}`
    const laneY    = stageIdx * LANE_H

    L.push(`    <!-- ═══ Stage ${esc(stage.seq)}: ${esc(stage.name)} ═══ -->`)

    // Build ordered element list for this lane
    const elems = [
      { id: startId, tag: 'startEvent', name: 'Start', ...{ w: EVT_SIZE, h: EVT_SIZE } },
      ...stage.steps.map(step => ({
        id: elemId(step), tag: stepTag(step), name: step.name, step,
        ...elemDims(step),
      })),
      { id: endId, tag: 'endEvent', name: 'End', ...{ w: EVT_SIZE, h: EVT_SIZE } },
    ]

    // Assign X positions
    let curX = MARGIN_X
    elems.forEach(el => {
      el.x = curX
      el.y = laneY + MARGIN_Y + (LANE_H - 2 * MARGIN_Y - el.h) / 2
      curX += el.w + H_GAP
    })

    // Emit flow nodes
    elems.forEach((el, idx) => {
      const inSF  = idx > 0             ? `SF_${elems[idx - 1].id}_${el.id}` : null
      const outSF = idx < elems.length - 1 ? `SF_${el.id}_${elems[idx + 1].id}` : null

      if (el.tag === 'startEvent') {
        L.push(`    <bpmn:startEvent id="${el.id}" name="${esc(el.name)}">`)
        if (outSF) L.push(`      <bpmn:outgoing>${outSF}</bpmn:outgoing>`)
        L.push(`    </bpmn:startEvent>`)

      } else if (el.tag === 'endEvent') {
        L.push(`    <bpmn:endEvent id="${el.id}" name="${esc(el.name)}">`)
        if (inSF) L.push(`      <bpmn:incoming>${inSF}</bpmn:incoming>`)
        L.push(`    </bpmn:endEvent>`)

      } else if (el.tag === 'exclusiveGateway') {
        L.push(`    <bpmn:exclusiveGateway id="${el.id}" name="${esc(el.name)}" gatewayDirection="Diverging">`)
        const doc = docText(el.step)
        if (doc) L.push(`      <bpmn:documentation>${esc(doc)}</bpmn:documentation>`)
        if (inSF)  L.push(`      <bpmn:incoming>${inSF}</bpmn:incoming>`)
        if (outSF) L.push(`      <bpmn:outgoing>${outSF}</bpmn:outgoing>`)
        L.push(`    </bpmn:exclusiveGateway>`)

      } else if (el.tag === 'subProcess') {
        // Collapsed subprocess; children are fully described inside
        L.push(`    <bpmn:subProcess id="${el.id}" name="${esc(el.name)}">`)
        const doc = docText(el.step)
        if (doc) L.push(`      <bpmn:documentation>${esc(doc)}</bpmn:documentation>`)
        if (inSF)  L.push(`      <bpmn:incoming>${inSF}</bpmn:incoming>`)
        if (outSF) L.push(`      <bpmn:outgoing>${outSF}</bpmn:outgoing>`)

        // Internal start/end + child tasks
        const cStartId = `SubStart_${sid(el.step.seq)}`
        const cEndId   = `SubEnd_${sid(el.step.seq)}`
        const children = el.step.children

        L.push(`      <bpmn:startEvent id="${cStartId}" name="Start">`)
        if (children.length > 0)
          L.push(`        <bpmn:outgoing>cSF_${cStartId}_Task_${sid(children[0].seq)}</bpmn:outgoing>`)
        L.push(`      </bpmn:startEvent>`)

        children.forEach((child, ci) => {
          const cId    = `Task_${sid(child.seq)}`
          const cInSF  = ci === 0
            ? `cSF_${cStartId}_${cId}`
            : `cSF_Task_${sid(children[ci - 1].seq)}_${cId}`
          const cOutSF = ci === children.length - 1
            ? `cSF_${cId}_${cEndId}`
            : `cSF_${cId}_Task_${sid(children[ci + 1].seq)}`
          const cDoc = docText(child)
          L.push(`      <bpmn:task id="${cId}" name="${esc(child.name)}">`)
          if (cDoc) L.push(`        <bpmn:documentation>${esc(cDoc)}</bpmn:documentation>`)
          L.push(`        <bpmn:incoming>${cInSF}</bpmn:incoming>`)
          L.push(`        <bpmn:outgoing>${cOutSF}</bpmn:outgoing>`)
          L.push(`      </bpmn:task>`)
        })

        L.push(`      <bpmn:endEvent id="${cEndId}" name="End">`)
        if (children.length > 0)
          L.push(`        <bpmn:incoming>cSF_Task_${sid(children[children.length - 1].seq)}_${cEndId}</bpmn:incoming>`)
        L.push(`      </bpmn:endEvent>`)

        // Child sequence flows
        if (children.length > 0) {
          const firstCId = `Task_${sid(children[0].seq)}`
          L.push(`      <bpmn:sequenceFlow id="cSF_${cStartId}_${firstCId}" sourceRef="${cStartId}" targetRef="${firstCId}" />`)
          children.forEach((child, ci) => {
            if (ci < children.length - 1) {
              const from = `Task_${sid(child.seq)}`
              const to   = `Task_${sid(children[ci + 1].seq)}`
              L.push(`      <bpmn:sequenceFlow id="cSF_${from}_${to}" sourceRef="${from}" targetRef="${to}" />`)
            }
          })
          const lastCId = `Task_${sid(children[children.length - 1].seq)}`
          L.push(`      <bpmn:sequenceFlow id="cSF_${lastCId}_${cEndId}" sourceRef="${lastCId}" targetRef="${cEndId}" />`)
        }
        L.push(`    </bpmn:subProcess>`)

      } else {
        // Regular task
        L.push(`    <bpmn:task id="${el.id}" name="${esc(el.name)}">`)
        const doc = docText(el.step)
        if (doc) L.push(`      <bpmn:documentation>${esc(doc)}</bpmn:documentation>`)
        if (inSF)  L.push(`      <bpmn:incoming>${inSF}</bpmn:incoming>`)
        if (outSF) L.push(`      <bpmn:outgoing>${outSF}</bpmn:outgoing>`)
        L.push(`    </bpmn:task>`)
      }

      // DI shape (collapsed subProcess or leaf node)
      diShapes.push({
        id: el.id,
        x: el.x,
        y: el.y,
        w: el.w,
        h: el.h,
        isExpanded: false,
        isMarker: el.tag === 'startEvent' || el.tag === 'endEvent',
      })
    })

    // Sequence flows
    L.push('')
    elems.forEach((el, idx) => {
      if (idx < elems.length - 1) {
        const sfId = `SF_${el.id}_${elems[idx + 1].id}`
        L.push(`    <bpmn:sequenceFlow id="${sfId}" sourceRef="${el.id}" targetRef="${elems[idx + 1].id}" />`)
        diEdges.push({
          id: sfId,
          x1: Math.round(el.x + el.w),
          y1: Math.round(el.y + el.h / 2),
          x2: Math.round(elems[idx + 1].x),
          y2: Math.round(elems[idx + 1].y + elems[idx + 1].h / 2),
        })
      }
    })
    L.push('')
  })

  L.push('  </bpmn:process>')
  L.push('')

  // ── BPMNDiagram ───────────────────────────────────────────
  L.push('  <bpmndi:BPMNDiagram id="BPMNDiagram_1">')
  L.push(`    <bpmndi:BPMNPlane id="BPMNPlane_1" bpmnElement="${processId}">`)

  // Lane shapes
  data.stages.forEach((stage, stageIdx) => {
    const stId  = stage.id.replace(/-/g, '_')
    const laneY = stageIdx * LANE_H
    L.push(`      <bpmndi:BPMNShape id="Lane_${stId}_di" bpmnElement="Lane_${stId}" isHorizontal="true">`)
    L.push(`        <dc:Bounds x="30" y="${laneY}" width="${LANE_W}" height="${LANE_H}" />`)
    L.push(`      </bpmndi:BPMNShape>`)
  })

  // Element shapes
  diShapes.forEach(s => {
    L.push(`      <bpmndi:BPMNShape id="${s.id}_di" bpmnElement="${s.id}">`)
    L.push(`        <dc:Bounds x="${Math.round(s.x)}" y="${Math.round(s.y)}" width="${s.w}" height="${s.h}" />`)
    L.push(`      </bpmndi:BPMNShape>`)
  })

  // Edges
  diEdges.forEach(e => {
    L.push(`      <bpmndi:BPMNEdge id="${e.id}_di" bpmnElement="${e.id}">`)
    L.push(`        <di:waypoint x="${e.x1}" y="${e.y1}" />`)
    L.push(`        <di:waypoint x="${e.x2}" y="${e.y2}" />`)
    L.push(`      </bpmndi:BPMNEdge>`)
  })

  L.push('    </bpmndi:BPMNPlane>')
  L.push('  </bpmndi:BPMNDiagram>')
  L.push('')
  L.push('</bpmn:definitions>')

  return L.join('\n')
}

// ── Trigger browser download ───────────────────────────────────────────────────
export function downloadBPMN(data) {
  const xml  = generateBPMN(data)
  const blob = new Blob([xml], { type: 'application/xml;charset=utf-8' })
  const url  = URL.createObjectURL(blob)
  const a    = document.createElement('a')
  a.href     = url
  a.download = `${data.l1_name.replace(/\s+/g, '_')}_BPMN2.xml`
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(a)
  URL.revokeObjectURL(url)
}
