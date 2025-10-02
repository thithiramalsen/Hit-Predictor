import React, { useEffect, useState } from "react";
import { api } from "../services/api";

export function ModelDropdown({ selected, onSelect }) {
  const [models, setModels] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.getModels()
      .then(setModels)
      .catch(() => setModels([]))
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