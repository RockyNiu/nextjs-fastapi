'use client';

import { authService } from '@/services/authService';
import { UserLoginAPI } from '@/types/api';
import Link from 'next/link';
import { useState } from 'react';

interface LoginFormProps {
  onSuccess?: (user: any) => void;
  onError?: (error: string) => void;
}

export default function LoginForm({ onSuccess, onError }: LoginFormProps) {
  const [formData, setFormData] = useState<UserLoginAPI>({
    email: '',
    password: '',
  });
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string>('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');

    try {
      const tokenResponse = await authService.login(formData);
      const user = await authService.getCurrentUser();

      if (onSuccess) {
        onSuccess(user);
      }
    } catch (err: any) {
      const errorMessage = err.detail || err.error || 'Login failed';
      setError(errorMessage);
      if (onError) {
        onError(errorMessage);
      }
    } finally {
      setIsLoading(false);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData((prev) => ({
      ...prev,
      [e.target.name]: e.target.value,
    }));
  };

  return (
    <div className="max-w-md mx-auto bg-white rounded-lg shadow-md p-6">
      <h2 className="text-2xl font-bold text-gray-900 mb-6 text-center">
        Sign In
      </h2>

      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label
            htmlFor="email"
            className="block text-sm font-medium text-gray-700 mb-1"
          >
            Email
          </label>
          <input
            type="email"
            id="email"
            name="email"
            value={formData.email}
            onChange={handleChange}
            required
            className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent text-gray-900 bg-white placeholder-gray-500"
            placeholder="Enter your email"
          />
        </div>

        <div>
          <label
            htmlFor="password"
            className="block text-sm font-medium text-gray-700 mb-1"
          >
            Password
          </label>
          <input
            type="password"
            id="password"
            name="password"
            value={formData.password}
            onChange={handleChange}
            required
            className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent text-gray-900 bg-white placeholder-gray-500"
            placeholder="Enter your password"
          />
        </div>

        {error && (
          <div className="bg-red-50 border border-red-200 rounded-md p-3">
            <p className="text-red-600 text-sm">{error}</p>
          </div>
        )}

        <button
          type="submit"
          disabled={isLoading}
          className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-blue-300 text-white font-medium py-2 px-4 rounded-md transition duration-200"
        >
          {isLoading ? 'Signing In...' : 'Sign In'}
        </button>
      </form>

      <div className="mt-4 text-center space-y-2">
        <Link
          href="/forgot-password"
          className="text-sm text-blue-600 hover:text-blue-800 transition duration-200 block"
        >
          Forgot your password?
        </Link>
        <p className="text-sm text-gray-600">
          Don&apos;t have an account?{' '}
          <Link
            href="/register"
            className="text-blue-600 hover:text-blue-800 transition duration-200"
          >
            Sign up
          </Link>
        </p>
      </div>
    </div>
  );
}
