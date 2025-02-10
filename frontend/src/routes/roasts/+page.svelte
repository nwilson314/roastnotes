<script lang="ts">
  import type { PageProps } from './$types';
  import RoastCard from '$lib/components/RoastCard.svelte';
  import { communityStats } from '$lib/stores/auth';

  let { data }: PageProps = $props();
  let selectedView = 'trending';
  
</script>

<div class="min-h-screen bg-coffee-paper/30">
  <!-- Top Actions Bar -->
  <div class="sticky top-0 z-10 bg-white/80 backdrop-blur-sm border-b border-coffee-light/20 shadow-sm">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
      <div class="flex items-center justify-between">
        <div class="flex items-center space-x-4">
          {#if data.user}
            <button 
              class="px-4 py-2 rounded-lg bg-coffee-deep text-coffee-cream 
                     hover:bg-coffee-medium transition-colors duration-200
                     border border-coffee-gold/20"
            >
              Add New Roast
            </button>
            <div class="flex items-center p-1 bg-coffee-cream/20 rounded-lg border border-coffee-light/20">
              <button 
                class="px-4 py-2 rounded-md font-medium transition-all duration-200
                       {selectedView === 'trending' ? 
                         'bg-white text-coffee-deep shadow-warm translate-y-[-1px]' : 
                         'text-coffee-medium hover:text-coffee-deep'}"
                on:click={() => selectedView = 'trending'}
              >
                Trending
              </button>
              <button 
                class="px-4 py-2 rounded-md font-medium transition-all duration-200
                       {selectedView === 'groups' ? 
                         'bg-white text-coffee-deep shadow-warm translate-y-[-1px]' : 
                         'text-coffee-medium hover:text-coffee-deep'}"
                on:click={() => selectedView = 'groups'}
              >
                Groups
              </button>
            </div>
          {:else}
            <a 
              href="/register"
              class="px-4 py-2 rounded-lg bg-coffee-deep text-coffee-cream 
                     hover:bg-coffee-medium transition-colors duration-200
                     border border-coffee-gold/20"
            >
              Join to Share Your Roasts
            </a>
          {/if}
        </div>
        
        <div class="flex items-center space-x-2">
          {#if data.user}
            <select 
              class="px-3 py-2 rounded-lg border border-coffee-light/20 
                     text-coffee-deep bg-white"
            >
              <option>Most Recent</option>
              <option>Highest Rated</option>
              <option>Most Reviews</option>
            </select>
          {/if}
        </div>
      </div>
    </div>
  </div>

  <!-- Main Content -->
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <div class="flex gap-8">
      <!-- Roasts Grid -->
      <div class="flex-1">
        <!-- Section Title -->
        <h2 class="font-garamond text-2xl text-coffee-deep mb-6">
          {#if data.user}
            {selectedView === 'trending' ? 'Trending Roasts' : 'Your Groups\' Roasts'}
          {:else}
            Trending Roasts
          {/if}
        </h2>
        
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          {#if displayedRoasts.length > 0}
            {#each displayedRoasts as roast}
              <RoastCard {roast} />
            {/each}
          {:else}
            <div class="col-span-full text-center py-12 text-coffee-medium">
              {#if data.user}
                {#if selectedView === 'trending'}
                  <p>No trending roasts yet. Be the first to share one!</p>
                {:else}
                  <p>No roasts in your groups yet. Start sharing or join more groups!</p>
                {/if}
              {:else}
                <p>No roasts to display. Join our community to see more!</p>
              {/if}
            </div>
          {/if}

          {#if !data.user}
            <div class="col-span-full mt-8 text-center">
              <p class="text-coffee-medium mb-4">
                Join {communityStats.active_roasters} roasters sharing their coffee journey
              </p>
              <a 
                href="/register"
                class="inline-block px-6 py-3 rounded-lg bg-coffee-deep text-coffee-cream 
                       hover:bg-coffee-medium transition-colors duration-200
                       border border-coffee-gold/20 font-medium"
              >
                Join the Table
              </a>
            </div>
          {/if}
        </div>
      </div>

      <!-- Sidebar -->
      <div class="hidden lg:block w-80">
        {#if data.user}
          <div class="sticky top-24 bg-white rounded-xl border border-coffee-light/20 p-6 shadow-warm">
            <h2 class="font-garamond text-2xl text-coffee-deep mb-6">
              Your Groups
            </h2>
            
            <div class="space-y-4">
              {#if data.userGroups.length > 0}
                {#each data.userGroups as group}
                  <div class="p-4 rounded-lg bg-coffee-cream/10 border border-coffee-light/10
                              hover:bg-coffee-cream/20 transition-colors duration-200 cursor-pointer">
                    <div class="flex items-center justify-between mb-2">
                      <h3 class="font-garamond text-lg text-coffee-deep">
                        {group.name}
                      </h3>
                      {#if group.new_roasts > 0}
                        <span class="px-2 py-1 text-xs rounded-full bg-coffee-gold/20 text-coffee-deep">
                          {group.new_roasts} new
                        </span>
                      {/if}
                    </div>
                    <div class="text-sm text-coffee-medium">
                      <p>{group.members} members</p>
                      <p>Last active {group.latest_activity}</p>
                    </div>
                  </div>
                {/each}
              {:else}
                <p class="text-coffee-medium text-center py-4">
                  No groups yet. Create or join one to start sharing!
                </p>
              {/if}

              <button 
                class="w-full mt-4 px-4 py-2 rounded-lg border border-coffee-gold/20
                       text-coffee-deep hover:bg-coffee-cream/20 
                       transition-colors duration-200"
              >
                Create New Group
              </button>
            </div>
          </div>
        {:else}
          <div class="sticky top-24 bg-white rounded-xl border border-coffee-light/20 p-6 shadow-warm">
            <h2 class="font-garamond text-2xl text-coffee-deep mb-6">
              Community Highlights
            </h2>
            
            <div class="space-y-6">
              <div>
                <h3 class="font-garamond text-lg text-coffee-deep mb-2">Active Community</h3>
                <div class="grid grid-cols-2 gap-4">
                  <div class="text-center p-3 bg-coffee-cream/10 rounded-lg">
                    <p class="text-2xl font-garamond text-coffee-deep">{communityStats.total_roasts}</p>
                    <p class="text-sm text-coffee-medium">Roasts Shared</p>
                  </div>
                  <div class="text-center p-3 bg-coffee-cream/10 rounded-lg">
                    <p class="text-2xl font-garamond text-coffee-deep">{communityStats.active_roasters}</p>
                    <p class="text-sm text-coffee-medium">Active Roasters</p>
                  </div>
                </div>
              </div>

              <div>
                <h3 class="font-garamond text-lg text-coffee-deep mb-2">Popular Origins</h3>
                <div class="space-y-2">
                  {#each communityStats.popular_origins as origin}
                    <div class="flex justify-between items-center p-2 bg-coffee-cream/10 rounded-lg">
                      <span class="text-coffee-deep">{origin.name}</span>
                      <span class="text-coffee-medium text-sm">{origin.roast_count} roasts</span>
                    </div>
                  {/each}
                </div>
              </div>

              <div>
                <h3 class="font-garamond text-lg text-coffee-deep mb-2">Recent Activity</h3>
                <div class="space-y-2">
                  <p class="text-coffee-medium">
                    {communityStats.recent_activity.new_roasts_24h} new roasts today
                  </p>
                  <p class="text-coffee-medium">
                    {communityStats.recent_activity.new_reviews_24h} new reviews today
                  </p>
                </div>
              </div>
            </div>
          </div>
        {/if}
      </div>
    </div>
  </div>
</div>

<style>
  /* Add any additional styles here */
  :global(.shadow-warm) {
    box-shadow: 0 4px 6px -1px rgba(120, 108, 59, 0.1), 
                0 2px 4px -1px rgba(120, 108, 59, 0.06);
  }
</style>