import { fail, redirect } from '@sveltejs/kit';
import type { Actions } from './$types';
import type { AuthResponse } from '$lib/types';
import { ApiClient, ApiError } from '$lib/server/api';

export const actions: Actions = {
  default: async ({ request, cookies }) => {
    const data = await request.formData();
    const username = data.get('username');
    const email = data.get('email');
    const password = data.get('password');

    try {
      const api = new ApiClient('');
      
      const auth_response: AuthResponse = await api.post('/users/register', {
        username,
        email,
        password
      });
      
      cookies.set('roastnotes_token', auth_response.token.access_token, { path: '/' });
      cookies.set('roastnotes_user', JSON.stringify(auth_response.user), { path: '/' });

      console.log("Registered user: ", auth_response.user);

      throw redirect(303, '/roasts');
      
    } catch (error) {
      if (error instanceof ApiError) {
        return fail(error.status, {
          invalid: true,
          message: error.message
        });
      } else {
        throw error
      }
    }
  }
};