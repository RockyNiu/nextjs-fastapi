'use client';

import { RoleOption, userService } from '@/services/userService';
import { RoleName, UserAPI, UserUpdateAPI } from '@/types/api';
import { useEffect, useState } from 'react';

interface FormData {
  firstName: string;
  lastName: string;
  isActive: boolean;
  role: RoleName;
}

interface UserEditModalProps {
  user: UserAPI;
  currentUser: UserAPI;
  onClose: () => void;
  onUserUpdated: (user: UserAPI) => void;
}

export default function UserEditModal({
  user,
  currentUser,
  onClose,
  onUserUpdated,
}: UserEditModalProps) {
  const [formData, setFormData] = useState<FormData>({
    firstName: user.firstName,
    lastName: user.lastName,
    isActive: user.isActive,
    role: user.role,
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [roles, setRoles] = useState<RoleOption[]>([]);

  useEffect(() => {
    const loadRoles = async () => {
      try {
        const roleOptions = await userService.getRoles();
        setRoles(roleOptions);
      } catch (err) {
        console.error('Failed to load roles:', err);
      }
    };

    loadRoles();
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      // Only send changed fields
      const updateData: UserUpdateAPI = {};

      if (formData.firstName !== user.firstName) {
        updateData.firstName = formData.firstName;
      }
      if (formData.lastName !== user.lastName) {
        updateData.lastName = formData.lastName;
      }
      if (formData.isActive !== user.isActive) {
        updateData.isActive = formData.isActive;
      }
      if (formData.role !== user.role) {
        updateData.role = formData.role;
      }

      // If no changes, just close the modal
      if (Object.keys(updateData).length === 0) {
        onClose();
        return;
      }

      const updatedUser = await userService.updateUser(user.id, updateData);
      onUserUpdated(updatedUser);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to update user');
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (
    field: keyof FormData,
    value: FormData[keyof FormData]
  ) => {
    setFormData((prev) => ({ ...prev, [field]: value }));
  };

  const canChangeRole = currentUser.role === 'admin';
  const isEditingSelf = user.id === currentUser.id;

  return (
    <div className="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
      <div className="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white">
        <div className="mt-3">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-medium text-gray-900">
              Edit User: {user.firstName} {user.lastName}
            </h3>
            <button
              onClick={onClose}
              className="text-gray-400 hover:text-gray-600 transition-colors"
            >
              <svg
                className="w-6 h-6"
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
            </button>
          </div>

          {error && (
            <div className="mb-4 bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
              {error}
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label
                htmlFor="firstName"
                className="block text-sm font-medium text-gray-700 mb-1"
              >
                First Name
              </label>
              <input
                id="firstName"
                type="text"
                required
                value={formData.firstName || ''}
                onChange={(e) => handleChange('firstName', e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500"
              />
            </div>

            <div>
              <label
                htmlFor="lastName"
                className="block text-sm font-medium text-gray-700 mb-1"
              >
                Last Name
              </label>
              <input
                id="lastName"
                type="text"
                required
                value={formData.lastName || ''}
                onChange={(e) => handleChange('lastName', e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500"
              />
            </div>

            <div>
              <label
                htmlFor="email"
                className="block text-sm font-medium text-gray-700 mb-1"
              >
                Email
              </label>
              <input
                id="email"
                type="email"
                value={user.email}
                disabled
                className="w-full px-3 py-2 border border-gray-300 rounded-md bg-gray-50 text-gray-500 cursor-not-allowed"
              />
              <p className="mt-1 text-xs text-gray-500">
                Email cannot be changed
              </p>
            </div>

            {canChangeRole && (
              <div>
                <label
                  htmlFor="role"
                  className="block text-sm font-medium text-gray-700 mb-1"
                >
                  Role
                </label>
                <select
                  id="role"
                  value={formData.role}
                  onChange={(e) =>
                    handleChange('role', e.target.value as RoleName)
                  }
                  disabled={isEditingSelf}
                  className={`w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500 ${
                    isEditingSelf
                      ? 'bg-gray-50 text-gray-500 cursor-not-allowed'
                      : ''
                  }`}
                >
                  {roles.map((role) => (
                    <option key={role.name} value={role.name}>
                      {role.display_name}
                    </option>
                  ))}
                </select>
                {isEditingSelf && (
                  <p className="mt-1 text-xs text-gray-500">
                    You cannot change your own role
                  </p>
                )}
              </div>
            )}

            <div className="flex items-center">
              <input
                id="isActive"
                type="checkbox"
                checked={formData.isActive ?? user.isActive}
                onChange={(e) => handleChange('isActive', e.target.checked)}
                disabled={isEditingSelf}
                className={`h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded ${
                  isEditingSelf ? 'cursor-not-allowed opacity-50' : ''
                }`}
              />
              <label
                htmlFor="isActive"
                className="ml-2 block text-sm text-gray-900"
              >
                Active User
              </label>
            </div>
            {isEditingSelf && (
              <p className="text-xs text-gray-500">
                You cannot deactivate your own account
              </p>
            )}

            <div className="flex items-center space-x-3 pt-4">
              <button
                type="submit"
                disabled={loading}
                className="flex-1 bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
              >
                {loading ? 'Updating...' : 'Update User'}
              </button>
              <button
                type="button"
                onClick={onClose}
                disabled={loading}
                className="flex-1 bg-gray-600 text-white px-4 py-2 rounded-md hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
              >
                Cancel
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}
