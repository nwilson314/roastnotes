<script>
  let user = null; // or set to a user obj when logged in
</script>

<nav class="fixed top-0 w-full bg-coffee-deep shadow-md z-50">
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
    <div class="flex justify-between items-center h-16">
      <div class="flex-shrink-0">
        <a href="/" class="flex items-center">
          <span class="font-garamond text-3xl font-medium text-coffee-cream hover:text-coffee-gold transition-colors duration-200">
            RoastNotes
          </span>
        </a>
      </div>
      
      <div class="flex items-center">
        {#if user}
          <img 
            class="w-10 h-10 rounded-full border-2 border-coffee-gold shadow-glow" 
            src={user.profilePic} 
            alt="Profile"
          />
        {:else}
          <button 
            class="px-5 py-2 rounded-full bg-coffee-cream text-coffee-deep font-medium shadow-sm
                   transition-all duration-200 ease-in-out transform hover:scale-102 hover:shadow-md
                   hover:bg-coffee-light hover:text-coffee-cream
                   border border-coffee-gold border-opacity-20"
          >
            Sign In
          </button>
        {/if}
      </div>
    </div>
  </div>
</nav>

<!-- Spacer to prevent content from being hidden under fixed header -->
<div class="h-16"></div>

<style>
  /* Add styles here if needed */
</style>