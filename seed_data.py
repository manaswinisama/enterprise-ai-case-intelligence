import json
import sqlite3
from scoring_engine import calculate_process_intelligence

processes = [
    {
        "name": "Invoice Processing",
        "department": "Finance",
        "description": "Extract invoice details, validate line items, match with purchase orders, and process payment.",
        "activities": [
            "Receive invoices from vendors",
            "Extract invoice details",
            "Validate invoice information",
            "Match invoice with purchase order",
            "Send invoice for approval",
            "Process payment"
        ]
    },
    {
        "name": "Employee Onboarding",
        "department": "HR",
        "description": "Verify identity credentials, generate employment contracts, provision software accounts, and schedule orientations.",
        "activities": [
            "Collect identity documents",
            "Verify background and references",
            "Generate employment agreement",
            "Provision IT accounts",
            "Schedule manager orientation"
        ]
    },
    {
        "name": "Commercial Loan Underwriting",
        "department": "Risk & Compliance",
        "description": "Analyze multi-year financial statements, run fraud detection checks, calculate debt service coverage, and issue credit decisions.",
        "activities": [
            "Extract corporate balance sheet metrics",
            "Execute anti-money laundering checks",
            "Calculate cash flow ratios",
            "Evaluate collateral assets",
            "Approve credit threshold"
        ]
    },
    {
        "name": "IT Helpdesk Ticket Triage",
        "department": "IT Operations",
        "description": "Categorize incoming support tickets, detect sentiment, attempt automated password resets, and route escalations to Tier 2 engineers.",
        "activities": [
            "Receive support email",
            "Classify incident severity",
            "Execute automated credential reset",
            "Assign ticket to technician"
        ]
    }
]

conn = sqlite3.connect("processiq.db")
with conn:
    # Drop and recreate the table with the complete schema
    conn.execute("DROP TABLE IF EXISTS processes")
    conn.execute("""
        CREATE TABLE processes (
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
    
    for p in processes:
        intel = calculate_process_intelligence(p["name"], p["department"], p["description"], p["activities"])
        conn.execute(
            """
            INSERT INTO processes (name, department, description, activities, analysis_result, priority_score)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                p["name"],
                p["department"],
                p["description"],
                json.dumps(p["activities"]),
                json.dumps(intel),
                intel["priority_score"]
            )
        )

print("Enterprise database schema updated and successfully seeded with 4 diverse workflows.")