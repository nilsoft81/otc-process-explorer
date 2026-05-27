"""Generate data/processes.py from Detailed Process Flows_v1.xlsx (Process Design tab).

Layout:
  Row 5 (idx 4): main headers
  Row 6 (idx 5): sub-headers
  Row 7+ (idx 6+): data

Column indices (0-based):
  A=0  AI Agent?
  B=1  System / Tool
  C=2  Level (L1-L4)
  D=3  Step Number
  E=4  Step Name
  F=5  Step Description
  G=6  Step Type
  H=7  Automated?
  Q=16 RACI – Responsible (R)
  R=17 RACI – Accountable (A)
  S=18 RACI – Contributing / Informed (I)
"""
import openpyxl, re, os

wb = openpyxl.load_workbook('Detailed Process Flows_v3.xlsx', data_only=True)
ws = wb['Process Design']
all_rows = list(ws.iter_rows(values_only=True))

C_AI, C_SYS, C_LVL, C_SEQ, C_NAME = 0, 1, 2, 3, 4
C_DESC, C_TYPE, C_AUTO = 5, 6, 7
C_R, C_A, C_I = 16, 17, 18

DATA_START = 6  # row 7 (0-indexed)


def v(row, col):
    if col >= len(row): return ''
    val = row[col]
    s = str(val).strip() if val is not None else ''
    return s.replace('–', '-').replace('—', '-').replace('‘', "'").replace('→', '->')


def esc(s):
    return s.replace('\\', '\\\\').replace('"', '\\"').replace('\n', ' ').replace('\r', ' ')


def parse_step_type(raw):
    if not raw:
        return 'Process', ''
    lines = [l.strip() for l in raw.split('\n') if l.strip()]
    if not lines:
        return 'Process', ''
    first = lines[0]
    is_dec = ('decision' in first.lower()
              or any(re.match(r'if\s+(yes|no)', l, re.I) for l in lines))
    if is_dec:
        outcomes = []
        for line in lines[1:]:
            m = re.match(r'If\s+(yes|no)[,.]?\s+(?:proceed to|return to)\s+(.+)', line, re.I)
            if m:
                target = m.group(2).strip().rstrip('.')
                target = re.sub(r'^step\s+', '', target, flags=re.I).strip()
                outcomes.append(m.group(1).capitalize() + ' - proceed to ' + target)
            elif re.match(r'if\s+(yes|no)', line, re.I):
                cleaned = re.sub(r'^if\s+', '', line, flags=re.I)
                outcomes.append(cleaned)
        return 'Decision', ' | '.join(outcomes)
    if 'start' in first.lower():
        return 'Start', ''
    return 'Process', ''


# Parse all data rows
rows_data = []
for raw in all_rows[DATA_START:]:
    lvl = v(raw, C_LVL)
    seq = v(raw, C_SEQ)
    name = v(raw, C_NAME)
    if not seq or not name:
        continue
    if not re.match(r'^\d[\d.]*$', seq):
        continue
    dots = seq.count('.')
    depth_lvl = {0: 'L1', 1: 'L2', 2: 'L3', 3: 'L4'}.get(dots)
    if depth_lvl is None:
        continue
    lvl = depth_lvl

    raw_type = v(raw, C_TYPE)
    step_type, outcomes = parse_step_type(raw_type)
    r_val = v(raw, C_R)
    a_val = v(raw, C_A)
    i_val = v(raw, C_I)

    if 'automated' in r_val.lower() and step_type == 'Process':
        step_type = 'Automated'

    ai_flag = v(raw, C_AI)
    is_ai = (bool(ai_flag) and ai_flag.lower() not in ('', 'n', 'no', 'none', 'future opportunity')) \
            or 'AI Agent' in r_val

    rows_data.append({
        'lvl': lvl, 'seq': seq, 'name': name,
        'desc': v(raw, C_DESC), 'step_type': step_type, 'outcomes': outcomes,
        'sys': v(raw, C_SYS), 'r': r_val, 'a': a_val, 'i': i_val,
        'is_ai': is_ai,
    })

# Inject synthetic L3 parents for orphaned L4s
l3_seqs = {r['seq'] for r in rows_data if r['lvl'] == 'L3'}
orphan_parents_added = set()
extra = []
for r in rows_data:
    if r['lvl'] == 'L4':
        parent = '.'.join(r['seq'].split('.')[:3])
        if parent not in l3_seqs and parent not in orphan_parents_added:
            orphan_parents_added.add(parent)
            extra.append({
                'lvl': 'L3', 'seq': parent, 'name': 'Approval & Sign-off',
                'desc': '', 'step_type': 'Process', 'outcomes': '',
                'sys': r['sys'], 'r': r['r'], 'a': r['a'], 'i': r['i'],
                'is_ai': False,
            })
rows_data.extend(extra)
rows_data.sort(key=lambda r: [int(x) for x in r['seq'].split('.')] + [0] * (4 - r['seq'].count('.') - 1))

# Build hierarchy dicts
l1_map = {}
l2_map = {}
l3_map = {}

