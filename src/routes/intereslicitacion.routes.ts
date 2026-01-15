import { Router } from 'express';
import { crearInteres, listarIntereses, eliminarInteres } from '../controllers/intereslicitacion.controller';
import { authenticateJWT } from '../middlewares/auth.middleware';

const router = Router();

// Todas las rutas requieren autenticación
router.post('/', authenticateJWT, crearInteres);
router.get('/', authenticateJWT, listarIntereses);
router.delete('/:id', authenticateJWT, eliminarInteres);

export default router;
