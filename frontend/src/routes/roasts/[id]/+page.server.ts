import { error, fail } from '@sveltejs/kit';
import type { PageServerLoad, Actions } from './$types';
import { createApiClient } from '$lib/server/api';
import type { Roast, Rating, Roaster } from '$lib/types';

export const load: PageServerLoad = async ({ params, cookies }) => {
  console.log("Loading roast details for id:", params.id);
  const api = await createApiClient(cookies);
  
  try {
    const roast = await api.get<Roast>(`/roasts/${params.id}`);
    console.log("Got roast:", roast);
    const [roaster, ratings] = await Promise.all([
      api.get<Roaster>(`/roasters/${roast.roaster_id}`),
      api.get<Rating[]>(`/ratings/roast/${params.id}`)
    ]);
    console.log("Got roaster:", roaster);
    console.log("Got ratings:", ratings);
    
    return {
      roast,
      roaster,
      ratings
    };
  } catch (err: any) {
    console.error("Error loading roast details:", err);
    throw error(err.status || 500, err.message || 'Failed to load roast details');
  }
};

export const actions: Actions = {
  submitRating: async ({ request, cookies }) => {
    try {
      const data = await request.formData();
      const roastId = data.get('roast_id');
      const rating = data.get('rating');
      const brewMethod = data.get('brew_method');
      const notes = data.get('notes');
      const preferredMethod = data.get('preferred_method') === 'on';

      if (!roastId || !rating || !brewMethod) {
        return fail(400, { 
          type: 'error', 
          error: { message: 'Missing required fields' }
        });
      }

      const api = await createApiClient(cookies);
      
      try {
        await api.post(`/roasts/${roastId}/ratings`, {
          overall_score: Number(rating),
          brew_method: brewMethod,
          tasting_notes: notes || undefined,
          preferred_method: preferredMethod
        });

        return {
          type: 'success'
        };
      } catch (err: any) {
        return fail(err.status || 500, {
          type: 'error',
          error: { message: err.message || 'Failed to submit rating' }
        });
      }
    } catch (error) {
      console.error('Error submitting rating:', error);
      return fail(500, { 
        type: 'error', 
        error: { message: 'Failed to submit rating. Please try again.' }
      });
    }
  }
};
