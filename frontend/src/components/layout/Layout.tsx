'use client';

import { ReactNode } from 'react';
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
    </div>
  );
}
