import type { PageServerLoad, Actions } from './$types';
import { error, fail } from '@sveltejs/kit';
import type { RoastDetails, Rating, UserResponse } from '$lib/types';

interface LoadResponse {
  roast: RoastDetails;
  groupRating?: {
    group_id: number;
    group_name: string;
    added_by_username: string;
    rating: number;
    total_ratings: number;
  };
  userRatings?: Rating[];
  auth: {
    isLoggedIn: boolean;
    userId?: number;
  };
}

export const load: PageServerLoad<LoadResponse> = async ({ params, url, cookies }) => {
  const roastId = parseInt(params.id);
  if (isNaN(roastId)) {
    throw error(400, {
      message: 'Hmm, that doesn\'t look like a valid roast ID. Care to try another?'
    });
  }

  const groupId = url.searchParams.get('group');
  const token = cookies.get('roastnotes_token');
  const user_logged_in = !!token;

  const headers: Record<string, string> = {
    'Content-Type': 'application/json'
  };

  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }
  
  try {
    // Get base roast details
    const roastResponse = await fetch(`https://roastnotes.fly.dev/roasts/${roastId}`, {
      headers
    });
    
    if (roastResponse.status === 404) {
      throw error(404, {
        message: 'We couldn\'t find this roast in our collection. Perhaps it was removed?'
      });
    }
    
    if (!roastResponse.ok) {
      throw error(roastResponse.status, {
        message: 'Something went wrong while brewing up the roast details. Mind trying again?'
      });
    }

    const roast: RoastDetails = await roastResponse.json();

    // Get group-specific rating if group ID is provided
    let groupRating = undefined;
    if (groupId) {
      const groupResponse = await fetch(
        `https://roastnotes.fly.dev/roasts/${roastId}/groups/${groupId}`,
        { headers }
      );
      
      if (groupResponse.status === 404) {
        throw error(404, {
          message: 'This roast doesn\'t seem to be part of the specified group anymore.'
        });
      }
      
      if (!groupResponse.ok) {
        throw error(groupResponse.status, {
          message: 'Had trouble getting the group\'s take on this roast. Care to refresh?'
        });
      }
      
      groupRating = await groupResponse.json();
    }

    // Get user ratings if logged in
    let userRatings = undefined;
    if (user_logged_in) {
      const user_str = cookies.get('roastnotes_user');
      if (!user_str) {
        throw error(401, {
          message: 'Looks like your session needs a refresh. Mind logging in again?'
        });
      }
      
      const user: UserResponse = JSON.parse(user_str);

      const ratingsResponse = await fetch(
        `https://roastnotes.fly.dev/ratings/roasts/${roastId}?user_id=${user.id}${groupId ? `&group_id=${groupId}` : ''}`,
        { headers }
      );
      
      if (!ratingsResponse.ok) {
        console.error('Failed to fetch user ratings:', ratingsResponse.statusText);
        // Don't throw here, just skip user ratings
        userRatings = [];
      } else {
        const data = await ratingsResponse.json();
        userRatings = data.ratings as Rating[];
      }
    }

    return {
      roast,
      groupRating,
      userRatings,
      auth: {
        isLoggedIn: user_logged_in,
        userId: user_logged_in ? JSON.parse(cookies.get('roastnotes_user')!).id : undefined
      }
    };
  } catch (err) {
    if (err instanceof Error) {
      console.error('Error loading roast details:', err);
      throw error(500, {
        message: 'Our coffee machine hit a snag. How about we try that again?'
      });
    }
    throw err;
  }
};

export const actions: Actions = {
  submitRating: async ({ request, cookies }) => {
    const token = cookies.get('roastnotes_token');
    if (!token) {
      return fail(401, {
        message: 'Looks like your session needs a refresh. Mind logging in again?'
      });
    }

    const user_str = cookies.get('roastnotes_user');
    if (!user_str) {
      return fail(401, {
        message: 'We couldn\'t find your user info. A quick login should fix that.'
      });
    }

    const user: UserResponse = JSON.parse(user_str);
    const data = await request.formData();
    
    // Validate required fields
    const requiredFields = ['roast_id', 'brew_method', 'overall_score'];
    for (const field of requiredFields) {
      if (!data.get(field)) {
        return fail(400, {
          message: `Oops! We need your ${field.replace('_', ' ')} to save this rating.`
        });
      }
    }

    // Prepare rating data
    const ratingData = {
      roast_id: parseInt(data.get('roast_id') as string),
      user_id: user.id,
      group_id: data.get('group_id') ? parseInt(data.get('group_id') as string) : undefined,
      brew_method: data.get('brew_method'),
      preferred_method: data.get('preferred_method') === 'true',
      ratio: data.get('ratio'),
      temperature: data.get('temperature') ? parseFloat(data.get('temperature') as string) : undefined,
      grind: data.get('grind'),
      tasting_notes: data.get('tasting_notes'),
      overall_score: parseInt(data.get('overall_score') as string)
    };

    try {
      const response = await fetch('https://roastnotes.fly.dev/ratings', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(ratingData)
      });

      if (!response.ok) {
        if (response.status === 409) {
          return fail(409, {
            message: 'You\'ve already rated this roast. Would you like to update it instead?'
          });
        }
        
        const errorData = await response.json().catch(() => ({}));
        return fail(response.status, {
          message: errorData.message || 'Something went wrong while saving your rating. Care to try again?'
        });
      }

      return { success: true };
    } catch (err) {
      console.error('Error submitting rating:', err);
      return fail(500, {
        message: 'Our coffee machine hit a snag while saving your rating. How about another try?'
      });
    }
  }
};
