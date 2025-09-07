'use client';

import UserProfile from '@/components/dashboard/UserProfile';
import Layout from '@/components/layout/Layout';
import { authService } from '@/services/authService';
import { useRouter } from 'next/navigation';
import { useEffect, useState } from 'react';

export default function DashboardPage() {
  const router = useRouter();
  const [key, setKey] = useState(0);

  useEffect(() => {
    if (!authService.isAuthenticated()) {
      router.push('/login');
    }
  }, [router]);

  const handleLogout = () => {
    setKey((prev) => prev + 1);
    router.push('/');
  };

  return (
    <Layout>
      <UserProfile key={key} onLogout={handleLogout} />
    </Layout>
  );
}
