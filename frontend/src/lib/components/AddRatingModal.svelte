<script lang="ts">
  import type { Rating } from '$lib/types';
  import { convertRatingToFiveScale, convertRatingToHundredScale } from '$lib/types';
  import { enhance } from '$app/forms';

  export let show = false;
  export let roastId: number;
  export let roastName: string;
  export let groupId: number | undefined = undefined;
  export let existingRating: Rating | undefined = undefined;
  export let onClose = () => {};
  export let onRatingAdded = () => {};

  // Form state
  let rating = existingRating?.overall_score ? convertRatingToFiveScale(existingRating.overall_score) : 3;
  let brewMethod = existingRating?.brew_method ?? '';
  let ratio = existingRating?.ratio ?? '1:16';
  let temperature = existingRating?.temperature ?? 95;
  let grind = existingRating?.grind ?? '';
  let tastingNotes = existingRating?.tasting_notes ?? '';
  let preferredMethod = existingRating?.preferred_method ?? false;
  let error: string | null = null;
  let isSubmitting = false;

  const commonBrewMethods = [
    'V60',
    'Aeropress',
    'French Press',
    'Moka Pot',
    'Espresso',
    'Chemex',
    'Cold Brew'
  ];

  function closeModal() {
    // Reset form
    rating = 3;
    brewMethod = '';
    ratio = '1:16';
    temperature = 95;
    grind = '';
    tastingNotes = '';
    preferredMethod = false;
    error = null;
    show = false;
    onClose();
  }

  function handleSubmit() {
    error = null;
    if (!brewMethod) {
      error = 'Please select or enter a brew method';
      return;
    }
  }
</script>

{#if show}
  <div class="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4">
    <div class="bg-white rounded-xl max-w-2xl w-full max-h-[90vh] overflow-y-auto shadow-xl" 
         role="dialog" 
         aria-modal="true">
      <!-- Header -->
      <div class="px-6 py-4 bg-coffee-deep text-white">
        <h2 class="text-xl font-garamond">
          {existingRating ? 'Update Rating' : 'Add Rating'} for {roastName}
        </h2>
      </div>

      <!-- Form -->
      <form 
        method="POST"
        action="?/submitRating"
        use:enhance={() => {
          isSubmitting = true;
          return async ({ result }) => {
            isSubmitting = false;
            if (result.type === 'success') {
              onRatingAdded();
              closeModal();
            } else if (result.type === 'error') {
              error = result.error?.message || 'Failed to create roast';
            }
          };
        }}
        onsubmit={handleSubmit}
        class="p-6 space-y-6"
      >
        {#if error}
          <div class="p-3 bg-red-50 border border-red-200 rounded-lg text-red-700 text-sm">
            {error}
          </div>
        {/if}

        <!-- Hidden fields -->
        <input type="hidden" name="roast_id" value={roastId} />
        {#if groupId}
          <input type="hidden" name="group_id" value={groupId} />
        {/if}
        <input type="hidden" name="rating" value={convertRatingToHundredScale(rating)} />

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
                onclick={() => rating = i + 1}
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
                class:bg-coffee-cream-light={brewMethod !== method}
                class:text-coffee-deep={brewMethod !== method}
                onclick={() => brewMethod = method}
              >
                {method}
              </button>
            {/each}
          </div>
          <input
            type="text"
            name="brew_method"
            bind:value={brewMethod}
            placeholder="Or enter your own method..."
            class="w-full px-3 py-2 rounded-lg bg-coffee-cream/10 border border-coffee-light/20 
                   focus:outline-none focus:border-coffee-medium/40 text-coffee-deep placeholder:text-coffee-medium/50"
          />
          <label class="flex items-center mt-2 text-coffee-medium">
            <input
              type="checkbox"
              name="preferred_method"
              bind:checked={preferredMethod}
              class="mr-2 text-coffee-deep focus:ring-coffee-medium/40"
            />
            This is my preferred brewing method for this roast
          </label>
        </div>

        <!-- Brew Parameters -->
        <div class="grid grid-cols-3 gap-4">
          <div>
            <label class="block font-garamond text-lg text-coffee-deep mb-2">
              Ratio
            </label>
            <input
              type="text"
              name="ratio"
              bind:value={ratio}
              placeholder="e.g. 1:16"
              class="w-full px-3 py-2 rounded-lg bg-coffee-cream/10 border border-coffee-light/20 
                     focus:outline-none focus:border-coffee-medium/40 text-coffee-deep"
            />
          </div>
          <div>
            <label class="block font-garamond text-lg text-coffee-deep mb-2">
              Temperature (°C)
            </label>
            <input
              type="number"
              name="temperature"
              bind:value={temperature}
              min="0"
              max="100"
              class="w-full px-3 py-2 rounded-lg bg-coffee-cream/10 border border-coffee-light/20 
                     focus:outline-none focus:border-coffee-medium/40 text-coffee-deep"
            />
          </div>
          <div>
            <label class="block font-garamond text-lg text-coffee-deep mb-2">
              Grind Size
            </label>
            <input
              type="text"
              name="grind"
              bind:value={grind}
              placeholder="e.g. Medium-Fine"
              class="w-full px-3 py-2 rounded-lg bg-coffee-cream/10 border border-coffee-light/20 
                     focus:outline-none focus:border-coffee-medium/40 text-coffee-deep"
            />
          </div>
        </div>

        <!-- Tasting Notes -->
        <div>
          <label class="block font-garamond text-lg text-coffee-deep mb-2">
            Tasting Notes
          </label>
          <textarea
            name="notes"
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
            onclick={closeModal}
            disabled={isSubmitting}
          >
            Cancel
          </button>
          <button
            type="submit"
            class="px-4 py-2 bg-coffee-deep text-white rounded-lg hover:bg-coffee-medium transition-colors"
            disabled={isSubmitting}
          >
            {#if isSubmitting}
              Saving...
            {:else}
              {existingRating ? 'Update Rating' : 'Add Rating'}
            {/if}
          </button>
        </div>
      </form>
    </div>
  </div>
{/if}
