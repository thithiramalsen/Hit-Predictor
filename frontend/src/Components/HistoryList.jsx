import React, { useState } from "react";

export function HistoryList({ predictions }) {
  const [open, setOpen] = useState(false);

  if (!predictions || predictions.length === 0) return null;

  return (
    <div className="mt-8">
      <button
        className="btn btn-secondary w-full mb-2"
        onClick={() => setOpen(o => !o)}
      >
        {open ? "Hide" : "Show"} Prediction History
      </button>
      {open && (
        <div className="bg-spotify-darkgray rounded-lg p-4 space-y-4">
          {predictions.map((item, idx) => (
            <div key={idx} className="border-b border-spotify-green pb-2 mb-2">
              <div className="text-sm text-spotify-lightgray">
                {new Date(item.timestamp).toLocaleString()}
              </div>
              <div className="font-semibold">{item.model?.label}</div>
              <div className="text-xs">
                Features: {Object.entries(item.features).map(([k, v]) => `${k}: ${v}`).join(", ")}
              </div>
              <div className="mt-1">
                {item.prediction.predicted_popularity !== undefined
                  ? <span>Popularity: <span className="text-spotify-green">{Math.round(item.prediction.predicted_popularity)}</span></span>
                  : <span>Class: <span className="text-spotify-green">{item.prediction.class === "Hit" || item.prediction.class === 1 ? "Hit" : "Not Hit"}</span> ({Math.round(item.prediction.probability * 100)}%)</span>
                }
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}