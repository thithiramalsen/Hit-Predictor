import { useState } from 'react';
import { UploadZone } from './Components/UploadZone';
import { FeatureForm } from './Components/FeatureForm';
import { NavBar } from './Components/NavBar';
import { ModelDropdown } from './Components/ModelDropdown';
import { PredictionResult } from './Components/PredictionResult';
import { HistoryList } from './Components/HistoryList';
import { useLocalStorage } from './hooks/useLocalStorage';
import { api } from './services/api';
import { KEY_OPTIONS } from './utils/constants'; // or define KEY_OPTIONS in this file
//import './index.css';


const parseKey = (keyStr) => {
  const map = {
    "C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3, "E": 4, "F": 5,
    "F#": 6, "Gb": 6, "G": 7, "G#": 8, "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11
  };
  for (const note in map) {
    if (keyStr && keyStr.toUpperCase().includes(note)) return map[note];
  }
  return 0;
};
const parseMode = (keyStr) => {
  if (keyStr && keyStr.toLowerCase().includes("major")) return "1";
  if (keyStr && keyStr.toLowerCase().includes("minor")) return "0";
  return "1";
};

function App() {
  const [features, setFeatures] = useState(null);
  const [selectedModel, setSelectedModel] = useState(null);
  const [uploadedImage, setUploadedImage] = useState(null);
  const [prediction, setPrediction] = useState(null);
  const [history, setHistory] = useLocalStorage('predictions', []);

  const handleClear = () => {
    setFeatures(null);
    setSelectedModel(null);
    setUploadedImage(null);
    setPrediction(null);
  };

  const normalizeFeatures = (features) => {
    const out = { ...features };
    // Explicit normalization
    if (typeof out.explicit === "string") {
      if (out.explicit.toLowerCase() === "no") out.explicit = "0";
      else if (out.explicit.toLowerCase() === "yes") out.explicit = "1";
    } else if (typeof out.explicit === "boolean") {
      out.explicit = out.explicit ? "1" : "0";
    } else if (out.explicit === undefined) {
      out.explicit = "0";
    }
    // Key/mode normalization
    if (typeof out.key === "undefined" && typeof out.key_str === "string") {
      out.key = parseKey(out.key_str);
      out.mode = parseMode(out.key_str);
    }
    if (typeof out.mode === "undefined" && typeof out.key_str === "string") {
      out.mode = parseMode(out.key_str);
    }
    // If still missing, default to C Major
    out.key = Number(out.key ?? 0);
    out.mode = Number(out.mode ?? 1);
    // Loudness: ensure it's a number and keep negative sign
    if (typeof out.loudness === "string") {
      out.loudness = parseFloat(out.loudness);
    }
    return out;
  };

  const handleUpload = async (file) => {
    try {
      const extractedFeatures = await api.uploadImage(file);
      console.log("Raw features from backend OCR:", extractedFeatures); // Debug
      const normalized = normalizeFeatures(extractedFeatures);
      console.log("Normalized features for form:", normalized); // Debug
      setFeatures(normalized);
      setUploadedImage(URL.createObjectURL(file));
    } catch (error) {
      console.error('Upload failed:', error);
    }
  };

  const handlePredict = async () => {
    if (!selectedModel || !features) return;

    // Always normalize before prediction
    const normalized = normalizeFeatures(features);

    try {
      const result = await api.predict(selectedModel.id, normalized);
      setPrediction(result);
      setHistory(prev => [{
        model: selectedModel,
        features: normalized,
        prediction: result,
        timestamp: new Date().toISOString()
      }, ...prev.slice(0, 4)]);
    } catch (error) {
      console.error('Prediction failed:', error);
    }
  };

    return (
    <div className="min-h-screen bg-spotify-black text-white">
      <NavBar />
      <main className="max-w-4xl mx-auto p-4 space-y-8">
        {!features ? (
          <UploadZone onUpload={handleUpload} />
        ) : (
          <div className="space-y-6">
            <FeatureForm features={features} onChange={setFeatures} image={uploadedImage} />
            <ModelDropdown selected={selectedModel} onSelect={setSelectedModel} />
            <div className="grid grid-cols-2 gap-4">
              <button
                className="btn btn-secondary"
                onClick={handleClear}
              >
                Start Over
              </button>
              <button
                className="btn btn-primary shadow-lg shadow-spotify-green/20"
                onClick={handlePredict}
                disabled={!selectedModel}
              >
                Predict
              </button>
            </div>
          </div>
        )}

        {prediction && <PredictionResult prediction={prediction} />}

        <HistoryList predictions={history} />
      </main>
    </div>
  );
}

export default App;
