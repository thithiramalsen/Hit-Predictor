import { useRef } from "react";

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

  return (
    <div
      className="border-2 border-dashed border-spotify-green rounded-lg p-8 flex flex-col items-center justify-center cursor-pointer bg-spotify-darkgray"
      onDrop={handleDrop}
      onDragOver={(e) => e.preventDefault()}
      onPaste={handlePaste}
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
      <span className="text-lg mb-2">Drag & drop, paste, or click to upload a screenshot</span>
      <span className="text-spotify-green text-sm">Supported: PNG, JPG, JPEG</span>
    </div>
  );
}