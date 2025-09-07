'use client';

import { authService } from '@/services/authService';
import { UserAPI } from '@/types/api';
import { useEffect, useState } from 'react';

interface UserProfileProps {
  onLogout?: () => void;
}

export default function UserProfile({ onLogout }: UserProfileProps) {
  const [user, setUser] = useState<UserAPI | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string>('');
  const [verificationSent, setVerificationSent] = useState(false);
  const [verificationLoading, setVerificationLoading] = useState(false);

  useEffect(() => {
    loadUser();
  }, []);

  const loadUser = async () => {
    try {
      const userData = await authService.getCurrentUser();
      setUser(userData);
    } catch (err: any) {
      setError(err.detail || err.error || 'Failed to load user data');
    } finally {
      setIsLoading(false);
    }
  };

  const handleLogout = async () => {
    try {
      await authService.logout();
      if (onLogout) {
        onLogout();
      }
    } catch (err) {
      console.error('Logout failed:', err);
    }
  };

  const handleResendVerification = async () => {
    setVerificationLoading(true);
    setError(''); // Clear any previous errors
    try {
      await authService.resendVerificationEmail();
      setVerificationSent(true);
      // Reset the success message after 5 seconds
      setTimeout(() => setVerificationSent(false), 5000);
    } catch (err: any) {
      console.error('Failed to resend verification:', err);
      const errorMessage =
        err.detail ||
        err.error ||
        err.message ||
        'Failed to resend verification email. Please try again.';
      setError(`Verification Error: ${errorMessage}`);
    } finally {
      setVerificationLoading(false);
    }
  };

  if (isLoading) {
    return (
      <div className="max-w-2xl mx-auto p-6">
        <div className="bg-white rounded-lg shadow-md p-6">
          <div className="animate-pulse">
            <div className="h-8 bg-gray-200 rounded mb-4"></div>
            <div className="h-4 bg-gray-200 rounded mb-2"></div>
            <div className="h-4 bg-gray-200 rounded mb-2"></div>
            <div className="h-4 bg-gray-200 rounded"></div>
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="max-w-2xl mx-auto p-6">
        <div className="bg-red-50 border border-red-200 rounded-md p-4">
          <p className="text-red-600">{error}</p>
          <button
            onClick={loadUser}
            className="mt-2 bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-md text-sm"
          >
            Try Again
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-2xl mx-auto p-6">
      <div className="bg-white rounded-lg shadow-md p-6">
        <div className="mb-6">
          <h1 className="text-2xl font-bold text-gray-900">User Profile</h1>
        </div>

        {user && (
          <div className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  First Name
                </label>
                <div className="px-3 py-2 bg-gray-50 border border-gray-300 rounded-md text-gray-900">
                  {user.firstName}
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Last Name
                </label>
                <div className="px-3 py-2 bg-gray-50 border border-gray-300 rounded-md text-gray-900">
                  {user.lastName}
                </div>
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Email Address
              </label>
              <div className="px-3 py-2 bg-gray-50 border border-gray-300 rounded-md text-gray-900">
                <div className="flex items-center justify-between">
                  <div>
                    {user.email}
                    {!user.emailVerified && (
                      <span className="ml-2 inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-yellow-100 text-yellow-800">
                        Not Verified
                      </span>
                    )}
                    {user.emailVerified && (
                      <span className="ml-2 inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                        Verified
                      </span>
                    )}
                  </div>
                  {!user.emailVerified && (
                    <button
                      onClick={handleResendVerification}
                      disabled={verificationLoading}
                      className="ml-3 bg-yellow-600 hover:bg-yellow-700 disabled:bg-yellow-400 text-white px-3 py-1 rounded text-xs font-medium transition duration-200 flex items-center"
                    >
                      {verificationLoading ? (
                        <>
                          <svg
                            className="animate-spin -ml-1 mr-2 h-3 w-3 text-white"
                            xmlns="http://www.w3.org/2000/svg"
                            fill="none"
                            viewBox="0 0 24 24"
                          >
                            <circle
                              className="opacity-25"
                              cx="12"
                              cy="12"
                              r="10"
                              stroke="currentColor"
                              strokeWidth="4"
                            ></circle>
                            <path
                              className="opacity-75"
                              fill="currentColor"
                              d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                            ></path>
                          </svg>
                          Sending...
                        </>
                      ) : verificationSent ? (
                        'Sent!'
                      ) : (
                        'Resend Verification'
                      )}
                    </button>
                  )}
                </div>
              </div>
              {!user.emailVerified && verificationSent && (
                <p className="mt-1 text-sm text-green-600">
                  Verification email sent! Check your inbox.
                </p>
              )}
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Account Status
              </label>
              <div className="px-3 py-2 bg-gray-50 border border-gray-300 rounded-md">
                <span
                  className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                    user.isActive
                      ? 'bg-green-100 text-green-800'
                      : 'bg-red-100 text-red-800'
                  }`}
                >
                  {user.isActive ? 'Active' : 'Inactive'}
                </span>
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Member Since
              </label>
              <div className="px-3 py-2 bg-gray-50 border border-gray-300 rounded-md text-gray-900">
                {new Date(user.dateCreated).toLocaleDateString('en-US', {
                  year: 'numeric',
                  month: 'long',
                  day: 'numeric',
                })}
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Last Updated
              </label>
              <div className="px-3 py-2 bg-gray-50 border border-gray-300 rounded-md text-gray-900">
                {new Date(user.dateUpdated).toLocaleDateString('en-US', {
                  year: 'numeric',
                  month: 'long',
                  day: 'numeric',
                  hour: '2-digit',
                  minute: '2-digit',
                })}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
