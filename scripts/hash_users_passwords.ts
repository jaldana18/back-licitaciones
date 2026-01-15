import mongoose from 'mongoose';
import dotenv from 'dotenv';
import bcrypt from 'bcryptjs';
import User from '../src/models/User.model';

dotenv.config();

const MONGODB_URI = process.env.MONGODB_URI || 'mongodb://localhost:27017/licitaciones-salud';

async function hashPlainPasswords() {
  await mongoose.connect(MONGODB_URI);
  console.log('Conectado a MongoDB');

  const users = await User.find({});
  let updated = 0;

  for (const user of users) {
    // Si la contraseña ya es un hash bcrypt, ignora
    if (user.password && user.password.startsWith('$2a$')) continue;
    // Si la contraseña es texto plano, hasheala
    const hashed = await bcrypt.hash(user.password, 10);
    user.password = hashed;
    await user.save();
    updated++;
    console.log(`Usuario ${user.email} actualizado`);
  }

  console.log(`Contraseñas actualizadas: ${updated}`);
  await mongoose.disconnect();
}

hashPlainPasswords().catch(err => {
  console.error('Error actualizando contraseñas:', err);
  process.exit(1);
});
