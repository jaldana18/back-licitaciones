# 🏗️ Arquitectura del Sistema de Licitaciones de Salud

## 📋 Descripción General

Plataforma monolítica basada en **Node.js + Express + TypeScript + MongoDB** para gestión y monitoreo automatizado de licitaciones de medicamentos en el sector salud.

---

## 🎯 Stack Tecnológico

### Backend
- **Runtime**: Node.js 18+
- **Framework**: Express.js
- **Lenguaje**: TypeScript
- **Base de datos**: MongoDB + Mongoose
- **Autenticación**: JWT (JSON Web Tokens)
- **Validación**: Zod

### Scraping & Automation
- **Browser Automation**: Puppeteer
- **Task Scheduling**: Bull (con Redis) + node-cron
- **Captcha Resolution**: Google Gemini API

### Seguridad & Monitoring
- **Seguridad HTTP**: Helmet
- **Rate Limiting**: express-rate-limit
- **Logging**: Winston
- **Hashing**: bcryptjs

### Testing
- **Framework**: Jest
- **API Testing**: Supertest

---

## 📁 Estructura del Proyecto

```
sistema-licitaciones/
│
├── src/                          # Código fuente principal
│   ├── config/                   # Configuraciones globales
│   │   ├── database.ts          # Conexión a MongoDB
│   │   ├── env.ts               # Variables de entorno
│   │   └── logger.ts            # Configuración de Winston
│   │
│   ├── controllers/              # Controladores (lógica de negocio)
│   │   ├── auth.controller.ts
│   │   ├── company.controller.ts
│   │   ├── user.controller.ts
│   │   ├── medicine.controller.ts
│   │   └── tender.controller.ts
│   │
│   ├── middlewares/              # Middlewares de Express
│   │   ├── auth.middleware.ts   # Verificación de JWT
│   │   ├── error.middleware.ts  # Manejo de errores
│   │   ├── validation.middleware.ts
│   │   └── rbac.middleware.ts   # Control de acceso por roles
│   │
│   ├── models/                   # Modelos de MongoDB (Mongoose)
│   │   ├── Company.model.ts
│   │   ├── User.model.ts
│   │   ├── Medicine.model.ts
│   │   ├── Tender.model.ts
│   │   └── TenderHistory.model.ts
│   │
│   ├── routes/                   # Definición de rutas
│   │   ├── auth.routes.ts
│   │   ├── company.routes.ts
│   │   ├── user.routes.ts
│   │   ├── medicine.routes.ts
│   │   ├── tender.routes.ts
│   │   └── index.ts             # Agregador de rutas
│   │
│   ├── services/                 # Servicios de negocio
│   │   ├── auth.service.ts
│   │   ├── company.service.ts
│   │   ├── user.service.ts
│   │   ├── medicine.service.ts
│   │   ├── tender.service.ts
│   │   │
│   │   ├── scraping/            # Módulo de scraping
│   │   │   ├── scraper.service.ts
│   │   │   ├── browser.service.ts
│   │   │   └── parser.service.ts
│   │   │
│   │   ├── captcha/             # Resolución de captchas
│   │   │   ├── gemini.service.ts
│   │   │   └── captcha.service.ts
│   │   │
│   │   └── jobs/                # Tareas programadas
│   │       ├── scraper.job.ts
│   │       └── notification.job.ts
│   │
│   ├── utils/                    # Utilidades
│   │   ├── jwt.util.ts
│   │   ├── bcrypt.util.ts
│   │   ├── date.util.ts
│   │   └── validator.util.ts
│   │
│   ├── types/                    # Tipos y interfaces TypeScript
│   │   ├── express.d.ts
│   │   ├── tender.types.ts
│   │   ├── user.types.ts
│   │   └── api.types.ts
│   │
│   ├── validators/               # Esquemas de validación (Zod)
│   │   ├── auth.validator.ts
│   │   ├── company.validator.ts
│   │   ├── medicine.validator.ts
│   │   └── tender.validator.ts
│   │
│   ├── app.ts                    # Configuración de Express
│   └── server.ts                 # Punto de entrada principal
│
├── tests/                        # Tests
│   ├── unit/                    # Tests unitarios
│   └── integration/             # Tests de integración
│
├── docs/                         # Documentación adicional
│   ├── API.md                   # Documentación de API
│   ├── DATABASE.md              # Esquemas de base de datos
│   └── DEPLOYMENT.md            # Guía de despliegue
│
├── logs/                         # Archivos de log
├── uploads/                      # Archivos subidos
├── temp/                         # Archivos temporales (captchas, etc)
├── scripts/                      # Scripts de utilidad
│   ├── seed.ts                  # Poblar base de datos
│   └── migrate.ts               # Migraciones
│
├── legacy-python/                # Código Python original (referencia)
│
├── .env.example                  # Ejemplo de variables de entorno
├── .gitignore
├── package.json
├── tsconfig.json
├── jest.config.js
├── .eslintrc.js
├── .prettierrc
└── README.md
```

