import { Schema, model, Document, Types } from 'mongoose';

export interface IUser extends Document {
  companyId?: Types.ObjectId | null;
  name: string;
  email: string;
  password: string;
  role: 'admin' | 'user' | 'viewer';
  isActive: boolean;
  lastLogin?: Date;
  createdAt: Date;
  updatedAt: Date;
}

const UserSchema = new Schema<IUser>({
  companyId: { type: Schema.Types.ObjectId, ref: 'Company', required: false, default: null },
  name: { type: String, required: true },
  email: { type: String, required: true, unique: true },
  password: { type: String, required: true },
  role: { type: String, enum: ['admin', 'user', 'viewer'], default: 'user' },
  isActive: { type: Boolean, default: true },
  lastLogin: { type: Date },
}, { timestamps: true });

export default model<IUser>('User', UserSchema);
