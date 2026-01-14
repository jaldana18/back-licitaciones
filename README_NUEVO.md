# 🏥 Sistema de Gestión de Licitaciones de Salud

Plataforma empresarial para gestión y monitoreo automatizado de oportunidades de licitación de medicamentos en el sector salud.

---

## 🎯 Descripción

Sistema que permite a empresas del sector salud:
- ✅ Gestionar usuarios y medicamentos de interés
- 🤖 Monitorear licitaciones automáticamente mediante scraping
- 📊 Consultar estado, adjudicaciones y valores de licitaciones
- 📈 Visualizar historial y trazabilidad completa
- 🔔 Recibir notificaciones de cambios importantes

---

## 🚀 Stack Tecnológico

### Backend
- **Node.js** 18+ con **TypeScript**
- **Express.js** para API REST
- **MongoDB** + **Mongoose** para persistencia
- **JWT** para autenticación

### Scraping & Automation
- **Puppeteer** para automatización del navegador
- **Bull** + **Redis** para colas de tareas
- **Google Gemini API** para resolución de captchas
- **node-cron** para tareas programadas

### Seguridad & Calidad
- **Helmet** para seguridad HTTP
- **Zod** para validación de esquemas
- **Winston** para logging
- **Jest** para testing

---

## 📦 Instalación

### Prerrequisitos
- Node.js 18 o superior
- MongoDB 6 o superior
- Redis (para Bull Queue)
- Chrome/Chromium (para Puppeteer)

### Pasos

1. **Clonar el repositorio**
```bash
cd e:\proyectos\sistema-licitaciones
```

2. **Instalar dependencias**
```bash
npm install
```

3. **Configurar variables de entorno**
```bash
cp .env.example .env
# Editar .env con tus credenciales
```

4. **Iniciar servicios externos**
```bash
# MongoDB (si es local)
mongod

# Redis (si es local)
redis-server
```

5. **Ejecutar en desarrollo**
```bash
npm run dev
```

El servidor estará disponible en `http://localhost:3000`

---

## 🏗️ Estructura del Proyecto

```
src/
├── config/           # Configuraciones (DB, env, logger)
├── controllers/      # Controladores de rutas
├── middlewares/      # Middlewares (auth, validation, error)
├── models/           # Modelos de MongoDB (Mongoose)
├── routes/           # Definición de rutas
├── services/         # Lógica de negocio
│   ├── scraping/    # Módulo de scraping
│   ├── captcha/     # Resolución de captchas
│   └── jobs/        # Tareas programadas
├── utils/            # Utilidades
├── types/            # Tipos TypeScript
├── validators/       # Esquemas de validación (Zod)
├── app.ts           # Configuración de Express
└── server.ts        # Punto de entrada
```

Ver [ARQUITECTURA.md](ARQUITECTURA.md) para más detalles.

---

## 🔧 Configuración

### Variables de Entorno (.env)

```env
# Server
NODE_ENV=development
PORT=3000

# Database
MONGODB_URI=mongodb://localhost:27017/licitaciones-salud

# JWT
JWT_SECRET=tu_secreto_seguro
JWT_EXPIRE=7d

# Gemini API
GEMINI_API_KEY=tu_api_key
GEMINI_MODEL=gemini-2.5-flash

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379

# Scraping
SCRAPING_ENABLED=true
SCRAPING_CRON_SCHEDULE=0 */6 * * *
BASE_URL=https://www.compraspublicas.gob.ec/...
```

---

## 📝 Scripts Disponibles

```bash
# Desarrollo con hot-reload
npm run dev

# Compilar TypeScript
npm run build

# Ejecutar en producción
npm start

# Tests
npm test
npm run test:watch

# Linting
npm run lint
npm run lint:fix

# Formateo de código
npm run format

# Ejecutar scraper manualmente
npm run scraper
```

---

## 🔐 Autenticación

El sistema usa **JWT** (JSON Web Tokens) para autenticación.

### Registro de Empresa
```bash
POST /api/auth/register
Content-Type: application/json

{
  "companyName": "Farmacia XYZ",
  "nit": "1234567890",
  "email": "admin@farmacia.com",
  "password": "Password123!",
  "phone": "+593999999999"
}
```

### Login
```bash
POST /api/auth/login
Content-Type: application/json

{
  "email": "admin@farmacia.com",
  "password": "Password123!"
}
```

Respuesta:
```json
{
  "token": "eyJhbGciOiJIUzI1NiIs...",
  "user": {
    "id": "...",
    "name": "Admin",
    "email": "admin@farmacia.com",
    "role": "admin"
  }
}
```

