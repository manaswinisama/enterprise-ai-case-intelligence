import re
from typing import List, Dict, Any

TECH_PATTERNS = {
    "IDP": [r"extract", r"invoice", r"receipt", r"document", r"scan", r"form", r"ocr", r"pdf"],
    "RPA": [r"enter", r"input", r"copy", r"paste", r"transfer", r"portal", r"system", r"database", r"export"],
    "LLM": [r"summarize", r"generate", r"draft", r"analyze", r"review", r"sentiment", r"classify", r"categorize"],
    "Rules Engine": [r"validate", r"verify", r"check", r"calculate", r"match", r"reconcile", r"compare"]
}

HITL_KEYWORDS = [r"approve", r"sign off", r"decision", r"sensitive", r"compliance", r"risk", r"legal", r"payment"]

def classify_activity(activity: str) -> Dict[str, Any]:
    text = activity.lower()
    
    suggested_tech = "Deterministic Logic"
    for tech, patterns in TECH_PATTERNS.items():
        if any(re.search(p, text) for p in patterns):
            suggested_tech = tech
            break

    hitl_required = any(re.search(k, text) for k in HITL_KEYWORDS)
    
    return {
        "activity": activity,
        "suggested_tech": suggested_tech,
        "hitl_required": hitl_required,
        "ai_suitability": 4 if suggested_tech in ["IDP", "LLM"] else 2,
        "automation_feasibility": 5 if suggested_tech in ["RPA", "Rules Engine"] else 3
    }

def calculate_process_intelligence(name: str, department: str, description: str, activities: List[str]) -> Dict[str, Any]:
    classified_activities = [classify_activity(a) for a in activities if a.strip()]
    
    num_activities = max(1, len(classified_activities))
    ai_count = sum(1 for a in classified_activities if a["suggested_tech"] in ["IDP", "LLM"])
    hitl_count = sum(1 for a in classified_activities if a["hitl_required"])

    # 1.0 to 5.0 normalized dimensions
    impact = min(5.0, max(1.0, 2.5 + (num_activities * 0.4)))
    ai_suitability = min(5.0, max(1.0, 1.5 + (ai_count / num_activities) * 3.5))
    feasibility = min(5.0, max(1.0, 4.5 - (hitl_count / num_activities) * 1.5))
    effort = min(5.0, max(1.0, 1.8 + (num_activities * 0.5)))
    risk = min(5.0, max(1.0, 1.5 + (hitl_count * 0.8)))

    # Priority formula
    raw_score = ((impact * ai_suitability * feasibility) / (effort * risk)) * (100.0 / 8.5)
    priority_score = int(min(98, max(25, round(raw_score))))

    # Quadrant Assignment
    if impact >= 3.0 and effort <= 3.0:
        quadrant = "Quick Wins"
    elif impact >= 3.0 and effort > 3.0:
        quadrant = "Strategic Bets"
    elif impact < 3.0 and effort <= 3.0:
        quadrant = "Operational Wins"
    else:
        quadrant = "Re-evaluate / Defer"

    return {
        "name": name,
        "department": department,
        "description": description,
        "priority_score": priority_score,
        "quadrant": quadrant,
        "dimensions": {
            "impact": round(impact, 2),
            "ai_suitability": round(ai_suitability, 2),
            "feasibility": round(feasibility, 2),
            "effort": round(effort, 2),
            "risk": round(risk, 2)
        },
        "activities": classified_activities
    }