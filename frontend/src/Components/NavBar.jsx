import React from 'react';

export function NavBar({ onTitleClick, onAboutClick, onPrivacyClick, onContactClick }) {
  return (
    <nav className="sticky top-0 z-40 bg-spotify-black/70 backdrop-blur supports-[backdrop-filter]:bg-spotify-black/60 shadow-lg mb-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center">
            <button onClick={onTitleClick} className="focus:outline-none">
              <span className="font-bold text-xl text-transparent bg-clip-text bg-gradient-to-r from-white to-spotify-green hover:from-spotify-green hover:to-white transition-colors">
                🎵 Hit Predictor
              </span>
            </button>
          </div>
          <div className="flex items-center space-x-4 text-sm font-semibold">
            <button onClick={onAboutClick} className="text-spotify-lightgray hover:text-white transition-colors hover:scale-105">
              About
            </button>
            <button onClick={onPrivacyClick} className="text-spotify-lightgray hover:text-white transition-colors hover:scale-105">
              Privacy
            </button>
            <button onClick={onContactClick} className="text-spotify-lightgray hover:text-white transition-colors hover:scale-105">
              Contact
            </button>
          </div>
        </div>
      </div>
    </nav>
  );
}