import type { PageServerLoad, Actions } from './$types';
import { error, fail } from '@sveltejs/kit';
import type { Roaster } from '$lib/types';
import { ApiClient, ApiError } from '$lib/server/api';
import { checkSession, validateSession } from '$lib/server/auth';

export const load: PageServerLoad = async ({ cookies }) => {

  const api = new ApiClient('');
  const roasters = await api.get<Roaster[]>('/roasters/');
  return { roasters };
};

export const actions: Actions = {
  createRoaster: async ({ request, cookies }) => {

    const { user, token } = await validateSession(cookies);

    const data = await request.formData();
    const roasterData = {
      name: data.get('name'),
      location: data.get('location') || undefined,
      website: data.get('website') || undefined,
      description: data.get('description') || undefined
    };

    const api = new ApiClient(token ?? '');
    const resp = await api.post('/roasters/', roasterData);
    console.log("Created roaster: ", resp)

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
