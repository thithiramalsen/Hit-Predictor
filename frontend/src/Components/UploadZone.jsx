import { useRef, useEffect } from "react";
import { ArrowUpTrayIcon } from "@heroicons/react/24/outline";

export function UploadZone({ onUpload }) {
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
      className="border-2 border-dashed border-spotify-lightgray/30 rounded-lg p-8 flex flex-col items-center justify-center cursor-pointer bg-spotify-darkgray hover:border-spotify-green transition-colors duration-300"
      onDrop={handleDrop}
      onDragOver={(e) => e.preventDefault()}
      // onPaste is now handled globally by useEffect
      tabIndex={0}
      onClick={() => fileInputRef.current.click()}
      style={{ minHeight: 200 }}
    >
      <input
        type="file"
        accept="image/*"
        ref={fileInputRef}
        className="hidden"
        onChange={handleFileChange}
      />
      <ArrowUpTrayIcon className="w-12 h-12 text-spotify-lightgray mb-4" />
      <span className="text-lg font-semibold text-white">Click to upload, or drag and drop</span>
      <span className="text-sm text-spotify-lightgray mt-1">PNG, JPG, or JPEG</span>
    </div>
  );
}