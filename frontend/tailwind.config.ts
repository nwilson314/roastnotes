import type { Config } from 'tailwindcss';

export default {
  content: ['./src/**/*.{html,js,svelte,ts}'],
  theme: {
    extend: {
      colors: {
        'coffee': {
          'deep': '#2C1810',      // Deep espresso
          'medium': '#4A3428',    // Roasted bean
          'light': '#8B6F5C',     // Aged wood
          'cream': '#F5E6D3',     // Steamed milk
          'gold': '#D4A24C',      // Brass/copper
          'burgundy': '#732F2F',  // Terra cotta
          'olive': '#4B4A3A',     // Aged leather
          'charcoal': '#2D2D2D',  // Blackboard
          'paper': '#F8F4E9'      // Aged paper
        }
      },
      fontFamily: {
        garamond: ['EB Garamond', 'serif'],
        inter: ['Inter', 'sans-serif'],
        crimson: ['Crimson Pro', 'serif']
      },
      scale: {
        '101': '1.01',
        '102': '1.02'
      },
      transitionTimingFunction: {
        'bounce-sm': 'cubic-bezier(0.175, 0.885, 0.32, 1.05)'
      },
      keyframes: {
        'warm-fade-in': {
          '0%': { opacity: '0', transform: 'scale(0.95)' },
          '100%': { opacity: '1', transform: 'scale(1)' }
        }
      },
      animation: {
        'warm-fade-in': 'warm-fade-in 0.3s ease-out'
      },
      boxShadow: {
        'warm': '0 4px 14px -2px rgba(44, 24, 16, 0.08)',
        'warm-lg': '0 10px 24px -4px rgba(44, 24, 16, 0.12)'
      },
      backgroundImage: {
        'texture': "url(\"data:image/svg+xml,%3Csvg width='100' height='100' viewBox='0 0 100 100' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.8' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100' height='100' filter='url(%23noise)' opacity='0.08'/%3E%3C/svg%3E\")"
      }
    }
  },
  plugins: []
} satisfies Config;
