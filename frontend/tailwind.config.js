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
          navy: '#0B132B',
          navyLight: '#1C2541',
          primary: '#3A506B',
          accent: '#4F46E5',
          accentHover: '#4338CA',
          emerald: '#10B981',
          rose: '#EF4444',
          amber: '#F59E0B'
        }
      }
    },
  },
  plugins: [],
}
