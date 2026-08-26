import React from "react";

export default function ExecutiveExportButton({ processName }) {
  const handlePrint = () => {
    window.print();
  };

  return (
    <button onClick={handlePrint} className="btn-export">
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
        <path d="M6 9V2h12v7M6 18H4a2 2 0 01-2-2v-5a2 2 0 012-2h16a2 2 0 012 2v5a2 2 0 01-2 2h-2" />
        <path d="M6 14h12v8H6z" />
      </svg>
      Export Executive Brief
    </button>
  );
}