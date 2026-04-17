from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from data.processes import ALL_PROCESSES

app = FastAPI(title="OTC Process Explorer API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_methods=["GET"],
    allow_headers=["*"],
)


@app.get("/api/processes")
def get_processes():
    return ALL_PROCESSES


@app.get("/health")
def health():
    return {"status": "ok"}
