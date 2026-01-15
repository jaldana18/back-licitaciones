
import { Request, Response } from 'express';
import User from '../models/User.model';
import bcrypt from 'bcryptjs';

export async function updateUser(req: Request, res: Response) {
  const { id } = req.params;
  try {
    let update = { ...req.body };
    if (update.password) {
      update.password = await bcrypt.hash(update.password, 10);
    }
    const user = await User.findByIdAndUpdate(id, update, { new: true });
    if (!user) return res.status(404).json({ message: 'Usuario no encontrado' });
    res.json(user);
  } catch (err) {
    res.status(400).json({ message: 'Error al actualizar usuario', error: err });
  }
}

export async function deleteUser(req: Request, res: Response) {
  const { id } = req.params;
  try {
    const user = await User.findByIdAndDelete(id);
    if (!user) return res.status(404).json({ message: 'Usuario no encontrado' });
    res.json({ message: 'Usuario eliminado' });
  } catch (err) {
    res.status(400).json({ message: 'Error al eliminar usuario', error: err });
  }
}

export async function getUsers(req: Request, res: Response) {
  const page = parseInt(req.query.page as string) || 1;
  const limit = parseInt(req.query.limit as string) || 10;
  const skip = (page - 1) * limit;
  const [users, total] = await Promise.all([
    User.find().skip(skip).limit(limit),
    User.countDocuments()
  ]);
  res.json({ data: users, total, page, pages: Math.ceil(total / limit) });
}

export async function getUserById(req: Request, res: Response) {
  const { id } = req.params;
  const user = await User.findById(id);
  if (!user) return res.status(404).json({ message: 'Usuario no encontrado' });
  res.json(user);
}

export async function createUser(req: Request, res: Response) {
  try {
    const { password, ...rest } = req.body;
    const hashedPassword = await bcrypt.hash(password, 10);
    const user = await User.create({ ...rest, password: hashedPassword });
    res.status(201).json(user);
  } catch (err) {
    res.status(400).json({ message: 'Error al crear usuario', error: err });
  }
}

