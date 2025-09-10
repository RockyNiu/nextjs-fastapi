'use client';

import ForgotPasswordForm from '@/components/auth/ForgotPasswordForm';
import Layout from '@/components/layout/Layout';

export default function ForgotPasswordPage() {
  return (
    <Layout>
      <div className="max-w-md mx-auto">
        <ForgotPasswordForm
          onSuccess={(message) => console.log('Success:', message)}
          onError={(error) => console.error('Error:', error)}
        />
      </div>
    </Layout>
  );
}
