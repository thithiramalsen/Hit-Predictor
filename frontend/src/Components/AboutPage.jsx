import React from 'react';

export function AboutPage() {
  return (
    <div className="bg-spotify-darkgray rounded-lg p-8 text-spotify-lightgray space-y-4">
      <h1 className="text-3xl font-bold text-white mb-4">About Hit Predictor</h1>
      <p>
        Hit Predictor is a machine learning-powered application designed to forecast the potential popularity of a song based on its musical features.
      </p>
      <p>
        Our goal is to provide artists, producers, and music enthusiasts with a data-driven perspective on what makes a track resonate with listeners. By analyzing attributes like danceability, energy, tempo, and key, our models identify patterns that correlate with commercial success.
      </p>
      <p>
        This project was born from a passion for both music and data science, aiming to bridge the gap between artistic creation and analytical insight.
      </p>
    </div>
  );
}