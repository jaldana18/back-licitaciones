import { Request, Response } from 'express';
import InteresLicitacion from '../models/InteresLicitacion.model';
import { Types } from 'mongoose';

// Crear un nuevo interés de licitación
export const crearInteres = async (req: Request, res: Response) => {
  try {
    const usuarioId = req.user?._id || req.body.usuarioId; // req.user si hay middleware de auth
    const { palabraClave, fechaInicio, fechaFin, valorMinimo } = req.body;
    if (!palabraClave) {
      return res.status(400).json({ message: 'La palabra clave es obligatoria.' });
    }
    const nuevoInteres = new InteresLicitacion({
      usuarioId,
      palabraClave,
      fechaInicio,
      fechaFin,
      valorMinimo,
    });
    await nuevoInteres.save();
    res.status(201).json(nuevoInteres);
  } catch (error) {
    res.status(500).json({ message: 'Error al crear el interés', error });
  }
};

// Listar intereses de un usuario
export const listarIntereses = async (req: Request, res: Response) => {
  try {
    const usuarioId = req.user?._id || req.query.usuarioId;
    if (!usuarioId) {
      return res.status(400).json({ message: 'Usuario no especificado.' });
    }
    const intereses = await InteresLicitacion.find({ usuarioId: new Types.ObjectId(usuarioId) });
    res.json(intereses);
  } catch (error) {
    res.status(500).json({ message: 'Error al listar intereses', error });
  }
};

// Eliminar un interés
export const eliminarInteres = async (req: Request, res: Response) => {
  try {
    const { id } = req.params;
    const usuarioId = req.user?._id || req.body.usuarioId;
    const interes = await InteresLicitacion.findOneAndDelete({ _id: id, usuarioId });
    if (!interes) {
      return res.status(404).json({ message: 'Interés no encontrado o no autorizado.' });
    }
    res.json({ message: 'Interés eliminado.' });
  } catch (error) {
    res.status(500).json({ message: 'Error al eliminar interés', error });
  }
};
