<script lang="ts">
  import { auth } from '$lib/stores/auth';
  import type { PageData } from './$types';
  
  export let data: PageData;
  
  // Initialize auth store with server data
  $: if (data.user && data.token) {
    auth.init(data.user, data.token);
  }
</script>

<div class="min-h-screen bg-coffee-paper/30">
  <div class="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    {#if $auth.user}
      <div class="bg-white rounded-xl border border-coffee-light/20 shadow-warm overflow-hidden">
        <div class="p-8">
          <!-- Profile Header -->
          <div class="flex items-center space-x-4 mb-6">
            <div class="w-16 h-16 rounded-full bg-coffee-cream/20 border-2 border-coffee-gold/30 
                        flex items-center justify-center">
              <span class="font-garamond text-3xl text-coffee-deep">
                {$auth.user.email[0].toUpperCase()}
              </span>
            </div>
            <div>
              <h1 class="font-garamond text-2xl text-coffee-deep">{$auth.user.email}</h1>
              <p class="text-coffee-medium">Member since {new Date($auth.user.created_at).toLocaleDateString()}</p>
            </div>
          </div>

          <!-- Stats -->
          <div class="grid grid-cols-2 gap-4 mt-6">
            <div class="p-4 rounded-lg bg-coffee-paper/30 border border-coffee-light/20">
              <h3 class="font-garamond text-lg text-coffee-deep mb-1">Your Ratings</h3>
              <p class="text-3xl font-garamond text-coffee-gold">0</p>
              <p class="text-sm text-coffee-medium">across all roasts</p>
            </div>
            <div class="p-4 rounded-lg bg-coffee-paper/30 border border-coffee-light/20">
              <h3 class="font-garamond text-lg text-coffee-deep mb-1">Groups</h3>
              <p class="text-3xl font-garamond text-coffee-gold">0</p>
              <p class="text-sm text-coffee-medium">coffee circles</p>
            </div>
          </div>
        </div>
      </div>
    {:else}
      <div class="text-center">
        <p class="text-coffee-medium">Loading profile...</p>
      </div>
    {/if}
  </div>
</div>

<style>
  .shadow-warm {
    box-shadow: 0 4px 8px rgba(255, 215, 0, 0.2);
  }
</style>