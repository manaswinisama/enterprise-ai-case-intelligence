from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import json
import sqlite3
from scoring_engine import calculate_process_intelligence

app = FastAPI(title="ProcessIQ API", version="1.0.0")

# Enable CORS for Vite frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database Setup Helper
def get_db():
    conn = sqlite3.connect("processiq.db")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS processes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                department TEXT NOT NULL,
                description TEXT,
                activities TEXT NOT NULL,
                analysis_result TEXT,
                priority_score INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
init_db()

class ProcessCreate(BaseModel):
    name: str
    department: str
    description: str
    activities: List[str]

@app.get("/processes")
def list_processes():
    with get_db() as conn:
        rows = conn.execute("SELECT id, name, department, priority_score, description, activities, analysis_result FROM processes ORDER BY id DESC").fetchall()
        result = []
        for r in rows:
            result.append({
                "id": r["id"],
                "name": r["name"],
                "department": r["department"],
                "priority_score": r["priority_score"],
                "description": r["description"],
                "activities": json.loads(r["activities"]),
                "analysis_result": json.loads(r["analysis_result"]) if r["analysis_result"] else None
            })
        return result

@app.post("/processes")
def create_process(payload: ProcessCreate):
    intel = calculate_process_intelligence(
        name=payload.name,
        department=payload.department,
        description=payload.description,
        activities=payload.activities
    )
    with get_db() as conn:
        cursor = conn.execute(
            """
            INSERT INTO processes (name, department, description, activities, analysis_result, priority_score)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                payload.name,
                payload.department,
                payload.description,
                json.dumps(payload.activities),
                json.dumps(intel),
                intel["priority_score"]
            )
        )
        process_id = cursor.lastrowid
        intel["id"] = process_id
    return intel

@app.post("/analyze/{process_id}")
def analyze_process(process_id: int):
    with get_db() as conn:
        row = conn.execute("SELECT * FROM processes WHERE id = ?", (process_id,)).fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Process not found")
        
        intel = calculate_process_intelligence(
            name=row["name"],
            department=row["department"],
            description=row["description"],
            activities=json.loads(row["activities"])
        )
        conn.execute(
            "UPDATE processes SET analysis_result = ?, priority_score = ? WHERE id = ?",
            (json.dumps(intel), intel["priority_score"], process_id)
        )
        intel["id"] = process_id
        return intel