import { Request, Response } from 'express';
import Company from '../models/Company.model';

export async function createCompany(req: Request, res: Response) {
  try {
    const company = await Company.create(req.body);
    res.status(201).json(company);
  } catch (err) {
    res.status(400).json({ message: 'Error al crear empresa', error: err });
  }
}

export async function getCompanies(req: Request, res: Response) {
  const page = parseInt(req.query.page as string) || 1;
  const limit = parseInt(req.query.limit as string) || 10;
  const skip = (page - 1) * limit;
  const [companies, total] = await Promise.all([
    Company.find().skip(skip).limit(limit),
    Company.countDocuments()
  ]);
  res.json({ data: companies, total, page, pages: Math.ceil(total / limit) });
}

export async function getCompanyById(req: Request, res: Response) {
  const { id } = req.params;
  const company = await Company.findById(id);
  if (!company) return res.status(404).json({ message: 'Empresa no encontrada' });
  res.json(company);
}

export async function updateCompany(req: Request, res: Response) {
  const { id } = req.params;
  const company = await Company.findByIdAndUpdate(id, req.body, { new: true });
  if (!company) return res.status(404).json({ message: 'Empresa no encontrada' });
  res.json(company);
}

export async function deleteCompany(req: Request, res: Response) {
  const { id } = req.params;
  const company = await Company.findByIdAndDelete(id);
  if (!company) return res.status(404).json({ message: 'Empresa no encontrada' });
  res.json({ message: 'Empresa eliminada' });
}
