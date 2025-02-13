<script lang="ts">
  import type { LayoutData } from '../../routes/$types';
  
  export let data: LayoutData;
</script>

<nav class="fixed top-0 left-0 right-0 w-full bg-coffee-deep shadow-lg z-50 border-b border-coffee-gold border-opacity-20">
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
    <div class="flex justify-between items-center h-16">
      <div class="flex-shrink-0">
        <a href={data.user_logged_in ? "/roasts" : "/"} class="flex items-center group">
          <span class="font-garamond text-3xl font-medium text-coffee-cream group-hover:text-coffee-gold transition-colors duration-300 text-shadow">
            RoastNotes
          </span>
          <span class="ml-2 text-coffee-gold text-opacity-80 italic font-garamond text-sm">
            il gusto del caffè
          </span>
        </a>
      </div>
      
      <div class="flex items-center space-x-4">
        {#if data.user_logged_in}
          <div class="flex items-center space-x-4">
            <nav class="flex items-center space-x-2 mr-4">
              <a href="/roasts" class="px-3 py-1.5 rounded-lg text-coffee-cream hover:bg-coffee-medium/30 transition-colors duration-200 text-sm font-medium">Roasts</a>
              <a href="/roasters" class="px-3 py-1.5 rounded-lg text-coffee-cream hover:bg-coffee-medium/30 transition-colors duration-200 text-sm font-medium">Roasters</a>
            </nav>
            <a href="/profile" class="flex items-center space-x-3 group">
              <div class="w-10 h-10 rounded-full bg-coffee-cream/20 border-2 border-coffee-gold/30 
                          flex items-center justify-center group-hover:border-coffee-gold/50 
                          transition-all duration-300">
                <span class="font-garamond text-xl text-coffee-cream group-hover:text-coffee-gold">
                  {data.user?.email?.[0]?.toUpperCase() ?? 'U'}
                </span>
              </div>
            </a>
          </div>
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
  .text-shadow {
    text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
  }
</style>