import { redirect } from '@sveltejs/kit';
import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async ({ cookies }) => {
    const token = cookies.get('roastnotes_token');
    if (token) {
        console.log("Redirecting from home to roasts")
        throw redirect(303, '/roasts');
    }
    return {};
};