---

## 🔄 Flujo de Datos

### 1. Autenticación y Registro
```
Cliente → POST /api/auth/register
  ↓
Controller valida datos
  ↓
Service crea empresa + usuario admin
  ↓
Retorna JWT token
```

### 2. Gestión de Medicamentos de Interés
```
Cliente autenticado → POST /api/medicines
  ↓
Middleware verifica JWT
  ↓
Controller recibe datos
  ↓
Service asocia medicamento a empresa
  ↓
Guarda en MongoDB
```

### 3. Scraping Automatizado (Tarea Programada)
```
Cron Job (cada 6 horas)
  ↓
Scraper Service inicia
  ↓
Browser Service abre Puppeteer
  ↓
Consulta plataforma de licitaciones
  ↓
Encuentra captcha
  ↓
Gemini Service resuelve captcha (IA)
  ↓
Busca medicamentos registrados
  ↓
Parser Service extrae datos
  ↓
Tender Service guarda/actualiza licitaciones
  ↓
Crea historial de cambios
  ↓
Notificación a empresas (opcional)
```

### 4. Consulta de Licitaciones
```
Cliente → GET /api/tenders?medicine=doxorubicina
  ↓
Middleware verifica autenticación
  ↓
Controller aplica filtros
  ↓
Service consulta MongoDB
  ↓
Retorna licitaciones con:
  - Estado actual
  - Empresa adjudicataria
  - Valor de adjudicación
  - Historial de cambios
```

---

## 🗄️ Modelo de Datos

### Colecciones Principales

#### Companies (Empresas)
```typescript
{
  _id: ObjectId,
  name: string,
  nit: string,
  sector: 'health',
  email: string,
  phone: string,
  address: string,
  isActive: boolean,
  createdAt: Date,
  updatedAt: Date
}
```

#### Users (Usuarios)
```typescript
{
  _id: ObjectId,
  companyId: ObjectId,
  name: string,
  email: string,
  password: string (hashed),
  role: 'admin' | 'user' | 'viewer',
  isActive: boolean,
  lastLogin: Date,
  createdAt: Date,
  updatedAt: Date
}
```

#### Medicines (Medicamentos de Interés)
```typescript
{
  _id: ObjectId,
  companyId: ObjectId,
  name: string,
  principioActivo: string,
  keywords: string[],
  isActive: boolean,
  createdBy: ObjectId,
  createdAt: Date,
  updatedAt: Date
}
```

#### Tenders (Licitaciones)
```typescript
{
  _id: ObjectId,
  codigo: string (unique),
  entidad: string,
  objeto: string,
  medicineId: ObjectId,
  status: 'abierta' | 'adjudicada' | 'cerrada',
  presupuesto: number,
  provincia: string,
  fechaPublicacion: Date,
  fechaCierre: Date,
  empresaAdjudicataria: string?,
  valorAdjudicacion: number?,
  url: string,
  scrapedAt: Date,
  createdAt: Date,
  updatedAt: Date
}
```

