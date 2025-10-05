import { useEffect } from "react";
import { motion, useAnimate, useMotionValue, useTransform } from "framer-motion";

// --- Interpretation for Regression Model ---
const getScoreVerdict = (score) => {
  if (score >= 70) return { text: "Certified Hit", color: "#1DB954", description: "This score suggests the song has strong potential to be a mainstream success." };
  if (score >= 60) return { text: "Strong Hit Potential", color: "#22C55E", description: "This song shows solid signs of becoming popular with a wide audience." };
  if (score >= 50) return { text: "Mainstream Appeal", color: "#F59E0B", description: "This track has qualities that could appeal to a broad commercial audience." };
  if (score >= 30) return { text: "Niche Following", color: "#3B82F6", description: "This song is likely to find a dedicated audience within a specific genre." };
  return { text: "Underground Track", color: "#A1A1AA", description: "This track has unique qualities that may appeal to a more selective audience." };
};

// --- Interpretation for Classification Model ---
const getClassificationVerdict = (predClass) => {
  if (predClass === "High") return { text: "Likely Hit", color: "#1DB954", description: "The model predicts this song has a high probability of becoming a hit." };
  if (predClass === "Medium") return { text: "Moderate Potential", color: "#F59E0B", description: "The model sees potential for this song to gain traction and popularity." };
  if (predClass === "Low") return { text: "Niche Appeal", color: "#3B82F6", description: "The model suggests this song will likely appeal to a specific audience." };
  return { text: "Not a Hit", color: "#EF4444", description: "The model predicts this song is unlikely to become a mainstream hit." };
};

export function PredictionResult({ prediction }) {
  const [scope, animate] = useAnimate();
  const motionValue = useMotionValue(0);

  let value, primaryText, secondaryText, verdict;
  if ("predicted_popularity" in prediction) {
    value = Math.round(prediction.predicted_popularity);
    primaryText = "Popularity Score";
    const verdictInfo = getScoreVerdict(value);
    secondaryText = `Verdict: ${verdictInfo.text}`;
    verdict = verdictInfo;
  } else {
    // Handle both binary (0/1) and multi-class ("Low", "Medium", "High")
    const isBinaryHit = prediction.class === "Hit" || prediction.class === 1;
    const predClass = isBinaryHit ? "High" : prediction.class; // Map binary to "High" for verdict

    const verdictInfo = getClassificationVerdict(predClass);
    value = Math.round(prediction.probability * 100);
    primaryText = verdictInfo.text;
    secondaryText = `Model Confidence`;
    verdict = verdictInfo;
  }

  const roundedValue = useTransform(motionValue, Math.round);

  useEffect(() => {
    const animation = animate(motionValue, value, {
      duration: 1.5,
      ease: "easeOut",
    });
    return animation.stop;
  }, [value]);

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.9 }}
      animate={{ opacity: 1, scale: 1 }}
      className="bg-spotify-darkgray rounded-lg p-8 flex flex-col items-center shadow-lg text-center"
    >
      <h2 className="text-2xl font-bold mb-2 text-white">{primaryText}</h2>
      <p className="font-semibold mb-6" style={{ color: verdict.color }}>{secondaryText}</p>
      <p className="text-sm text-spotify-lightgray mb-6 -mt-4 max-w-xs">{verdict.description}</p>
      <div className="relative w-48 h-48">
        <svg className="w-full h-full" viewBox="0 0 100 100">
          {/* Background circle */}
          <circle
            className="stroke-current text-spotify-lightgray/20"
            strokeWidth="10"
            cx="50"
            cy="50"
            r="40"
            fill="transparent"
          />
          {/* Progress circle */}
          <motion.circle
            className="stroke-current"
            strokeWidth="10"
            strokeLinecap="round"
            cx="50"
            cy="50"
            r="40"
            fill="transparent"
            style={{ color: verdict.color, pathLength: motionValue / 100 }}
            transform="rotate(-90 50 50)"
          />
        </svg>
        <motion.div ref={scope} className="absolute inset-0 flex items-center justify-center text-4xl font-bold text-white">
          {roundedValue}
        </motion.div>
      </div>
    </motion.div>
  );
}