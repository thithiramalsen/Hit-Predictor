import React from 'react';

export function SliderInput({ label, value, onChange, min = 0, max = 100, step = 1 }) {
  const percentage = ((value - min) / (max - min)) * 100;

  return (
    <div className="flex flex-col">
      <div className="flex justify-between items-baseline mb-1">
        <label className="text-spotify-green font-semibold capitalize">{label.replace(/_/g, " ")}</label>
        <span className="text-sm font-medium text-white">{Math.round(value)}</span>
      </div>
      <div className="flex items-center gap-4">
        <input
          type="range"
          min={min}
          max={max}
          step={step}
          value={value}
          onChange={e => onChange(parseFloat(e.target.value))}
          className="w-full h-2 bg-spotify-lightgray/20 rounded-lg appearance-none cursor-pointer slider-thumb"
          style={{
            background: `linear-gradient(to right, #1DB954 ${percentage}%, #4a4a4a ${percentage}%)`,
          }}
        />
      </div>
    </div>
  );
}