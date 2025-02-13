<script lang="ts">
  import type { UserGroup, Roaster } from '$lib/types';
  import { RoastLevel } from '$lib/types';
  import SearchableDropdown from './SearchableDropdown.svelte';
  import { enhance } from '$app/forms';

  export let show = false;
  export let userGroups: UserGroup[] = [];
  export let selectedGroupId: number | null = null;
  export let onClose = () => {};
  export let onRoastAdded = () => {};
  export let roasters: Roaster[] = [];

  let name = '';
  let origin = '';
  let singleOrigin = false;
  let roastLevel = RoastLevel.medium;
  let species = '';
  let cultivar = '';
  let processingMethod = '';
  let altitude: number | undefined = undefined;
  let selectedGroup = selectedGroupId;
  let selectedRoaster: Roaster | null = null;
  let isSubmitting = false;
  let error: string | null = null;

  const roastLevels = [
    { value: RoastLevel.light, label: 'Light' },
    { value: RoastLevel.medium, label: 'Medium' },
    { value: RoastLevel.medium_dark, label: 'Medium-Dark' },
    { value: RoastLevel.dark, label: 'Dark' }
  ];

  function closeModal() {
    // Reset form
    name = '';
    origin = '';
    singleOrigin = false;
    roastLevel = RoastLevel.medium;
    species = '';
    cultivar = '';
    processingMethod = '';
    altitude = undefined;
    selectedGroup = selectedGroupId;
    selectedRoaster = null;
    error = null;
    onClose();
  }

  function handleSubmit(event: SubmitEvent) {
    error = null;
    if (!name.trim()) {
      error = 'Name is required';
      return;
    }
    if (!origin.trim()) {
      error = 'Origin is required';
      return;
    }
    if (!selectedRoaster) {
      error = 'Roaster is required';
      return;
    }
    if (!species.trim()) {
      error = 'Coffee species is required';
      return;
    }
  }
</script>

