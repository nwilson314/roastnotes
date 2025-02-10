<script>
  export let data;
</script>

<nav class="fixed top-0 left-0 right-0 w-full bg-coffee-deep shadow-lg z-50 border-b border-coffee-gold border-opacity-20">
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
    <div class="flex justify-between items-center h-16">
      <div class="flex-shrink-0">
        <a href="/" class="flex items-center group">
          <span class="font-garamond text-3xl font-medium text-coffee-cream group-hover:text-coffee-gold transition-colors duration-300 text-shadow">
            RoastNotes
          </span>
          <span class="ml-2 text-coffee-gold text-opacity-80 italic font-garamond text-sm">
            il gusto del caffè
          </span>
        </a>
      </div>
      
      <div class="flex items-center space-x-4">
        {#if data?.user}
          <img 
            class="w-10 h-10 rounded-full border-2 border-coffee-gold shadow-glow
                   transition-all duration-300 ease-out hover:scale-102" 
            src={data.user.profilePic || '/default-avatar.png'} 
            alt="Profile"
          />
        {:else}
          <div class="flex items-center space-x-4">
            <a
              href="/register"
              class="px-4 py-2 rounded-lg bg-coffee-deep text-coffee-cream 
                     hover:bg-coffee-medium transition-colors duration-200
                     border border-coffee-gold/20"
            >
              Join the Table
            </a>
            <a
              href="/login"
              class="px-4 py-2 rounded-lg bg-coffee-cream/50 text-coffee-deep 
                     hover:bg-coffee-cream transition-colors duration-200
                     border border-coffee-gold/20"
            >
              Sign In
            </a>
          </div>
        {/if}
      </div>
    </div>
  </div>
</nav>

<!-- Spacer to prevent content from being hidden under fixed header -->
<div class="h-16"></div>

<style>
  /* Styles moved to app.css */
</style>