<script>
  import LandingOverview from '$lib/components/LandingOverview.svelte';
  import Header from '$lib/components/Header.svelte';
  import { goto } from '$app/navigation';

  const login = () => {
    // trigger login flow
  }
  const data = {}

</script>

  <div class="min-h-screen bg-coffee-cream bg-texture">
    <Header {data} />
    
    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div class="text-center mb-12">
          <h1 class="text-5xl font-garamond font-medium text-coffee-deep mb-4 text-shadow">
            Welcome to RoastNotes
          </h1>
          <p class="text-xl text-coffee-medium font-garamond italic">
            il gusto del caffè
          </p>
        </div>
        
        <LandingOverview />
        
        <div class="flex flex-col items-center mt-12 mb-16 space-y-6">
          <a 
            href="/register"
            class="px-8 py-3 rounded-full bg-coffee-deep text-coffee-cream font-medium 
                   shadow-md transition-all duration-300 ease-out transform 
                   hover:scale-102 hover:shadow-lg hover:bg-coffee-medium
                   border border-coffee-gold/20 text-lg"
          >
            Join the Table
          </a>
          <div class="flex items-center space-x-2 text-coffee-medium">
            <span>Already have an account?</span>
            <a 
              href="/login"
              class="font-medium text-coffee-deep hover:text-coffee-burgundy 
                     transition-colors duration-200 underline"
            >
              Sign In
            </a>
          </div>
        </div>
      </div>
    </main>
  </div>

<style>
  :root {
    --bg-color: #f4ece3;         /* parchment-like background */
    --primary-color: #8a4b28;    /* rich mahogany */
    --secondary-color: #6c4f3d;  /* deep leather brown */
    --accent-color: #a05a35;     /* warm accent */
    --text-color: #5a3e2b;       /* dark, bookish text */
    --font-serif: 'Garamond', serif;
    --font-sans: 'Helvetica Neue', sans-serif;
  }

  body {
    background-color: var(--bg-color);
    font-family: var(--font-sans);
    color: var(--text-color);
    margin: 0;
    padding: 0;
  }

  .min-h-screen {
    min-height: 100vh;
  }
  .bg-texture {
    background-image: url('texture.jpg');
    background-size: cover;
    background-position: center;
  }
  .max-w-4xl {
    max-width: 44rem;
  }
  .mx-auto {
    margin-left: auto;
    margin-right: auto;
  }
  .px-4 {
    padding-left: 1rem;
    padding-right: 1rem;
  }
  .sm\:px-6 {
    padding-left: 1.5rem;
    padding-right: 1.5rem;
  }
  .lg\:px-8 {
    padding-left: 2rem;
    padding-right: 2rem;
  }
  .py-16 {
    padding-top: 4rem;
    padding-bottom: 4rem;
  }
  .text-center {
    text-align: center;
  }
  .mb-12 {
    margin-bottom: 3rem;
  }
  .text-5xl {
    font-size: 3rem;
  }
  .font-garamond {
    font-family: 'Garamond', serif;
  }
  .font-medium {
    font-weight: 500;
  }
  .text-coffee-deep {
    color: #452B1F;
  }
  .mb-4 {
    margin-bottom: 1rem;
  }
  .text-shadow {
    text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
  }
  .text-xl {
    font-size: 1.25rem;
  }
  .text-coffee-medium {
    color: #964B00;
  }
  .italic {
    font-style: italic;
  }
  .flex {
    display: flex;
  }
  .flex-col {
    flex-direction: column;
  }
  .items-center {
    align-items: center;
  }
  .mt-12 {
    margin-top: 3rem;
  }
  .mb-16 {
    margin-bottom: 4rem;
  }
  .space-y-6 {
    margin-top: 1.5rem;
    margin-bottom: 1.5rem;
  }
  .px-8 {
    padding-left: 2rem;
    padding-right: 2rem;
  }
  .py-3 {
    padding-top: 0.75rem;
    padding-bottom: 0.75rem;
  }
  .rounded-full {
    border-radius: 9999px;
  }
  .bg-coffee-deep {
    background-color: #452B1F;
  }
  .text-coffee-cream {
    color: #F5F5DC;
  }
  .shadow-md {
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  }
  .transition-all {
    transition: all 0.2s ease-in-out;
  }
  .duration-300 {
    transition-duration: 300ms;
  }
  .ease-out {
    transition-timing-function: cubic-bezier(0, 0, 0.2, 1);
  }
  .transform {
    transform: translateZ(0);
  }
  .hover\:scale-102:hover {
    transform: scale(1.02);
  }
  .hover\:shadow-lg:hover {
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
  }
  .hover\:bg-coffee-medium:hover {
    background-color: #964B00;
  }
  .border {
    border-width: 1px;
  }
  .border-coffee-gold {
    border-color: #FFD700;
  }
  .border-opacity-20 {
    border-opacity: 0.2;
  }
  .text-lg {
    font-size: 1.125rem;
  }
  .text-sm {
    font-size: 0.875rem;
  }
</style>