#### TenderHistory (Historial de Cambios)
```typescript
{
  _id: ObjectId,
  tenderId: ObjectId,
  changes: {
    field: string,
    oldValue: any,
    newValue: any
  }[],
  changedAt: Date
}
```

---

## 🔐 Seguridad

### Autenticación
- JWT con expiración configurable
- Passwords hasheados con bcrypt (10 rounds)
- Refresh tokens (opcional, implementar en fase 2)

### Autorización (RBAC)
- **Admin**: CRUD completo de empresa, usuarios, medicamentos
- **User**: Crear/editar medicamentos, ver licitaciones
- **Viewer**: Solo lectura

### Protecciones
- Helmet para headers HTTP seguros
- Rate limiting por IP
- Validación de entrada con Zod
- Sanitización de datos

---

## ⚙️ Tareas Programadas

### Scraping Job
- **Frecuencia**: Cada 6 horas (configurable)
- **Tecnología**: Bull Queue + Redis
- **Proceso**:
  1. Obtener medicamentos activos
  2. Ejecutar scraping por cada medicamento
  3. Comparar con datos existentes
  4. Guardar cambios en historial
  5. Notificar si hay cambios importantes

### Limpieza de Archivos Temporales
- **Frecuencia**: Diaria (2:00 AM)
- **Proceso**: Eliminar captchas y archivos temp >24h

---

## 🚀 Despliegue

### Desarrollo
```bash
npm install
cp .env.example .env
# Configurar variables de entorno
npm run dev
```

### Producción
```bash
npm run build
npm start
```

### Requerimientos
- Node.js 18+
- MongoDB 6+
- Redis (para Bull Queue)
- Chrome/Chromium (para Puppeteer)

---

## 📊 Endpoints Principales

### Autenticación
- `POST /api/auth/register` - Registro de empresa
- `POST /api/auth/login` - Inicio de sesión
- `POST /api/auth/logout` - Cerrar sesión
- `GET /api/auth/me` - Usuario actual

### Empresas
- `GET /api/companies/:id` - Detalle de empresa
- `PATCH /api/companies/:id` - Actualizar empresa

### Usuarios
- `GET /api/users` - Listar usuarios de la empresa
- `POST /api/users` - Crear usuario
- `PATCH /api/users/:id` - Actualizar usuario
- `DELETE /api/users/:id` - Desactivar usuario

### Medicamentos
- `GET /api/medicines` - Listar medicamentos de interés
- `POST /api/medicines` - Agregar medicamento
- `PATCH /api/medicines/:id` - Actualizar medicamento
- `DELETE /api/medicines/:id` - Eliminar medicamento

### Licitaciones
- `GET /api/tenders` - Listar licitaciones (filtros)
- `GET /api/tenders/:id` - Detalle de licitación
- `GET /api/tenders/:id/history` - Historial de cambios

### Jobs (Admin)
- `POST /api/jobs/scraping/trigger` - Ejecutar scraping manual
- `GET /api/jobs/scraping/status` - Estado del job

---

## 🎯 Próximas Fases

### Fase 2
- [ ] Sistema de notificaciones (email/webhook)
- [ ] Dashboard con métricas y gráficos
- [ ] Exportación de reportes (PDF/Excel)
- [ ] Búsqueda avanzada con filtros

### Fase 3
- [ ] Multi-plataforma de scraping
- [ ] Machine Learning para predicción
- [ ] API pública para integraciones
- [ ] App móvil

---

## 📞 Contacto y Soporte

Para más información, consultar los siguientes documentos:
- [README.md](README.md) - Introducción y inicio rápido
- [API.md](docs/API.md) - Documentación completa de API
- [DATABASE.md](docs/DATABASE.md) - Esquemas detallados
- [DEPLOYMENT.md](docs/DEPLOYMENT.md) - Guía de despliegue
