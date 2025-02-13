import type { LayoutServerLoad } from './$types';
import type { UserResponse } from '$lib/types';

export const load: LayoutServerLoad = async ({ cookies }) => {
  const token = cookies.get('roastnotes_token');
  const user_logged_in = !!token;
  
  let user: UserResponse | null = null;
  if (user_logged_in) {
    const user_str = cookies.get('roastnotes_user');
    if (user_str) {
      user = JSON.parse(user_str);
    }
  }

  return {
    user_logged_in,
    user
  };
};
