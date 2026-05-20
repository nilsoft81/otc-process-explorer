import json
import os
import subprocess

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

from data.processes import ALL_PROCESSES as _STATIC_PROCESSES
from excel_parser import validate_excel, parse_excel, COLUMNS_META

app = FastAPI(title="OTC Process Explorer API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
UPLOADED_JSON = os.path.join(DATA_DIR, 'uploaded_processes.json')
UPLOADED_EXCEL = os.path.join(DATA_DIR, 'uploaded_process.xlsx')


def _load_processes():
    if os.path.exists(UPLOADED_JSON):
        try:
            with open(UPLOADED_JSON, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            pass
    return _STATIC_PROCESSES


@app.get("/api/processes")
def get_processes():
    return _load_processes()


@app.get("/api/upload/columns")
def get_columns():
    return {"columns": COLUMNS_META}


@app.post("/api/upload")
async def upload_excel(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(('.xlsx', '.xls')):
        return {"success": False, "error": "Only Excel files (.xlsx or .xls) are accepted", "missing_columns": []}

    contents = await file.read()

    ok, error, missing = validate_excel(contents)
    if not ok:
        return {"success": False, "error": error, "missing_columns": missing}

    try:
        processes = parse_excel(contents)
    except Exception as e:
        return {"success": False, "error": f"Failed to parse Excel: {e}", "missing_columns": []}

    # Persist JSON (serves immediately on next /api/processes call)
    with open(UPLOADED_JSON, 'w', encoding='utf-8') as f:
        json.dump(processes, f, ensure_ascii=False, indent=2)

    # Save Excel file
    with open(UPLOADED_EXCEL, 'wb') as f:
        f.write(contents)

    # Best-effort git commit
    git_committed = False
    try:
        repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        rel_json = os.path.relpath(UPLOADED_JSON, repo_root)
        rel_xlsx = os.path.relpath(UPLOADED_EXCEL, repo_root)
        subprocess.run(['git', 'add', rel_json, rel_xlsx],
                       cwd=repo_root, capture_output=True, timeout=15)
        r = subprocess.run(
            ['git', 'commit', '-m', f'Upload: process data from {file.filename}'],
            cwd=repo_root, capture_output=True, timeout=15
        )
        git_committed = (r.returncode == 0)
    except Exception:
        pass

    l1_count = len(processes)
    return {
        "success": True,
        "message": f"Process map updated with {l1_count} L1 process{'es' if l1_count != 1 else ''}.",
        "git_committed": git_committed,
        "process_count": l1_count,
    }


@app.get("/health")
def health():
    return {"status": "ok"}
