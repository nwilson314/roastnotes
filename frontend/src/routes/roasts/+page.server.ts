import type { PageServerLoad } from './$types';

interface Roast {
  title: string;
  roast_type: string;
  origin: string;
  overall_score: number;
  group: string;
  brew_methods: {
    name: string;
    score: number;
  }[];
  tasting_notes: string[];
}

interface Group {
  name: string;
  members: number;
  new_roasts: number;
  latest_activity: string;
}

export const load: PageServerLoad = async ({ cookies }) => {
  const token = cookies.get('token');
  
  // In a real app, we'd fetch this data from the API
  // For now, return empty arrays until we implement the API
  return {
    user: token ? { email: 'user@example.com' } : null,
    trendingRoasts: [] as Roast[],
    groupRoasts: [] as Roast[],
    userGroups: [] as Group[]
  };
};
