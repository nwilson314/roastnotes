<script lang="ts">
  import { enhance } from '$app/forms';
  import type { Roaster } from '$lib/types';

  export let show = false;
  export let onClose = () => {};
  export let onRoasterAdded = () => {};

  let name = '';
  let location = '';
  let website = '';
  let description = '';
  let error: string | null = null;

  function closeModal() {
    name = '';
    location = '';
    website = '';
    description = '';
    error = null;
    onClose();
  }

  async function handleSubmit(event: SubmitEvent) {
    error = null;
    if (!name.trim()) {
      error = 'Name is required';
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
        <h2 class="text-xl font-medium text-coffee-deep">Add New Roaster</h2>
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
        action="?/createRoaster" 
        use:enhance={() => {
          return async ({ result }) => {
            if (result.type === 'success') {
              closeModal();
              onRoasterAdded();
            } else if (result.type === 'error') {
              error = result.error?.message || 'Failed to create roaster';
            }
          };
        }}
        class="p-6 space-y-4"
      >
        {#if error}
          <div class="p-3 bg-red-50 border border-red-200 rounded-lg text-red-700 text-sm">
            {error}
          </div>
        {/if}

        <!-- Name -->
        <div class="space-y-1">
          <label for="name" class="block text-sm font-medium text-coffee-deep">
            Name <span class="text-red-500">*</span>
          </label>
          <input
            type="text"
            id="name"
            name="name"
            bind:value={name}
            class="w-full px-3 py-2 rounded-lg border border-coffee-light/20 
                   focus:outline-none focus:ring-2 focus:ring-coffee-cream
                   placeholder:text-coffee-medium/50"
            placeholder="Counter Culture Coffee"
          />
        </div>

        <!-- Location -->
        <div class="space-y-1">
          <label for="location" class="block text-sm font-medium text-coffee-deep">
            Location
          </label>
          <input
            type="text"
            id="location"
            name="location"
            bind:value={location}
            class="w-full px-3 py-2 rounded-lg border border-coffee-light/20 
                   focus:outline-none focus:ring-2 focus:ring-coffee-cream
                   placeholder:text-coffee-medium/50"
            placeholder="Durham, NC"
          />
        </div>

        <!-- Website -->
        <div class="space-y-1">
          <label for="website" class="block text-sm font-medium text-coffee-deep">
            Website
          </label>
          <input
            type="url"
            id="website"
            name="website"
            bind:value={website}
            class="w-full px-3 py-2 rounded-lg border border-coffee-light/20 
                   focus:outline-none focus:ring-2 focus:ring-coffee-cream
                   placeholder:text-coffee-medium/50"
            placeholder="https://counterculturecoffee.com"
          />
        </div>

        <!-- Description -->
        <div class="space-y-1">
          <label for="description" class="block text-sm font-medium text-coffee-deep">
            Description
          </label>
          <textarea
            id="description"
            name="description"
            bind:value={description}
            rows="3"
            class="w-full px-3 py-2 rounded-lg border border-coffee-light/20 
                   focus:outline-none focus:ring-2 focus:ring-coffee-cream
                   placeholder:text-coffee-medium/50 resize-none"
            placeholder="Quality focused coffee roaster since 1995"
          ></textarea>
        </div>

        <!-- Actions -->
        <div class="flex justify-end space-x-3 pt-2">
          <button
            type="button"
            class="px-4 py-2 rounded-lg border border-coffee-light/20 text-coffee-medium 
                   hover:bg-coffee-light/10 transition-colors duration-200"
            onclick={closeModal}
          >
            Cancel
          </button>
          <button
            type="submit"
            class="px-4 py-2 rounded-lg bg-coffee-deep text-coffee-cream 
                   hover:bg-coffee-medium transition-colors duration-200"
          >
            Add Roaster
          </button>
        </div>
      </form>
    </div>
  </div>
{/if}
