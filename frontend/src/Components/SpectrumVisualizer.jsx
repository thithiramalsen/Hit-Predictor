import React, { useEffect, useRef } from 'react';

export function SpectrumVisualizer({ width = 800, height = 140 }) {
  const canvasRef = useRef(null);
  const rafRef = useRef(0);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    let t = 0;

    const render = () => {
      const w = canvas.width = canvas.clientWidth * window.devicePixelRatio;
      const h = canvas.height = canvas.clientHeight * window.devicePixelRatio;
      const barWidth = Math.max(2, Math.floor(w / 90));
      const gap = Math.max(3, Math.floor(barWidth * 0.6));
      const count = Math.floor(w / (barWidth + gap));
      const centerY = Math.floor(h * 0.65);

      ctx.clearRect(0, 0, w, h);

      // Background glow
      const gradient = ctx.createLinearGradient(0, 0, 0, h);
      gradient.addColorStop(0, 'rgba(29,185,84,0.35)');
      gradient.addColorStop(1, 'rgba(29,185,84,0.05)');

      for (let i = 0; i < count; i++) {
        const x = Math.floor(i * (barWidth + gap));
        const noise = Math.sin((i * 0.35) + t * 0.12) * 0.5 + 0.5;
        const envelope = 0.6 + 0.4 * Math.sin(t * 0.02 + i * 0.08);
        const heightNorm = Math.pow(noise * envelope, 1.2);
        const barHeight = Math.max(6, Math.floor(heightNorm * h * 0.6));

        // Shadow/glow
        ctx.fillStyle = 'rgba(29,185,84,0.12)';
        ctx.fillRect(x, centerY - barHeight - 6, barWidth, barHeight + 12);

        // Main bar
        ctx.fillStyle = gradient;
        ctx.fillRect(x, centerY - barHeight, barWidth, barHeight);

        // Top cap
        ctx.fillStyle = 'rgba(255,255,255,0.65)';
        ctx.fillRect(x, centerY - barHeight - 2, barWidth, 2);
      }

      t += 1;
      rafRef.current = requestAnimationFrame(render);
    };

    rafRef.current = requestAnimationFrame(render);
    return () => cancelAnimationFrame(rafRef.current);
  }, []);

  return (
    <div className="relative">
      <div className="absolute -inset-6 rounded-2xl bg-spotify-green/10 blur-2xl" />
      <canvas ref={canvasRef} style={{ width: '100%', height: height }} className="relative rounded-xl ring-1 ring-spotify-green/30 bg-gradient-to-b from-spotify-black/60 to-spotify-darkgray/60" />
    </div>
  );
}


