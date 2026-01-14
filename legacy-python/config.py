# ============================================
# CONFIGURACIÓN DEL PROYECTO DE SCRAPING
# ============================================

# ============================================
# CONFIGURACIÓN DE MONGODB ATLAS
# ============================================
# Para obtener tu MONGO_URI:
# 1. Ve a https://www.mongodb.com/cloud/atlas
# 2. Crea un cluster (o usa uno existente)
# 3. Click en "Connect" → "Drivers" → "Python"
# 4. Copia la connection string y reemplaza la contraseña
# Formato: mongodb+srv://usuario:contraseña@cluster.mongodb.net/nombre_bd?retryWrites=true&w=majority

MONGO_URI = "mongodb+srv://usuario:contraseña@cluster.mongodb.net/licitaciones?retryWrites=true&w=majority"
DB_NAME = "licitaciones"
COLLECTION_NAME = "procesos"

# ============================================
# CONFIGURACIÓN DE BÚSQUEDA
# ============================================
# Palabra clave(s) para buscar licitaciones
KEYWORD = "doxorubicina"

# ============================================
# CONFIGURACIÓN DE LA URL
# ============================================
# URL base del sitio de compras públicas
BASE_URL = "https://www.compraspublicas.gob.ec/ProcesoContratacion/compras/PC/buscarProceso.cpe?sg=1#"

# ============================================
# CONFIGURACIÓN DE GEMINI API
# ============================================
# La API key se configura directamente en resolver_captcha_gemini.py
# Límites: 15 requests/min, 1500 requests/day (free tier)
GEMINI_MODEL = "gemini-2.5-flash"
