import React from 'react';

const ChevronDownIcon = (props) => (
    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor" {...props}><path strokeLinecap="round" strokeLinejoin="round" d="m19.5 8.25-7.5 7.5-7.5-7.5" /></svg>
);

const scoreVerdicts = [
  { text: "Certified Hit", color: "text-spotify-green", description: "This score suggests the song has strong potential to be a mainstream success.", score: "70+" },
  { text: "Strong Hit Potential", color: "text-green-400", description: "This song shows solid signs of becoming popular with a wide audience.", score: "60-69" },
  { text: "Mainstream Appeal", color: "text-yellow-400", description: "This track has qualities that could appeal to a broad commercial audience.", score: "50-59" },
  { text: "Niche Following", color: "text-blue-400", description: "This song is likely to find a dedicated audience within a specific genre.", score: "30-49" },
  { text: "Underground Track", color: "text-spotify-lightgray", description: "This track has unique qualities that may appeal to a more selective audience.", score: "<30" }
];

const classVerdicts = [
    { text: "Likely Hit", color: "text-spotify-green", description: "The model predicts this song has a high probability of becoming a hit." },
    { text: "Moderate Potential", color: "text-yellow-400", description: "The model sees potential for this song to gain traction and popularity." },
    { text: "Niche Appeal", color: "text-blue-400", description: "The model suggests this song will likely appeal to a specific audience." }
];

export function GradingExplanation() {
  return (
    <div className="space-y-4 mt-12">
      <details className="group bg-spotify-darkgray p-4 rounded-lg border border-spotify-lightgray/10 open:bg-spotify-lightgray/5 transition-colors">
        <summary className="flex justify-between items-center text-lg font-bold text-white cursor-pointer list-none">
          Understanding the "Popularity Score"
          <ChevronDownIcon className="w-5 h-5 text-spotify-lightgray transition-transform duration-300 group-open:rotate-180" />
        </summary>
        <div className="mt-4">
          <p className="text-spotify-lightgray mb-6">
            When you choose to predict a specific score, our XGBoost regression model analyzes the song's features to estimate its popularity on a scale from 0 to 100. Here’s what the different score ranges generally mean:
          </p>
          <div className="space-y-4">
            {scoreVerdicts.map(v => (
              <div key={v.text} className="p-4 bg-spotify-black/50 rounded-lg border border-spotify-lightgray/10">
                <div className="flex justify-between items-baseline">
                  <p className={`font-bold text-lg ${v.color}`}>{v.text}</p>
                  <p className="text-sm font-mono text-spotify-lightgray bg-spotify-black px-2 py-1 rounded">{v.score}</p>
                </div>
                <p className="text-sm text-spotify-lightgray mt-1">{v.description}</p>
              </div>
            ))}
          </div>
        </div>
      </details>

      <details className="group bg-spotify-darkgray p-4 rounded-lg border border-spotify-lightgray/10 open:bg-spotify-lightgray/5 transition-colors">
        <summary className="flex justify-between items-center text-lg font-bold text-white cursor-pointer list-none">
          Understanding the "Will it be a Hit?" Verdict
          <ChevronDownIcon className="w-5 h-5 text-spotify-lightgray transition-transform duration-300 group-open:rotate-180" />
        </summary>
        <div className="mt-4">
          <p className="text-spotify-lightgray mb-6">
            When you ask if a song will be a hit, our Neural Network classification model categorizes its potential into one of three tiers. This gives you a quick assessment of its likely market performance.
          </p>
          <div className="space-y-4">
            {classVerdicts.map(v => (
              <div key={v.text} className="p-4 bg-spotify-black/50 rounded-lg border border-spotify-lightgray/10">
                <p className={`font-bold text-lg ${v.color}`}>{v.text}</p>
                <p className="text-sm text-spotify-lightgray mt-1">{v.description}</p>
              </div>
            ))}
          </div>
        </div>
      </details>
    </div>
  );
}