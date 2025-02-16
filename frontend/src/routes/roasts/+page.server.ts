import type { PageServerLoad, Actions } from './$types';
import { error, fail, redirect } from '@sveltejs/kit';
import type { Roast, UserResponse, GroupRoast, UserGroup, UserGroupRoastsResponse, GroupRoastCollection, Roaster } from '$lib/types';

export const load: PageServerLoad = async ({ cookies }) => {
  const token = cookies.get('roastnotes_token');
  const user_logged_in = !!token;

  const headers: Record<string, string> = {
    'Content-Type': 'application/json'
  };

  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  // Fetch trending roasts
  const trending_res = await fetch('https://roastnotes.fly.dev/roasts/', {
    method: 'GET',
    headers
  });

  if (!trending_res.ok) {
    throw error(trending_res.status, 'Failed to fetch trending roasts');
  }

  const roasts: Roast[] = await trending_res.json();

  // Fetch all roasters
  const roastersRes = await fetch('https://roastnotes.fly.dev/roasters/', {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json'
    }
  });

  if (!roastersRes.ok) {
    if (roastersRes.status === 401) {
      // Most likely an auth error, redirect through logout page for proper handling
      throw redirect(303, '/auth/logout');
    }
    throw error(roastersRes.status, 'Failed to fetch roasters');
  }

  const roasters: Roaster[] = await roastersRes.json();

  let group_roasts: GroupRoast[] = [];
  let user_groups: UserGroup[] = [];
  let groups: {[key: string]: GroupRoastCollection} = {};

  if (user_logged_in) {
    // Get user info from cookie
    const user_str = cookies.get('roastnotes_user');
    if (!user_str) {
      throw error(401, 'User info not found');
    }
    const user: UserResponse = JSON.parse(user_str);

    // First get user's groups
    const groups_res = await fetch(`https://roastnotes.fly.dev/groups/user/${user.id}`, {
      method: 'GET',
      headers,
      credentials: 'include'
    });

    if (!groups_res.ok) {
      if (groups_res.status === 401) {
        // Most likely an auth error, redirect through logout page for proper handling
        throw redirect(303, '/auth/logout');
      }
      throw error(groups_res.status, 'Failed to fetch user groups');
    }

    user_groups = await groups_res.json();

    // Then get all roasts for user's groups
    const group_roasts_res = await fetch(`https://roastnotes.fly.dev/groups/user/${user.id}/roasts`, {
      method: 'GET',
      headers,
      credentials: 'include'
    });

    if (!group_roasts_res.ok) {
      throw error(group_roasts_res.status, 'Failed to fetch user group roasts');
    }

    let user_groups_roasts_response: UserGroupRoastsResponse = await group_roasts_res.json();
    let groups = user_groups_roasts_response.groups;
    group_roasts = Object.values(groups).flatMap(group => group.roasts);
    console.log(roasts)
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
};

export const actions: Actions = {
  createRoast: async ({ request, cookies }) => {
    const token = cookies.get('roastnotes_token');
    if (!token) {
      throw error(401, 'Unauthorized');
    }

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

    const res = await fetch('https://roastnotes.fly.dev/roasts/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify(roastData)
    });

    if (!res.ok) {
      return fail(res.status, { error: 'Failed to create roast' });
    }

    return { success: true };
  },
  submitRating: async ({ request, cookies }) => {
    try {
      const data = await request.formData();
      const roastId = data.get('roast_id');
      const rating = data.get('rating');
      const brewMethod = data.get('brew_method');
      const notes = data.get('notes');

      if (!roastId || !rating || !brewMethod) {
        return { type: 'error', error: { message: 'Missing required fields' } };
      }

      const token = cookies.get('roastnotes_token');
      if (!token) {
        return { type: 'error', error: { message: 'Not authenticated' } };
      }

      const response = await fetch(`https://roastnotes.fly.dev/roasts/${roastId}/ratings`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          rating: Number(rating),
          brew_method: brewMethod,
          notes: notes || undefined
        })
      });

      if (!response.ok) {
        const error = await response.json();
        return { type: 'error', error };
      }

      return { type: 'success' };
    } catch (error) {
      console.error('Error submitting rating:', error);
      return { 
        type: 'error', 
        error: { message: 'Failed to submit rating. Please try again.' }
      };
    }
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
