import React, { useState, useEffect } from "react";
import "./App.css";
import PrioritizationMatrix from "./components/PrioritizationMatrix";
import ScoreBreakdown from "./components/ScoreBreakdown";
import ExecutiveExportButton from "./components/ExecutiveExportButton";

const API_BASE = "http://127.0.0.1:8000";

export default function App() {
  const [processName, setProcessName] = useState("Invoice Processing");
  const [department, setDepartment] = useState("Finance");
  const [description, setDescription] = useState(
    "The finance team receives invoices from vendors, extracts invoice details, validates the information, matches invoices with purchase orders, obtains approval, and processes payments."
  );
  const [activities, setActivities] = useState([
    "Receive invoices from vendors",
    "Extract invoice details",
    "Validate invoice information",
    "Match invoice with purchase order",
    "Send invoice for approval",
    "Process payment",
  ]);

  const [loading, setLoading] = useState(false);
  const [analysisResult, setAnalysisResult] = useState(null);
  const [library, setLibrary] = useState([]);
  const [activeTab, setActiveTab] = useState("matrix"); // 'matrix' | 'library'

  const fetchLibrary = async () => {
    try {
      const res = await fetch(`${API_BASE}/processes`);
      if (res.ok) {
        const data = await res.json();
        setLibrary(data);
        if (!analysisResult && data.length > 0 && data[0].analysis_result) {
          setAnalysisResult(data[0].analysis_result);
        }
      }
    } catch (err) {
      console.warn("Backend offline or unreachable.");
    }
  };

  useEffect(() => {
    fetchLibrary();
  }, []);

  const handleAddActivity = () => setActivities([...activities, ""]);
  const handleActivityChange = (index, value) => {
    const updated = [...activities];
    updated[index] = value;
    setActivities(updated);
  };
  const handleRemoveActivity = (index) => setActivities(activities.filter((_, i) => i !== index));

  const handleAnalyze = async () => {
    const cleaned = activities.filter((a) => a.trim().length > 0);
    if (!processName || cleaned.length === 0) {
      alert("Please provide a Process Name and at least one activity.");
      return;
    }

    setLoading(true);
    try {
      const res = await fetch(`${API_BASE}/processes`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          name: processName,
          department: department || "General",
          description,
          activities: cleaned,
        }),
      });

      if (res.ok) {
        const data = await res.json();
        setAnalysisResult(data);
        fetchLibrary();
      }
    } catch (err) {
      console.error(err);
      alert("Error connecting to backend API.");
    } finally {
      setLoading(false);
    }
  };

  const handleSelectProcess = (item) => {
    setProcessName(item.name);
    setDepartment(item.department);
    setDescription(item.description || "");
    setActivities(item.activities || []);
    if (item.analysis_result) {
      setAnalysisResult(item.analysis_result);
    }
  };

  return (
    <div className="enterprise-layout">
      {/* Global Navigation Header */}
      <header className="global-header">
        <div className="brand-group">
          <div className="brand-badge">PIQ</div>
          <div>
            <h1 className="brand-title">ProcessIQ</h1>
            <span className="brand-sub">Enterprise AI Decision Intelligence</span>
          </div>
        </div>
        <div className="header-meta">
          <span className="environment-tag">Production Demo</span>
          <span className="status-indicator"></span>
        </div>
      </header>

      {/* Main Workspace: 2-Column Split */}
      <div className="workspace-container">
        
        {/* LEFT COLUMN: Input & Portfolio Management */}
        <aside className="left-panel">
          <div className="panel-card">
            <div className="card-header-clean">
              <span className="step-tag">01 / INPUT WORKSPACE</span>
              <h2 className="panel-title">Process Definition</h2>
            </div>

            <div className="form-stack">
              <div className="input-group">
                <label>Process Name</label>
                <input
                  type="text"
                  value={processName}
                  onChange={(e) => setProcessName(e.target.value)}
                  placeholder="e.g. Accounts Payable Invoicing"
                />
              </div>

              <div className="input-group">
                <label>Department / Business Unit</label>
                <input
                  type="text"
                  value={department}
                  onChange={(e) => setDepartment(e.target.value)}
                  placeholder="e.g. Finance Operations"
                />
              </div>

              <div className="input-group">
                <label>Workflow Description</label>
                <textarea
                  rows={3}
                  value={description}
                  onChange={(e) => setDescription(e.target.value)}
                  placeholder="Executive overview of the operational workflow..."
                />
              </div>

              <div className="activities-container">
                <div className="activities-label-row">
                  <label>Operational Activities ({activities.length})</label>
                  <button type="button" onClick={handleAddActivity} className="btn-text-action">
                    + Add Step
                  </button>
                </div>

                <div className="activity-list-scroll">
                  {activities.map((act, index) => (
                    <div key={index} className="activity-row-item">
                      <span className="step-num">{String(index + 1).padStart(2, "0")}</span>
                      <input
                        type="text"
                        value={act}
                        onChange={(e) => handleActivityChange(index, e.target.value)}
                        placeholder="Define operational task..."
                      />
                      {activities.length > 1 && (
                        <button
                          type="button"
                          onClick={() => handleRemoveActivity(index)}
                          className="btn-del"
                        >
                          ✕
                        </button>
                      )}
                    </div>
                  ))}
                </div>
              </div>

              <button onClick={handleAnalyze} disabled={loading} className="btn-execute">
                {loading ? "Evaluating Decision Intelligence..." : "Run AI Case Analysis →"}
              </button>
            </div>
          </div>

          {/* Portfolio Tabs (Matrix / Library) */}
          <div className="panel-card mt-16">
            <div className="tab-switch-row">
              <button
                className={`tab-btn ${activeTab === "matrix" ? "active" : ""}`}
                onClick={() => setActiveTab("matrix")}
              >
                2x2 Strategic Matrix
              </button>
              <button
                className={`tab-btn ${activeTab === "library" ? "active" : ""}`}
                onClick={() => setActiveTab("library")}
              >
                Process Library ({library.length})
              </button>
            </div>

            {activeTab === "matrix" ? (
              <PrioritizationMatrix
                processes={library.map((l) => ({
                  id: l.id,
                  name: l.name,
                  priority_score: l.priority_score,
                  impact: l.analysis_result?.dimensions?.business_impact?.score || 4.0,
                  effort: l.analysis_result?.dimensions?.implementation_effort?.score || 2.5,
                }))}
                currentProcessId={analysisResult?.id}
                onSelectProcess={(id) => {
                  const match = library.find((p) => p.id === id);
                  if (match) handleSelectProcess(match);
                }}
              />
            ) : (
              <div className="library-compact-list">
                {library.map((item) => (
                  <div
                    key={item.id}
                    onClick={() => handleSelectProcess(item)}
                    className={`library-compact-card ${analysisResult?.process_name === item.name ? "selected" : ""}`}
                  >
                    <div>
                      <div className="lib-item-name">{item.name}</div>
                      <div className="lib-item-dept">{item.department}</div>
                    </div>
                    <div className="lib-score-tag">{item.priority_score}/100</div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </aside>

        {/* RIGHT COLUMN: Analysis Dashboard & Report */}
        <main className="right-panel">
          {analysisResult ? (
            <div className="report-card">
              {/* Report Header */}
              <div className="report-header">
                <div>
                  <span className="step-tag">02 / EXECUTIVE DECISION BRIEF</span>
                  <h2 className="report-title">{analysisResult.process_name}</h2>
                  <p className="report-dept-badge">{analysisResult.department} Strategy Review</p>
                </div>
                <ExecutiveExportButton processName={analysisResult.process_name} />
              </div>

              {/* Summary Metrics Bar */}
              <div className="summary-metrics-bar">
                <div className="metric-box hero-metric">
                  <span className="metric-lbl">PRIORITY SCORE</span>
                  <div className="metric-val-hero">{analysisResult.priority_score}<span>/100</span></div>
                  <span className="metric-status-pill pill-green">High Value Target</span>
                </div>
                <div className="metric-box">
                  <span className="metric-lbl">AI Opportunity</span>
                  <div className="metric-val text-green">{analysisResult.ai_opportunity}</div>
                </div>
                <div className="metric-box">
                  <span className="metric-lbl">Automation Potential</span>
                  <div className="metric-val text-blue">{analysisResult.automation_potential}</div>
                </div>
                <div className="metric-box">
                  <span className="metric-lbl">Human Oversight</span>
                  <div className="metric-val text-amber">{analysisResult.human_involvement}</div>
                </div>
              </div>

              {/* Explainable Decision Logic */}
              <ScoreBreakdown
                dimensions={analysisResult.dimensions}
                priorityScore={analysisResult.priority_score}
                quadrant={analysisResult.quadrant}
              />

              {/* Clean Activity Breakdown Table */}
              <div className="intel-block">
                <h3 className="block-title">Activity-Level Automation & AI Taxonomy</h3>
                <div className="table-responsive">
                  <table className="enterprise-table">
                    <thead>
                      <tr>
                        <th style={{ width: "40px" }}>#</th>
                        <th>Activity Description</th>
                        <th>Recommended Action</th>
                        <th>AI / Auto</th>
                        <th>Governance</th>
                        <th>Target Stack</th>
                      </tr>
                    </thead>
                    <tbody>
                      {analysisResult.activities_intelligence?.map((act) => (
                        <tr key={act.id}>
                          <td className="text-muted font-mono">{act.id}</td>
                          <td className="font-semibold">{act.title}</td>
                          <td>
                            <span className={`status-pill ${
                              act.human === "High" ? "pill-amber" : act.auto === "High" ? "pill-green" : "pill-blue"
                            }`}>
                              {act.recommendation}
                            </span>
                          </td>
                          <td>
                            <span className="text-muted">AI:</span> {act.ai} · <span className="text-muted">Auto:</span> {act.auto}
                          </td>
                          <td>
                            <span className={act.human === "High" ? "text-amber font-semibold" : "text-muted"}>
                              {act.human === "High" ? "Required (HITL)" : "Low Risk"}
                            </span>
                          </td>
                          <td>
                            <div className="badge-wrap">
                              {act.tech.map((t, idx) => (
                                <span key={idx} className="tech-chip">{t}</span>
                              ))}
                            </div>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>

              {/* Two Column: Governance & Strategy */}
              <div className="two-col-grid">
                <div className="intel-box-clean">
                  <h4 className="box-title-clean text-green">Expected Business Impact</h4>
                  <ul className="clean-list">
                    {analysisResult.benefits?.map((b, i) => (
                      <li key={i}>{b}</li>
                    ))}
                  </ul>
                </div>

                <div className="intel-box-clean">
                  <h4 className="box-title-clean text-red">HITL Governance & Risks</h4>
                  <ul className="clean-list">
                    {analysisResult.risks?.map((r, i) => (
                      <li key={i}>{r}</li>
                    ))}
                  </ul>
                </div>
              </div>

              {/* Phased Roadmap */}
              <div className="intel-block">
                <h3 className="block-title">Recommended AI Transformation Roadmap</h3>
                <div className="roadmap-row">
                  <div className="road-step">
                    <span className="road-step-num">Phase 01</span>
                    <h4>Quick Wins & RPA</h4>
                    <p>Automate deterministic, rule-based extraction and repetitive data entry.</p>
                  </div>
                  <div className="road-step">
                    <span className="road-step-num">Phase 02</span>
                    <h4>Cognitive AI Assist</h4>
                    <p>Deploy LLM/IDP for document comprehension, validation, and automated routing.</p>
                  </div>
                  <div className="road-step">
                    <span className="road-step-num">Phase 03</span>
                    <h4>HITL Governance</h4>
                    <p>Establish automated validation gates with mandatory human exception handling.</p>
                  </div>
                </div>
              </div>

              {/* Report Footer */}
              <footer className="report-footer">
                <span>ProcessIQ Decision Engine v1.0</span>
                <span>CONFIDENTIAL · INTERNAL ENTERPRISE EVALUATION</span>
              </footer>
            </div>
          ) : (
            <div className="empty-state-panel">
              <p>Select a process or click "Run AI Case Analysis" to generate an executive intelligence brief.</p>
            </div>
          )}
        </main>
      </div>
    </div>
  );
}