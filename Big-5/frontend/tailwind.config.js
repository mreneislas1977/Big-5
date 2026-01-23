/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          green: '#014421',  // Your Hunter Green
          cream: '#fdfbf5',  // Your Warm White/Cream
          brown: '#5c4033',  // Your Coffee Brown
        }
      }
    },
  },
  plugins: [],
}
