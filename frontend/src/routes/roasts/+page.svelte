<script lang="ts">
  import type { PageProps } from './$types';
  import { invalidateAll } from '$app/navigation';
  import RoastCard from '$lib/components/RoastCard.svelte';
  import GroupRoastCard from '$lib/components/GroupRoastCard.svelte';
  import type { Roast, UserGroup, GroupRoast, RoastDetails } from '$lib/types';
  import { RoastsView } from '$lib/types';
  import AddRoastModal from '$lib/components/AddRoastModal.svelte';
  import { goto } from '$app/navigation';

  let { data }: PageProps = $props();
  let roasts: Roast[] = data.roasts;
  let user_groups: UserGroup[] = data.user_groups;
  let group_roasts: GroupRoast[] = data.group_roasts;
  let groups = data.groups;
  const user_logged_in = data.user_logged_in;
  let selectedView: RoastsView = $state(RoastsView.Trending);
  let displayedRoasts: (Roast | GroupRoast)[] = $state(roasts);
  let selectedGroupId: number | null = $state(null);
  let showAddRoastModal = $state(false);

  $effect(() => {
    displayedRoasts = selectedView === RoastsView.Trending ? roasts : group_roasts;
  });

  function showTrendingView() {
    selectedView = RoastsView.Trending;
    selectedGroupId = null;
  }

  function showGroupsView() {
    selectedView = RoastsView.Groups;
    selectedGroupId = null;
  }

  function selectGroup(groupId: number) {
    selectedGroupId = groupId;
    displayedRoasts = group_roasts.filter((roast) => roast.id === groupId);
  }

  function showAllGroups() {
    selectedGroupId = null;
    displayedRoasts = group_roasts;
  }

  function isGroupRoast(roast: Roast | GroupRoast): roast is GroupRoast {
    return 'group_id' in roast && 'added_by_username' in roast;
  }

  function isRoast(roast: Roast | GroupRoast): roast is Roast {
    return !('group_id' in roast) || !('added_by_username' in roast);
  }

  function handleAddRoast() {
    showAddRoastModal = true;
  }

  function handleRoastClick(roast: Roast | GroupRoast) {
    const roastId = roast.id;
    goto(`/roasts/${roastId}`);
  }

</script>

<div class="min-h-screen bg-coffee-paper/30">
  <!-- Top Actions Bar -->
  <div class="sticky top-0 z-10 bg-white/80 backdrop-blur-sm border-b border-coffee-light/20 shadow-sm">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
      <div class="flex items-center justify-between">
        <div class="flex items-center space-x-4">
          <div class="flex items-center p-1.5 bg-coffee-cream/20 rounded-lg border border-coffee-light/20">
            <button 
              class="px-4 py-1.5 mx-0.5 rounded-md font-medium transition-all duration-200
                     {selectedView === RoastsView.Trending ? 
                       'bg-white text-coffee-deep shadow-warm translate-y-[-1px] active:translate-y-0' : 
                       'text-coffee-medium hover:text-coffee-deep'}"
              onclick={showTrendingView}
            >
              Trending
            </button>
            {#if user_logged_in}
              <button 
                class="px-4 py-1.5 mx-0.5 rounded-md font-medium transition-all duration-200
                       {selectedView === RoastsView.Groups ? 
                         'bg-white text-coffee-deep shadow-warm translate-y-[-1px] active:translate-y-0' : 
                         'text-coffee-medium hover:text-coffee-deep'}"
                onclick={showGroupsView}
              >
                Groups
              </button>
            {/if}
          </div>
        </div>
        
        <div class="flex items-center space-x-2">
          {#if user_logged_in}
            <button 
              class="px-3 py-1.5 bg-coffee-deep text-coffee-cream rounded-lg
                     hover:bg-coffee-medium transition-colors duration-200
                     flex items-center gap-1.5 text-sm"
              onclick={handleAddRoast}
            >
              <svg class="h-4 w-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" clip-rule="evenodd" />
              </svg>
              Add Roast
            </button>
            <select 
              class="px-3 py-2 rounded-lg border border-coffee-light/20 
                     text-coffee-deep bg-white"
            >
              <option>Most Recent</option>
              <option>Highest Rated</option>
              <option>Most Reviews</option>
            </select>
          {/if}
        </div>
      </div>
    </div>
  </div>

  <!-- Main Content -->
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <div class="flex gap-8">
      {#if selectedView === RoastsView.Groups && user_logged_in}
        <!-- Groups Sidebar -->
        <div class="w-64 shrink-0">
          <div class="bg-white rounded-xl border border-coffee-light/20 p-4 shadow-warm">
            <h3 class="font-garamond text-xl text-coffee-deep mb-4">Your Groups</h3>
            <div class="space-y-2">
              <button
                class="w-full px-3 py-2 text-left rounded-lg transition-colors duration-200
                       {selectedGroupId === null ? 
                         'bg-coffee-cream/20 text-coffee-deep' : 
                         'text-coffee-medium hover:bg-coffee-cream/10'}"
                onclick={showAllGroups}
              >
                All Groups ({user_groups.length})
              </button>
              {#each user_groups as group}
                <button
                  class="w-full px-3 py-2 text-left rounded-lg transition-colors duration-200
                         {selectedGroupId === group.id ? 
                           'bg-coffee-cream/20 text-coffee-deep' : 
                           'text-coffee-medium hover:bg-coffee-cream/10'}"
                  onclick={() => selectGroup(group.id)}
                >
                  <div class="font-medium">{group.name}</div>
                  <div class="text-sm text-coffee-medium">
                    {group.roast_count} roasts · {group.member_count} members
                  </div>
                </button>
              {/each}
            </div>
          </div>
        </div>
      {/if}

      <!-- Roasts Grid -->
      <div class="flex-1">
        <div class="bg-white rounded-xl border border-coffee-light/20 p-6 shadow-warm">
          <!-- Section Title -->
          <div class="flex items-center justify-between mb-6">
            <h2 class="font-garamond text-2xl text-coffee-deep">
              {#if selectedView === RoastsView.Groups}
                {#if selectedGroupId}
                  {groups[selectedGroupId].group_name}
                {:else}
                  All Group Roasts
                {/if}
              {:else}
                Trending Roasts
              {/if}
            </h2>
            {#if selectedView === RoastsView.Groups && selectedGroupId}
              <p class="text-coffee-medium">
                {data.groups[selectedGroupId].group_description}
              </p>
            {/if}
          </div>
          
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {#each displayedRoasts as roast (roast.id)}
              <div 
                class="cursor-pointer"
                onclick={() => handleRoastClick(roast)}
              >
                {#if isGroupRoast(roast)}
                  <GroupRoastCard {roast} />
                {:else if isRoast(roast)}
                  <RoastCard {roast} />
                {/if}
              </div>
            {/each}
          </div>
        </div>
      </div>
    </div>
  </div>
</div>

<AddRoastModal
  bind:show={showAddRoastModal}
  userGroups={data.user_groups}
  roasters={data.roasters}
  selectedGroupId={selectedGroupId}
  onClose={() => {
    showAddRoastModal = false;
  }}
  onRoastAdded={() => {
    invalidateAll();
  }}
/>

<style>
  /* Add any additional styles here */
  :global(.shadow-warm) {
    box-shadow: 0 4px 6px -1px rgba(120, 108, 59, 0.1), 
                0 2px 4px -1px rgba(120, 108, 59, 0.06);
  }
</style>