### Uso del Token
```bash
GET /api/medicines
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
```

---

## 📊 Endpoints Principales

### Medicamentos de Interés
```bash
# Listar medicamentos
GET /api/medicines

# Agregar medicamento
POST /api/medicines
{
  "name": "Doxorubicina",
  "principioActivo": "Doxorubicina HCl",
  "keywords": ["doxo", "doxorubicina"]
}

# Actualizar
PATCH /api/medicines/:id

# Eliminar
DELETE /api/medicines/:id
```

### Licitaciones
```bash
# Listar con filtros
GET /api/tenders?medicine=doxorubicina&status=abierta

# Detalle
GET /api/tenders/:id

# Historial de cambios
GET /api/tenders/:id/history
```

Ver [docs/API.md](docs/API.md) para documentación completa.

---

## 🤖 Scraping Automatizado

### ¿Cómo Funciona?

1. **Tarea programada** se ejecuta cada 6 horas (configurable)
2. **Puppeteer** abre la plataforma de compras públicas
3. **Resuelve captchas** automáticamente con Gemini AI
4. **Busca medicamentos** registrados por las empresas
5. **Extrae datos** de licitaciones encontradas
6. **Compara con datos existentes** y detecta cambios
7. **Guarda en MongoDB** y crea historial
8. **Notifica a usuarios** (opcional)

### Ejecutar Manualmente
```bash
npm run scraper
```

### Configurar Frecuencia
Editar `.env`:
```env
SCRAPING_CRON_SCHEDULE=0 */6 * * *
# Formato cron: minuto hora día mes día-semana
# Ejemplos:
# 0 */6 * * *    = Cada 6 horas
# 0 0 * * *      = Diario a medianoche
# */30 * * * *   = Cada 30 minutos
```

---

## 🧪 Testing

```bash
# Ejecutar todos los tests
npm test

# Tests en modo watch
npm run test:watch

# Coverage
npm test -- --coverage
```

---

## 🚢 Despliegue

### Opción 1: VPS/Cloud Server

1. **Preparar servidor** (Ubuntu 22.04 recomendado)
```bash
# Instalar Node.js 18
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# Instalar PM2 para gestión de procesos
npm install -g pm2

# Instalar MongoDB y Redis
sudo apt-get install mongodb redis-server
```

2. **Clonar y configurar**
```bash
git clone <repo>
cd sistema-licitaciones
npm install
npm run build
```

3. **Configurar .env** con datos de producción

4. **Iniciar con PM2**
```bash
pm2 start dist/server.js --name licitaciones-api
pm2 startup
pm2 save
```

### Opción 2: Docker (recomendado)

Ver [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) para configuración con Docker Compose.

---

## 📚 Documentación Adicional

- [ARQUITECTURA.md](ARQUITECTURA.md) - Arquitectura completa del sistema
- [docs/API.md](docs/API.md) - Documentación de endpoints
- [docs/DATABASE.md](docs/DATABASE.md) - Esquemas de base de datos
- [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) - Guía de despliegue
- [legacy-python/README.md](legacy-python/README.md) - Código Python original

---

## 🔄 Migración desde Python

El código Python original ha sido movido a `legacy-python/` para referencia. 

La nueva arquitectura mantiene la funcionalidad de scraping pero con:
- ✅ Mejor estructura y escalabilidad
- ✅ Tipado fuerte con TypeScript
- ✅ API REST completa
- ✅ Multi-tenant (múltiples empresas)
- ✅ Sistema de usuarios y roles
- ✅ Tareas programadas robustas

---

## 🐛 Troubleshooting

### Puppeteer no encuentra Chrome
```bash
# Linux
sudo apt-get install chromium-browser

# Variables de entorno
export PUPPETEER_SKIP_CHROMIUM_DOWNLOAD=true
export PUPPETEER_EXECUTABLE_PATH=/usr/bin/chromium-browser
```

### Error de conexión a MongoDB
- Verificar que MongoDB esté corriendo: `sudo systemctl status mongodb`
- Revisar MONGODB_URI en `.env`
- Verificar permisos de red si es MongoDB Atlas

### Error de conexión a Redis
- Verificar que Redis esté corriendo: `redis-cli ping`
- Revisar REDIS_HOST y REDIS_PORT en `.env`

---

## 🤝 Contribuir

1. Fork el proyecto
2. Crear rama de feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit cambios (`git commit -m 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abrir Pull Request

---

## 📄 Licencia

ISC

---

## 📞 Soporte

Para preguntas o soporte, contactar a: [tu_email@ejemplo.com]
