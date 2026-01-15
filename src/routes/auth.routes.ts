import { Router } from 'express';
import { login, refreshToken, generateCompanyToken, generateUserToken } from '../controllers/auth.controller';
import { authenticateRefreshToken } from '../middlewares/refresh.middleware';

const router = Router();

router.post('/login', login);
router.post('/refresh', authenticateRefreshToken, refreshToken);
router.post('/company-token', generateCompanyToken);
router.post('/user-token', generateUserToken);

export default router;
