'use client';

import UserManagement from '@/components/admin/UserManagement';
import Layout from '@/components/layout/Layout';
import { authService } from '@/services/authService';
import { UserAPI, UserRole } from '@/types/api';
import { useRouter } from 'next/navigation';
import { useEffect, useState } from 'react';

export default function AdminUsersPage() {
  const router = useRouter();
  const [currentUser, setCurrentUser] = useState<UserAPI | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const checkAuth = async () => {
      if (!authService.isAuthenticated()) {
        router.push('/login');
        return;
      }

      try {
        const user = await authService.getCurrentUser();
        setCurrentUser(user);

        // Check if user has admin or moderator role
        if (
          user.roleId !== UserRole.ADMIN &&
          user.roleId !== UserRole.MODERATOR
        ) {
          router.push('/dashboard');
          return;
        }
      } catch (error) {
        console.error('Failed to get current user:', error);
        router.push('/login');
      } finally {
        setLoading(false);
      }
    };

    checkAuth();
  }, [router]);

  if (loading) {
    return (
      <Layout>
        <div className="flex items-center justify-center min-h-64">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
        </div>
      </Layout>
    );
  }

  if (!currentUser) {
    return null;
  }

  return (
    <Layout>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 bg-white text-black">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">User Management</h1>
          <p className="mt-2 text-gray-600">
            Manage user accounts, roles, and permissions
          </p>
        </div>
        <UserManagement currentUser={currentUser} />
      </div>
    </Layout>
  );
}
