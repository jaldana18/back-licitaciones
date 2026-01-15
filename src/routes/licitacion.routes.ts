import { Router } from 'express';
import { buscarLicitaciones } from '../controllers/licitacion.controller';

const router = Router();

// GET /api/licitaciones/buscar?keywords=...&startDate=...&endDate=...&minValue=...
router.get('/buscar', buscarLicitaciones);

export default router;
