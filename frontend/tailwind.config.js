/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'cute': {
          pink: '#ff6b9d',
          purple: '#9b6bff',
          yellow: '#ffde6b',
          blue: '#6bafff',
          green: '#6bffb8'
        }
      },
      fontFamily: {
        'comic': ['Comic Neue', 'cursive']
      },
      borderRadius: {
        'xl': '1rem',
        '2xl': '2rem'
      }
    },
  },
  plugins: [],
} 