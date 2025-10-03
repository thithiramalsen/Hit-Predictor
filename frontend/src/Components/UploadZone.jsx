import { useRef, useEffect } from "react";
import { ArrowUpTrayIcon } from "@heroicons/react/24/outline";

export function UploadZone({ onUpload, loading }) {
  const fileInputRef = useRef();

  const handleDrop = (e) => {
    e.preventDefault();
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      onUpload(e.dataTransfer.files[0]);
    }
  };

  const handlePaste = (e) => {
    const items = e.clipboardData.items;
    for (const item of items) {
      if (item.kind === "file") {
        const file = item.getAsFile();
        if (file) {
          onUpload(file);
        }
      }
    }
  };

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      onUpload(e.target.files[0]);
    }
  };

  useEffect(() => {
    window.addEventListener("paste", handlePaste);
    return () => {
      window.removeEventListener("paste", handlePaste);
    };
  }, [onUpload]);

  return (
    <div
      className="relative overflow-hidden border-2 border-dashed border-spotify-lightgray/30 rounded-2xl p-10 flex flex-col items-center justify-center cursor-pointer bg-spotify-darkgray/70 hover:border-spotify-green transition-all duration-300 focus:outline-none focus:ring-2 focus:ring-spotify-green/60"
      onDrop={handleDrop}
      onDragOver={(e) => e.preventDefault()}
      tabIndex={0}
      onClick={() => fileInputRef.current.click()}
      style={{ minHeight: 220 }}
    >
      {/* Background accents */}
      <div className="pointer-events-none absolute -top-14 -left-14 w-40 h-40 rounded-full bg-spotify-green/10 blur-2xl animate-float" />
      <div className="pointer-events-none absolute -bottom-16 -right-20 w-56 h-56 rounded-full bg-spotify-green/10 blur-3xl animate-float" style={{animationDelay:'400ms'}}/>

      {/* Glow ring on hover */}
      <div className="pointer-events-none absolute inset-0 rounded-2xl ring-0 group-hover:ring-2 ring-spotify-green/30 transition-all" />
      <input
        type="file"
        accept="image/*"
        ref={fileInputRef}
        className="hidden"
        onChange={handleFileChange}
      />
      {/* Vinyl + arrow motif */}
      <div className="relative mb-4">
        <svg className="w-16 h-16 animate-spin-slow" viewBox="0 0 100 100" fill="none">
          <circle cx="50" cy="50" r="46" stroke="rgba(255,255,255,0.12)" strokeWidth="4" />
          <circle cx="50" cy="50" r="30" stroke="rgba(29,185,84,0.5)" strokeWidth="2" />
          <circle cx="50" cy="50" r="6" fill="#1DB954" />
        </svg>
        <ArrowUpTrayIcon className="w-8 h-8 text-spotify-green absolute inset-0 m-auto animate-bounce" />
      </div>
      <span className="text-lg font-semibold text-white">Click to upload, or drag and drop</span>
      <span className="text-sm text-spotify-lightgray mt-1">PNG, JPG, or JPEG • Tip: paste image from clipboard</span>

      {loading && (
        <div className="absolute inset-0 rounded-2xl bg-black/40 backdrop-blur-sm flex items-center justify-center">
          <span className="text-white font-semibold animate-pulse">Extracting features...</span>
        </div>
      )}
    </div>
  );
}