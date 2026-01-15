import { Schema, model, Document } from 'mongoose';

export interface ICompany extends Document {
  name: string;
  nit: string;
  sector: string;
  email: string;
  phone?: string;
  address?: string;
  isActive: boolean;
  createdAt: Date;
  updatedAt: Date;
}

const CompanySchema = new Schema<ICompany>({
  name: { type: String, required: true },
  nit: { type: String, required: true, unique: true },
  sector: { type: String, default: 'health' },
  email: { type: String, required: true },
  phone: { type: String },
  address: { type: String },
  isActive: { type: Boolean, default: true },
}, { timestamps: true });

export default model<ICompany>('Company', CompanySchema);
