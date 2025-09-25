// tailwind.config.js
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#4d5cb7',   // Tono 6
          100: '#3c4cb0',  // Tono 5
          200: '#2b3ba5',  // Tono 4
          300: '#1a2b9c',  // Tono 3
          400: '#111e88',  // Tono 2
          500: '#0f0b7a',  // Tono 1
          600: '#0d046c',  // Base
        },
      },
    },
  },
  plugins: [],
};
