'use client';

import { useRouter } from 'next/navigation';
import { useEffect } from 'react';
import Layout from '@/components/layout/Layout';
import UserProfile from '@/components/dashboard/UserProfile';
import { authService } from '@/services/authService';

export default function DashboardPage() {
  const router = useRouter();

  useEffect(() => {
    if (!authService.isAuthenticated()) {
      router.push('/login');
    }
  }, [router]);

  const handleLogout = () => {
    router.push('/');
  };

  return (
    <Layout>
      <UserProfile onLogout={handleLogout} />
    </Layout>
  );
}