<script lang="ts">
  import type { PageData } from './$types';
  import AddRoasterModal from '$lib/components/AddRoasterModal.svelte';
  import { page } from '$app/stores';
  import { invalidateAll } from '$app/navigation';

  export let data: PageData;

  let searchInput = '';
  let showAddRoasterModal = false;

  $: roasters = data.roasters.filter(roaster => {
    if (!searchInput) return true;
    const search = searchInput.toLowerCase();
    return (
      roaster.name.toLowerCase().includes(search) ||
      (roaster.location?.toLowerCase().includes(search)) ||
      (roaster.description?.toLowerCase().includes(search))
    );
  });

  $: isLoggedIn = !!$page.data.user;

  async function handleRoasterAdded() {
    await invalidateAll();
  }
</script>

<div class="min-h-screen bg-coffee-paper/30">
  <!-- Top Bar -->
  <div class="sticky top-0 z-10 bg-white/80 backdrop-blur-sm border-b border-coffee-light/20 shadow-sm">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
      <div class="flex justify-between items-center gap-4">
        <!-- Search Bar -->
        <div class="flex-1 max-w-2xl">
          <div class="relative">
            <input
              type="text"
              bind:value={searchInput}
              placeholder=" Search roasters..."
              class="w-full pl-14 pr-4 py-2 rounded-lg border border-coffee-light/20 
                     focus:outline-none focus:ring-2 focus:ring-coffee-cream"
            />
            <div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
              <svg class="h-5 w-5 text-coffee-medium" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z" clip-rule="evenodd" />
              </svg>
            </div>
            {#if searchInput}
              <button
                class="absolute inset-y-0 right-0 pr-3 flex items-center text-coffee-medium hover:text-coffee-deep"
                onclick={() => searchInput = ''}
              >
                <svg class="h-5 w-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
                </svg>
              </button>
            {/if}
          </div>
        </div>

        <!-- Add New Button -->
        {#if isLoggedIn}
          <button
            onclick={() => showAddRoasterModal = true}
            class="px-3 py-1.5 bg-coffee-deep text-coffee-cream rounded-lg
                   hover:bg-coffee-medium transition-colors duration-200
                   flex items-center gap-1.5 text-sm"
          >
            <svg class="h-4 w-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" clip-rule="evenodd" />
            </svg>
            Add Roaster
          </button>
        {/if}
      </div>
    </div>
  </div>

  <!-- Main Content -->
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    {#if roasters.length === 0}
      <div class="text-center py-12">
        {#if searchInput}
          <p class="text-coffee-medium">No roasters found matching "{searchInput}"</p>
        {:else}
          <p class="text-coffee-medium">No roasters added yet. {#if isLoggedIn}Add your first roaster!{/if}</p>
        {/if}
      </div>
    {:else}
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
        {#each roasters as roaster (roaster.id)}
          <div class="bg-white rounded-lg shadow-warm border border-coffee-light/10 p-6 hover:border-coffee-light/30 transition-colors duration-200">
            <h3 class="text-xl font-medium text-coffee-deep mb-2">{roaster.name}</h3>
            {#if roaster.location}
              <p class="text-coffee-medium text-sm mb-3">{roaster.location}</p>
            {/if}
            {#if roaster.description}
              <p class="text-coffee-medium/80 text-sm mb-4">{roaster.description}</p>
            {/if}
            {#if roaster.website}
              <a 
                href={roaster.website} 
                target="_blank" 
                rel="noopener noreferrer"
                class="inline-flex items-center text-sm text-coffee-medium hover:text-coffee-deep transition-colors duration-200"
              >
                <svg class="h-4 w-4 mr-1" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd" d="M4.083 9h1.946c.089-1.546.383-2.97.837-4.118A6.004 6.004 0 004.083 9zM10 2a8 8 0 100 16 8 8 0 000-16zm0 2c-.076 0-.232.032-.465.262-.238.234-.497.623-.737 1.182-.389.907-.673 2.142-.766 3.556h3.936c-.093-1.414-.377-2.649-.766-3.556-.24-.56-.5-.948-.737-1.182C10.232 4.032 10.076 4 10 4zm3.971 5c-.089-1.546-.383-2.97-.837-4.118A6.004 6.004 0 0115.917 9h-1.946zm-2.003 2H8.032c.093 1.414.377 2.649.766 3.556.24.56.5.948.737 1.182.233.23.389.262.465.262.076 0 .232-.032.465-.262.238-.234.498-.623.737-1.182.389-.907.673-2.142.766-3.556zm1.166 4.118c.454-1.147.748-2.572.837-4.118h1.946a6.004 6.004 0 01-2.783 4.118zm-6.268 0C6.412 13.97 6.118 12.546 6.03 11H4.083a6.004 6.004 0 002.783 4.118z" clip-rule="evenodd" />
                </svg>
                Visit Website
              </a>
            {/if}
          </div>
        {/each}
      </div>
    {/if}
  </div>
</div>

<AddRoasterModal
  bind:show={showAddRoasterModal}
  onClose={() => showAddRoasterModal = false}
  onRoasterAdded={handleRoasterAdded}
/>
