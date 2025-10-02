import React from "react";
import { motion } from "framer-motion";
import { RadialBarChart, RadialBar, Legend, ResponsiveContainer } from "recharts";

export function PredictionResult({ prediction }) {
  let value, label, max, color;
  if ("predicted_popularity" in prediction) {
    value = prediction.predicted_popularity;
    label = `Predicted Popularity: ${Math.round(value)}`;
    max = 100;
    color = "#1DB954";
  } else {
    value = Math.round(prediction.probability * 100);
    label = `Prediction: ${prediction.class === "Hit" || prediction.class === 1 ? "Hit" : "Not Hit"} (${value}%)`;
    max = 100;
    color = "#1DB954";
  }

  const data = [
    { name: label, value, fill: color }
  ];

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.9 }}
      animate={{ opacity: 1, scale: 1 }}
      className="bg-spotify-darkgray rounded-lg p-6 flex flex-col items-center shadow-lg"
    >
      <div className="w-full flex flex-col items-center">
        <div className="text-2xl font-bold mb-2">{label}</div>
        <div className="w-40 h-40">
          <ResponsiveContainer width="100%" height="100%">
            <RadialBarChart
              innerRadius="80%"
              outerRadius="100%"
              barSize={20}
              data={data}
              startAngle={90}
              endAngle={450}
            >
              <RadialBar
                minAngle={15}
                background
                clockWise
                dataKey="value"
              />
              <Legend
                iconSize={10}
                layout="vertical"
                verticalAlign="middle"
                align="center"
              />
            </RadialBarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </motion.div>
  );
}