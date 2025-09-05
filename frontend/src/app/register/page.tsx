'use client';

import { useRouter } from 'next/navigation';
import Layout from '@/components/layout/Layout';
import RegisterForm from '@/components/auth/RegisterForm';

export default function RegisterPage() {
  const router = useRouter();

  const handleSuccess = () => {
    router.push('/login?message=Registration successful! Please log in.');
  };

  return (
    <Layout>
      <div className="max-w-md mx-auto">
        <RegisterForm 
          onSuccess={handleSuccess}
          onError={(error) => console.error('Registration error:', error)}
        />
      </div>
    </Layout>
  );
}