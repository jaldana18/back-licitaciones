export interface JwtPayload {
  userId: string;
  companyId: string;
  role: 'admin' | 'user' | 'viewer';
  email: string;
  iat?: number;
  exp?: number;
}
