import re


def analyze_activity(activity: str):
    """
    Analyze one individual process activity.
    """

    text = activity.lower()

    automation_patterns = [
        r"\bextract\b",
        r"\benter\b",
        r"\bdata entry\b",
        r"\brecord\b",
        r"\bupdate\b",
        r"\bcollect\b",
        r"\bvalidate\b",
        r"\bverify\b",
        r"\bcheck\b",
        r"\bprocess\b",
        r"\bgenerate\b",
        r"\bschedule\b",
        r"\bclassify\b",
        r"\bcategorize\b",
        r"\broute\b",
        r"\bsend\b",
        r"\bnotify\b",
        r"\breconcile\b",
        r"\bcalculate\b",
        r"\btranscribe\b",
    ]

    human_patterns = [
        r"\bapprove\b",
        r"\bapproval\b",
        r"\bdecision\b",
        r"\bdecide\b",
        r"\bnegotiate\b",
        r"\binterview\b",
        r"\bescalate\b",
        r"\bexception\b",
        r"\breview\b",
        r"\bauthorize\b",
    ]

    ai_patterns = [
        r"\bextract\b",
        r"\bclassify\b",
        r"\bcategorize\b",
        r"\bvalidate\b",
        r"\bverify\b",
        r"\breview\b",
        r"\bgenerate\b",
        r"\bsummarize\b",
        r"\banalyze\b",
        r"\bpredict\b",
        r"\bdetect\b",
        r"\bmatch\b",
    ]

    automation_match = any(
        re.search(pattern, text)
        for pattern in automation_patterns
    )

    human_match = any(
        re.search(pattern, text)
        for pattern in human_patterns
    )

    ai_match = any(
        re.search(pattern, text)
        for pattern in ai_patterns
    )

    # ----------------------------------------------
    # Activity classification
    # ----------------------------------------------

    if human_match and automation_match:
        automation = "Medium"
        human = "High"

    elif human_match:
        automation = "Low"
        human = "High"

    elif automation_match and ai_match:
        automation = "High"
        human = "Low"

    elif automation_match:
        automation = "High"
        human = "Low"

    elif ai_match:
        automation = "Medium"
        human = "Medium"

    else:
        automation = "Low"
        human = "Medium"

    # ----------------------------------------------
    # AI opportunity
    # ----------------------------------------------

    if ai_match:
        ai_opportunity = "High"
    elif automation_match:
        ai_opportunity = "Medium"
    else:
        ai_opportunity = "Low"

    # ----------------------------------------------
    # Recommended technology
    # ----------------------------------------------

    technology = []

    if any(
        re.search(pattern, text)
        for pattern in [
            r"\bextract\b",
            r"\bdocument\b",
            r"\bcollect\b",
            r"\bvalidate\b",
        ]
    ):
        technology.append("Document AI")

    if automation_match:
        technology.append("RPA")

    if ai_match:
        technology.append("LLM")

    if any(
        word in text
        for word in [
            "schedule",
            "route",
            "notify",
            "process",
        ]
    ):
        technology.append("Workflow Automation")

    if not technology:
        technology.append("AI-assisted Workflow")

    technology = list(dict.fromkeys(technology))

    # ----------------------------------------------
    # Recommendation
    # ----------------------------------------------

    if human == "High":
        recommendation = "Keep human-in-the-loop"

    elif automation == "High":
        recommendation = "Prioritize for automation"

    elif ai_opportunity == "High":
        recommendation = "Prioritize for AI assistance"

    else:
        recommendation = "Monitor for future automation"

    return {
        "activity": activity,
        "ai_opportunity": ai_opportunity,
        "automation_potential": automation,
        "human_involvement": human,
        "technology": technology,
        "recommendation": recommendation,
    }


