<script lang="ts">
  import type { GroupRoast } from '$lib/types';
  
  export let roast: GroupRoast;

  $: ratingDiff = roast.group_rating - roast.global_rating;
  $: ratingColor = ratingDiff > 0 ? 'text-emerald-500' : ratingDiff < 0 ? 'text-rose-500' : 'text-coffee-medium';
  $: ratingIcon = ratingDiff > 0 ? '↑' : ratingDiff < 0 ? '↓' : '•';
</script>

<div class="bg-white rounded-xl border border-coffee-light/20 shadow-warm overflow-hidden">
  <div class="p-6 bg-coffee-paper/30">
    <!-- Header: Name, Origin, Rating -->
    <div class="flex items-center justify-between mb-4">
      <div class="flex items-center space-x-3">
        <div class="w-10 h-10 rounded-full bg-coffee-deep/10 flex items-center justify-center">
          <span class="font-garamond text-coffee-deep text-lg">
            {roast.name.substring(0, 2)}
          </span>
        </div>
        <div class="text-left">
          <h3 class="font-garamond text-xl text-coffee-deep">{roast.name}</h3>
          <p class="text-sm text-coffee-medium">{roast.origin}</p>
        </div>
      </div>
      <div class="text-right">
        <div class="flex items-baseline justify-end">
          <span class="text-2xl font-garamond text-coffee-gold">{roast.group_rating.toFixed(1)}</span>
          <span class="text-sm text-coffee-medium ml-1">/5</span>
        </div>
        <p class="text-xs text-coffee-medium">
          {roast.group_total_ratings} group rating{roast.group_total_ratings !== 1 ? 's' : ''}
        </p>
      </div>
    </div>

    <!-- Rating Comparison -->
    <div class="mt-4 p-3 rounded-lg bg-white/50 border border-coffee-light/10">
      <div class="flex items-center justify-between mb-2">
        <h4 class="font-garamond text-lg text-coffee-deep">Ratings</h4>
        <div class="flex items-center space-x-1">
          <span class={ratingColor}>{ratingIcon}</span>
          <span class="text-sm text-coffee-medium">
            {Math.abs(ratingDiff).toFixed(1)} {ratingDiff > 0 ? 'higher' : ratingDiff < 0 ? 'lower' : 'same'} than global
          </span>
        </div>
      </div>
      
      <div class="grid grid-cols-2 gap-4">
        <!-- Group Rating -->
        <div class="text-center p-2 rounded-lg bg-coffee-cream/10">
          <p class="text-sm text-coffee-medium mb-1">Group</p>
          <div class="flex items-baseline justify-center">
            <span class="text-xl font-garamond text-coffee-gold">{roast.group_rating.toFixed(1)}</span>
            <span class="text-xs text-coffee-medium ml-1">/5</span>
          </div>
          <p class="text-xs text-coffee-medium mt-1">
            {roast.group_total_ratings} rating{roast.group_total_ratings !== 1 ? 's' : ''}
          </p>
        </div>

        <!-- Global Rating -->
        <div class="text-center p-2 rounded-lg bg-coffee-cream/10">
          <p class="text-sm text-coffee-medium mb-1">Global</p>
          <div class="flex items-baseline justify-center">
            <span class="text-xl font-garamond text-coffee-gold">{roast.global_rating.toFixed(1)}</span>
            <span class="text-xs text-coffee-medium ml-1">/5</span>
          </div>
          <p class="text-xs text-coffee-medium mt-1">
            {roast.global_total_ratings} rating{roast.global_total_ratings !== 1 ? 's' : ''}
          </p>
        </div>
      </div>
    </div>

    <!-- Added By -->
    <div class="mt-4 text-sm text-coffee-medium">
      <p>Added by {roast.added_by} • {new Date(roast.added_at).toLocaleDateString()}</p>
      {#if roast.notes}
        <p class="mt-2 italic">{roast.notes}</p>
      {/if}
    </div>
  </div>
</div>
