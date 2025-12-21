'use client';

import { ReactNode } from 'react';
import { Toaster } from 'react-hot-toast';
import Header from './Header';

interface LayoutProps {
  children: ReactNode;
  onAuthChange?: (isAuthenticated: boolean) => void;
}

export default function Layout({ children, onAuthChange }: LayoutProps) {
  return (
    <div className="min-h-screen bg-gray-50">
      <Header onAuthChange={onAuthChange} />
      <main className="py-8">{children}</main>
      <Toaster
        position="top-right"
        toastOptions={{
          duration: 4000,
          style: {
            background: '#363636',
            color: '#fff',
          },
          success: {
            duration: 3000,
            iconTheme: {
              primary: '#4ade80',
              secondary: '#fff',
            },
          },
          error: {
            duration: 5000,
            iconTheme: {
              primary: '#ef4444',
              secondary: '#fff',
            },
          },
        }}
      />
    </div>
  );
}
