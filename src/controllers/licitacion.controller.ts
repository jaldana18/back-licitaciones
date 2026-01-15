import { Request, Response } from 'express';
import Licitacion from '../models/Licitacion.model';

export const buscarLicitaciones = async (req: Request, res: Response) => {
  try {
    const { keywords, startDate, endDate, minValue } = req.query;
    if (!keywords || typeof keywords !== 'string') {
      return res.status(400).json({ message: 'La palabra clave es obligatoria.' });
    }

    const query: any = {
      $or: [
        { titulo: { $regex: keywords, $options: 'i' } },
        { descripcion: { $regex: keywords, $options: 'i' } },
      ],
    };

    if (startDate || endDate) {
      query.fechaPublicacion = {};
      if (startDate) query.fechaPublicacion.$gte = new Date(startDate as string);
      if (endDate) query.fechaPublicacion.$lte = new Date(endDate as string);
    }
    if (minValue) {
      query.valor = { $gte: Number(minValue) };
    }

    const resultados = await Licitacion.find(query).sort({ fechaPublicacion: -1 });
    res.json(resultados);
  } catch (error) {
    res.status(500).json({ message: 'Error al buscar licitaciones', error });
  }
};
