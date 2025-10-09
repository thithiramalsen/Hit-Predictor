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
      <select
        className="input"
        value={selected?.id || ""}
        onChange={e => {
          const model = models.find(m => m.id === e.target.value);
          onSelect(model);
        }}
        disabled={status !== 'ready'}
      >
        {status === 'loading' && <option>Warming up the models...</option>}
        {status === 'error' && <option>Error loading models</option>}
        {status === 'ready' && (
          <>
            <option value="">-- Choose Model --</option>
            {models.map(model => (
              <option key={model.id} value={model.id}>{model.label}</option>
            ))}
          </>
        )}
      </select>
    </div>
  );
}