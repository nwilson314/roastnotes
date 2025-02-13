export enum RoastLevel {
  unspecified = 'unspecified',
  light = 'light',
  medium = 'medium',
  dark = 'dark'
}

export interface BeanDetails {
  id: number;
  roast_id: number;
  species: string;
  cultivar?: string;
  processing_method?: string;
  altitude?: number;
  extra?: Record<string, any>;
}

export interface Roast {
  id: number;
  user_id: number;
  roaster_id: number;
  name: string;
  origin: string;
  single_origin: boolean;
  roast_level: RoastLevel;
  created_at: string;
  bean_details: BeanDetails;
  cached_rating_stats: {
    avg_rating: number;
    total_ratings: number;
    brew_methods: {
      [method: string]: {
        count: number;
        avg_rating: number;
      }
    };
    // other cached stats...
  }
}

export interface UserGroup {
  id: number;
  name: string;
  description?: string;
  member_count: number | null;
  roast_count: number | null;
}

export interface GroupRoast {
  id: number;
  name: string;
  origin: string;
  single_origin: boolean;
  roast_level: RoastLevel;
  roaster: Roaster;
  added_by_username: string;
  added_at: string;
  notes?: string;
  group_rating?: number;
  group_total_ratings?: number;
  global_rating?: number;
  global_total_ratings?: number;
}

export interface GroupRoastCollection {
  group_name: string;
  group_description?: string;
  roasts: GroupRoast[];
}

export interface UserGroupRoastsResponse {
  groups: Record<string, GroupRoastCollection>;
}

export interface Roaster {
  id: number;
  name: string;
  location?: string;
  website?: string;
  description?: string;
  social_media?: Record<string, string>;
}

export enum RoastsView {
  Trending = 'trending', 
  Groups = 'groups'
}

export interface Token {
  access_token: string;
  token_type: string;
}

export interface AuthResponse {
  token: Token;
  user: {
    id: number;
    username: string;
    email: string;
    created_at: string;
  };
}

export interface RoastDetails {
  // Base roast data
  id: number;
  name: string;
  origin: string;
  single_origin: boolean;
  roast_level: RoastLevel;
  bean_details: BeanDetails;
  created_at: string;
  
  // Rating stats - could be either global or group-specific
  rating_stats: {
    avg_rating: number;
    total_ratings: number;
    brew_methods: Record<string, { count: number; avg_rating: number }>;
  };
  
  // Optional group-specific data
  group_context?: {
    group_id: number;
    added_by_username: string;
    user_rating?: {
      rating: number;
      brew_method: string;
      notes?: string;
    };
  };
}

export interface UserResponse {
  id: number;
  username: string;
  email: string;
  created_at: string;
}