for r in rows_data:
    seq = r['seq']
    if r['lvl'] == 'L1':
        rec = dict(r, stages=[])
        l1_map[seq] = rec
    elif r['lvl'] == 'L2':
        l1_key = seq.split('.')[0]
        rec = dict(r, steps=[])
        l2_map[seq] = rec
        if l1_key in l1_map:
            l1_map[l1_key]['stages'].append(rec)
    elif r['lvl'] == 'L3':
        l2_key = '.'.join(seq.split('.')[:2])
        rec = dict(r, children=[])
        l3_map[seq] = rec
        if l2_key in l2_map:
            l2_map[l2_key]['steps'].append(rec)
    elif r['lvl'] == 'L4':
        l3_key = '.'.join(seq.split('.')[:3])
        if l3_key in l3_map:
            l3_map[l3_key]['children'].append(r)

# ── Code generation ────────────────────────────────────────────────────────────

def py_str(s):
    if not s or s == 'NA':
        return '""'
    return '"' + esc(s) + '"'


def render_step(r, indent=0):
    pad = ' ' * indent
    parts = [f'seq={py_str(r["seq"])}', f'name={py_str(r["name"])}']
    if r['desc']:
        parts.append(f'desc={py_str(r["desc"])}')
    if r['step_type'] not in ('', 'Process'):
        parts.append(f'step_type={py_str(r["step_type"])}')
    if r['r']:
        parts.append(f'r={py_str(r["r"])}')
    if r['a']:
        parts.append(f'a={py_str(r["a"])}')
    if r['i']:
        parts.append(f'i={py_str(r["i"])}')
    if r['sys'] and r['sys'] not in ('See L4',):
        parts.append(f'sys={py_str(r["sys"])}')
    if r['outcomes']:
        parts.append(f'outcomes={py_str(r["outcomes"])}')

    children = r.get('children', [])
    if not children:
        return f'{pad}_s({", ".join(parts)})'
    child_lines = [render_step(c, indent + 4) for c in children]
    children_str = '[\n' + ',\n'.join(child_lines) + '\n' + pad + '    ]'
    parts.append(f'children={children_str}')
    return f'{pad}_s({", ".join(parts)})'


L1_COLORS = {
    '1': '#7C3AED',
    '2': '#0E7490',
    '3': '#0891B2',
    '4': '#16A34A',
    '5': '#D97706',
    '6': '#2563EB',
    '7': '#0F766E',
}

lines = []
lines.append('# Auto-generated from Process_Flow_Template_v2 8.xlsx (Process Design tab)')
lines.append('')
lines.append('')
lines.append('def _s(seq, name, desc="", step_type="Process", r="", a="", i="", sys="",')
lines.append('        outcomes="", children=None):')
lines.append('    node = {')
lines.append('        "seq": seq, "name": name, "description": desc,')
lines.append('        "step_type": step_type, "system_tool": sys,')
lines.append('        "raci": {"r": r, "a": a, "i": i},')
lines.append('        "decision_outcomes": outcomes if outcomes else None,')
lines.append('    }')
lines.append('    if children is not None:')
lines.append('        node["children"] = children')
lines.append('    return node')
lines.append('')
lines.append('')

proc_var_names = []
for l1_seq, l1 in l1_map.items():
    color = L1_COLORS.get(l1_seq, '#475569')
    var_name = l1['name'].upper().replace(' ', '_').replace('&', 'AND').replace('(', '').replace(')', '').replace('/', '_')
    var_name = re.sub(r'[^A-Z0-9_]', '', var_name)
    proc_var_names.append(var_name)

    lines.append(f'{var_name} = {{')
    raw_id = l1['name'].lower()
    raw_id = re.sub(r'[^a-z0-9]+', '-', raw_id).strip('-')
    lines.append(f'    "id": "{raw_id}",')
    lines.append(f'    "l1_seq": "{l1_seq}",')
    lines.append(f'    "l1_name": {py_str(l1["name"])},')
    lines.append(f'    "l1_description": {py_str(l1["desc"])},')
    lines.append(f'    "l1_color": "{color}",')
    lines.append(f'    "raci": {{"r": {py_str(l1["r"])}, "a": {py_str(l1["a"])}}},')
    lines.append(f'    "system_tool": {py_str(l1["sys"])},')
    lines.append(f'    "stages": [')

    for l2 in l1['stages']:
        l2_seq = l2['seq']
        lines.append(f'        {{')
        lines.append(f'            "id": "{l2_seq}",')
        lines.append(f'            "seq": {py_str(l2_seq)},')
        lines.append(f'            "name": {py_str(l2["name"])},')
        lines.append(f'            "description": {py_str(l2["desc"])},')
        lines.append(f'            "step_type": {py_str(l2["step_type"])},')
        lines.append(f'            "system_tool": {py_str(l2["sys"])},')
        lines.append(f'            "raci": {{"r": {py_str(l2["r"])}, "a": {py_str(l2["a"])}, "i": {py_str(l2["i"])}}},')
        lines.append(f'            "steps": [')
        for l3 in l2['steps']:
            lines.append('                ' + render_step(l3, 16)[16:] + ',')
        lines.append(f'            ],')
        lines.append(f'        }},')

    lines.append('    ],')
    lines.append('}')
    lines.append('')

lines.append('')
lines.append('ALL_PROCESSES = [')
for v_name in proc_var_names:
    lines.append(f'    {v_name},')
lines.append(']')

out_path = os.path.join('data', 'processes.py')
with open(out_path, 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))

print(f'Written to {out_path}')
print(f'L1 processes: {len(l1_map)}')
print(f'Total steps: {len(rows_data)}')
for seq, l1 in l1_map.items():
    print(f'  L1-{seq} {l1["name"]}: {len(l1["stages"])} stages')
