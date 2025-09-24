import {
  MessageResponseAPI,
  UserAPI,
  UserListResponseAPI,
  UserRole,
  UserUpdateAPI,
} from '@/types/api';
import { apiService } from './apiRequest';

export interface RoleOption {
  id: UserRole;
  name: string;
  display_name: string;
}

class UserService {
  async getAllUsers(
    skip: number = 0,
    limit: number = 100
  ): Promise<UserListResponseAPI> {
    const response = await apiService.request<UserListResponseAPI>({
      endpoint: `/users/?skip=${skip}&limit=${limit}`,
      method: 'GET',
      requiresAuth: true,
    });
    return response.data;
  }

  async getUserById(userId: number): Promise<UserAPI> {
    const response = await apiService.request<UserAPI>({
      endpoint: `/users/${userId}`,
      method: 'GET',
      requiresAuth: true,
    });
    return response.data;
  }

  async updateUser(userId: number, userData: UserUpdateAPI): Promise<UserAPI> {
    const response = await apiService.request<UserAPI>({
      endpoint: `/users/${userId}`,
      method: 'PUT',
      data: userData,
      requiresAuth: true,
    });
    return response.data;
  }

  async deactivateUser(userId: number): Promise<MessageResponseAPI> {
    const response = await apiService.request<MessageResponseAPI>({
      endpoint: `/users/${userId}/deactivate`,
      method: 'POST',
      requiresAuth: true,
    });
    return response.data;
  }

  async activateUser(userId: number): Promise<MessageResponseAPI> {
    const response = await apiService.request<MessageResponseAPI>({
      endpoint: `/users/${userId}/activate`,
      method: 'POST',
      requiresAuth: true,
    });
    return response.data;
  }

  async getRoles(): Promise<RoleOption[]> {
    const response = await apiService.request<RoleOption[]>({
      endpoint: '/users/roles/',
      method: 'GET',
      requiresAuth: true,
    });
    return response.data;
  }

  getRoleDisplayName(roleId: UserRole): string {
    switch (roleId) {
      case UserRole.ADMIN:
        return 'Admin';
      case UserRole.MODERATOR:
        return 'Moderator';
      case UserRole.USER:
        return 'User';
      default:
        return 'Unknown';
    }
  }

  getRoleBadgeColor(roleId: UserRole): string {
    switch (roleId) {
      case UserRole.ADMIN:
        return 'bg-red-100 text-red-800';
      case UserRole.MODERATOR:
        return 'bg-yellow-100 text-yellow-800';
      case UserRole.USER:
        return 'bg-green-100 text-green-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  }
}

export const userService = new UserService();
