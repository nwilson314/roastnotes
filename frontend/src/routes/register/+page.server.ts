import { fail, redirect } from '@sveltejs/kit';
import type { Actions } from './$types';
import type { AuthResponse } from '$lib/types';
import { ApiClient, ApiError } from '$lib/server/api';
import { auth } from '$lib/stores/auth';

export const actions: Actions = {
  default: async ({ request, cookies }) => {
    const data = await request.formData();
    const username = data.get('username');
    const email = data.get('email');
    const password = data.get('password');

    try {
      // For registration, we use an empty token since we're not authenticated yet
      const api = new ApiClient('');
      
      const auth_response: AuthResponse = await api.post('/users/register', {
        username,
        email,
        password
      });
      
      // Store both token and user info in cookies
      cookies.set('roastnotes_token', auth_response.token.access_token, { path: '/' });
      cookies.set('roastnotes_user', JSON.stringify(auth_response.user), { path: '/' });

      // Initialize auth store with full response
      auth.initWithAuth(auth_response);

      throw redirect(303, '/roasts');
      
    } catch (error) {
      if (error instanceof ApiError) {
        return fail(error.status, {
          invalid: true,
          message: error.message
        });
      }
      // Handle unexpected errors
      return fail(500, {
        invalid: true,
        message: 'An unexpected error occurred during registration'
      });
    }
  }
} satisfies Actions;