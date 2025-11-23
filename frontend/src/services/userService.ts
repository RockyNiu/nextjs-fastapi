import {
  MessageResponseAPI,
  RoleName,
  UserAPI,
  UserListResponseAPI,
  UserUpdateAPI,
} from '@/types/api';
import { apiService } from './apiRequest';

export interface RoleOption {
  id: number;
  name: RoleName;
  display_name: string;
}

export interface UserFilters {
  search?: string;
  role?: RoleName | null;
  isActive?: boolean | null;
}

class UserService {
  async getAllUsers(
    skip: number = 0,
    limit: number = 100,
    filters?: UserFilters
  ): Promise<UserListResponseAPI> {
    const params = new URLSearchParams();
    params.append('skip', skip.toString());
    params.append('limit', limit.toString());

    if (filters?.search) {
      params.append('search', filters.search);
    }
    if (filters?.role != null) {
      params.append('role_id', filters.role);
    }
    if (filters?.isActive != null) {
      params.append('is_active', filters.isActive.toString());
    }

    const response = await apiService.request<UserListResponseAPI>({
      endpoint: `/users/?${params.toString()}`,
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

  getRoleDisplayName(role: RoleName): string {
    switch (role) {
      case 'admin':
        return 'Admin';
      case 'moderator':
        return 'Moderator';
      case 'user':
        return 'User';
      default:
        return 'Unknown';
    }
  }

  getRoleBadgeColor(role: RoleName): string {
    switch (role) {
      case 'admin':
        return 'bg-red-100 text-red-800';
      case 'moderator':
        return 'bg-yellow-100 text-yellow-800';
      case 'user':
        return 'bg-green-100 text-green-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  }
}

export const userService = new UserService();
