

'use client';

import Layout from '@/components/layout/Layout';
import { authService } from '@/services/authService';
import Link from 'next/link';
import { useRouter, useSearchParams } from 'next/navigation';
import { useEffect, useState, useRef } from 'react';

export default function VerifyEmailPage() {
  const searchParams = useSearchParams();
  const [status, setStatus] = useState<'loading' | 'success' | 'error'>('loading');
  const [message, setMessage] = useState('');
  const hasVerifiedRef = useRef(false);

  useEffect(() => {
    const verifyEmail = async () => {
      if (hasVerifiedRef.current) return; // Prevent multiple calls
      hasVerifiedRef.current = true;
      
      const token = searchParams.get('token');
      
      if (!token) {
        setStatus('error');
        setMessage('Verification token is missing');
        return;
      }

      console.log('🔄 Starting email verification with token:', token.substring(0, 10) + '...');

      try {
        const result = await authService.verifyEmail(token);
        console.log('✅ Email verification successful:', result);
        setStatus('success');
        setMessage(result.message || 'Email verified successfully!');
      } catch (error: any) {
        console.log('❌ Email verification failed:', error);
        setStatus('error');
        // Handle different error response formats
        let errorMessage = 'Email verification failed';
        if (error.detail) {
          errorMessage = error.detail;
        } else if (error.message) {
          errorMessage = error.message;
        } else if (error.error) {
          errorMessage = error.error;
        }
        setMessage(errorMessage);
        console.error('Email verification error:', error);
      }
    };

    verifyEmail();
  }, [searchParams]);

  return (
    <Layout>
      <div className="max-w-md mx-auto mt-20 px-4">
        <div className="bg-white rounded-lg shadow-md p-8 text-center">
          {status === 'loading' && (
            <>
              <div className="flex justify-center mb-4">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
              </div>
              <h1 className="text-2xl font-bold text-gray-900 mb-2">
                Verifying Email
              </h1>
              <p className="text-gray-600">
                Please wait while we verify your email address...
              </p>
            </>
          )}

          {status === 'success' && (
            <>
              <div className="flex justify-center mb-4">
                <div className="rounded-full bg-green-100 p-3">
                  <svg
                    className="w-8 h-8 text-green-600"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M5 13l4 4L19 7"
                    />
                  </svg>
                </div>
              </div>
              <h1 className="text-2xl font-bold text-gray-900 mb-2">
                Email Verified!
              </h1>
              <p className="text-gray-600 mb-4">{message}</p>
              <div className="mt-6 space-y-3">
                <Link
                  href="/dashboard"
                  className="block w-full bg-blue-600 hover:bg-blue-700 text-white py-2 px-4 rounded-md text-sm font-medium transition duration-200"
                >
                  Go to Dashboard
                </Link>
                <Link
                  href="/login"
                  className="block w-full border border-gray-300 hover:border-gray-400 text-gray-700 py-2 px-4 rounded-md text-sm font-medium transition duration-200"
                >
                  Sign In
                </Link>
              </div>
            </>
          )}

          {status === 'error' && (
            <>
              <div className="flex justify-center mb-4">
                <div className="rounded-full bg-red-100 p-3">
                  <svg
                    className="w-8 h-8 text-red-600"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M6 18L18 6M6 6l12 12"
                    />
                  </svg>
                </div>
              </div>
              <h1 className="text-2xl font-bold text-gray-900 mb-2">
                Verification Failed
              </h1>
              <p className="text-gray-600 mb-6">{message}</p>
              <div className="space-y-3">
                <Link
                  href="/dashboard"
                  className="block w-full bg-blue-600 hover:bg-blue-700 text-white py-2 px-4 rounded-md text-sm font-medium transition duration-200"
                >
                  Try Again from Dashboard
                </Link>
                <Link
                  href="/login"
                  className="block w-full border border-gray-300 hover:border-gray-400 text-gray-700 py-2 px-4 rounded-md text-sm font-medium transition duration-200"
                >
                  Sign In
                </Link>
              </div>
            </>
          )}
        </div>
      </div>
    </Layout>
  );
}