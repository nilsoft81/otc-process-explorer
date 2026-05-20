"""Validate and parse Process Design Excel into ALL_PROCESSES list."""
import io
import re
import openpyxl

REQUIRED_SHEET = 'Process Design'
HEADER_ROW_IDX = 3   # row 4 in Excel (0-indexed)
DATA_START_IDX = 4   # row 5 in Excel

# Column indices (0-based)
C_AI, C_SYS, C_LVL, C_SEQ, C_NAME = 0, 1, 2, 3, 4
C_DESC, C_TYPE, C_AUTO = 5, 6, 7
C_R, C_A, C_C = 16, 17, 18
C_ART, C_SLA, C_DATA, C_CHG = 23, 24, 25, 27

REQUIRED_COLUMNS = {
    C_AI:   ("A",  "AI Agent"),
    C_SYS:  ("B",  "System / Tool"),
    C_LVL:  ("C",  "Level"),
    C_SEQ:  ("D",  "Step Number / Seq"),
    C_NAME: ("E",  "Step Name"),
    C_DESC: ("F",  "Description"),
    C_TYPE: ("G",  "Step Type"),
    C_AUTO: ("H",  "Automated"),
    C_R:    ("Q",  "RACI – Responsible"),
    C_A:    ("R",  "RACI – Accountable"),
    C_C:    ("S",  "RACI – Contributing"),
    C_ART:  ("X",  "Critical Artefact"),
    C_SLA:  ("Y",  "SLA"),
    C_DATA: ("Z",  "Key Data Points"),
    C_CHG:  ("AB", "Change Highlight"),
}

L1_COLORS = {
    '1': '#7C3AED',
    '2': '#0E7490',
    '3': '#0891B2',
    '4': '#16A34A',
    '5': '#D97706',
    '6': '#2563EB',
    '7': '#0F766E',
}


def validate_excel(file_content: bytes):
    """Returns (ok: bool, error: str|None, missing_columns: list[str])."""
    try:
        wb = openpyxl.load_workbook(io.BytesIO(file_content), data_only=True)
    except Exception as e:
        return False, f"Cannot read Excel file: {e}", []

    if REQUIRED_SHEET not in wb.sheetnames:
        available = ', '.join(wb.sheetnames)
        return False, (
            f"Sheet '{REQUIRED_SHEET}' not found. "
            f"Available sheets: {available}"
        ), []

    ws = wb[REQUIRED_SHEET]
    all_rows = list(ws.iter_rows(values_only=True))

    if len(all_rows) <= HEADER_ROW_IDX:
        return False, "File has fewer than 4 rows — header expected at row 4", []

    header_row = all_rows[HEADER_ROW_IDX]
    missing = []
    for col_idx, (col_letter, col_name) in REQUIRED_COLUMNS.items():
        val = header_row[col_idx] if col_idx < len(header_row) else None
        if not val or str(val).strip() == '':
            missing.append(f"Column {col_letter} – {col_name}")

    if missing:
        return False, "Missing required columns in the header row (row 4)", missing

    return True, None, []


