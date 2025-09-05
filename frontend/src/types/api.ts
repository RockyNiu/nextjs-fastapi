// Frontend TypeScript types in camelCase (converted from backend snake_case)

export interface UserCreateAPI {
  email: string;
  firstName: string;
  lastName: string;
  password: string;
}

export interface UserLoginAPI {
  email: string;
  password: string;
}

export interface UserAPI {
  id: number;
  email: string;
  firstName: string;
  lastName: string;
  isActive: boolean;
  dateCreated: string;
  dateUpdated: string;
  emailVerified: boolean;
}

export interface TokenResponseAPI {
  accessToken: string;
  tokenType: string;
  expiresIn: number;
}

export interface ForgotPasswordAPI {
  email: string;
}

export interface PasswordResetAPI {
  token: string;
  newPassword: string;
}

export interface MessageResponseAPI {
  message: string;
  success: boolean;
}

export interface ErrorResponseAPI {
  error: string;
  detail?: string;
  success: boolean;
}

// API Response types
export type ApiResponse<T> = {
  data: T;
  status: number;
};

export type ApiError = {
  error: string;
  detail?: string;
  status: number;
};
