import { redirect } from '@sveltejs/kit';
import type { Cookies } from '@sveltejs/kit';
import type { UserResponse } from '$lib/types';

export async function validateSession(cookies: Cookies): Promise<UserResponse> {
  const token = cookies.get('roastnotes_token');
  if (!token) {
    throw redirect(303, '/auth/logout');
  }

  const user_str = cookies.get('roastnotes_user');
  if (!user_str) {
    throw redirect(303, '/auth/logout');
  }

  try {
    const user = JSON.parse(user_str);
    return user;
  } catch (e) {
    // If we can't parse the user data, clear cookies and redirect
    cookies.delete('roastnotes_token', { path: '/' });
    cookies.delete('roastnotes_user', { path: '/' });
    throw redirect(303, '/auth/logout');
  }
}
