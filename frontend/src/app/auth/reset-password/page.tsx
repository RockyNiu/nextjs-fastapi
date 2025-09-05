'use client';

import ResetPasswordForm from '@/components/auth/ResetPasswordForm';
import Layout from '@/components/layout/Layout';
import { useRouter, useSearchParams } from 'next/navigation';
import { Suspense } from 'react';

function ResetPasswordContent() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const token = searchParams.get('token');

  if (!token) {
    return (
      <Layout>
        <div className="max-w-md mx-auto text-center">
          <div className="bg-red-50 border border-red-200 rounded-md p-6">
            <h2 className="text-xl font-semibold text-red-800 mb-2">
              Invalid Reset Link
            </h2>
            <p className="text-red-600 mb-4">
              The password reset link is invalid or has expired.
            </p>
            <button
              onClick={() => router.push('/forgot-password')}
              className="bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded-md transition duration-200"
            >
              Request New Reset Link
            </button>
          </div>
        </div>
      </Layout>
    );
  }

  const handleSuccess = () => {
    router.push(
      '/login?message=Password%20reset%20successful!%20Please%20log%20in%20with%20your%20new%20password.'
    );
  };

  const handleError = (error: string) => {
    console.error('Reset password error:', error);
  };

  return (
    <Layout>
      <div className="max-w-md mx-auto">
        <ResetPasswordForm
          token={token}
          onSuccess={handleSuccess}
          onError={handleError}
        />
      </div>
    </Layout>
  );
}

export default function ResetPasswordPage() {
  return (
    <Suspense
      fallback={
        <Layout>
          <div className="max-w-md mx-auto text-center">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto"></div>
            <p className="mt-2 text-gray-600">Loading...</p>
          </div>
        </Layout>
      }
    >
      <ResetPasswordContent />
    </Suspense>
  );
}
