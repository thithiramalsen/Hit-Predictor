import React from 'react';
import { ArrowUpTrayIcon, PencilSquareIcon, LinkIcon } from '@heroicons/react/24/outline';

export function ChoiceScreen({ onUploadClick, onManualClick }) {
  return (
    <div className="bg-spotify-darkgray rounded-lg p-8">
      <h2 className="text-2xl font-bold text-center text-white mb-6">How would you like to input song data?</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Upload Option */}
        <button onClick={onUploadClick} className="flex flex-col items-center justify-center p-8 bg-spotify-black rounded-lg hover:bg-spotify-lightgray/10 transition-colors duration-200">
          <ArrowUpTrayIcon className="w-12 h-12 text-spotify-green mb-4" />
          <span className="text-lg font-semibold text-white">Upload Screenshot</span>
          <span className="text-sm text-spotify-lightgray mt-1 text-center">Automatically extract features from an image.</span>
        </button>

        {/* Manual Entry Option */}
        <button onClick={onManualClick} className="flex flex-col items-center justify-center p-8 bg-spotify-black rounded-lg hover:bg-spotify-lightgray/10 transition-colors duration-200">
          <PencilSquareIcon className="w-12 h-12 text-spotify-green mb-4" />
          <span className="text-lg font-semibold text-white">Enter Manually</span>
          <span className="text-sm text-spotify-lightgray mt-1 text-center">Input the song feature values directly.</span>
        </button>
      </div>
    </div>
  );
}