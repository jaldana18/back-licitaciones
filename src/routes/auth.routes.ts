import { Router } from 'express';
import { login, refreshToken } from '../controllers/auth.controller';
import { authenticateRefreshToken } from '../middlewares/refresh.middleware';

const router = Router();

router.post('/login', login);
router.post('/refresh', authenticateRefreshToken, refreshToken);

export default router;
