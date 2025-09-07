'use client';

import Layout from '@/components/layout/Layout';
import Link from 'next/link';
import { authService } from '@/services/authService';
import { useRouter } from 'next/navigation';
import { useEffect, useState } from 'react';
import { UserAPI } from '@/types/api';

export default function Home() {
  const router = useRouter();
  const [user, setUser] = useState<UserAPI | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [verificationSent, setVerificationSent] = useState(false);

  useEffect(() => {
    checkAuthAndUser();
  }, [router]);

  const checkAuthAndUser = async () => {
    if (authService.isAuthenticated()) {
      try {
        const userData = await authService.getCurrentUser();
        setUser(userData);
        
        // If user is verified, redirect to dashboard
        if (userData.emailVerified) {
          router.push('/dashboard');
          return;
        }
      } catch (error) {
        console.error('Failed to get user data:', error);
        // If API fails, just treat as not authenticated
        setUser(null);
      }
    }
    setIsLoading(false);
  };

  const handleResendVerification = async () => {
    try {
      await authService.resendVerificationEmail();
      setVerificationSent(true);
    } catch (error) {
      console.error('Failed to resend verification:', error);
    }
  };

  // Show loading while checking auth status
  if (isLoading) {
    return (
      <Layout>
        <div className="flex justify-center items-center min-h-64">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
        </div>
      </Layout>
    );
  }

  // Show verification prompt for unverified users
  if (user && !user.emailVerified) {
    return (
      <Layout>
        <div className="max-w-2xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
          <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-6">
            <div className="flex">
              <div className="flex-shrink-0">
                <svg className="h-5 w-5 text-yellow-400" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
                </svg>
              </div>
              <div className="ml-3">
                <h3 className="text-sm font-medium text-yellow-800">
                  Email Verification Required
                </h3>
                <div className="mt-2 text-sm text-yellow-700">
                  <p>
                    Please verify your email address ({user.email}) to access the dashboard.
                    Check your inbox for a verification email.
                  </p>
                </div>
                <div className="mt-4">
                  <div className="-mx-2 -my-1.5 flex">
                    <button
                      type="button"
                      onClick={handleResendVerification}
                      className="bg-yellow-50 px-2 py-1.5 rounded-md text-sm font-medium text-yellow-800 hover:bg-yellow-100 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-yellow-50 focus:ring-yellow-600"
                    >
                      {verificationSent ? 'Verification Sent!' : 'Resend Verification Email'}
                    </button>
                    <Link
                      href="/dashboard"
                      className="ml-3 bg-yellow-50 px-2 py-1.5 rounded-md text-sm font-medium text-yellow-800 hover:bg-yellow-100 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-yellow-50 focus:ring-yellow-600"
                    >
                      Continue to Dashboard
                    </Link>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </Layout>
    );
  }

  // Show welcome page for unauthenticated users
  return (
    <Layout>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center py-20">
          <h1 className="text-4xl font-bold text-gray-900 sm:text-6xl">
            Welcome to NextJS FastAPI
          </h1>
          <p className="mt-6 text-xl text-gray-600 max-w-3xl mx-auto">
            A full-stack application with React/NextJS frontend and FastAPI
            backend, featuring user authentication, profile management, and
            more.
          </p>

          <div className="mt-10 flex justify-center gap-6">
            <Link
              href="/register"
              className="bg-blue-600 hover:bg-blue-700 text-white px-8 py-3 rounded-lg font-medium text-lg transition duration-200"
            >
              Get Started
            </Link>
            <Link
              href="/login"
              className="border border-gray-300 hover:border-gray-400 text-gray-700 px-8 py-3 rounded-lg font-medium text-lg transition duration-200"
            >
              Sign In
            </Link>
          </div>
        </div>

        <div className="mt-20">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="bg-white rounded-lg shadow-md p-6">
              <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mb-4">
                <svg
                  className="w-6 h-6 text-blue-600"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"
                  />
                </svg>
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">
                User Authentication
              </h3>
              <p className="text-gray-600">
                Secure user registration, login, password reset, and email
                verification features.
              </p>
            </div>

            <div className="bg-white rounded-lg shadow-md p-6">
              <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center mb-4">
                <svg
                  className="w-6 h-6 text-green-600"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
                  />
                </svg>
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">
                Modern Tech Stack
              </h3>
              <p className="text-gray-600">
                Built with NextJS 14, React 18, TypeScript, Tailwind CSS, and
                FastAPI.
              </p>
            </div>

            <div className="bg-white rounded-lg shadow-md p-6">
              <div className="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center mb-4">
                <svg
                  className="w-6 h-6 text-purple-600"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M13 10V3L4 14h7v7l9-11h-7z"
                  />
                </svg>
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">
                Fast & Scalable
              </h3>
              <p className="text-gray-600">
                Optimized for performance with server-side rendering and
                efficient API design.
              </p>
            </div>
          </div>
        </div>
      </div>
    </Layout>
  );
}
