import React, { useEffect, useState } from "react";
import { api } from "../services/api";

// Define user-friendly labels for your top models
const MODEL_MAP = {
  'xgboost_regression': 'Predict Popularity Score (0-100)',
  'neuralnet_classification': 'Will it be a Hit?'
};

export function ModelDropdown({ selected, onSelect, onModelsLoaded }) {
  const [models, setModels] = useState([]);
  const [status, setStatus] = useState('loading'); // 'loading', 'ready', 'error'
  const [progress, setProgress] = useState(0);

  useEffect(() => {
    // Function to fetch the models once the backend is ready
    const fetchModels = () => {
      api.getModels()
        .then(models => {
          const filteredAndMapped = models
            .filter(m => MODEL_MAP[m.id])
            .map(m => ({ ...m, label: MODEL_MAP[m.id] }));
          
          if (onModelsLoaded) {
            onModelsLoaded(filteredAndMapped);
          }
          setModels(filteredAndMapped);
          setStatus('ready');
        })
        .catch(error => {
          console.error("Failed to fetch models:", error);
          setStatus('error');
        });
    };

    // Poll the backend status endpoint
    const intervalId = setInterval(async () => {
      try {
        const backendStatus = await api.getStatus();
        // Update percent if provided by backend
        if (typeof backendStatus.progress === 'number') {
          setProgress(backendStatus.progress);
        }

        if (backendStatus.models_loaded) {
          clearInterval(intervalId);
          fetchModels();
        } else if (backendStatus.loading_error) {
          clearInterval(intervalId);
          setStatus('error');
          console.error("Backend model loading error:", backendStatus.loading_error);
        }
      } catch (error) {
        console.log("Waiting for backend to be ready...");
      }
    }, 2500); // Poll every 2.5 seconds

    return () => clearInterval(intervalId); // Cleanup on unmount
  }, [onModelsLoaded]);

  return (
    <div className="flex flex-col gap-2">
      <label className="text-spotify-green font-semibold">Select Model</label>
      {status === 'loading' && (
        <div className="space-y-2">
          <div className="bg-yellow-50 border border-yellow-200 text-yellow-800 px-3 py-2 rounded">
            <div className="font-semibold">Models are loading</div>
            <div className="text-sm">Warming models on the server — this may take 10–60 seconds. Please wait.</div>
            <div className="mt-2 h-3 bg-gray-200 rounded overflow-hidden">
              <div
                className="h-3 bg-spotify-green rounded"
                style={{ width: `${Math.min(Math.max(progress, 0), 100)}%`, transition: 'width 300ms ease' }}
              />
            </div>
            <div className="text-sm mt-1">{progress ? `${progress}%` : 'Starting...'}</div>
          </div>

          <select className="input" disabled>
            <option>Warming up the models...</option>
          </select>
        </div>
      )}

      {status === 'error' && (
        <select className="input" disabled>
          <option>Error loading models</option>
        </select>
      )}

      {status === 'ready' && (
        <select
          className="input"
          value={selected?.id || ""}
          onChange={e => {
            const model = models.find(m => m.id === e.target.value);
            onSelect(model);
          }}
        >
          <option value="">-- Choose Model --</option>
          {models.map(model => (
            <option key={model.id} value={model.id}>{model.label}</option>
          ))}
        </select>
      )}
    </div>
  );
}