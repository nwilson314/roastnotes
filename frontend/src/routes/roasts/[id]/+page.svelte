<script lang="ts">
  import type { PageData } from './$types';
  import { page } from '$app/stores';
  import { goto } from '$app/navigation';
  import { invalidateAll } from '$app/navigation';
  import type { Rating } from '$lib/types';
  import AddRatingModal from '$lib/components/AddRatingModal.svelte';
  import { convertRatingToFiveScale } from '$lib/types';
  import { fade } from 'svelte/transition';

  export let data: PageData;
  export let form;
  
  $: roast = data.roast;
  $: groupId = $page.url.searchParams.get('group');
  $: groupRating = data.groupRating;
  $: userRatings = data.userRatings;
  $: isLoggedIn = data.auth.isLoggedIn;
  $: currentRating = userRatings?.find(r => 
    r.roast_id === roast.id && 
    (!groupId || r.group_id?.toString() === groupId)
  );

  let showRatingModal = false;
  let notification: { type: 'success' | 'error'; message: string } | null = null;

  // Clear notification after 5 seconds
  $: if (notification) {
    const timer = setTimeout(() => {
      notification = null;
    }, 5000);
    return () => clearTimeout(timer);
  }

  // Show notification when form action completes
  $: if (form) {
    if (form.success) {
      notification = {
        type: 'success',
        message: 'Your rating has been saved. Thanks for sharing!'
      };
      showRatingModal = false;
    } else {
      notification = {
        type: 'error',
        message: form.message
      };
    }
  }

  // Get top 3 brew methods by rating
  $: topBrewMethods = roast.rating_stats?.brew_methods 
    ? Object.entries(roast.rating_stats.brew_methods)
        .sort((a, b) => b[1].avg_rating - a[1].avg_rating)
        .slice(0, 3)
    : [];

  function handleBack() {
    goto('/roasts');
  }

  async function handleRatingSubmit(event: CustomEvent<{ rating: Omit<Rating, 'id' | 'user_id' | 'created_at'> }>) {
    const formData = new FormData();
    const rating = event.detail.rating;
    
    Object.entries(rating).forEach(([key, value]) => {
      if (value !== undefined) {
        formData.append(key, value.toString());
      }
    });

    const response = await fetch('?/submitRating', {
      method: 'POST',
      body: formData
    });

    if (response.ok) {
      invalidateAll();
    }
  }
</script>

