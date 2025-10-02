import React, { useState } from 'react';
import { LinkIcon, MagnifyingGlassIcon } from '@heroicons/react/24/outline';

export function ScrapePage({ onScrape, loading }) {
  const [url, setUrl] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (url) {
      onScrape(url);
    }
  };

  return (
    <div className="bg-spotify-darkgray rounded-lg p-8">
      <h2 className="text-2xl font-bold text-center text-white mb-6">Scrape from Spotify URL</h2>
      <p className="text-center text-spotify-lightgray mb-6">
        Paste a Spotify track URL to find it on chosic.com and automatically fill the features.
      </p>
      <form onSubmit={handleSubmit} className="flex flex-col gap-4">
        <div className="relative">
          <LinkIcon className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-spotify-lightgray" />
          <input type="url" placeholder="https://open.spotify.com/track/..." value={url} onChange={e => setUrl(e.target.value)} className="input pl-10" required />
        </div>
        <button type="submit" className="btn btn-primary flex items-center justify-center gap-2" disabled={loading || !url}>
          <MagnifyingGlassIcon className="w-5 h-5" />
          {loading ? 'Scraping...' : 'Scrape Data'}
        </button>
      </form>
    </div>
  );
}