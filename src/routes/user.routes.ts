import { Router } from 'express';
import {
  createUser,
  getUsers,
  getUserById,
  updateUser,
  deleteUser
} from '../controllers/user.controller';
import { authenticateJWT } from '../middlewares/auth.middleware';

const router = Router();

router.post('/', authenticateJWT, createUser);
router.get('/', authenticateJWT, getUsers);
router.get('/:id', authenticateJWT, getUserById);
router.patch('/:id', authenticateJWT, updateUser);
router.delete('/:id', authenticateJWT, deleteUser);

export default router;
