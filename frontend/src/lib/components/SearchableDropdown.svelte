<script lang="ts">
  import { onMount } from 'svelte';
  import type { Roaster } from '$lib/types';

  export let selectedValue: Roaster | null = null;
  export let placeholder = 'Search...';
  export let label = '';
  export let required = false;
  export let allRoasters: Roaster[] = [];

  let searchTerm = '';
  let isOpen = false;
  let inputElement: HTMLInputElement;

  $: filteredRoasters = searchTerm
    ? allRoasters.filter(roaster => {
        const search = searchTerm.toLowerCase();
        return (
          roaster.name.toLowerCase().includes(search) ||
          (roaster.location?.toLowerCase().includes(search)) ||
          (roaster.description?.toLowerCase().includes(search))
        );
      })
    : [];

  function handleSelect(option: Roaster) {
    selectedValue = option;
    searchTerm = option.name;
    isOpen = false;
  }

  function handleFocus() {
    if (searchTerm) {
      isOpen = true;
    }
  }

  function handleBlur() {
    // Delay closing to allow click events to fire
    setTimeout(() => {
      isOpen = false;
      if (!selectedValue) {
        searchTerm = '';
      }
    }, 200);
  }
</script>

<div class="relative">
  {#if label}
    <label for="roaster-search" class="block text-sm font-medium text-coffee-deep mb-1">
      {label} {#if required}<span class="text-red-500">*</span>{/if}
    </label>
  {/if}
  <div class="relative">
    <input
      type="text"
      id="roaster-search"
      bind:value={searchTerm}
      bind:this={inputElement}
      on:input={() => isOpen = true}
      on:focus={handleFocus}
      on:blur={handleBlur}
      placeholder={placeholder}
      class="w-full px-3 py-2 rounded-lg border border-coffee-light/20 
             focus:outline-none focus:ring-2 focus:ring-coffee-cream"
      {required}
    />
  </div>

  {#if isOpen && filteredRoasters.length > 0}
    <ul
      class="absolute z-50 w-full mt-1 bg-white rounded-lg shadow-lg border border-coffee-light/20 
             max-h-60 overflow-auto"
    >
      {#each filteredRoasters as option (option.id)}
        <li>
          <button
            type="button"
            class="w-full px-4 py-2 text-left hover:bg-coffee-cream/10 focus:bg-coffee-cream/10
                   focus:outline-none transition-colors duration-150"
            on:click={() => handleSelect(option)}
          >
            <div class="font-medium">{option.name}</div>
            {#if option.location}
              <div class="text-sm text-coffee-medium">{option.location}</div>
            {/if}
          </button>
        </li>
      {/each}
    </ul>
  {:else if isOpen && searchTerm}
    <div class="absolute z-50 w-full mt-1 bg-white rounded-lg shadow-lg border border-coffee-light/20 p-4 text-center text-coffee-medium">
      No roasters found
    </div>
  {/if}
</div>
