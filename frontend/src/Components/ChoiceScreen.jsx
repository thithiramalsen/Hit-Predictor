import React from 'react';
import { ArrowUpTrayIcon, PencilSquareIcon, LinkIcon } from '@heroicons/react/24/outline';

export function ChoiceScreen({ onUploadClick, onManualClick }) {
  return (
    <div className="relative overflow-hidden bg-spotify-darkgray/70 rounded-2xl p-8 border border-spotify-lightgray/10 shadow-spotify">
      {/* Background accents */}
      <div className="pointer-events-none absolute -top-16 -left-16 w-56 h-56 rounded-full bg-spotify-green/10 blur-3xl animate-float" />
      <div className="pointer-events-none absolute -bottom-20 -right-20 w-72 h-72 rounded-full bg-spotify-green/10 blur-3xl animate-float" style={{animationDelay:'500ms'}}/>
      <h2 className="text-2xl font-bold text-center text-white mb-6">How would you like to input song data?</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Upload Option */}
        <button onClick={onUploadClick} className="group relative overflow-hidden flex flex-col items-center justify-center p-8 bg-spotify-black rounded-xl hover:bg-spotify-lightgray/10 active:scale-[0.98] transition-all duration-300 border border-spotify-lightgray/10 hover:shadow-spotify">
          <div className="absolute -inset-12 opacity-0 group-hover:opacity-30 bg-gradient-to-r from-spotify-green/40 to-transparent blur-3xl transition-opacity"></div>
          {/* Vinyl disc */}
          <svg className="mb-4 w-14 h-14 group-hover:rotate-12 transition-transform" viewBox="0 0 100 100" fill="none">
            <circle cx="50" cy="50" r="45" stroke="rgba(255,255,255,0.12)" strokeWidth="4" />
            <circle cx="50" cy="50" r="30" stroke="rgba(29,185,84,0.45)" strokeWidth="2" />
            <circle cx="50" cy="50" r="6" fill="#1DB954" />
          </svg>
          <span className="text-lg font-semibold text-white">Upload Screenshot</span>
          <span className="text-sm text-spotify-lightgray mt-1 text-center">Automatically extract features from an image.</span>
        </button>

        {/* Manual Entry Option */}
        <button onClick={onManualClick} className="group relative overflow-hidden flex flex-col items-center justify-center p-8 bg-spotify-black rounded-xl hover:bg-spotify-lightgray/10 active:scale-[0.98] transition-all duration-300 border border-spotify-lightgray/10 hover:shadow-spotify">
          <div className="absolute -inset-12 opacity-0 group-hover:opacity-30 bg-gradient-to-r from-transparent to-spotify-green/40 blur-3xl transition-opacity"></div>
          {/* Musical note */}
          <svg className="mb-4 w-14 h-14 text-spotify-green group-hover:translate-y-[-2px] transition-transform" viewBox="0 0 24 24" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
            <path d="M9 3v12.132A3.5 3.5 0 1 1 7 12.5V6h10V3H9z"/>
          </svg>
          <span className="text-lg font-semibold text-white">Enter Manually</span>
          <span className="text-sm text-spotify-lightgray mt-1 text-center">Input the song feature values directly.</span>
        </button>
      </div>
    </div>
  );
}