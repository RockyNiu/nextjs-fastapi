// Frontend TypeScript types in camelCase (converted from backend snake_case)

export type RoleName = 'user' | 'moderator' | 'admin';

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
  role: RoleName;
  dateCreated: string;
  dateUpdated: string;
  emailVerified: boolean;
}

export interface TokenAPI {
  accessToken: string;
  tokenType: string;
  expiresIn: number;
}

export interface TokenResponseAPI extends TokenAPI {}

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

export interface EmailVerificationResponseAPI extends TokenAPI {
  message: string;
  success: boolean;
}

export interface UserRegistrationResponseAPI extends TokenAPI {
  user: UserAPI;
}

export interface ErrorResponseAPI {
  error: string;
  detail?: string;
  success: boolean;
}

export interface UserUpdateAPI {
  firstName?: string;
  lastName?: string;
  isActive?: boolean;
  role?: RoleName;
}

export interface UserListResponseAPI {
  users: UserAPI[];
  total: number;
  skip: number;
  limit: number;
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
