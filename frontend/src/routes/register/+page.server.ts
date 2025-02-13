import { fail, redirect } from '@sveltejs/kit';
import type { Actions } from './$types';
import type { AuthResponse } from '$lib/types';

export const actions: Actions = {
  default: async ({ request, cookies }) => {
    const data = await request.formData();
    const username = data.get('username');
    const email = data.get('email');
    const password = data.get('password');

    const res = await fetch('https://roastnotes.fly.dev/users/register', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        username,
        email,
        password
      })
    });

    if (!res.ok) {
      return fail(400, { invalid: true });
    }

    const auth_response: AuthResponse = await res.json();
    
    // Store both token and user info
    cookies.set('roastnotes_token', auth_response.token.access_token, { path: '/' });
    cookies.set('roastnotes_user', JSON.stringify(auth_response.user), { path: '/' });

    throw redirect(303, '/roasts');
  }
} satisfies Actions;