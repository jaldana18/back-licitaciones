import { Router } from 'express';
import {
  createCompany,
  getCompanies,
  getCompanyById,
  updateCompany,
  deleteCompany
} from '../controllers/company.controller';
import { authenticateJWT } from '../middlewares/auth.middleware';

const router = Router();

router.post('/', authenticateJWT, createCompany);
router.get('/', authenticateJWT, getCompanies);
router.get('/:id', authenticateJWT, getCompanyById);
router.patch('/:id', authenticateJWT, updateCompany);
router.delete('/:id', authenticateJWT, deleteCompany);

export default router;