def analyze_process(
    name: str,
    description: str,
    department: str,
    activities: list[str]
):
    text = " ".join(
        [name, description, department] + activities
    ).lower()

    activity_text = " ".join(activities).lower()

    # ----------------------------------------------
    # Pattern definitions
    # ----------------------------------------------

    automation_patterns = [
        r"\bextract\b",
        r"\benter\b",
        r"\bdata entry\b",
        r"\brecord\b",
        r"\bupdate\b",
        r"\bcollect\b",
        r"\bvalidate\b",
        r"\bverify\b",
        r"\bcheck\b",
        r"\bprocess\b",
        r"\bgenerate\b",
        r"\bschedule\b",
        r"\bclassify\b",
        r"\bcategorize\b",
        r"\broute\b",
        r"\bsend\b",
        r"\bnotify\b",
        r"\breconcile\b",
        r"\bcalculate\b",
        r"\btranscribe\b",
    ]

    human_patterns = [
        r"\bapprove\b",
        r"\bapproval\b",
        r"\bdecision\b",
        r"\bdecide\b",
        r"\bnegotiate\b",
        r"\binterview\b",
        r"\bescalate\b",
        r"\bexception\b",
        r"\breview\b",
        r"\bauthorize\b",
    ]

    ai_patterns = [
        r"\bextract\b",
        r"\bclassify\b",
        r"\bcategorize\b",
        r"\bvalidate\b",
        r"\bverify\b",
        r"\breview\b",
        r"\bgenerate\b",
        r"\bsummarize\b",
        r"\banalyze\b",
        r"\bpredict\b",
        r"\bdetect\b",
        r"\bmatch\b",
    ]

    # ----------------------------------------------
    # Process-level matching
    # ----------------------------------------------

    automation_matches = sum(
        bool(re.search(pattern, activity_text))
        for pattern in automation_patterns
    )

    human_matches = sum(
        bool(re.search(pattern, activity_text))
        for pattern in human_patterns
    )

    ai_matches = sum(
        bool(re.search(pattern, activity_text))
        for pattern in ai_patterns
    )

    activity_count = len(activities)

    # ----------------------------------------------
    # Priority score
    # ----------------------------------------------

    score = 35

    if activity_count >= 5:
        score += 15
    elif activity_count >= 3:
        score += 10
    elif activity_count >= 2:
        score += 5

    score += min(automation_matches * 6, 30)
    score += min(ai_matches * 4, 20)

    score = min(score, 100)

    # ----------------------------------------------
    # AI opportunity
    # ----------------------------------------------

    if ai_matches >= 3 or score >= 75:
        ai_opportunity = "High"
    elif ai_matches >= 1 or score >= 50:
        ai_opportunity = "Medium"
    else:
        ai_opportunity = "Low"

    # ----------------------------------------------
    # Automation potential
    # ----------------------------------------------

    if automation_matches >= 4:
        automation_potential = "High"
    elif automation_matches >= 2:
        automation_potential = "Medium"
    else:
        automation_potential = "Low"

    # ----------------------------------------------
    # Human involvement
    # ----------------------------------------------

    if human_matches >= 2:
        human_involvement = "High"
    elif human_matches >= 1:
        human_involvement = "Medium"
    else:
        human_involvement = "Low"

    # ----------------------------------------------
    # Benefits
    # ----------------------------------------------

    benefits = [
        "Reduced manual effort",
        "Faster process execution",
        "Improved consistency",
        "Reduced operational errors"
    ]

    if automation_matches >= 3:
        benefits.append(
            "Significant opportunity for workflow automation"
        )

    if ai_matches >= 2:
        benefits.append(
            "AI-assisted decision support and data processing"
        )

    # ----------------------------------------------
    # Risks
    # ----------------------------------------------

    risks = [
        "Incorrect automation decisions",
        "Data privacy and security concerns",
        "Human oversight is required for exceptions"
    ]

    if human_matches > 0:
        risks.append(
            "Automated recommendations should remain subject to human approval"
        )

    # ----------------------------------------------
    # Technology recommendations
    # ----------------------------------------------

    technologies = []

    if any(
        re.search(pattern, activity_text)
        for pattern in [
            r"\bextract\b",
            r"\bdocument\b",
            r"\bcollect\b",
            r"\bvalidate\b",
        ]
    ):
        technologies.append("Document AI")

    if automation_matches >= 2:
        technologies.append("RPA")

    if ai_matches >= 2:
        technologies.append("LLM")

    if any(
        word in activity_text
        for word in [
            "schedule",
            "route",
            "notify",
            "process",
        ]
    ):
        technologies.append("Workflow Automation")

    if not technologies:
        technologies.append("AI-assisted Workflow")

    technologies = list(dict.fromkeys(technologies))

    # ----------------------------------------------
    # Activity-level analysis
    # ----------------------------------------------

    activity_analysis = [
        analyze_activity(activity)
        for activity in activities
    ]

    # ----------------------------------------------
    # Reasoning
    # ----------------------------------------------

    reasoning_parts = [
        f"The process contains {activity_count} activities."
    ]

    if automation_matches > 0:
        reasoning_parts.append(
            f"{automation_matches} activities contain "
            "characteristics suitable for automation."
        )

    if ai_matches > 0:
        reasoning_parts.append(
            f"{ai_matches} activities present potential "
            "for AI-assisted processing or decision support."
        )

    if human_matches > 0:
        reasoning_parts.append(
            f"{human_matches} activities require or benefit "
            "from human oversight."
        )

    reasoning_parts.append(
        f"The resulting AI opportunity is {ai_opportunity} "
        f"with an automation potential of {automation_potential}."
    )

    reasoning_parts.append(
        f"The estimated priority score is {score}/100."
    )

    reasoning_parts.append(
        "A human-in-the-loop approach should be maintained "
        "for approvals, exceptions, and business-critical decisions."
    )

    reasoning = " ".join(reasoning_parts)

    return {
        "ai_opportunity": ai_opportunity,
        "automation_potential": automation_potential,
        "human_involvement": human_involvement,
        "benefits": benefits,
        "risks": risks,
        "technology": technologies,
        "priority_score": score,
        "reasoning": reasoning,
        "activity_analysis": activity_analysis,
    }