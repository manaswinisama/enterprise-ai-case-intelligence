import React from "react";

export default function PrioritizationMatrix({ processes, currentProcessId, onSelectProcess }) {
  const uniqueProcesses = React.useMemo(() => {
    if (!processes || processes.length === 0) return [];
    const seen = new Set();
    return processes.filter((p) => {
      const key = p.name || p.id;
      if (seen.has(key)) return false;
      seen.add(key);
      return true;
    });
  }, [processes]);

  const quickWins = uniqueProcesses.filter((p) => (p.impact || 4) >= 3.5 && (p.effort || 2.5) <= 3.0);
  const strategicBets = uniqueProcesses.filter((p) => (p.impact || 4) >= 3.5 && (p.effort || 2.5) > 3.0);
  const operationalWins = uniqueProcesses.filter((p) => (p.impact || 4) < 3.5 && (p.effort || 2.5) <= 3.0);
  const deferList = uniqueProcesses.filter((p) => (p.impact || 4) < 3.5 && (p.effort || 2.5) > 3.0);

  const renderList = (items, dotColor) => {
    if (!items || items.length === 0) {
      return <div style={{ fontSize: "11px", color: "#94a3b8", fontStyle: "italic", padding: "8px 0" }}>No processes assigned</div>;
    }
    return (
      <div style={{ display: "flex", flexDirection: "column", gap: "6px", marginTop: "8px" }}>
        {items.map((p) => (
          <div
            key={p.id || p.name}
            onClick={() => onSelectProcess && onSelectProcess(p.id)}
            style={{
              display: "flex",
              justifyContent: "space-between",
              alignItems: "center",
              background: "#ffffff",
              border: currentProcessId === p.id ? "1.5px solid #0f172a" : "1px solid #e2e8f0",
              borderRadius: "6px",
              padding: "6px 8px",
              cursor: "pointer",
              boxShadow: "0 1px 2px rgba(0,0,0,0.03)"
            }}
          >
            <div style={{ display: "flex", alignItems: "center", gap: "6px", minWidth: 0, flex: 1 }}>
              <span style={{ width: "6px", height: "6px", borderRadius: "50%", background: dotColor, flexShrink: 0 }}></span>
              <span style={{ fontSize: "11px", fontWeight: "600", color: "#0f172a", whiteSpace: "nowrap", overflow: "hidden", textOverflow: "ellipsis" }}>
                {p.name}
              </span>
            </div>
            <span style={{ fontFamily: "monospace", fontSize: "10px", fontWeight: "700", color: "#334155", background: "#f1f5f9", padding: "1px 5px", borderRadius: "3px", marginLeft: "4px", flexShrink: 0 }}>
              {p.priority_score || p.priority || 80}
            </span>
          </div>
        ))}
      </div>
    );
  };

  return (
    <div style={{ background: "#ffffff", border: "1px solid #e2e8f0", borderRadius: "8px", padding: "14px", marginTop: "12px" }}>
      <div style={{ marginBottom: "10px" }}>
        <span style={{ fontSize: "10px", fontWeight: "700", color: "#64748b", letterSpacing: "0.5px", textTransform: "uppercase" }}>
          Portfolio Allocation
        </span>
        <h3 style={{ fontSize: "13px", fontWeight: "700", color: "#0f172a", margin: "2px 0 0 0" }}>
          Strategic 2×2 Matrix
        </h3>
        <span style={{ fontSize: "11px", color: "#94a3b8" }}>Impact vs. Implementation Effort</span>
      </div>

      {/* 2x2 Grid */}
      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "8px" }}>
        {/* Quick Wins */}
        <div style={{ background: "#f0fdf4", border: "1px solid #bbf7d0", borderRadius: "6px", padding: "8px", minHeight: "90px" }}>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
            <span style={{ fontSize: "11px", fontWeight: "700", color: "#166534" }}>Quick Wins</span>
            <span style={{ fontSize: "9px", fontWeight: "600", color: "#15803d", background: "#dcfce7", padding: "1px 4px", borderRadius: "3px", whiteSpace: "nowrap" }}>High I / Low E</span>
          </div>
          {renderList(quickWins, "#16a34a")}
        </div>

        {/* Strategic Bets */}
        <div style={{ background: "#eff6ff", border: "1px solid #bfdbfe", borderRadius: "6px", padding: "8px", minHeight: "90px" }}>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
            <span style={{ fontSize: "11px", fontWeight: "700", color: "#1e40af" }}>Strategic Bets</span>
            <span style={{ fontSize: "9px", fontWeight: "600", color: "#1d4ed8", background: "#dbeafe", padding: "1px 4px", borderRadius: "3px", whiteSpace: "nowrap" }}>High I / High E</span>
          </div>
          {renderList(strategicBets, "#2563eb")}
        </div>

        {/* Operational Wins */}
        <div style={{ background: "#fffbeb", border: "1px solid #fde68a", borderRadius: "6px", padding: "8px", minHeight: "90px" }}>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
            <span style={{ fontSize: "11px", fontWeight: "700", color: "#92400e" }}>Operational</span>
            <span style={{ fontSize: "9px", fontWeight: "600", color: "#b45309", background: "#fef3c7", padding: "1px 4px", borderRadius: "3px", whiteSpace: "nowrap" }}>Low I / Low E</span>
          </div>
          {renderList(operationalWins, "#d97706")}
        </div>

        {/* Re-evaluate / Defer */}
        <div style={{ background: "#f8fafc", border: "1px solid #e2e8f0", borderRadius: "6px", padding: "8px", minHeight: "90px" }}>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
            <span style={{ fontSize: "11px", fontWeight: "700", color: "#475569" }}>Re-evaluate</span>
            <span style={{ fontSize: "9px", fontWeight: "600", color: "#64748b", background: "#e2e8f0", padding: "1px 4px", borderRadius: "3px", whiteSpace: "nowrap" }}>Low I / High E</span>
          </div>
          {renderList(deferList, "#64748b")}
        </div>
      </div>

      <div style={{ display: "flex", justifyContent: "space-between", fontSize: "9px", fontWeight: "700", color: "#94a3b8", marginTop: "8px", textTransform: "uppercase" }}>
        <span>← Lower Effort</span>
        <span>Higher Effort →</span>
      </div>
    </div>
  );
}