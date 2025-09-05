'use client';

import UserProfile from '@/components/dashboard/UserProfile';
import Layout from '@/components/layout/Layout';
import { authService } from '@/services/authService';
import { useRouter } from 'next/navigation';
import { useEffect } from 'react';

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
