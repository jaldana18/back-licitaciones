import { Request, Response } from 'express';
import { signAccessToken, signRefreshToken } from '../utils/jwt.util';
import User from '../models/User.model';
import bcrypt from 'bcryptjs';

export async function login(req: Request, res: Response) {
  const { email, password } = req.body;

  console.log(`[LOGIN] Intento de login para el usuario: ${email}`);

  try {
    const user = await User.findOne({ email, isActive: true });

    if (!user) {
      console.log(`[LOGIN] Login fallido para: ${email} - Usuario no encontrado o inactivo`);
      return res.status(401).json({ message: 'Credenciales inválidas' });
    }

    // DEBUG: Mostrar contraseñas para depuración
    console.log(`[DEBUG] Contraseña recibida: ${password}`);
    console.log(`[DEBUG] Contraseña en BD: ${user.password}`);

    const passwordMatch = await bcrypt.compare(password, user.password);
    if (!passwordMatch) {
      console.log(`[LOGIN] Login fallido para: ${email} - Contraseña incorrecta`);
      return res.status(401).json({ message: 'Credenciales inválidas' });
    }

    // Actualizar lastLogin
    user.lastLogin = new Date();
    await user.save();

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

    console.log(`[LOGIN] Login exitoso para: ${email} (userId: ${user._id}, role: ${user.role})`);
    return res.json({ accessToken, refreshToken });
  } catch (err) {
    console.error(`[LOGIN] Error en login para: ${email}`, err);
    return res.status(500).json({ message: 'Error interno del servidor' });
  }
}

export async function refreshToken(req: Request, res: Response) {
  // El middleware ya habrá validado el refresh token y puesto el payload en req.user
  // @ts-ignore
  const user = req.user;
  if (!user) return res.status(401).json({ message: 'Refresh token inválido' });
  const accessToken = signAccessToken(user);
  return res.json({ accessToken });
}

export async function generateCompanyToken(req: Request, res: Response) {
  // Token especial para crear empresas, expira en 10 minutos
  const payload = {
    role: 'company_creator',
    purpose: 'create_company',
  };
  const token = signAccessToken(payload);
  res.json({ token });
}

export async function generateUserToken(req: Request, res: Response) {
  // Token especial para crear usuarios, expira en 10 minutos
  const payload = {
    role: 'user_creator',
    purpose: 'create_user',
  };
  const token = signAccessToken(payload);
  res.json({ token });
}
