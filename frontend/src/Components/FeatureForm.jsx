import React from "react";
import { SliderInput } from "./SliderInput";

const KEY_OPTIONS = [
  "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"
];

export function FeatureForm({ features, onChange, image }) {
  console.log("FeatureForm received features:", features); // Debug

  const handleInputChange = (key, value) => {
    onChange({ ...features, [key]: value });
  };

  // Helper to split duration_min into mins and secs
  const durationMin = parseFloat(features.duration_min || 0);
  const mins = Math.floor(durationMin);
  const secs = Math.round((durationMin - mins) * 60);

  const sliderFields = new Set([
    "happiness", "danceability", "energy", "acousticness",
    "instrumentalness", "liveness", "speechiness", "valence" // Add valence here
  ]);

  const allFields = [
    "danceability", "energy", "loudness", "tempo", "happiness",
    "acousticness", "instrumentalness", "liveness", "speechiness",
    "duration_min", "key", "mode", "explicit"
  ];

  return (
    <div className="bg-spotify-darkgray rounded-lg p-6 space-y-6">
      {image && (
        <div className="flex justify-center mb-4">
          <img src={image} alt="Uploaded Screenshot" className="max-h-96 rounded-lg" />
        </div>
      )}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
      {allFields.map((key) => {
        // Use 'valence' for the 'happiness' slider, otherwise use the feature's key.
        const featureKey = key === 'happiness' ? 'valence' : key;
        let value = features[featureKey] ?? "";

        if (sliderFields.has(key)) {
          return (
            <SliderInput 
              key={key} 
              label={key} 
              value={value > 1 ? value : value * 100} onChange={v => handleInputChange(featureKey, v / 100)} />
          );
        }
        if (key === "explicit") {
          return (
            <div key={key} className="flex flex-col">
              <label className="mb-1 text-spotify-green font-semibold capitalize">{key.replace(/_/g, " ")}</label>
              <select
                className="input"
                value={String(value)}
                onChange={e => handleInputChange(key, e.target.value)}
              >
                <option value="0">No</option>
                <option value="1">Yes</option>
              </select>
            </div>
          );
        }
        if (key === "key") {
          return (
            <div key={key} className="flex flex-col">
              <label className="mb-1 text-spotify-green font-semibold">Key</label>
              <select
                className="input"
                value={Number(value)} // <-- ensure value is a number
                onChange={e => handleInputChange("key", Number(e.target.value))}
              >
                {KEY_OPTIONS.map((k, idx) => (
                  <option key={k} value={idx}>{k}</option> // <-- value is a number
                ))}
              </select>
            </div>
          );
        }
        if (key === "mode") {
          return (
            <div key={key} className="flex flex-col">
              <label className="mb-1 text-spotify-green font-semibold">Mode</label>
              <select
                className="input"
                value={Number(value)} // <-- ensure value is a number
                onChange={e => handleInputChange("mode", Number(e.target.value))}
              >
                <option value={1}>Major</option>
                <option value={0}>Minor</option>
              </select>
            </div>
          );
        }
        if (key === "duration_min") {
          return (
            <div key={key} className="flex flex-col">
              <label className="mb-1 text-spotify-green font-semibold">Duration</label>
              <div className="flex gap-2">
                <input
                  className="input w-1/2"
                  type="number"
                  min={0}
                  value={mins}
                  onChange={e => {
                    const newMins = parseInt(e.target.value) || 0;
                    onChange({
                      ...features,
                      duration_min: (newMins + secs / 60).toFixed(6)
                    });
                  }}
                />
                <span className="self-center">min</span>
                <input
                  className="input w-1/2"
                  type="number"
                  min={0}
                  max={59}
                  value={secs}
                  onChange={e => {
                    const newSecs = parseInt(e.target.value) || 0;
                    onChange({
                      ...features,
                      duration_min: (mins + newSecs / 60).toFixed(6)
                    });
                  }}
                />
                <span className="self-center">sec</span>
              </div>
            </div>
          );
        }
        // Default: numeric input
        return (
          <div key={key} className="flex flex-col">
            <label className="mb-1 text-spotify-green font-semibold capitalize">{key.replace(/_/g, " ")}</label>
            <input
              className="input"
              type="number"
              step="any"
              value={value}
              onChange={e => handleInputChange(key, e.target.value)}
            />
          </div>
        );
      })}
      </div>
    </div>
  );
}