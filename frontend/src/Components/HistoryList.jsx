import React, { useState } from "react";
import { ChevronDownIcon, ChevronUpIcon } from "@heroicons/react/20/solid";

export function HistoryList({ predictions }) {
  const [open, setOpen] = useState(false);

  if (!predictions || predictions.length === 0) return null;

  return (
    <div className="mt-8">
      <div className="border-t border-spotify-lightgray/20 pt-8">
        <button
          className="w-full flex justify-between items-center text-left text-white"
          onClick={() => setOpen(o => !o)}
        >
          <span className="text-xl font-bold">Prediction History</span>
          {open ? <ChevronUpIcon className="w-6 h-6" /> : <ChevronDownIcon className="w-6 h-6" />}
        </button>
      </div>
      {open && (
        <div className="mt-4 space-y-4">
          {predictions.map((item, idx) => (
            <div key={idx} className="bg-spotify-darkgray rounded-lg p-4 flex justify-between items-center">
              <div>
                <div className="font-semibold text-white">{item.model?.label}</div>
                <div className="text-sm text-spotify-lightgray mt-1">
                  {new Date(item.timestamp).toLocaleString()}
                </div>
              </div>
              <div className="text-right">
                {item.prediction.predicted_popularity !== undefined
                  ? <span className="text-lg font-bold text-white">{Math.round(item.prediction.predicted_popularity)}</span>
                  : (
                    <span className={`text-lg font-bold ${item.prediction.class === "Hit" || item.prediction.class === 1 ? 'text-spotify-green' : 'text-red-500'}`}>
                      {item.prediction.class === "Hit" || item.prediction.class === 1 ? "Hit" : "Flop"}
                    </span>
                  )
                }
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}