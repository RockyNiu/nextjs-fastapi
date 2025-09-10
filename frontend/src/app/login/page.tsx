'use client';

import LoginForm from '@/components/auth/LoginForm';
import Layout from '@/components/layout/Layout';
import { useRouter } from 'next/navigation';

export default function LoginPage() {
  const router = useRouter();

  const handleSuccess = () => {
    router.push('/dashboard');
  };

  return (
    <Layout>
      <div className="max-w-md mx-auto">
        <LoginForm
          onSuccess={handleSuccess}
          onError={(error) => console.error('Login error:', error)}
        />
      </div>
    </Layout>
  );
}
