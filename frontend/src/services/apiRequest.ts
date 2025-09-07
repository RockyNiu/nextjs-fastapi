import { ApiError, ApiResponse } from '@/types/api';
import { toCamelCaseKeys, toSnakeCaseKeys } from '@/utils/caseConverter';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export interface IRequest {
  endpoint: string;
  method: 'GET' | 'POST' | 'PUT' | 'DELETE';
  data?: any;
  contentType?: string;
  requiresAuth?: boolean;
}

class ApiService {
  private baseURL: string;

  constructor() {
    this.baseURL = API_URL;
  }

  private getAuthToken(): string | null {
    if (typeof window !== 'undefined') {
      return localStorage.getItem('access_token');
    }
    return null;
  }

  private getHeaders(
    contentType = 'application/json',
    requiresAuth = false
  ): HeadersInit {
    const headers: HeadersInit = {};

    if (contentType) {
      headers['Content-Type'] = contentType;
    }

    if (requiresAuth) {
      const token = this.getAuthToken();
      if (token) {
        headers['Authorization'] = `Bearer ${token}`;
      }
    }

    return headers;
  }

  async request<T>({
    endpoint,
    method,
    data,
    contentType = 'application/json',
    requiresAuth = false,
  }: IRequest): Promise<ApiResponse<T>> {
    try {
      let headers = this.getHeaders(contentType, requiresAuth);
      let body: string | FormData | undefined;

      if (data instanceof FormData) {
        headers = this.getHeaders('', requiresAuth);
        body = data;
      } else if (data) {
        const snakeCaseData = toSnakeCaseKeys(data);
        body = JSON.stringify(snakeCaseData);
      }

      console.log(`🔄 API Request: ${method} ${this.baseURL}${endpoint}`, {
        headers,
        body: data
          ? data instanceof FormData
            ? '[FormData]'
            : data
          : undefined,
      });

      const response = await fetch(`${this.baseURL}${endpoint}`, {
        method,
        headers,
        body,
      });

      console.log(`📡 API Response: ${response.status} ${response.statusText}`);

      let responseData;
      try {
        responseData = await response.json();
      } catch (error) {
        console.error('Failed to parse JSON response:', error);
        const apiError: ApiError = {
          error: 'Invalid response format',
          detail: `HTTP ${response.status}: ${response.statusText}`,
          status: response.status,
        };
        throw apiError;
      }

      if (!response.ok) {
        const apiError: ApiError = {
          error:
            responseData.error ||
            responseData.message ||
            `HTTP ${response.status}`,
          detail:
            responseData.detail || responseData.message || response.statusText,
          status: response.status,
        };
        throw apiError;
      }

      const camelCaseData = toCamelCaseKeys(responseData);

      return {
        data: camelCaseData,
        status: response.status,
      };
    } catch (error) {
      if ((error as ApiError).status) {
        throw error;
      }

      const apiError: ApiError = {
        error: 'Network error',
        detail: error instanceof Error ? error.message : 'Unknown error',
        status: 0,
      };
      throw apiError;
    }
  }
}

const apiService = new ApiService();

export { apiService };
