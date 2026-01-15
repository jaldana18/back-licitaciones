import mongoose, { Document, Schema } from 'mongoose';

export interface ILicitacion extends Document {
  titulo: string;
  descripcion: string;
  fechaPublicacion: Date;
  valor: number;
  entidad: string;
  // Puedes agregar más campos según necesidad
}

const LicitacionSchema = new Schema<ILicitacion>({
  titulo: { type: String, required: true },
  descripcion: { type: String, required: true },
  fechaPublicacion: { type: Date, required: true },
  valor: { type: Number, required: true },
  entidad: { type: String, required: true },
  // Agrega más campos si es necesario
});

export default mongoose.model<ILicitacion>('Licitacion', LicitacionSchema);
