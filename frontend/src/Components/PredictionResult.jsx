import { useEffect } from "react";
import { motion, useAnimate, useMotionValue, useTransform } from "framer-motion";

// Helper to determine color based on score
const getColor = (value) => {
  if (value >= 70) return "#1DB954"; // Spotify Green
  if (value >= 50) return "#F59E0B"; // Amber
  return "#EF4444"; // Red
};

export function PredictionResult({ prediction }) {
  const [scope, animate] = useAnimate();
  const motionValue = useMotionValue(0);

  let value, primaryText, secondaryText;
  if ("predicted_popularity" in prediction) {
    value = Math.round(prediction.predicted_popularity);
    primaryText = "Popularity Score";
    secondaryText = "Based on regression model";
  } else {
    value = Math.round(prediction.probability * 100);
    primaryText = prediction.class === "Hit" || prediction.class === 1 ? "Hit" : "Not a Hit";
    secondaryText = `${value}% Confidence`;
  }

  const color = getColor(value);
  const rounded = useTransform(motionValue, Math.round);

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
      <p className="text-spotify-lightgray mb-6">{secondaryText}</p>
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
            style={{ color, pathLength: motionValue / 100 }}
            transform="rotate(-90 50 50)"
          />
        </svg>
        <motion.div ref={scope} className="absolute inset-0 flex items-center justify-center text-4xl font-bold text-white">
          {rounded}
        </motion.div>
      </div>
    </motion.div>
  );
}