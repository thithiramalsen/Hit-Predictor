import React from 'react';

export function PrivacyPage() {
  return (
    <div className="bg-spotify-darkgray rounded-lg p-8 text-spotify-lightgray space-y-4">
      <h1 className="text-3xl font-bold text-white mb-4">Privacy & Usage Policy</h1>
      <h2 className="text-xl font-semibold text-white">Data Usage</h2>
      <p>
        When you upload a screenshot, the image is temporarily processed on our server to extract musical features using Optical Character Recognition (OCR). The image file is deleted immediately after processing and is not stored.
      </p>
      <p>
        The extracted musical data (e.g., tempo, key, danceability) is used to make a prediction and may be stored anonymously in your browser's local storage to provide a prediction history. This data is not sent to or stored on our servers permanently.
      </p>
      <h2 className="text-xl font-semibold text-white mt-4">Disclaimer</h2>
      <p>
        This tool is provided for educational and entertainment purposes only. The predictions are based on statistical models and are not a guarantee of a song's future performance.
      </p>
      <p>This application is not affiliated with, endorsed, or sponsored by Spotify. The use of the Spotify name and theme is for thematic and demonstrative purposes only.</p>
    </div>
  );
}