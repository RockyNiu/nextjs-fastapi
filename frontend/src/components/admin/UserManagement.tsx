'use client';

import { userService } from '@/services/userService';
import { UserAPI, UserRole } from '@/types/api';
import React, { useEffect, useState } from 'react';
import { toast } from 'react-hot-toast';
import UserEditModal from './UserEditModal';
import UserList from './UserList';

interface UserManagementProps {
  currentUser: UserAPI;
}

export default function UserManagement({ currentUser }: UserManagementProps) {
  const [users, setUsers] = useState<UserAPI[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedUser, setSelectedUser] = useState<UserAPI | null>(null);
  const [isEditModalOpen, setIsEditModalOpen] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');
  const [roleFilter, setRoleFilter] = useState<UserRole | 'all'>('all');
  const [statusFilter, setStatusFilter] = useState<
    'all' | 'active' | 'inactive'
  >('all');

  // Pagination
  const [currentPage, setCurrentPage] = useState(1);
  const [totalUsers, setTotalUsers] = useState(0);
  const usersPerPage = 10;

  const loadUsers = async (page: number = 1) => {
    try {
      setLoading(true);
      setError(null);
      const skip = (page - 1) * usersPerPage;
      const response = await userService.getAllUsers(skip, usersPerPage);
      setUsers(response.users);
      setTotalUsers(response.total);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load users');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadUsers(currentPage);
  }, [currentPage]);

  const handleEditUser = (user: UserAPI) => {
    setSelectedUser(user);
    setIsEditModalOpen(true);
  };

  const handleUserUpdated = async (updatedUser: UserAPI) => {
    setUsers(
      users.map((user) => (user.id === updatedUser.id ? updatedUser : user))
    );
    setIsEditModalOpen(false);
    setSelectedUser(null);
    toast.success('User updated successfully');
  };

  const handleToggleUserStatus = async (user: UserAPI) => {
    try {
      if (user.isActive) {
        await userService.deactivateUser(user.id);
        toast.success('User deactivated');
      } else {
        await userService.activateUser(user.id);
        toast.success('User activated');
      }
      await loadUsers(currentPage);
    } catch (err) {
      toast.error(
        err instanceof Error ? err.message : 'Failed to update user status'
      );
    }
  };

  const handleSearch = (term: string) => {
    setSearchTerm(term);
    // In a real app, you'd want to implement server-side search
    // For now, this is just for UI demonstration
  };

  const handleRoleFilter = (role: UserRole | 'all') => {
    setRoleFilter(role);
    // In a real app, you'd want to implement server-side filtering
  };

  const handleStatusFilter = (status: 'all' | 'active' | 'inactive') => {
    setStatusFilter(status);
    // In a real app, you'd want to implement server-side filtering
  };

  // Filter users based on search term, role, and status
  const filteredUsers = users.filter((user) => {
    const matchesSearch =
      user.firstName.toLowerCase().includes(searchTerm.toLowerCase()) ||
      user.lastName.toLowerCase().includes(searchTerm.toLowerCase()) ||
      user.email.toLowerCase().includes(searchTerm.toLowerCase());

    const matchesRole = roleFilter === 'all' || user.roleId === roleFilter;
    const matchesStatus =
      statusFilter === 'all' ||
      (statusFilter === 'active' && user.isActive) ||
      (statusFilter === 'inactive' && !user.isActive);

    return matchesSearch && matchesRole && matchesStatus;
  });

  const totalPages = Math.ceil(totalUsers / usersPerPage);

  if (loading && users.length === 0) {
    return (
      <div className="flex items-center justify-center min-h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (error && users.length === 0) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-lg p-6">
        <h3 className="text-lg font-medium text-red-800 mb-2">
          Error Loading Users
        </h3>
        <p className="text-red-600">{error}</p>
        <button
          onClick={() => loadUsers(currentPage)}
          className="mt-4 px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors"
        >
          Try Again
        </button>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Search and Filters */}
      <div className="bg-white rounded-lg shadow p-6">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <label
              htmlFor="search"
              className="block text-sm font-medium text-gray-700 mb-2"
            >
              Search Users
            </label>
            <input
              id="search"
              type="text"
              placeholder="Search by name or email..."
              value={searchTerm}
              onChange={(e) => handleSearch(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500"
            />
          </div>

          <div>
            <label
              htmlFor="roleFilter"
              className="block text-sm font-medium text-gray-700 mb-2"
            >
              Filter by Role
            </label>
            <select
              id="roleFilter"
              value={roleFilter}
              onChange={(e) =>
                handleRoleFilter(e.target.value as UserRole | 'all')
              }
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500"
            >
              <option value="all">All Roles</option>
              <option value={UserRole.USER}>User</option>
              <option value={UserRole.MODERATOR}>Moderator</option>
              <option value={UserRole.ADMIN}>Admin</option>
            </select>
          </div>

          <div>
            <label
              htmlFor="statusFilter"
              className="block text-sm font-medium text-gray-700 mb-2"
            >
              Filter by Status
            </label>
            <select
              id="statusFilter"
              value={statusFilter}
              onChange={(e) =>
                handleStatusFilter(
                  e.target.value as 'all' | 'active' | 'inactive'
                )
              }
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500"
            >
              <option value="all">All Status</option>
              <option value="active">Active</option>
              <option value="inactive">Inactive</option>
            </select>
          </div>
        </div>
      </div>

      {/* User List */}
      <UserList
        users={filteredUsers}
        currentUser={currentUser}
        onEditUser={handleEditUser}
        onToggleUserStatus={handleToggleUserStatus}
        loading={loading}
      />

      {/* Pagination */}
      {totalPages > 1 && (
        <div className="bg-white px-4 py-3 flex items-center justify-between border-t border-gray-200 sm:px-6 rounded-lg shadow">
          <div className="flex-1 flex justify-between sm:hidden">
            <button
              onClick={() => setCurrentPage(Math.max(1, currentPage - 1))}
              disabled={currentPage === 1}
              className="relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Previous
            </button>
            <button
              onClick={() =>
                setCurrentPage(Math.min(totalPages, currentPage + 1))
              }
              disabled={currentPage === totalPages}
              className="ml-3 relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Next
            </button>
          </div>

          <div className="hidden sm:flex-1 sm:flex sm:items-center sm:justify-between">
            <div>
              <p className="text-sm text-gray-700">
                Showing{' '}
                <span className="font-medium">
                  {(currentPage - 1) * usersPerPage + 1}
                </span>{' '}
                to{' '}
                <span className="font-medium">
                  {Math.min(currentPage * usersPerPage, totalUsers)}
                </span>{' '}
                of <span className="font-medium">{totalUsers}</span> results
              </p>
            </div>
            <div>
              <nav className="relative z-0 inline-flex rounded-md shadow-sm -space-x-px">
                <button
                  onClick={() => setCurrentPage(Math.max(1, currentPage - 1))}
                  disabled={currentPage === 1}
                  className="relative inline-flex items-center px-2 py-2 rounded-l-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  Previous
                </button>

                {(() => {
                  const pages: React.ReactNode[] = [];
                  const pageButtonClass = (page: number) =>
                    `relative inline-flex items-center px-4 py-2 border text-sm font-medium ${
                      currentPage === page
                        ? 'z-10 bg-blue-50 border-blue-500 text-blue-600'
                        : 'bg-white border-gray-300 text-gray-500 hover:bg-gray-50'
                    }`;
                  const ellipsisClass =
                    'relative inline-flex items-center px-4 py-2 border border-gray-300 bg-white text-sm font-medium text-gray-700';

                  // Always show first page
                  pages.push(
                    <button
                      key={1}
                      onClick={() => setCurrentPage(1)}
                      className={pageButtonClass(1)}
                    >
                      1
                    </button>
                  );

                  // Show left ellipsis if needed
                  if (currentPage > 4) {
                    pages.push(
                      <span key="left-ellipsis" className={ellipsisClass}>
                        ...
                      </span>
                    );
                  }

                  // Show pages around current page
                  const startPage = Math.max(2, currentPage - 1);
                  const endPage = Math.min(totalPages - 1, currentPage + 1);

                  for (let page = startPage; page <= endPage; page++) {
                    // Skip if already showing as first or last page
                    if (page === 1 || page === totalPages) continue;
                    // Skip pages too close to first page when we're showing ellipsis
                    if (currentPage > 4 && page < currentPage - 1) continue;
                    // Skip pages too close to last page when we're showing ellipsis
                    if (currentPage < totalPages - 3 && page > currentPage + 1)
                      continue;

                    pages.push(
                      <button
                        key={page}
                        onClick={() => setCurrentPage(page)}
                        className={pageButtonClass(page)}
                      >
                        {page}
                      </button>
                    );
                  }

                  // Show right ellipsis if needed
                  if (currentPage < totalPages - 3) {
                    pages.push(
                      <span key="right-ellipsis" className={ellipsisClass}>
                        ...
                      </span>
                    );
                  }

                  // Always show last page if more than 1 page
                  if (totalPages > 1) {
                    pages.push(
                      <button
                        key={totalPages}
                        onClick={() => setCurrentPage(totalPages)}
                        className={pageButtonClass(totalPages)}
                      >
                        {totalPages}
                      </button>
                    );
                  }

                  return pages;
                })()}

                <button
                  onClick={() =>
                    setCurrentPage(Math.min(totalPages, currentPage + 1))
                  }
                  disabled={currentPage === totalPages}
                  className="relative inline-flex items-center px-2 py-2 rounded-r-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  Next
                </button>
              </nav>
            </div>
          </div>
        </div>
      )}

      {/* Edit User Modal */}
      {isEditModalOpen && selectedUser && (
        <UserEditModal
          user={selectedUser}
          currentUser={currentUser}
          onClose={() => {
            setIsEditModalOpen(false);
            setSelectedUser(null);
          }}
          onUserUpdated={handleUserUpdated}
        />
      )}
    </div>
  );
}
