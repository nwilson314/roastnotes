import { redirect } from '@sveltejs/kit';
import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async ({ cookies }) => {
    const token = cookies.get('token_roastnotes_user');
    if (token) {
        throw redirect(303, '/roasts');
    }
    return {};
};
