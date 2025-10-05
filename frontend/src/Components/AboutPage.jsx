import React from 'react';
import { GradingExplanation } from './GradingExplanation';

export function AboutPage() {
  return (
    <div className="bg-spotify-darkgray/50 rounded-lg p-8 text-spotify-lightgray leading-relaxed">
      <h1 className="text-4xl font-bold text-white mb-4">About Hit Predictor</h1>
      <p className="mb-4">
        The Hit Predictor is a final year project designed to explore the power of machine learning in the music industry. By analyzing a song's audio features—such as danceability, energy, tempo, and key—our models can forecast its potential popularity.
      </p>
      <p className="mb-4">
        We offer two primary prediction methods: a regression model (XGBoost) that provides a precise popularity score from 0 to 100, and a classification model (Neural Network) that determines if a song is likely to be a "Hit", have "Moderate Potential", or "Niche Appeal".
      </p>
      <p>
        This tool demonstrates a complete MLOps pipeline, from data preprocessing and model training to API deployment and a user-friendly web interface.
      </p>

      <GradingExplanation />
    </div>
  );
}