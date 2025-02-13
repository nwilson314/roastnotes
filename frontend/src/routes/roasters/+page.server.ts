import type { PageServerLoad, Actions } from './$types';
import { error, fail } from '@sveltejs/kit';
import type { Roaster } from '$lib/types';

export const load: PageServerLoad = async ({ cookies }) => {
  const token = cookies.get('roastnotes_token');
  const user_logged_in = !!token;

  const headers = {
    'Content-Type': 'application/json'
  };

  const res = await fetch('https://roastnotes.fly.dev/roasters/', {
    method: 'GET',
    headers
  });

  if (!res.ok) {
    throw error(res.status, 'Failed to fetch roasters');
  }

  const roasters: Roaster[] = await res.json();
  return { roasters };
};

export const actions: Actions = {
  createRoaster: async ({ request, cookies }) => {
    const token = cookies.get('roastnotes_token');
    if (!token) {
      throw error(401, 'Unauthorized');
    }

    const data = await request.formData();
    const roasterData = {
      name: data.get('name'),
      location: data.get('location') || undefined,
      website: data.get('website') || undefined,
      description: data.get('description') || undefined
    };

    const res = await fetch('https://roastnotes.fly.dev/roasters/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify(roasterData)
    });

    if (!res.ok) {
      throw error(res.status, 'Failed to create roaster');
    }

    return { success: true };
  },

  searchRoasters: async ({ url, cookies }) => {
    const token = cookies.get('roastnotes_token');
    if (!token) {
      return fail(401, { error: 'Unauthorized' });
    }

    const query = url.searchParams.get('q');
    if (!query) {
      return { roasters: [] };
    }

    const res = await fetch(`https://roastnotes.fly.dev/roasters/search?q=${encodeURIComponent(query)}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      }
    });

    if (!res.ok) {
      return fail(res.status, { error: 'Failed to search roasters' });
    }

    const roasters = await res.json();
    return { roasters };
  }
};
