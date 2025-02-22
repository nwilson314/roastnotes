<script lang="ts">
  import type { PageData } from './$types';
  import { RoastLevel } from '$lib/types';
  import AddRatingModal from '$lib/components/AddRatingModal.svelte';
  import { invalidateAll } from '$app/navigation';

  export let data: PageData;

  let showAddRatingModal = false;
  
  const roastLevelColors = {
    [RoastLevel.light]: 'bg-amber-100 text-amber-800',
    [RoastLevel.medium]: 'bg-amber-200 text-amber-900',
    [RoastLevel.dark]: 'bg-amber-300 text-amber-950',
    [RoastLevel.unspecified]: 'bg-gray-100 text-gray-700'
  };

  function handleRatingAdded() {
    showAddRatingModal = false;
    invalidateAll();
  }
</script>

<div class="min-h-screen bg-coffee-paper/30">
  <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    {#if data.roast}
      <!-- Roast Details Card -->
      <div class="bg-white rounded-xl border border-coffee-light/20 shadow-warm overflow-hidden">
        <!-- Header -->
        <div class="p-6 bg-coffee-deep text-white">
          <div class="flex items-center justify-between">
            <h1 class="text-3xl font-garamond text-coffee-cream">{data.roast.name}</h1>
            <button
              class="px-4 py-2 bg-coffee-gold hover:bg-coffee-gold/90 text-coffee-deep rounded-lg transition-colors duration-200"
              on:click={() => showAddRatingModal = true}
            >
              Add Rating
            </button>
          </div>
          <p class="mt-2 text-coffee-cream/80">by {data.roaster.name}</p>
        </div>

        <!-- Content -->
        <div class="p-6 space-y-8">
          <!-- Basic Info -->
          <div class="grid grid-cols-2 gap-6">
            <div>
              <h3 class="text-sm font-medium text-coffee-medium mb-1">Origin</h3>
              <p class="text-coffee-deep">
                {data.roast.origin}
                {#if data.roast.single_origin}
                  <span class="inline-block ml-2 px-2 py-0.5 text-xs bg-coffee-cream/50 text-coffee-deep rounded-full">
                    Single Origin
                  </span>
                {/if}
              </p>
            </div>
            <div>
              <h3 class="text-sm font-medium text-coffee-medium mb-1">Roast Level</h3>
              <span class="inline-block px-3 py-1 rounded-full text-sm {roastLevelColors[data.roast.roast_level]}">
                {data.roast.roast_level}
              </span>
            </div>
          </div>

          <!-- Bean Details -->
          {#if data.roast.bean_details}
            <div class="border-t border-coffee-light/10 pt-6">
              <h2 class="text-xl font-garamond text-coffee-deep mb-4">Bean Details</h2>
              <div class="grid grid-cols-2 gap-6">
                <div>
                  <h3 class="text-sm font-medium text-coffee-medium mb-1">Species</h3>
                  <p class="text-coffee-deep">{data.roast.bean_details.species}</p>
                </div>
                {#if data.roast.bean_details.cultivar}
                  <div>
                    <h3 class="text-sm font-medium text-coffee-medium mb-1">Cultivar</h3>
                    <p class="text-coffee-deep">{data.roast.bean_details.cultivar}</p>
                  </div>
                {/if}
                {#if data.roast.bean_details.processing_method}
                  <div>
                    <h3 class="text-sm font-medium text-coffee-medium mb-1">Processing Method</h3>
                    <p class="text-coffee-deep">{data.roast.bean_details.processing_method}</p>
                  </div>
                {/if}
                {#if data.roast.bean_details.altitude}
                  <div>
                    <h3 class="text-sm font-medium text-coffee-medium mb-1">Altitude</h3>
                    <p class="text-coffee-deep">{data.roast.bean_details.altitude}m</p>
                  </div>
                {/if}
              </div>
            </div>
          {/if}

          <!-- Ratings Overview -->
          {#if data.roast.cached_rating_stats}
            <div class="border-t border-coffee-light/10 pt-6">
              <h2 class="text-xl font-garamond text-coffee-deep mb-4">Community Ratings</h2>
              
              {#if data.roast.cached_rating_stats.total_ratings > 0}
                <div class="grid grid-cols-2 gap-6">
                  <div>
                    <h3 class="text-sm font-medium text-coffee-medium mb-1">Average Rating</h3>
                    <div class="flex items-center space-x-1">
                      <span class="text-2xl text-coffee-deep">
                        {(data.roast.cached_rating_stats.avg_rating / 20).toFixed(1)}
                      </span>
                      <span class="text-coffee-gold text-2xl">★</span>
                    </div>
                    <p class="text-sm text-coffee-medium mt-1">
                      from {data.roast.cached_rating_stats.total_ratings} ratings
                    </p>
                  </div>

                  <!-- Popular Brew Methods -->
                  <div>
                    <h3 class="text-sm font-medium text-coffee-medium mb-1">Popular Brew Methods</h3>
                    <div class="space-y-2">
                      {#each Object.entries(data.roast.cached_rating_stats.brew_methods) as [method, stats]}
                        <div class="flex items-center justify-between">
                          <span class="text-coffee-deep">{method}</span>
                          <div class="flex items-center space-x-2">
                            <span class="text-coffee-medium text-sm">{(stats.avg_rating / 20).toFixed(1)}★</span>
                            <span class="text-coffee-medium text-sm">({stats.count})</span>
                          </div>
                        </div>
                      {/each}
                    </div>
                  </div>
                </div>
              {:else}
                <p class="text-coffee-medium text-center py-4">
                  No ratings yet. Be the first to rate this roast!
                </p>
              {/if}
            </div>
          {/if}

          <!-- Recent Ratings -->
          {#if data.ratings?.length > 0}
            <div class="border-t border-coffee-light/10 pt-6">
              <h2 class="text-xl font-garamond text-coffee-deep mb-4">Recent Ratings</h2>
              <div class="space-y-4">
                {#each data.ratings as rating}
                  <div class="bg-coffee-paper/30 rounded-lg p-4">
                    <div class="flex items-center justify-between mb-2">
                      <div class="flex items-center space-x-2">
                        <span class="text-coffee-deep font-medium">{rating.brew_method}</span>
                        {#if rating.preferred_method}
                          <span class="text-xs bg-coffee-gold/20 text-coffee-deep px-2 py-0.5 rounded-full">
                            Preferred Method
                          </span>
                        {/if}
                      </div>
                      <span class="text-coffee-deep">{(rating.overall_score / 20).toFixed(1)}★</span>
                    </div>
                    <div class="grid grid-cols-3 gap-4 text-sm text-coffee-medium mb-2">
                      <div>
                        <span class="font-medium">Ratio:</span> {rating.ratio}
                      </div>
                      <div>
                        <span class="font-medium">Temp:</span> {rating.temperature}°C
                      </div>
                      <div>
                        <span class="font-medium">Grind:</span> {rating.grind}
                      </div>
                    </div>
                    {#if rating.tasting_notes}
                      <p class="text-coffee-deep text-sm mt-2">{rating.tasting_notes}</p>
                    {/if}
                  </div>
                {/each}
              </div>
            </div>
          {/if}
        </div>
      </div>
    {:else}
      <p>Loading roast details...</p>
    {/if}
  </div>
</div>

<AddRatingModal
  show={showAddRatingModal}
  roastId={data.roast?.id}
  roastName={data.roast?.name}
  on:close={() => showAddRatingModal = false}
  on:submit={handleRatingAdded}
/>
