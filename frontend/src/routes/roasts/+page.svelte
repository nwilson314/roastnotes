<script>
    import Tabs from '$lib/components/Tabs.svelte';
    import RoastCard from '$lib/components/RoastCard.svelte';
  
    let inGroup = true; // placeholder; replace with real group check
    let activeTab = inGroup ? 'Group' : 'Trending';
    const tabList = inGroup ? ['Group', 'Trending'] : ['Trending'];
  
    let trendingRoasts = [
      { id: 1, title: 'Espresso Magic', description: 'a bold, daring brew.' },
      { id: 2, title: 'Sunrise Blend', description: 'bright and early vibes.' }
    ];
  
    let groupRoasts = [
      { id: 3, title: 'Group Secret', description: 'crafted by your crew.' }
    ];
  
    function handleTabClick(tab) {
      activeTab = tab;
    }
  </script>
  
  <Tabs tabs={tabList} active={activeTab} on:tabClick={e => handleTabClick(e.detail)} />
  
  {#if activeTab === 'Group' && inGroup}
    {#each groupRoasts as roast (roast.id)}
      <RoastCard {roast} />
    {/each}
  {:else}
    {#each trendingRoasts as roast (roast.id)}
      <RoastCard {roast} />
    {/each}
  {/if}
  
  <style>
    /* additional styling as needed */
  </style>
  