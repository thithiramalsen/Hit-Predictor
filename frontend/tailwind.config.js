// tailwind.config.js
/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'spotify-green': '#1DB954',
        'spotify-black': '#191414',
        'spotify-darkgray': '#282828',
        'spotify-lightgray': '#B3B3B3'
      },
      boxShadow: {
        'spotify': '0 10px 25px -5px rgba(29,185,84,0.35), 0 8px 10px -6px rgba(29,185,84,0.25)'
      },
      keyframes: {
        'float': {
          '0%, 100%': { transform: 'translateY(0px)' },
          '50%': { transform: 'translateY(-8px)' }
        },
        'pulse-glow': {
          '0%, 100%': { boxShadow: '0 0 0 0 rgba(29,185,84,0.6)' },
          '50%': { boxShadow: '0 0 0 12px rgba(29,185,84,0)' }
        },
        'equalize': {
          '0%': { transform: 'scaleY(0.2)' },
          '50%': { transform: 'scaleY(1)' },
          '100%': { transform: 'scaleY(0.2)' }
        },
        'gradient-move': {
          '0%': { backgroundPosition: '0% 50%' },
          '50%': { backgroundPosition: '100% 50%' },
          '100%': { backgroundPosition: '0% 50%' }
        }
      },
      animation: {
        'float': 'float 6s ease-in-out infinite',
        'pulse-glow': 'pulse-glow 2.5s ease-in-out infinite',
        'equalize': 'equalize 1.2s ease-in-out infinite',
        'equalize-slow': 'equalize 1.8s ease-in-out infinite',
        'equalize-fast': 'equalize 0.9s ease-in-out infinite',
        'gradient-move': 'gradient-move 12s ease infinite'
      }
    },
  },
  plugins: [],
}
