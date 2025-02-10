import { writable } from 'svelte/store';

// Auth store
export const user = writable<null | { email: string }>(null);

// Basic community stats for non-authenticated users
export const communityStats = writable({
  total_roasts: 0,
  active_roasters: 0,
  popular_origins: [],
  recent_activity: {
    new_roasts_24h: 0,
    new_reviews_24h: 0
  }
});
