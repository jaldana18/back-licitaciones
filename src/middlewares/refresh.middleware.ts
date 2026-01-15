import { Request, Response, NextFunction } from 'express';
import { verifyRefreshToken } from '../utils/jwt.util';
import { JwtPayload } from '../types/jwt.types';

export function authenticateRefreshToken(req: Request, res: Response, next: NextFunction) {
  const { refreshToken } = req.body;
  if (!refreshToken) {
    return res.status(401).json({ message: 'Refresh token no proporcionado' });
  }
  const payload = verifyRefreshToken(refreshToken);
  if (!payload) {
    return res.status(401).json({ message: 'Refresh token inválido o expirado' });
  }
  // @ts-ignore
  req.user = payload;
  next();
}
