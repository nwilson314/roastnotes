import { redirect } from '@sveltejs/kit';
import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async ({ cookies }) => {
  const token = cookies.get('roastnotes_token');
  if (!token) {
    throw redirect(303, '/auth/logout');
  }

  const user_str = cookies.get('roastnotes_user');
  if (!user_str) {
    throw redirect(303, '/auth/logout');
  }

  const user = JSON.parse(user_str);

  return {
    user
  };
};
