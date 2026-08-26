import React from "react";

export default function ScoreBreakdown({ dimensions, priorityScore, quadrant }) {
  const dims = dimensions || {
    business_impact: { score: 4.6, max: 5.0, label: "Business Impact", weight: "High" },
    ai_suitability: { score: 4.4, max: 5.0, label: "AI Suitability", weight: "High" },
    automation_feasibility: { score: 4.8, max: 5.0, label: "Automation Feasibility", weight: "High" },
    implementation_effort: { score: 2.2, max: 5.0, label: "Implementation Effort", weight: "Inverse" },
    governance_risk: { score: 1.8, max: 5.0, label: "Governance & Risk", weight: "Inverse" },
  };

  return (
    <div style={{ background: "#f8fafc", border: "1px solid #e2e8f0", borderRadius: "8px", padding: "16px", margin: "16px 0" }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "12px", borderBottom: "1px solid #e2e8f0", paddingBottom: "8px" }}>
        <div>
          <span style={{ fontSize: "10px", fontWeight: "700", color: "#64748b", textTransform: "uppercase", letterSpacing: "0.5px" }}>DECISION LOGIC</span>
          <h4 style={{ fontSize: "14px", fontWeight: "700", color: "#0f172a", margin: "2px 0 0 0" }}>Multi-Factor Scoring Dimensions</h4>
        </div>
        <span style={{ fontSize: "11px", fontWeight: "600", background: "#e2e8f0", color: "#334155", padding: "3px 8px", borderRadius: "4px" }}>
          Stance: {quadrant || "Quick Win"}
        </span>
      </div>

      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(180px, 1fr))", gap: "12px" }}>
        {Object.entries(dims).map(([key, dim]) => {
          const percent = Math.min(100, Math.max(0, (dim.score / dim.max) * 100));
          const isInverse = dim.weight === "Inverse";
          return (
            <div key={key} style={{ background: "#ffffff", border: "1px solid #e2e8f0", borderRadius: "6px", padding: "10px" }}>
              <div style={{ display: "flex", justifyContent: "space-between", fontSize: "11px", fontWeight: "600", color: "#334155", marginBottom: "6px" }}>
                <span>{dim.label}</span>
                <span style={{ fontFamily: "monospace", color: "#0f172a" }}>{dim.score.toFixed(1)} / {dim.max.toFixed(1)}</span>
              </div>
              
              <div style={{ height: "6px", background: "#f1f5f9", borderRadius: "3px", overflow: "hidden", marginBottom: "6px" }}>
                <div style={{
                  height: "100%",
                  width: `${percent}%`,
                  background: isInverse ? "#f59e0b" : "#2563eb",
                  borderRadius: "3px"
                }}></div>
              </div>

              <span style={{ fontSize: "10px", color: "#94a3b8", display: "block" }}>
                {isInverse ? "Lower reduces friction" : "Higher drives priority"}
              </span>
            </div>
          );
        })}
      </div>
    </div>
  );
}