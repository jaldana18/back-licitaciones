import jwt from 'jsonwebtoken';
import { JwtPayload } from '../types/jwt.types';

const JWT_SECRET = process.env.JWT_SECRET || 'changeme';
const JWT_EXPIRE = process.env.JWT_EXPIRE || '15m';
const JWT_REFRESH_SECRET = process.env.JWT_REFRESH_SECRET || 'refreshchangeme';
const JWT_REFRESH_EXPIRE = process.env.JWT_REFRESH_EXPIRE || '7d';

export function signAccessToken(payload: JwtPayload): string {
  return jwt.sign(payload, JWT_SECRET, { expiresIn: JWT_EXPIRE });
}

export function signRefreshToken(payload: JwtPayload): string {
  return jwt.sign(payload, JWT_REFRESH_SECRET, { expiresIn: JWT_REFRESH_EXPIRE });
}

export function verifyAccessToken(token: string): JwtPayload | null {
  try {
    return jwt.verify(token, JWT_SECRET) as JwtPayload;
  } catch {
    return null;
  }
}

export function verifyRefreshToken(token: string): JwtPayload | null {
  try {
    return jwt.verify(token, JWT_REFRESH_SECRET) as JwtPayload;
  } catch {
    return null;
  }
}
