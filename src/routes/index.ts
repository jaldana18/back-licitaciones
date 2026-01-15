import { Router } from 'express';

import authRoutes from './auth.routes';
import companyRoutes from './company.routes';
import userRoutes from './user.routes';
import interesLicitacionRoutes from './intereslicitacion.routes';

const router = Router();


router.use('/auth', authRoutes);
router.use('/companies', companyRoutes);
router.use('/users', userRoutes);
router.use('/intereses-licitacion', interesLicitacionRoutes);

export default router;
