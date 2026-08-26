import React from "react";

function ScoreBreakdown({ process }) {
  if (!process) {
    return <p className="placeholder-text">No process data selected.</p>;
  }

  // Fallback defaults to ensure no dimension is undefined
  const dims = {
    impact: 0,
    ai_suitability: 0,
    feasibility: 0,
    effort: 0,
    risk: 0,
    ...(process.dimensions || {}),
  };

  const priorityScore = process.priority_score ?? 0;
  const quadrant = process.quadrant || "Unclassified";

  return (
    <div className="score-overview">
      <div className="priority-gauge">
        <div className="score-number">{priorityScore}</div>
        <div className="score-label">Priority Index (0-100)</div>
        <div className="quadrant-tag">{quadrant}</div>
      </div>

      <div className="dimension-meters">
        {Object.entries(dims).map(([key, val]) => {
          // Ensure val is a valid number before calling .toFixed()
          const numericVal = typeof val === "number" && !isNaN(val) ? val : 0;
          const percentage = Math.min(100, Math.max(0, (numericVal / 5.0) * 100));

          return (
            <div key={key} className="dim-row">
              <span className="dim-title">
                {key.replace(/_/g, " ").toUpperCase()}
              </span>
              <div className="progress-bar">
                <div
                  className="progress-fill"
                  style={{ width: `${percentage}%` }}
                ></div>
              </div>
              <span className="dim-val">
                {numericVal.toFixed(1)}/5.0
              </span>
            </div>
          );
        })}
      </div>
    </div>
  );
}

export default ScoreBreakdown;