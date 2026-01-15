import { Schema, Document, model, Types } from 'mongoose';

export interface IInteresLicitacion extends Document {
  usuarioId: Types.ObjectId;
  palabraClave: string;
  fechaInicio?: Date;
  fechaFin?: Date;
  valorMinimo?: number;
}

const InteresLicitacionSchema = new Schema<IInteresLicitacion>({
  usuarioId: { type: Schema.Types.ObjectId, ref: 'User', required: true },
  palabraClave: { type: String, required: true },
  fechaInicio: { type: Date },
  fechaFin: { type: Date },
  valorMinimo: { type: Number },
});

export default model<IInteresLicitacion>('InteresLicitacion', InteresLicitacionSchema);
