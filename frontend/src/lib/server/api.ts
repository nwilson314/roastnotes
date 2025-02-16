import { redirect } from '@sveltejs/kit';
import type { Cookies } from '@sveltejs/kit';
import { validateSession } from './auth';

// API Error class for consistent error handling
export class ApiError extends Error {
  constructor(
    message: string,
    public status: number,
    public data?: any
  ) {
    super(message);
    this.name = 'ApiError';
  }
}

export class ApiClient {
  // private baseUrl = 'http://localhost:8000';
  private baseUrl = 'https://roastnotes.fly.dev';
  private token: string;

  constructor(token: string) {
    this.token = token;
  }

  private async fetch<T>(
    path: string,
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${this.baseUrl}${path}`;
    const headers = {
      'Authorization': `Bearer ${this.token}`,
      'Content-Type': 'application/json',
      ...options.headers,
    };

    const response = await fetch(url, {
      ...options,
      headers,
    });

    // Handle common error cases
    if (response.status === 401) {
      throw redirect(303, '/auth/logout');
    }

    if (!response.ok) {
      let errorData;
      try {
        errorData = await response.json();
      } catch {
        errorData = null;
      }
      
      throw new ApiError(
        errorData?.message || 'An error occurred',
        response.status,
        errorData
      );
    }

    // Handle empty responses
    if (response.status === 204) {
      return null as T;
    }

    return response.json();
  }

  async get<T>(path: string): Promise<T> {
    return this.fetch<T>(path, { method: 'GET' });
  }

  async post<T>(path: string, data?: any): Promise<T> {
    return this.fetch<T>(path, {
      method: 'POST',
      body: data ? JSON.stringify(data) : undefined,
    });
  }

  async put<T>(path: string, data: any): Promise<T> {
    return this.fetch<T>(path, {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  }

  async delete<T>(path: string): Promise<T> {
    return this.fetch<T>(path, { method: 'DELETE' });
  }
}

// Helper to create an API client from cookies
export async function createApiClient(cookies: Cookies): Promise<ApiClient> {
  const token = cookies.get('roastnotes_token');
  if (!token) {
    throw redirect(303, '/auth/logout');
  }
  return new ApiClient(token);
}
