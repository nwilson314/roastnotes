<script lang="ts">
  import '../app.css';
  import Header from '$lib/components/Header.svelte';
  import type { LayoutData } from './$types';

  let { data }: { data: LayoutData } = $props();
</script>
  
<div class="min-h-screen bg-coffee-cream bg-texture-paper">
  <Header {data} />
  
  <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <slot />
  </main>
</div>
  
<style>
:root {
  --bg-color: #f4ece3;         /* parchment-like background */
  --primary-color: #8a4b28;    /* rich mahogany */
  --secondary-color: #6c4f3d;  /* deep leather brown */
  --accent-color: #a05a35;     /* warm accent */
  --text-color: #5a3e2b;       /* dark, bookish text */
  --font-serif: 'Garamond', serif;
  --font-sans: 'Helvetica Neue', sans-serif;
}

body {
  background-color: var(--bg-color);
  font-family: var(--font-sans);
  color: var(--text-color);
  margin: 0;
  padding: 0;
}
</style>