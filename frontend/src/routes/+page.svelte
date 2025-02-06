<script>
    import LandingOverview from '$lib/components/LandingOverview.svelte';
    import { goto } from '$app/navigation';
    
    let loggedIn = false; // replace with real auth check
  
    const login = () => {
      // trigger login flow
    }
  
    // redirect if logged in
    if (loggedIn) {
      goto('/roasts');
    }
  </script>
  
  {#if !loggedIn}
    <LandingOverview />
    <div class="flex justify-center mt-8 mb-16">
      <button 
        on:click={login}
        class="px-8 py-3 rounded-full bg-coffee-cream text-coffee-deep font-medium shadow-sm
               transition-all duration-200 ease-in-out transform hover:scale-102 hover:shadow-md
               hover:bg-coffee-light hover:text-coffee-cream
               border border-coffee-gold border-opacity-20 text-lg"
      >
        Welcome Back
      </button>
    </div>
  {/if}
  
  <style>
    .flex {
      display: flex;
    }
    .justify-center {
      justify-content: center;
    }
    .mt-8 {
      margin-top: 2rem;
    }
    .mb-16 {
      margin-bottom: 4rem;
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
    .bg-coffee-cream {
      background-color: #F5F5DC;
    }
    .text-coffee-deep {
      color: #452B1F;
    }
    .font-medium {
      font-weight: 500;
    }
    .shadow-sm {
      box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
    }
    .transition-all {
      transition: all 0.2s ease-in-out;
    }
    .duration-200 {
      transition-duration: 200ms;
    }
    .ease-in-out {
      transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
    }
    .transform {
      transform: translateZ(0);
    }
    .hover\:scale-102:hover {
      transform: scale(1.02);
    }
    .hover\:shadow-md:hover {
      box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    }
    .hover\:bg-coffee-light:hover {
      background-color: #F0E4CC;
    }
    .hover\:text-coffee-cream:hover {
      color: #F5F5DC;
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
  </style>