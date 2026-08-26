from typing import Dict, Any, List

def classify_activity(activity_text: str) -> Dict[str, Any]:
    text = activity_text.lower()
    
    # Heuristic pattern matching for enterprise activities
    is_doc = any(k in text for k in ["invoice", "document", "extract", "receipt", "pdf", "scan", "form"])
    is_decision = any(k in text for k in ["approve", "review", "evaluate", "verify", "validate", "assess", "decision"])
    is_auto = any(k in text for k in ["payment", "send", "notify", "update", "create", "enter", "record", "match"])
    
    ai_level = "High" if (is_doc or is_decision) else "Low"
    auto_level = "High" if (is_auto or is_doc) else ("Medium" if is_decision else "Low")
    human_level = "High" if ("approve" in text or "decision" in text or "compliance" in text) else ("Medium" if is_decision else "Low")
    
    tech_stack = []
    if is_doc:
        tech_stack.extend(["Document AI", "LLM"])
    if is_auto:
        tech_stack.extend(["RPA", "Workflow Automation"])
    if not tech_stack:
        tech_stack.append("AI-assisted Workflow")
        
    # Deduplicate while preserving order
    tech_stack = list(dict.fromkeys(tech_stack))
    
    rec = "Prioritize for automation"
    if human_level == "High":
        rec = "Keep human-in-the-loop"
    elif ai_level == "High" and auto_level != "High":
        rec = "Prioritize for AI assistance"
    elif auto_level == "Low" and ai_level == "Low":
        rec = "Monitor for future automation"

    return {
        "title": activity_text,
        "recommendation": rec,
        "ai": ai_level,
        "auto": auto_level,
        "human": human_level,
        "tech": tech_stack
    }

def calculate_process_intelligence(name: str, department: str, description: str, activities: List[str]) -> Dict[str, Any]:
    classified_activities = []
    for idx, act in enumerate(activities, 1):
        c = classify_activity(act)
        c["id"] = f"{idx:02d}"
        classified_activities.append(c)
        
    total_acts = len(classified_activities) or 1
    high_auto = sum(1 for a in classified_activities if a["auto"] == "High")
    high_ai = sum(1 for a in classified_activities if a["ai"] == "High")
    high_human = sum(1 for a in classified_activities if a["human"] == "High")
    
    # 5-Dimension Sub-scores (1.0 to 5.0)
    business_impact = round(min(5.0, 2.5 + (high_auto * 0.5) + (high_ai * 0.4)), 1)
    ai_suitability = round(min(5.0, 1.5 + (high_ai / total_acts) * 3.5), 1)
    automation_feasibility = round(min(5.0, 1.5 + (high_auto / total_acts) * 3.5), 1)
    implementation_effort = round(min(5.0, 1.5 + (total_acts * 0.25) + (high_human * 0.3)), 1)
    
    dept_risk = 0.5 if department.lower() in ["finance", "legal", "hr", "compliance"] else 0.2
    governance_risk = round(min(5.0, 1.2 + (high_human * 0.6) + dept_risk), 1)
    
    # Score calculation
    raw_ratio = (business_impact * ai_suitability * automation_feasibility) / (implementation_effort * governance_risk)
    priority_score = int(min(98, max(25, (raw_ratio / 8.5) * 100)))
    
    # Quadrant assignment
    if business_impact >= 3.5 and implementation_effort <= 3.0:
        quadrant = "Quick Win"
    elif business_impact >= 3.5 and implementation_effort > 3.0:
        quadrant = "Strategic Bet"
    elif business_impact < 3.5 and implementation_effort <= 3.0:
        quadrant = "Operational Efficiency"
    else:
        quadrant = "Deprioritize / Re-evaluate"

    # Aggregates
    all_tech = list(dict.fromkeys([t for a in classified_activities for t in a["tech"]]))
    
    ai_opp = "High" if high_ai >= 2 else ("Medium" if high_ai == 1 else "Low")
    auto_pot = "High" if high_auto >= 2 else ("Medium" if high_auto == 1 else "Low")
    human_inv = "High" if high_human >= 2 else ("Medium" if high_human == 1 else "Low")
    
    reasoning = (
        f"The process contains {total_acts} activities. {high_auto} activities contain characteristics suitable for automation. "
        f"{high_ai} activities present potential for AI-assisted processing or decision support. "
        f"{high_human} activities require or benefit from human oversight. The resulting AI opportunity is {ai_opp} "
        f"with an automation potential of {auto_pot}. The estimated priority score is {priority_score}/100. "
        f"A human-in-the-loop approach should be maintained for approvals, exceptions, and business-critical decisions."
    )
    
    return {
        "process_name": name,
        "department": department,
        "description": description,
        "priority_score": priority_score,
        "quadrant": quadrant,
        "ai_opportunity": ai_opp,
        "automation_potential": auto_pot,
        "human_involvement": human_inv,
        "dimensions": {
            "business_impact": {"score": business_impact, "max": 5.0, "label": "Business Impact", "weight": "High"},
            "ai_suitability": {"score": ai_suitability, "max": 5.0, "label": "AI Suitability", "weight": "High"},
            "automation_feasibility": {"score": automation_feasibility, "max": 5.0, "label": "Automation Feasibility", "weight": "High"},
            "implementation_effort": {"score": implementation_effort, "max": 5.0, "label": "Implementation Effort", "weight": "Inverse"},
            "governance_risk": {"score": governance_risk, "max": 5.0, "label": "Governance & Risk", "weight": "Inverse"}
        },
        "activities_intelligence": classified_activities,
        "benefits": [
            "Reduced manual effort",
            "Faster process execution",
            "Improved consistency",
            "Reduced operational errors",
            "Significant opportunity for workflow automation",
            "AI-assisted decision support and data processing"
        ],
        "risks": [
            "Incorrect automation decisions",
            "Data privacy and security concerns",
            "Human oversight is required for exceptions",
            "Automated recommendations should remain subject to human approval"
        ],
        "technologies": all_tech,
        "ai_reasoning": reasoning
    }