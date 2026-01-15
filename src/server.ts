import mongoose from 'mongoose';
import dotenv from 'dotenv';
import app from './app';

dotenv.config();

const PORT = process.env.PORT || 3000;
const MONGODB_URI = process.env.MONGODB_URI || 'mongodb://localhost:27017/licitaciones-salud';

mongoose.connect(MONGODB_URI)
  .then(() => {
    console.log('✅ Conectado a MongoDB');
    app.listen(PORT, () => {
      console.log(`🚀 Servidor escuchando en http://localhost:${PORT}`);
      console.log(`📚 Swagger en http://localhost:${PORT}/api-docs`);
    });
  })
  .catch((err) => {
    console.error('❌ Error conectando a MongoDB:', err);
    process.exit(1);
  });
