import { writable } from 'svelte/store';
import type { UserResponse } from '$lib/types';

type AuthState = {
  isLoggedIn: boolean;
  user: UserResponse | null;
};

function createAuthStore() {
  const { subscribe, set, update } = writable<AuthState>({
    isLoggedIn: false,
    user: null
  });

  return {
    subscribe,
    
    // Initialize store with server-side data
    init: (user: UserResponse | null) => {
      set({
        isLoggedIn: !!user,
        user
      });
    },

    // Update user data
    updateUser: (user: UserResponse) => {
      set({
        isLoggedIn: true,
        user
      });
    },

    // Clear auth state
    logout: () => {
      set({
        isLoggedIn: false,
        user: null
      });
    }
  };
}

export const auth = createAuthStore();
