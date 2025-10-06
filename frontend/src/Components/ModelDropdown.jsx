import React, { useEffect, useState } from "react";
import { api } from "../services/api";

// Define user-friendly labels for your top models
const MODEL_MAP = {
  'xgboost_regression': 'Predict Popularity Score (0-100)',
  'neuralnet_classification': 'Will it be a Hit?'
};

export function ModelDropdown({ selected, onSelect, onModelsLoaded }) {
  const [models, setModels] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.getModels()
      .then(models => {
        // Debug: Log the models received from the API
        console.log("All models from API:", models);
        // Filter for only the models we want to show and map their labels
        const filteredAndMapped = models
          .filter(m => MODEL_MAP[m.id])
          .map(m => ({ ...m, label: MODEL_MAP[m.id] }));
        console.log("Filtered models for dropdown:", filteredAndMapped);
        if (onModelsLoaded) {
          onModelsLoaded(filteredAndMapped);
        }
        setModels(filteredAndMapped);
      })
      .catch((error) => {
        console.error("Failed to fetch models:", error);
        setModels([]);
      })
      .finally(() => setLoading(false));
  }, []);

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
        disabled={loading}
      >
        <option value="">-- Choose Model --</option>
        {models.map(model => (
          <option key={model.id} value={model.id}>{model.label}</option>
        ))}
      </select>
    </div>
  );
}