<!-- Notification -->
{#if notification}
  <div
    class="fixed top-4 right-4 z-50 max-w-sm"
    transition:fade
  >
    <div
      class="p-4 rounded-lg shadow-lg"
      class:bg-coffee-deep={notification.type === 'success'}
      class:text-white={notification.type === 'success'}
      class:bg-red-500={notification.type === 'error'}
      class:text-white={notification.type === 'error'}
    >
      {notification.message}
    </div>
  </div>
{/if}

<div class="min-h-screen bg-coffee-paper/30">
  <!-- Header -->
  <div class="sticky top-0 z-10 bg-white/80 backdrop-blur-sm border-b border-coffee-light/20 shadow-sm">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
      <div class="flex items-center justify-between">
        <div class="flex items-center space-x-4">
          <button
            class="text-coffee-medium hover:text-coffee-deep transition-colors"
            on:click={handleBack}
          >
            <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
            </svg>
          </button>
          <div>
            <h1 class="font-garamond text-2xl text-coffee-deep">{roast.name}</h1>
            <p class="text-coffee-medium">{roast.origin} • {roast.roast_level}</p>
          </div>
        </div>

        {#if isLoggedIn}
          <button
            class="px-4 py-2 bg-coffee-deep text-white rounded-lg hover:bg-coffee-deep/90 
                   transition-colors font-medium"
            on:click={() => showRatingModal = true}
          >
            {currentRating ? 'Update Rating' : 'Add Rating'}
          </button>
        {/if}
      </div>
    </div>
  </div>

  <!-- Main Content -->
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
      <!-- Bean Details -->
      <section class="bg-white rounded-xl border border-coffee-light/20 shadow-warm p-6">
        <h2 class="font-garamond text-xl text-coffee-deep mb-4">Bean Details</h2>
        <div class="grid grid-cols-2 gap-4 text-coffee-medium">
          <div>
            <p class="font-medium">Species</p>
            <p>{roast.bean_details.species}</p>
          </div>
          {#if roast.bean_details.cultivar}
            <div>
              <p class="font-medium">Cultivar</p>
              <p>{roast.bean_details.cultivar}</p>
            </div>
          {/if}
          {#if roast.bean_details.processing_method}
            <div>
              <p class="font-medium">Processing</p>
              <p>{roast.bean_details.processing_method}</p>
            </div>
          {/if}
          {#if roast.bean_details.altitude}
            <div>
              <p class="font-medium">Altitude</p>
              <p>{roast.bean_details.altitude}m</p>
            </div>
          {/if}
        </div>
      </section>

      <!-- Ratings Overview -->
      <section class="bg-white rounded-xl border border-coffee-light/20 shadow-warm p-6">
        <h2 class="font-garamond text-xl text-coffee-deep mb-4">
          {#if groupRating}
            {groupRating.group_name} Ratings
          {:else}
            Global Ratings
          {/if}
        </h2>

        <!-- Overall Rating -->
        <div class="flex items-baseline space-x-2 mb-6">
          <span class="text-4xl font-garamond text-coffee-gold">
            {(groupRating?.rating ?? roast.rating_stats.avg_rating).toFixed(1)}
          </span>
          <span class="text-coffee-medium">/ 5</span>
          <span class="text-coffee-medium ml-2">
            ({groupRating?.total_ratings ?? roast.rating_stats.total_ratings} ratings)
          </span>
        </div>

        <!-- Top Brew Methods -->
        {#if topBrewMethods.length > 0}
          <h3 class="font-garamond text-lg text-coffee-deep mb-3">Top Brewing Methods</h3>
          <div class="grid grid-cols-3 gap-4">
            {#each topBrewMethods as [method, stats]}
              <div class="p-3 rounded-lg bg-coffee-cream/10 border border-coffee-light/10">
                <h4 class="font-garamond text-coffee-deep mb-1">{method}</h4>
                <div class="flex items-baseline justify-center">
                  <span class="text-xl font-garamond text-coffee-gold">
                    {convertRatingToFiveScale(stats.avg_rating).toFixed(1)}
                  </span>
                  <span class="text-xs text-coffee-medium ml-1">/5</span>
                </div>
                <p class="text-xs text-coffee-medium text-center mt-1">
                  {stats.count} brew{stats.count !== 1 ? 's' : ''}
                </p>
              </div>
            {/each}
          </div>
        {/if}

        {#if groupRating && roast.rating_stats}
          <!-- Group vs Global Comparison -->
          <div class="mt-6 p-4 rounded-lg bg-coffee-cream/10 border border-coffee-light/10">
            <h3 class="font-garamond text-lg text-coffee-deep mb-3">Rating Comparison</h3>
            <div class="grid grid-cols-2 gap-4">
              <div class="text-center">
                <p class="text-sm text-coffee-medium mb-1">Group</p>
                <p class="text-xl font-garamond text-coffee-gold">
                  {groupRating.rating.toFixed(1)}
                </p>
                <p class="text-xs text-coffee-medium">
                  {groupRating.total_ratings} ratings
                </p>
              </div>
              <div class="text-center">
                <p class="text-sm text-coffee-medium mb-1">Global</p>
                <p class="text-xl font-garamond text-coffee-gold">
                  {roast.rating_stats.avg_rating.toFixed(1)}
                </p>
                <p class="text-xs text-coffee-medium">
                  {roast.rating_stats.total_ratings} ratings
                </p>
              </div>
            </div>
          </div>
        {/if}

        {#if !isLoggedIn}
          <div class="mt-6 p-4 rounded-lg bg-coffee-cream/10 border border-coffee-light/10 text-center">
            <p class="text-coffee-medium mb-3">Sign in to rate this roast and share your brewing experience.</p>
            <a
              href="/login"
              class="inline-block px-6 py-2 bg-coffee-deep text-white rounded-lg hover:bg-coffee-deep/90 
                     transition-colors font-medium"
            >
              Sign In
            </a>
          </div>
        {/if}
      </section>
    </div>
  </div>
</div>

<AddRatingModal
  show={showRatingModal}
  roastId={roast.id}
  roastName={roast.name}
  groupId={groupId ? parseInt(groupId) : undefined}
  existingRating={currentRating}
  on:close={() => showRatingModal = false}
  on:submit={handleRatingSubmit}
/>
