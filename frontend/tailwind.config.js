/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx}",
    "./src/components/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        neu: {
          red: "#8B0000",
          dark: "#1E293B",
          light: "#F8FAFC",
        },
      },
    },
  },
  plugins: [],
};
