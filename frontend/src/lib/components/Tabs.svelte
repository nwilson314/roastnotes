<script>
  import { createEventDispatcher } from 'svelte';
  const dispatch = createEventDispatcher();
  
  export let tabs = [];
  export let active = '';

  function handleClick(tab) {
    dispatch('tabClick', tab);
  }
</script>

<div class="border-b border-coffee-deep/10">
  <nav class="-mb-px flex space-x-8" aria-label="Tabs">
    {#each tabs as tab}
      <button
        class="
          whitespace-nowrap py-4 px-1 border-b-2 font-inter text-sm font-medium
          {tab === active
            ? 'border-coffee-gold text-coffee-deep'
            : 'border-transparent text-coffee-medium hover:text-coffee-deep hover:border-coffee-light'}
          transition-all duration-200 ease-in-out
        "
        class:active={tab === active}
        on:click={() => handleClick(tab)}
      >
        {tab}
      </button>
    {/each}
  </nav>
</div>

<style>
  .border-b {
    display: flex;
    gap: 1rem;
    margin-bottom: 2rem;
    border-bottom: 2px solid var(--secondary-color);
  }
  .border-b button {
    background: none;
    border: none;
    padding: 0.5rem 1rem;
    font-size: 1.1rem;
    color: var(--text-color);
    cursor: pointer;
    transition: color 0.3s ease, border-bottom 0.3s ease;
  }
  .border-b button:hover {
    color: var(--primary-color);
  }
  .border-b button.active {
    border-bottom: 3px solid var(--primary-color);
    font-weight: bold;
  }
</style>