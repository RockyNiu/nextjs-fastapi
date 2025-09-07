import {
  EmailVerificationResponseAPI,
  ForgotPasswordAPI,
  MessageResponseAPI,
  PasswordResetAPI,
  TokenResponseAPI,
  UserAPI,
  UserCreateAPI,
  UserLoginAPI,
} from '@/types/api';
import { apiService } from './apiRequest';

class AuthService {
  async register(userData: UserCreateAPI): Promise<UserAPI> {
    const response = await apiService.request<UserAPI>({
      endpoint: '/auth/register',
      method: 'POST',
      data: userData,
    });
    return response.data;
  }

  async login(credentials: UserLoginAPI): Promise<TokenResponseAPI> {
    const response = await apiService.request<TokenResponseAPI>({
      endpoint: '/auth/login',
      method: 'POST',
      data: credentials,
    });

    // Store token in localStorage
    if (typeof window !== 'undefined') {
      localStorage.setItem('access_token', response.data.accessToken);
      localStorage.setItem('token_type', response.data.tokenType);
      localStorage.setItem('expires_in', response.data.expiresIn.toString());
    }

    return response.data;
  }

  async logout(): Promise<MessageResponseAPI> {
    try {
      const response = await apiService.request<MessageResponseAPI>({
        endpoint: '/auth/logout',
        method: 'POST',
        requiresAuth: true,
      });

      // Clear token from localStorage
      this.clearTokens();

      return response.data;
    } catch (error) {
      // Clear tokens even if API call fails
      this.clearTokens();
      throw error;
    }
  }

  async getCurrentUser(): Promise<UserAPI> {
    const response = await apiService.request<UserAPI>({
      endpoint: '/auth/me',
      method: 'GET',
      requiresAuth: true,
    });
    return response.data;
  }

  async forgotPassword(email: ForgotPasswordAPI): Promise<MessageResponseAPI> {
    const response = await apiService.request<MessageResponseAPI>({
      endpoint: '/auth/forgot-password',
      method: 'POST',
      data: email,
    });
    return response.data;
  }

  async resetPassword(
    resetData: PasswordResetAPI
  ): Promise<MessageResponseAPI> {
    const response = await apiService.request<MessageResponseAPI>({
      endpoint: '/auth/reset-password',
      method: 'POST',
      data: resetData,
    });
    return response.data;
  }

  async verifyEmail(token: string): Promise<EmailVerificationResponseAPI> {
    const response = await apiService.request<EmailVerificationResponseAPI>({
      endpoint: `/auth/verify-email?token=${encodeURIComponent(token)}`,
      method: 'GET',
    });
    return response.data;
  }

  async resendVerificationEmail(): Promise<MessageResponseAPI> {
    const response = await apiService.request<MessageResponseAPI>({
      endpoint: '/auth/resend-verification',
      method: 'POST',
      requiresAuth: true,
    });
    return response.data;
  }

  isAuthenticated(): boolean {
    if (typeof window === 'undefined') return false;
    const token = localStorage.getItem('access_token');
    return !!token;
  }

  getToken(): string | null {
    if (typeof window === 'undefined') return null;
    return localStorage.getItem('access_token');
  }

  private clearTokens(): void {
    if (typeof window !== 'undefined') {
      localStorage.removeItem('access_token');
      localStorage.removeItem('token_type');
      localStorage.removeItem('expires_in');
    }
  }
}

export const authService = new AuthService();
