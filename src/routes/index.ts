import { Router } from 'express';
import authRoutes from './auth.routes';
import companyRoutes from './company.routes';
import userRoutes from './user.routes';

const router = Router();

router.use('/auth', authRoutes);
router.use('/companies', companyRoutes);
router.use('/users', userRoutes);

export default router;
