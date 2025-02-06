import type { Config } from 'tailwindcss';

export default {
  content: ['./src/**/*.{html,js,svelte,ts}'],
  theme: {
    extend: {
      colors: {
        'coffee-deep': 'var(--coffee-deep)',
        'coffee-medium': 'var(--coffee-medium)',
        'coffee-light': 'var(--coffee-light)',
        'coffee-cream': 'var(--coffee-cream)',
        'coffee-gold': 'var(--coffee-gold)',
        'coffee-burgundy': 'var(--coffee-burgundy)',
        'coffee-olive': 'var(--coffee-olive)',
        'coffee-charcoal': 'var(--coffee-charcoal)'
      },
      fontFamily: {
        garamond: ['EB Garamond', 'serif'],
        inter: ['Inter', 'sans-serif']
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
      ringColor: {
        'coffee-gold': 'var(--coffee-gold)',
      },
      ringOpacity: {
        '50': '0.5'
      }
    }
  },
  plugins: []
} satisfies Config;
