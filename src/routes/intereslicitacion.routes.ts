import { Router } from 'express';
import { crearInteres, listarIntereses, eliminarInteres } from '../controllers/intereslicitacion.controller';
import authMiddleware from '../middlewares/auth.middleware';

const router = Router();

// Todas las rutas requieren autenticación
router.post('/', authMiddleware, crearInteres);
router.get('/', authMiddleware, listarIntereses);
router.delete('/:id', authMiddleware, eliminarInteres);

export default router;
