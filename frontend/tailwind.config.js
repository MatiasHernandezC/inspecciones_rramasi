/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./public/index.html",
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          DEFAULT: "#1d4ed8", // blue-700 baseline for brand
          dark: "#1e40af", // blue-800
          light: "#3b82f6", // blue-500
        },
      },
    },
  },
  plugins: [],
};