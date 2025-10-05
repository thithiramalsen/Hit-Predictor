import React from 'react';
import { SpectrumVisualizer } from './SpectrumVisualizer';

export function LandingPage({ onGetStarted }) {
  return (
    <div className="relative overflow-hidden min-h-[calc(100vh-4rem)]">
      {/* Animated gradient backdrop */}
      <div className="absolute inset-0 -z-10 opacity-80 bg-particles" style={{
        backgroundImage: 'linear-gradient(120deg, rgba(29,185,84,0.15), rgba(25,20,20,0.0), rgba(29,185,84,0.15))',
        backgroundSize: '200% 200%'
      }}>
        <div className="w-full h-full animate-gradient-move"></div>
      </div>

      {/* Subtle grid */}
      <div className="pointer-events-none absolute inset-0 -z-10 opacity-[0.06]" style={{
        backgroundImage: "linear-gradient(rgba(255,255,255,0.08) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.08) 1px, transparent 1px)",
        backgroundSize: '48px 48px'
      }}></div>

      {/* Floating decorative blobs */}
      <div className="absolute top-24 left-10 w-40 h-40 rounded-full bg-spotify-green/10 blur-2xl animate-float" />
      <div className="absolute bottom-16 right-16 w-56 h-56 rounded-full bg-spotify-green/15 blur-3xl animate-float" style={{animationDelay:'400ms'}}/>
      <div className="absolute top-1/3 right-1/4 w-24 h-24 rounded-full bg-spotify-green/10 blur-xl animate-float" style={{animationDelay:'800ms'}}/>

      {/* HERO CONTAINER */}
      <div className="max-w-6xl mx-auto px-6 text-center py-16 md:py-24 flex flex-col items-center">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-spotify-darkgray/70 border border-spotify-lightgray/20 mb-6 animate-float">
          <span className="w-1.5 h-1.5 rounded-full bg-spotify-green animate-pulse"></span>
          <span className="text-xs text-spotify-lightgray">AI-Powered Music Insights</span>
        </div>
        <h1 className="text-4xl md:text-6xl font-extrabold text-white mb-4 tracking-tight glow-text">
          Predict the Next Big Hit
        </h1>
        <p className="text-base md:text-xl text-spotify-lightgray mb-10 max-w-2xl mx-auto fade-in">
          Analyze song features like energy, danceability, tempo and more to forecast popularity. Upload a screenshot or enter data manually.
        </p>

        {/* Equalizer motif */}
        <div className="flex items-end justify-center gap-1 h-16 mb-8">
          <span className="w-1.5 bg-spotify-green/80 origin-bottom animate-equalize" style={{animationDelay:'0ms'}}></span>
          <span className="w-1.5 bg-spotify-green/70 origin-bottom animate-equalize-slow" style={{animationDelay:'150ms'}}></span>
          <span className="w-1.5 bg-spotify-green/90 origin-bottom animate-equalize-fast" style={{animationDelay:'300ms'}}></span>
          <span className="w-1.5 bg-spotify-green/70 origin-bottom animate-equalize" style={{animationDelay:'450ms'}}></span>
          <span className="w-1.5 bg-spotify-green/80 origin-bottom animate-equalize-slow" style={{animationDelay:'600ms'}}></span>
          <span className="w-1.5 bg-spotify-green/60 origin-bottom animate-equalize-fast" style={{animationDelay:'750ms'}}></span>
        </div>

        <div className="w-full max-w-3xl mx-auto mb-10">
          <SpectrumVisualizer height={160} />
        </div>

        <div className="flex items-center justify-center gap-4">
          <button onClick={onGetStarted} className="btn btn-primary btn-lg animate-pulse-glow shadow-spotify">
            Get Started
          </button>
          <button onClick={() => onGetStarted && onGetStarted()} className="btn btn-secondary btn-lg">
            Try Demo
          </button>
        </div>
      </div>

      {/* Feature cards */}
      <div className="max-w-6xl mx-auto px-6 pb-20 grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="h-full rounded-2xl bg-spotify-darkgray/70 border border-spotify-lightgray/10 p-6 hover:shadow-spotify transition-all flex flex-col">
          <div className="mb-4">
            <svg className="w-10 h-10 text-spotify-green" viewBox="0 0 24 24" fill="currentColor"><path d="M4 5h16v14H4zM8 3h8v2H8z"/></svg>
          </div>
          <h3 className="text-white font-semibold mb-2">Upload a Screenshot</h3>
          <p className="text-sm text-spotify-lightgray">Drop a Spotify stats image and we’ll extract features automatically.</p>
        </div>
        <div className="h-full rounded-2xl bg-spotify-darkgray/70 border border-spotify-lightgray/10 p-6 hover:shadow-spotify transition-all flex flex-col">
          <div className="mb-4">
            <svg className="w-10 h-10 text-spotify-green" viewBox="0 0 24 24" fill="currentColor"><path d="M12 3l9 4-9 4-9-4 9-4zm9 7l-9 4-9-4v7l9 4 9-4v-7z"/></svg>
          </div>
          <h3 className="text-white font-semibold mb-2">AI Analyzes Song Features</h3>
          <p className="text-sm text-spotify-lightgray">Our models parse energy, tempo, danceability and more.</p>
        </div>
        <div className="h-full rounded-2xl bg-spotify-darkgray/70 border border-spotify-lightgray/10 p-6 hover:shadow-spotify transition-all flex flex-col">
          <div className="mb-4">
            <svg className="w-10 h-10 text-spotify-green" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2a10 10 0 100 20 10 10 0 000-20zm1 5h-2v6h6v-2h-4V7z"/></svg>
          </div>
          <h3 className="text-white font-semibold mb-2">Get Popularity Prediction</h3>
          <p className="text-sm text-spotify-lightgray">Receive an instant popularity score or hit classification.</p>
        </div>
      </div>

      {/* Footer */}
      <footer className="border-t border-spotify-lightgray/10 py-6 text-center text-sm text-spotify-lightgray/80">
        <div className="max-w-6xl mx-auto px-6">
          <div className="opacity-60">© {new Date().getFullYear()} Hit Predictor. All rights reserved.</div>
        </div>
      </footer>
    </div>
  );
}