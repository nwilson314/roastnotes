<script lang="ts">
  import type { PageData } from './$types';
  import LandingOverview from '$lib/components/LandingOverview.svelte';

  export let data: PageData;
</script>

<div class="min-h-screen bg-coffee-cream bg-texture">
  <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-2 pb-8">
    <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
      <div class="text-center mb-6">
        <h1 class="text-5xl font-garamond font-medium text-coffee-deep mb-2">
          Welcome to RoastNotes
        </h1>
        <p class="text-xl text-coffee-medium font-garamond italic">
          il gusto del caffè
        </p>
      </div>
      
      <LandingOverview />
      
      <div class="flex flex-col items-center mt-10 mb-12 space-y-5">
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
  .bg-texture {
    background-image: url('/coffee-texture-light.png');
    background-repeat: repeat;
    background-size: 300px 300px;
    background-blend-mode: multiply;
  }

  :global(.hover\:scale-102:hover) {
    transform: scale(1.02);
  }
</style>