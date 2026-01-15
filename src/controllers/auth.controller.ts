import { Request, Response } from 'express';
import { signAccessToken, signRefreshToken } from '../utils/jwt.util';
// import User from '../models/User.model'; // Se implementará después

export async function login(req: Request, res: Response) {
  const { email, password } = req.body;
  // TODO: Buscar usuario y validar contraseña (mock temporal)
  if (email !== 'admin@demo.com' || password !== 'Password123!') {
    return res.status(401).json({ message: 'Credenciales inválidas' });
  }
  // Simulación de datos de usuario y empresa
  const user = {
    _id: 'userId123',
    companyId: 'companyId456',
    role: 'admin',
    email: 'admin@demo.com',
  };
  const accessToken = signAccessToken({
    userId: user._id,
    companyId: user.companyId,
    role: user.role,
    email: user.email,
  });
  const refreshToken = signRefreshToken({
    userId: user._id,
    companyId: user.companyId,
    role: user.role,
    email: user.email,
  });
  return res.json({ accessToken, refreshToken });
}

export async function refreshToken(req: Request, res: Response) {
  // El middleware ya habrá validado el refresh token y puesto el payload en req.user
  // @ts-ignore
  const user = req.user;
  if (!user) return res.status(401).json({ message: 'Refresh token inválido' });
  const accessToken = signAccessToken(user);
  return res.json({ accessToken });
}
