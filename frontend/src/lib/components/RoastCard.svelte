<script lang="ts">
  import type { Roast } from '$lib/types';
  
  export let roast: Roast;

  // Get top 3 brew methods by rating
  $: topBrewMethods = roast.cached_rating_stats?.brew_methods 
    ? Object.entries(roast.cached_rating_stats.brew_methods)
        .sort((a, b) => b[1].avg_rating - a[1].avg_rating)
        .slice(0, 3)
    : [];
</script>

<div class="bg-white rounded-xl border border-coffee-light/20 shadow-warm overflow-hidden">
  <div class="p-6 bg-coffee-paper/30">
    <div class="flex items-center justify-between mb-4">
      <div class="flex items-center space-x-3">
        <div class="w-10 h-10 rounded-full bg-coffee-deep/10 flex items-center justify-center">
          <span class="font-garamond text-coffee-deep text-lg">
            {roast.name.substring(0, 2)}
          </span>
        </div>
        <div class="text-left">
          <h3 class="font-garamond text-xl text-coffee-deep">{roast.name}</h3>
          <p class="text-sm text-coffee-medium">{roast.roast_level} • {roast.origin}</p>
        </div>
      </div>
      {#if roast.cached_rating_stats}
        <div class="text-right">
          <div class="flex items-baseline justify-end">
            <span class="text-2xl font-garamond text-coffee-gold">{roast.cached_rating_stats.avg_rating.toFixed(1)}</span>
            <span class="text-sm text-coffee-medium ml-1">/5</span>
          </div>
          <p class="text-xs text-coffee-medium">
            {roast.cached_rating_stats.total_ratings} rating{roast.cached_rating_stats.total_ratings !== 1 ? 's' : ''}
          </p>
        </div>
      {/if}
    </div>
    
    <!-- Top Brew Methods -->
    {#if topBrewMethods.length > 0}
      <div class="mt-4">
        <h4 class="font-garamond text-lg text-coffee-deep mb-2">Top Brewing Methods</h4>
        <div class="grid grid-cols-3 gap-4">
          {#each topBrewMethods as [method, stats]}
            <div class="p-3 rounded-lg bg-white/50 border border-coffee-light/10 
                       hover:shadow-warm transition-all duration-300">
              <h5 class="font-garamond text-coffee-deep mb-1">{method}</h5>
              <div class="flex items-baseline justify-center">
                <span class="text-xl font-garamond text-coffee-gold">{stats.avg_rating.toFixed(1)}</span>
                <span class="text-xs text-coffee-medium ml-1">/5</span>
              </div>
              <p class="text-xs text-coffee-medium text-center mt-1">
                {stats.count} brew{stats.count !== 1 ? 's' : ''}
              </p>
            </div>
          {/each}
        </div>
      </div>
    {/if}
    
    <!-- Bean Details -->
    {#if roast.bean_details}
      <div class="mt-6">
        <h4 class="font-garamond text-lg text-coffee-deep mb-2">Bean Details</h4>
        <div class="flex flex-wrap gap-2">
          <div class="inline-flex items-center px-3 py-1 rounded-full bg-coffee-cream/30 text-coffee-deep text-sm">
            <span class="font-medium">{roast.bean_details.species}</span>
          </div>
          {#if roast.bean_details.cultivar}
            <div class="inline-flex items-center px-3 py-1 rounded-full bg-coffee-cream/30 text-coffee-deep text-sm">
              <span class="text-coffee-medium mr-1">Cultivar:</span>
              <span class="font-medium">{roast.bean_details.cultivar}</span>
            </div>
          {/if}
          {#if roast.bean_details.processing_method}
            <div class="inline-flex items-center px-3 py-1 rounded-full bg-coffee-cream/30 text-coffee-deep text-sm">
              <span class="text-coffee-medium mr-1">Process:</span>
              <span class="font-medium">{roast.bean_details.processing_method}</span>
            </div>
          {/if}
          {#if roast.bean_details.altitude}
            <div class="inline-flex items-center px-3 py-1 rounded-full bg-coffee-cream/30 text-coffee-deep text-sm">
              <span class="text-coffee-medium mr-1">Altitude:</span>
              <span class="font-medium">{roast.bean_details.altitude}m</span>
            </div>
          {/if}
          {#if roast.bean_details.extra?.region}
            <div class="inline-flex items-center px-3 py-1 rounded-full bg-coffee-cream/30 text-coffee-deep text-sm">
              <span class="text-coffee-medium mr-1">Region:</span>
              <span class="font-medium">{roast.bean_details.extra.region}</span>
            </div>
          {/if}
        </div>
      </div>
    {/if}
  </div>
</div>

<style>
  .bg-coffee-paper {
    background-color: #F5F5DC;
  }
  .bg-coffee-cream {
    background-color: #FFF599;
  }
  .text-coffee-deep {
    color: #786C3B;
  }
  .text-coffee-medium {
    color: #964B00;
  }
  .text-coffee-gold {
    color: #FFD700;
  }
  .border-coffee-light {
    border-color: #F5F5DC;
  }
  .border-coffee-gold {
    border-color: #FFD700;
  }
  .shadow-warm {
    box-shadow: 0 4px 8px rgba(255, 215, 0, 0.2);
  }
</style>