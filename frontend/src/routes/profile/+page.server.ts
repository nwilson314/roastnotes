import type { PageServerLoad } from './$types';
import { validateSession } from '$lib/server/auth';

export const load: PageServerLoad = async ({ cookies }) => {
  const user = await validateSession(cookies);
  return { user };
};
