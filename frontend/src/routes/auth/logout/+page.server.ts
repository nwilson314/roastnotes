import { redirect } from '@sveltejs/kit';
import type { PageServerLoad, Actions } from './$types';

// Redirect if someone tries to visit /auth/logout directly
export const load: PageServerLoad = async ({cookies}) => {
  cookies.delete('roastnotes_token', { path: '/' });
  cookies.delete('roastnotes_user', { path: '/' });
  throw redirect(303, '/');
};

export const actions = {
  default: async ({ cookies }) => {
    cookies.delete('roastnotes_token', { path: '/' });
    cookies.delete('roastnotes_user', { path: '/' });
    
    throw redirect(303, '/');
  }
} satisfies Actions;
