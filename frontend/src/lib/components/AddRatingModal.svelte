<script lang="ts">
  import { createEventDispatcher } from 'svelte';
  import Modal from './Modal.svelte';
  import type { Rating } from '$lib/types';
  import { convertRatingToFiveScale, convertRatingToHundredScale } from '$lib/types';

  export let show = false;
  export let roastId: number;
  export let roastName: string;
  export let groupId: number | undefined = undefined;
  export let existingRating: Rating | undefined = undefined;

  const dispatch = createEventDispatcher<{
    close: void;
    submit: { rating: Omit<Rating, 'id' | 'user_id' | 'created_at'> };
  }>();

  // Form state
  let rating = existingRating?.overall_score ? convertRatingToFiveScale(existingRating.overall_score) : 3;
  let brewMethod = existingRating?.brew_method ?? '';
  let ratio = existingRating?.ratio ?? '1:16';
  let temperature = existingRating?.temperature ?? 95;
  let grind = existingRating?.grind ?? '';
  let tastingNotes = existingRating?.tasting_notes ?? '';
  let preferredMethod = existingRating?.preferred_method ?? false;

  const commonBrewMethods = [
    'V60',
    'Aeropress',
    'French Press',
    'Moka Pot',
    'Espresso',
    'Chemex',
    'Cold Brew'
  ];

  function handleClose() {
    dispatch('close');
  }

  function handleSubmit() {
    dispatch('submit', {
      rating: {
        roast_id: roastId,
        group_id: groupId,
        brew_method: brewMethod,
        preferred_method: preferredMethod,
        ratio,
        temperature,
        grind,
        tasting_notes: tastingNotes || undefined,
        overall_score: convertRatingToHundredScale(rating)
      }
    });
    handleClose();
  }
</script>

<Modal {show} on:close={handleClose}>
  <div class="w-full max-w-2xl">
    <div class="bg-white rounded-xl shadow-warm overflow-hidden">
      <!-- Header -->
      <div class="px-6 py-4 bg-coffee-deep text-white">
        <h2 class="text-xl font-garamond">
          {existingRating ? 'Update Rating' : 'Add Rating'} for {roastName}
        </h2>
      </div>

      <!-- Form -->
      <form class="p-6 space-y-6" on:submit|preventDefault={handleSubmit}>
        <!-- Rating -->
        <div>
          <label class="block font-garamond text-lg text-coffee-deep mb-2">
            Overall Rating
          </label>
          <div class="flex items-center space-x-2">
            {#each Array(5) as _, i}
              <button
                type="button"
                class="text-2xl focus:outline-none"
                class:text-coffee-gold={i < rating}
                class:text-coffee-light={i >= rating}
                on:click={() => rating = i + 1}
              >
                ★
              </button>
            {/each}
            <span class="text-coffee-medium ml-2">({rating} / 5)</span>
          </div>
        </div>

        <!-- Brew Method -->
        <div>
          <label class="block font-garamond text-lg text-coffee-deep mb-2">
            Brew Method
          </label>
          <div class="flex flex-wrap gap-2 mb-2">
            {#each commonBrewMethods as method}
              <button
                type="button"
                class="px-3 py-1 rounded-full text-sm transition-colors"
                class:bg-coffee-deep={brewMethod === method}
                class:text-white={brewMethod === method}
                class:bg-coffee-cream/30={brewMethod !== method}
                class:text-coffee-deep={brewMethod !== method}
                on:click={() => brewMethod = method}
              >
                {method}
              </button>
            {/each}
          </div>
          <input
            type="text"
            bind:value={brewMethod}
            placeholder="Or enter your own method..."
            class="w-full px-3 py-2 rounded-lg bg-coffee-cream/10 border border-coffee-light/20 
                   focus:outline-none focus:border-coffee-medium/40 text-coffee-deep placeholder:text-coffee-medium/50"
          />
          <label class="flex items-center mt-2 text-coffee-medium">
            <input
              type="checkbox"
              bind:checked={preferredMethod}
              class="mr-2"
            />
            This is my preferred method for this roast
          </label>
        </div>

        <!-- Ratio -->
        <div>
          <label class="block font-garamond text-lg text-coffee-deep mb-2">
            Water to Coffee Ratio
          </label>
          <div class="flex items-center space-x-2">
            <input
              type="text"
              bind:value={ratio}
              placeholder="e.g., 1:16"
              class="w-32 px-3 py-2 rounded-lg bg-coffee-cream/10 border border-coffee-light/20 
                     focus:outline-none focus:border-coffee-medium/40 text-coffee-deep"
            />
            <span class="text-coffee-medium">(water:coffee)</span>
          </div>
        </div>

        <!-- Temperature -->
        <div>
          <label class="block font-garamond text-lg text-coffee-deep mb-2">
            Water Temperature (°C)
          </label>
          <input
            type="number"
            bind:value={temperature}
            min="0"
            max="100"
            step="0.5"
            class="w-32 px-3 py-2 rounded-lg bg-coffee-cream/10 border border-coffee-light/20 
                   focus:outline-none focus:border-coffee-medium/40 text-coffee-deep"
          />
        </div>

        <!-- Grind -->
        <div>
          <label class="block font-garamond text-lg text-coffee-deep mb-2">
            Grind Details
          </label>
          <input
            type="text"
            bind:value={grind}
            placeholder="e.g., Medium-fine, 15 clicks on Comandante"
            class="w-full px-3 py-2 rounded-lg bg-coffee-cream/10 border border-coffee-light/20 
                   focus:outline-none focus:border-coffee-medium/40 text-coffee-deep placeholder:text-coffee-medium/50"
          />
        </div>

        <!-- Tasting Notes -->
        <div>
          <label class="block font-garamond text-lg text-coffee-deep mb-2">
            Tasting Notes
          </label>
          <textarea
            bind:value={tastingNotes}
            rows="3"
            placeholder="Share your thoughts on the flavor profile..."
            class="w-full px-3 py-2 rounded-lg bg-coffee-cream/10 border border-coffee-light/20 
                   focus:outline-none focus:border-coffee-medium/40 text-coffee-deep placeholder:text-coffee-medium/50"
          ></textarea>
        </div>

        <!-- Actions -->
        <div class="flex justify-end space-x-3">
          <button
            type="button"
            class="px-4 py-2 text-coffee-medium hover:text-coffee-deep transition-colors"
            on:click={handleClose}
          >
            Cancel
          </button>
          <button
            type="submit"
            class="px-6 py-2 bg-coffee-deep text-white rounded-lg hover:bg-coffee-deep/90 
                   transition-colors font-medium"
          >
            {existingRating ? 'Update Rating' : 'Add Rating'}
          </button>
        </div>
      </form>
    </div>
  </div>
</Modal>