{#if show}
  <div class="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4">
    <div class="bg-white rounded-xl max-w-lg w-full max-h-[90vh] overflow-y-auto shadow-xl" 
         role="dialog" 
         aria-modal="true">
      <!-- Header -->
      <div class="px-6 py-4 border-b border-coffee-light/20 flex items-center justify-between">
        <h2 class="text-xl font-medium text-coffee-deep">Add New Roast</h2>
        <button 
          class="text-coffee-medium hover:text-coffee-deep p-1 rounded-lg 
                 hover:bg-coffee-light/10 transition-colors duration-200"
          onclick={closeModal}
        >
          <svg class="h-5 w-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
          </svg>
        </button>
      </div>

      <!-- Form -->
      <form 
        method="POST" 
        action="?/createRoast" 
        use:enhance={() => {
          isSubmitting = true;
          return async ({ result }) => {
            isSubmitting = false;
            if (result.type === 'success') {
              onRoastAdded();
              closeModal();
            } else if (result.type === 'error') {
              error = result.error?.message || 'Failed to create roast';
            }
          };
        }}
        onsubmit={handleSubmit}
        class="p-6 space-y-4"
      >
        {#if error}
          <div class="p-3 bg-red-50 border border-red-200 rounded-lg text-red-700 text-sm">
            {error}
          </div>
        {/if}

        <!-- Roaster -->
        <SearchableDropdown
          bind:selectedValue={selectedRoaster}
          label="Roaster"
          placeholder="Search for a roaster..."
          required
          allRoasters={roasters}
        />
        <input type="hidden" name="roaster_id" value={selectedRoaster?.id || ''}>

        <!-- Name -->
        <div>
          <label for="name" class="block text-sm font-medium text-coffee-deep mb-1">
            Name <span class="text-red-500">*</span>
          </label>
          <input
            type="text"
            id="name"
            name="name"
            bind:value={name}
            class="w-full px-3 py-2 rounded-lg border border-coffee-light/20 
                   focus:outline-none focus:ring-2 focus:ring-coffee-cream"
            placeholder="e.g., Ethiopia Yirgacheffe"
            required
          />
        </div>

        <!-- Origin -->
        <div>
          <label for="origin" class="block text-sm font-medium text-coffee-deep mb-1">
            Origin <span class="text-red-500">*</span>
          </label>
          <input
            type="text"
            id="origin"
            name="origin"
            bind:value={origin}
            class="w-full px-3 py-2 rounded-lg border border-coffee-light/20 
                   focus:outline-none focus:ring-2 focus:ring-coffee-cream"
            placeholder="e.g., Ethiopia"
            required
          />
        </div>

        <!-- Single Origin -->
        <div class="flex items-center">
          <input
            type="checkbox"
            id="single-origin"
            name="single_origin"
            bind:checked={singleOrigin}
            class="h-4 w-4 text-coffee-deep rounded border-coffee-light/20 
                   focus:ring-coffee-cream focus:ring-2"
          />
          <label for="single-origin" class="ml-2 text-sm text-coffee-deep">
            Single Origin
          </label>
        </div>

        <!-- Roast Level -->
        <div>
          <label for="roast-level" class="block text-sm font-medium text-coffee-deep mb-1">
            Roast Level
          </label>
          <select
            id="roast-level"
            name="roast_level"
            bind:value={roastLevel}
            class="w-full px-3 py-2 rounded-lg border border-coffee-light/20 
                   focus:outline-none focus:ring-2 focus:ring-coffee-cream"
          >
            {#each roastLevels as level}
              <option value={level.value}>{level.label}</option>
            {/each}
          </select>
        </div>

        <!-- Bean Details -->
        <div class="space-y-4">
          <h3 class="font-medium text-coffee-deep">Bean Details</h3>
          
          <!-- Species -->
          <div>
            <label for="species" class="block text-sm font-medium text-coffee-deep mb-1">
              Species <span class="text-red-500">*</span>
            </label>
            <input
              type="text"
              id="species"
              name="species"
              bind:value={species}
              class="w-full px-3 py-2 rounded-lg border border-coffee-light/20 
                     focus:outline-none focus:ring-2 focus:ring-coffee-cream"
              placeholder="e.g., Arabica"
              required
            />
          </div>

          <!-- Cultivar -->
          <div>
            <label for="cultivar" class="block text-sm font-medium text-coffee-deep mb-1">
              Cultivar
            </label>
            <input
              type="text"
              id="cultivar"
              name="cultivar"
              bind:value={cultivar}
              class="w-full px-3 py-2 rounded-lg border border-coffee-light/20 
                     focus:outline-none focus:ring-2 focus:ring-coffee-cream"
              placeholder="e.g., Bourbon"
            />
          </div>

          <!-- Processing Method -->
          <div>
            <label for="processing-method" class="block text-sm font-medium text-coffee-deep mb-1">
              Processing Method
            </label>
            <input
              type="text"
              id="processing-method"
              name="processing_method"
              bind:value={processingMethod}
              class="w-full px-3 py-2 rounded-lg border border-coffee-light/20 
                     focus:outline-none focus:ring-2 focus:ring-coffee-cream"
              placeholder="e.g., Washed"
            />
          </div>

          <!-- Altitude -->
          <div>
            <label for="altitude" class="block text-sm font-medium text-coffee-deep mb-1">
              Altitude (meters)
            </label>
            <input
              type="number"
              id="altitude"
              name="altitude"
              bind:value={altitude}
              class="w-full px-3 py-2 rounded-lg border border-coffee-light/20 
                     focus:outline-none focus:ring-2 focus:ring-coffee-cream"
              placeholder="e.g., 1800"
            />
          </div>
        </div>

        <!-- Group Selection -->
        {#if userGroups.length > 0}
          <div>
            <label for="group" class="block text-sm font-medium text-coffee-deep mb-1">
              Share with Group
            </label>
            <select
              id="group"
              bind:value={selectedGroup}
              class="w-full px-3 py-2 rounded-lg border border-coffee-light/20 
                     focus:outline-none focus:ring-2 focus:ring-coffee-cream"
            >
              <option value={null}>No Group</option>
              {#each userGroups as group}
                <option value={group.id}>{group.name}</option>
              {/each}
            </select>
          </div>
        {/if}

        <!-- Submit Button -->
        <div class="pt-2">
          <button
            type="submit"
            disabled={isSubmitting}
            class="w-full px-4 py-2 bg-coffee-deep text-coffee-cream rounded-lg
                   hover:bg-coffee-medium transition-colors duration-200
                   disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isSubmitting ? 'Adding Roast...' : 'Add Roast'}
          </button>
        </div>
      </form>
    </div>
  </div>
{/if}
