import type { PageServerLoad, Actions } from './$types';
import { error, fail, redirect } from '@sveltejs/kit';
import type { AuthResponse } from '$lib/types';
import { ApiClient, ApiError } from '$lib/server/api';
import { checkSession, validateSession } from '$lib/server/auth';
import type { Roast, UserResponse, GroupRoast, UserGroup, UserGroupRoastsResponse, GroupRoastCollection, Roaster } from '$lib/types';

export const load: PageServerLoad = async ({ cookies }) => {
  const { user, token } = await checkSession(cookies);
  const user_logged_in = !!token;

  const api = new ApiClient(token ?? '');

  try {
    // Fetch trending roasts and roasters in parallel
    const [roasts, roasters] = await Promise.all([
      api.get<Roast[]>('/roasts/'),
      api.get<Roaster[]>('/roasters/')
    ]);

    let group_roasts: GroupRoast[] = [];
    let user_groups: UserGroup[] = [];
    let groups: {[key: string]: GroupRoastCollection} = {};

    if (user_logged_in && user) {

      const [user_groups, user_groups_roasts_response] = await Promise.all([
        api.get<UserGroup[]>(`/groups/user/${user.id}`),
        api.get<UserGroupRoastsResponse>(`/groups/user/${user.id}/roasts`)
      ]);
      groups = user_groups_roasts_response.groups;
      group_roasts = Object.values(groups).flatMap(group => group.roasts);
    }

    return {
      roasts: roasts.map((roast: Roast) => ({
        id: roast.id,
        user_id: roast.user_id,
        roaster_id: roast.roaster_id,
        name: roast.name,
        origin: roast.origin,
        single_origin: roast.single_origin,
        roast_level: roast.roast_level,
        created_at: roast.created_at,
        bean_details: roast.bean_details,
        cached_rating_stats: roast.cached_rating_stats
      })),
      group_roasts,
      groups,
      user_groups,
      roasters,
      user_logged_in
    };
  } catch (err) {
    if (err instanceof ApiError) {
      if (err.status === 401) {
        throw redirect(303, '/auth/logout');
      }
      throw error(err.status, err.message);
    }
    throw error(500, `Failed to load roasts data ${err}`);
  }
};

export const actions: Actions = {
  createRoast: async ({ request, cookies }) => {

    const { user, token } = await validateSession(cookies);

    const data = await request.formData();
    const roastData = {
      name: data.get('name'),
      origin: data.get('origin'),
      single_origin: data.get('single_origin') === 'true',
      roast_level: data.get('roast_level'),
      bean_details: {
        species: data.get('species'),
        cultivar: data.get('cultivar') || undefined,
        processing_method: data.get('processing_method') || undefined,
        altitude: data.get('altitude') ? Number(data.get('altitude')) : undefined
      },
      roaster_id: Number(data.get('roaster_id'))
    };

    const api = new ApiClient(token ?? '');
    const resp = await api.post('/roasts/', roastData);

    return { success: true };
  },
  getUserRatings: async ({ request, cookies }) => {
    const token = cookies.get('roastnotes_token');
    if (!token) {
      return fail(401, { message: 'Not authenticated' });
    }

    const data = await request.formData();
    const roastId = data.get('roastId');
    if (!roastId) {
      return fail(400, { message: 'Roast ID is required' });
    }

    const user_str = cookies.get('roastnotes_user');
    if (!user_str) {
      return fail(401, { message: 'User info not found' });
    }
    const user: UserResponse = JSON.parse(user_str);

    const res = await fetch(`https://roastnotes.fly.dev/ratings/roast/${roastId}?user_id=${user.id}`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });

    if (!res.ok) {
      return fail(res.status, { message: 'Failed to fetch user ratings' });
    }

    const ratings = await res.json();
    return { success: true, ratings };
  }
};
