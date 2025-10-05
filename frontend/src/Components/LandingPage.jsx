import React from 'react';

export function LandingPage({ onGetStarted }) {
  return (
    <div className="text-center py-16">
      <h1 className="text-5xl font-bold text-white mb-4">Predict the Next Big Hit</h1>
      <p className="text-xl text-spotify-lightgray mb-8 max-w-2xl mx-auto">
        Use machine learning to analyze song features and predict its popularity.
        Upload a screenshot or enter data manually to get started.
      </p>
      <button onClick={onGetStarted} className="btn btn-primary btn-lg shadow-lg shadow-spotify-green/30">
        Get Started
      </button>
    </div>
  );
}