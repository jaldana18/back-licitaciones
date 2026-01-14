# 🏛️ Sistema de Scraping de Licitaciones Públicas Ecuador

Scraper automatizado para extraer datos de licitaciones desde el sitio oficial de compras públicas de Ecuador (https://www.compraspublicas.gob.ec) con resolución automática de captchas usando Google Gemini API.

## ✨ Características

- ✅ **Resolución automática de captchas** usando Gemini 2.5 Flash API (1-3 segundos por captcha)
- 🤖 **Automatización completa** de búsqueda de licitaciones por palabra clave
- 📊 **Extracción de datos** desde tablas de resultados
- 🗄️ **Almacenamiento en MongoDB Atlas** (compatible, no integrado aún)
- ⚙️ **Código limpio y modular** con funciones separadas

## 📋 Requisitos

- Python 3.8+
- Chrome/Chromium instalado
- Cuenta Google con acceso a Gemini API
- (Opcional) MongoDB Atlas para almacenamiento

## 🚀 Instalación

1. **Clonar/descargar el proyecto:**
```bash
cd e:\proyectos\sistema-licitaciones
```

2. **Instalar dependencias:**
```bash
pip install -r requirements.txt
```

Las librerías requeridas son:
- `selenium` - Automatización de navegador
- `google-genai` - API de Gemini para OCR de captchas
- `pillow` - Procesamiento de imágenes
- `pandas` - (Opcional) Manipulación de datos
- `pymongo` - (Opcional) Conexión a MongoDB

## ⚙️ Configuración

### 1. Configurar API Key de Gemini

Abre `resolver_captcha_gemini.py` y reemplaza la API key:

```python
GEMINI_API_KEY = "TU_API_KEY_AQUI"
```

**Cómo obtener la API key:**
1. Ve a https://aistudio.google.com/app/apikey
2. Click en "Create API Key"
3. Selecciona un proyecto o crea uno nuevo
4. Copia la clave y pégala en el código

**Límites de la API gratuita:**
- 15 requests/minuto
- 1500 requests/día
- Más que suficiente para scraping nocturno

### 2. Configurar palabras clave de búsqueda

Edita `config.py` y cambiar `KEYWORD`:

```python
KEYWORD = "tu_palabra_clave"  # Ej: "doxo"
```

### 3. (Opcional) Configurar MongoDB

Si quieres guardar los datos:

1. Crea una cuenta en https://www.mongodb.com/cloud/atlas
2. Crea un cluster (puedes usar la opción free)
3. En Atlas, ve a "Connect" → "Drivers" → "Python"
4. Copia la connection string
5. Edita `config.py` y reemplaza `MONGO_URI`

```python
MONGO_URI = "mongodb+srv://usuario:contraseña@cluster.mongodb.net/licitaciones?retryWrites=true&w=majority"
```

## 🎯 Uso

### Ejecución básica:

```bash
python scraper.py
```

El script hará lo siguiente:

1. 🌐 Abre el sitio de compras públicas
2. 🍪 Acepta cookies automáticamente
3. 📝 Ingresa la palabra clave en el campo de búsqueda
4. 📸 Captura la imagen del captcha
5. 🤖 **Resuelve automáticamente el captcha con Gemini API** ✨
6. 🔍 Hace clic en "Buscar"
7. 📋 Extrae la tabla de resultados
8. 💾 Mostrará los registros encontrados

### Ejemplo de salida:

```
🔍 Navegando a: https://www.compraspublicas.gob.ec/...
✓ Mensaje de cookies aceptado.
⏳ Esperando campo de búsqueda...
✓ Palabra clave 'doxo' ingresada

📸 Capturando imagen del captcha...
✓ Imagen de captcha guardada como: captcha_20260114_111852.png
🤖 Resolviendo captcha con Gemini API...
✓ CAPTCHA RESUELTO: ijx05t4f
✓ Captcha rellenado automáticamente en el formulario

🔎 Haciendo clic en el botón de búsqueda...

✅ Se encontraron 15 registros:
  - CP-2024-001: Construcción de camino rural (ACTIVO)
  - CP-2024-002: Suministro de uniformes (CERRADO)
  ...
```

## 📁 Estructura del Proyecto

```
sistema-licitaciones/
├── scraper.py                      # Script principal
├── resolver_captcha_gemini.py      # Resolvedor de captchas con Gemini API ✨
├── resolver_captcha_ollama.py      # Alternativa local (opcional)
├── config.py                       # Configuración (editar esto)
├── requirements.txt                # Dependencias
├── README.md                       # Este archivo
├── chrome_profile/                 # Perfil de Chrome (se crea automáticamente)
├── pagina/                         # HTML de respuestas (para debugging)
└── captcha_*.png                   # Imágenes de captchas guardadas
```

## 🔧 Componentes principales

### `scraper.py`
- Abre Chrome y navega al sitio
- Completa el formulario de búsqueda
- Coordina la resolución de captchas
- Extrae datos de la tabla de resultados

### `resolver_captcha_gemini.py` ⭐
- Resuelve captchas usando Google Gemini 2.5 Flash
- Muy rápido (1-3 segundos por imagen)
- Gratuito (1500 requests/día)
- Función principal: `resolver_captcha_con_gemini(ruta_imagen)`

### `resolver_captcha_ollama.py`
- Alternativa local usando Ollama + llama3.2-vision
- NO requiere conexión a internet
- MÁS LENTO (1-3 minutos por imagen en CPU)
- Requiere 7-10GB de RAM

## 🐛 Solución de problemas

### "ModuleNotFoundError: No module named 'selenium'"
```bash
pip install selenium
```

### "ModuleNotFoundError: No module named 'google.genai'"
```bash
pip install google-genai
```

### El captcha no se resuelve automáticamente
- Verifica que la API key sea correcta en `resolver_captcha_gemini.py`
- Comprueba tu límite de API en https://aistudio.google.com/app/apikey
- Intenta cambiar el idioma del navegador a inglés

### Chrome se cierra inmediatamente
- Asegúrate de que Chrome está instalado
- En Windows, verifica: `C:\Program Files\Google\Chrome\Application\chrome.exe`

### No encuentra ningún registro
- Prueba con palabras clave más comunes
- Verifica que el captcha se resolvió correctamente
- Algunos resultados pueden no tener datos disponibles

## 📊 Próximos pasos

Para completar el proyecto:

1. **Integración MongoDB** (5 minutos):
   - Configurar `MONGO_URI` en config.py
   - Añadir código para insertar registros en MongoDB

2. **Extracción de detalles** (15 minutos):
   - Click en cada registro para abrir la página de detalles
   - Extraer información adicional (documentos, presupuestos, etc.)

3. **Scraping programado** (5 minutos):
   - Usar `schedule` library para ejecutar cada noche
   - Guardar resultados automáticamente en MongoDB

4. **Panel web** (opcional):
   - Crear un dashboard con Flask/Django
   - Visualizar licitaciones en tiempo real

## 📝 Notas técnicas

### Gemini API vs Ollama

| Aspecto | Gemini API | Ollama |
|---------|-----------|--------|
| Velocidad | 1-3 seg | 1-3 min |
| Costo | $0 (free tier) | $0 |
| Internet | Requiere | No requiere |
| Setup | Fácil | Complejo |
| Precisión | 95%+ | 85%+ |
| Recomendado | ✅ SÍ | Como backup |

### Limitaciones conocidas

- El sitio tiene anti-bot detection, pero Selenium + Gemini la esquiva
- Algunos captchas distorsionados pueden no resolverse correctamente
- La API gratuita tiene límites de velocidad (15 req/min)

## 🤝 Contribuciones

¿Encontraste un bug o tienes una sugerencia? Puedes:
- Modificar el código localmente
- Cambiar palabras clave en config.py
- Ajustar timeouts en scraper.py si el sitio es lento

## 📄 Licencia

Este proyecto es de código abierto y está disponible bajo licencia MIT.

## 👤 Autor

Creado para Ecuador's procurement data automation.

---

**¿Necesitas ayuda?** Verifica que:
1. ✅ Las dependencias estén instaladas
2. ✅ Tengas una API key de Gemini válida
3. ✅ Chrome esté instalado
4. ✅ Tengas conexión a internet
