import React from 'react';

export function NavBar() {
  return (
    <nav className="bg-spotify-black shadow-lg mb-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center">
            <span className="font-bold text-xl text-transparent bg-clip-text bg-gradient-to-r from-white to-spotify-green">
              🎵 Hit Predictor
            </span>
          </div>
        </div>
      </div>
    </nav>
  );
}