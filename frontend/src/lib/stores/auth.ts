import { writable } from 'svelte/store';
import type { UserResponse, AuthResponse } from '$lib/types';

type AuthState = {
  isLoggedIn: boolean;
  user: UserResponse | null;
  token: string | null;
};

function createAuthStore() {
  const { subscribe, set, update } = writable<AuthState>({
    isLoggedIn: false,
    user: null,
    token: null
  });

  return {
    subscribe,
    
    // Initialize store with server-side data
    init: (user: UserResponse | null, token: string | null) => {
      set({
        isLoggedIn: !!user && !!token,
        user,
        token
      });
    },

    // Initialize with full auth response (for registration/login)
    initWithAuth: (auth: AuthResponse) => {
      set({
        isLoggedIn: true,
        user: auth.user,
        token: auth.token.access_token
      });
    },

    // Update user data only
    updateUser: (user: UserResponse) => {
      update(state => ({
        ...state,
        user
      }));
    },

    // Clear auth state
    logout: () => {
      set({
        isLoggedIn: false,
        user: null,
        token: null
      });
    }
  };
}

export const auth = createAuthStore();
