import { Request, Response, NextFunction } from 'express';
import jwt from 'jsonwebtoken';
import { JwtPayload } from '../types/jwt.types';

const JWT_SECRET = process.env.JWT_SECRET || 'changeme';

export interface AuthRequest extends Request {
  user?: JwtPayload;
}

export function authenticateJWT(req: AuthRequest, res: Response, next: NextFunction) {
  const authHeader = req.headers.authorization;
  if (!authHeader || !authHeader.startsWith('Bearer ')) {
    return res.status(401).json({ message: 'Token no proporcionado' });
  }
  const token = authHeader.split(' ')[1];
  try {
    const decoded = jwt.verify(token, JWT_SECRET) as JwtPayload;
    req.user = decoded;
    next();
  } catch (err) {
    return res.status(401).json({ message: 'Token inválido o expirado' });
  }
}