def parse_excel(file_content: bytes) -> list:
    """Parse Excel bytes and return ALL_PROCESSES list (same structure as data/processes.py)."""
    wb = openpyxl.load_workbook(io.BytesIO(file_content), data_only=True)
    ws = wb[REQUIRED_SHEET]
    all_rows = list(ws.iter_rows(values_only=True))

    def v(row, col):
        if col >= len(row):
            return ''
        val = row[col]
        s = str(val).strip() if val is not None else ''
        return s.replace('–', '-').replace('—', '-').replace('‘', "'").replace('→', '->')

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
                    outcomes.append(m.group(1).capitalize() + ' - proceed to ' + m.group(2).strip().rstrip('.'))
                elif re.match(r'if\s+(yes|no)', line, re.I):
                    cleaned = re.sub(r'^if\s+', '', line, flags=re.I)
                    outcomes.append(cleaned)
            return 'Decision', ' | '.join(outcomes)
        if 'start' in first.lower():
            return 'Start', ''
        return 'Process', ''

    rows_data = []
    for raw in all_rows[DATA_START_IDX:]:
        seq = v(raw, C_SEQ)
        name = v(raw, C_NAME)
        if not seq or not name:
            continue
        if not re.match(r'^\d[\d.]*$', seq):
            continue
        dots = seq.count('.')
        lvl = {0: 'L1', 1: 'L2', 2: 'L3', 3: 'L4'}.get(dots)
        if lvl is None:
            continue

        raw_type = v(raw, C_TYPE)
        step_type, outcomes = parse_step_type(raw_type)
        r_val = v(raw, C_R)
        a_val = v(raw, C_A)
        c_val = v(raw, C_C)

        if 'automated' in r_val.lower() and step_type == 'Process':
            step_type = 'Automated'

        ai_flag = v(raw, C_AI)
        is_ai = (bool(ai_flag) and ai_flag.lower() not in ('', 'n', 'no', 'none', 'future opportunity')) \
                or 'AI Agent' in r_val

        rows_data.append({
            'lvl': lvl, 'seq': seq, 'name': name,
            'desc': v(raw, C_DESC), 'step_type': step_type, 'outcomes': outcomes,
            'sys': v(raw, C_SYS), 'r': r_val, 'a': a_val, 'c': c_val,
            'art': v(raw, C_ART), 'sla': v(raw, C_SLA),
            'data': v(raw, C_DATA), 'chg': v(raw, C_CHG), 'is_ai': is_ai,
        })

    # Inject synthetic L3 parents for orphaned L4s
    l3_seqs = {r['seq'] for r in rows_data if r['lvl'] == 'L3'}
    orphan_added = set()
    extra = []
    for r in rows_data:
        if r['lvl'] == 'L4':
            parent = '.'.join(r['seq'].split('.')[:3])
            if parent not in l3_seqs and parent not in orphan_added:
                orphan_added.add(parent)
                extra.append({
                    'lvl': 'L3', 'seq': parent, 'name': 'Approval & Sign-off',
                    'desc': '', 'step_type': 'Process', 'outcomes': '',
                    'sys': r['sys'], 'r': r['r'], 'a': r['a'], 'c': r['c'],
                    'art': '', 'sla': '', 'data': '', 'chg': '', 'is_ai': False,
                })
    rows_data.extend(extra)
    rows_data.sort(
        key=lambda r: [int(x) for x in r['seq'].split('.')] + [0] * (4 - r['seq'].count('.') - 1)
    )

    def make_node(r, children=None):
        node = {
            'seq': r['seq'], 'name': r['name'], 'description': r['desc'],
            'step_type': r['step_type'], 'system_tool': r['sys'],
            'raci': {'r': r['r'], 'a': r['a'], 'c': r['c']},
            'decision_outcomes': r['outcomes'] if r['outcomes'] else None,
            'critical_artefact': r['art'], 'sla': r['sla'],
            'key_data_points': r['data'], 'change_highlight': r['chg'],
        }
        if children is not None:
            node['children'] = children
        return node

    l1_map, l2_map, l3_map = {}, {}, {}

    for r in rows_data:
        seq = r['seq']
        if r['lvl'] == 'L1':
            raw_id = re.sub(r'[^a-z0-9]+', '-', r['name'].lower()).strip('-')
            l1_map[seq] = {
                'id': raw_id, 'l1_seq': seq, 'l1_name': r['name'],
                'l1_description': r['desc'],
                'l1_color': L1_COLORS.get(seq, '#475569'),
                'raci': {'r': r['r'], 'a': r['a']},
                'system_tool': r['sys'], 'stages': [],
            }
        elif r['lvl'] == 'L2':
            l1_key = seq.split('.')[0]
            rec = {
                'id': seq, 'seq': seq, 'name': r['name'], 'description': r['desc'],
                'step_type': r['step_type'], 'system_tool': r['sys'],
                'raci': {'r': r['r'], 'a': r['a']},
                'critical_artefact': r['art'], 'sla': r['sla'],
                'key_data_points': r['data'], 'change_highlight': r['chg'],
                'steps': [],
            }
            l2_map[seq] = rec
            if l1_key in l1_map:
                l1_map[l1_key]['stages'].append(rec)
        elif r['lvl'] == 'L3':
            l2_key = '.'.join(seq.split('.')[:2])
            rec = make_node(r, children=[])
            l3_map[seq] = rec
            if l2_key in l2_map:
                l2_map[l2_key]['steps'].append(rec)
        elif r['lvl'] == 'L4':
            l3_key = '.'.join(seq.split('.')[:3])
            if l3_key in l3_map:
                l3_map[l3_key]['children'].append(make_node(r))

    return list(l1_map.values())


# Column metadata for the frontend /api/upload/columns endpoint
COLUMNS_META = [
    {"col": col_letter, "index": idx, "name": col_name,
     "description": desc}
    for idx, (col_letter, col_name), desc in [
        (C_AI,   ("A",  "AI Agent"),                "Flag for AI Agent steps (e.g. Y / Yes)"),
        (C_SYS,  ("B",  "System / Tool"),           "System or tool used in the step"),
        (C_LVL,  ("C",  "Level"),                   "Process level (L1, L2, L3, L4)"),
        (C_SEQ,  ("D",  "Step Number / Seq"),        "Sequence number (e.g. 1, 1.1, 1.1.1, 1.1.1.1)"),
        (C_NAME, ("E",  "Step Name"),                "Name of the process step"),
        (C_DESC, ("F",  "Description"),              "Detailed description of the step"),
        (C_TYPE, ("G",  "Step Type"),                "Process, Decision, Start, or Automated — Decisions include If yes/no routing"),
        (C_AUTO, ("H",  "Automated"),                "Whether the step is fully automated"),
        (C_R,    ("Q",  "RACI – Responsible"),       "Who is responsible for executing the step"),
        (C_A,    ("R",  "RACI – Accountable"),       "Who is ultimately accountable"),
        (C_C,    ("S",  "RACI – Contributing"),      "Who is consulted or contributes"),
        (C_ART,  ("X",  "Critical Artefact"),        "Key document or deliverable produced"),
        (C_SLA,  ("Y",  "SLA"),                      "Service level agreement / time target"),
        (C_DATA, ("Z",  "Key Data Points"),          "Key data fields and dimensionality"),
        (C_CHG,  ("AB", "Change Highlight"),         "To-Be process change or delta"),
    ]
]
