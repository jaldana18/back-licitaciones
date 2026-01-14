# 🤖 Cómo Funciona la Resolución Automática de Captchas

## El Desafío Original

El sitio `compraspublicas.gob.ec` utiliza un **captcha visual** (código distorsionado de caracteres) para prevenir bots. El scraper necesitaba resolver estos automáticamente.

## La Solución: Gemini API + Vision

Usamos **Google Gemini 2.5 Flash** - un modelo de IA que puede:
1. 👀 Ver y analizar imágenes
2. 🔍 Reconocer texto distorsionado (OCR)
3. ⚡ Procesar en 1-3 segundos
4. 💰 Costo: Gratuito (1500 solicitudes/día)

## ¿Cómo Funciona el Flujo?

```
┌─────────────────────────────────────────────────────────┐
│                                                         │
│  1. SCRAPER ABRE EL SITIO                             │
│     └─ Selenium navega a compraspublicas.gob.ec       │
│                                                         │
│  2. COMPLETA EL FORMULARIO                            │
│     └─ Ingresa palabra clave (ej: "doxo")             │
│                                                         │
│  3. CAPTURA LA IMAGEN DEL CAPTCHA                     │
│     └─ Toma screenshot del elemento <img captcha>     │
│     └─ Guarda como: captcha_20260114_111852.png       │
│                                                         │
│  4. ENVÍA A GEMINI API ⭐                              │
│     ├─ Imagen: archivo PNG (4-5 KB)                   │
│     ├─ Modelo: gemini-2.5-flash                       │
│     └─ Prompt: "Extrae el texto de esta imagen"       │
│                                                         │
│  5. GEMINI RECONOCE EL TEXTO                          │
│     ├─ Analiza los caracteres distorsionados          │
│     ├─ Usa visión por computadora y IA                │
│     └─ Retorna: "ijx05t4f" (texto del captcha)        │
│                                                         │
│  6. RELLENA EL CAMPO AUTOMÁTICAMENTE                  │
│     └─ Ingresa "ijx05t4f" en el campo del captcha     │
│                                                         │
│  7. HACE CLIC EN BUSCAR                               │
│     └─ Ejecuta la búsqueda automáticamente            │
│                                                         │
│  8. EXTRAE RESULTADOS                                 │
│     └─ Tabla de licitaciones encontradas              │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## El Código Detrás

### Función Principal
```python
def resolver_captcha_con_gemini(ruta_imagen):
    """Resuelve un captcha enviándolo a Gemini API"""
    
    # 1. Leer imagen del disco
    with open(ruta_imagen, 'rb') as img_file:
        imagen_bytes = img_file.read()
    
    # 2. Enviar a Gemini con instrucciones claras
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=[
            types.Part.from_bytes(
                data=imagen_bytes, 
                mime_type='image/png'
            ),
            prompt  # Instrucción: "Extrae el texto"
        ]
    )
    
    # 3. Retornar el texto reconocido
    return response.text.strip()
```

### Integración en Scraper
```python
# En scraper.py:
image_path = guardar_captcha(driver)  # Captura screenshot
captcha_text = resolver_captcha_con_gemini(image_path)  # Resuelve
campo_captcha.send_keys(captcha_text)  # Rellena automáticamente
```

## ¿Por Qué Gemini API?

| Solución | Velocidad | Costo | Setup | Precisión |
|----------|-----------|-------|-------|-----------|
| **Gemini API** ⭐ | 1-3 seg | GRATIS | Fácil | 95%+ |
| Ollama Local | 1-3 min | GRATIS | Complejo | 85% |
| Tesseract OCR | <1 seg | GRATIS | Fácil | 60% |
| Solver comercial | Instant | $$ | Fácil | 99% |

**Elegimos Gemini porque:**
- ✅ Más rápido que alternativas locales
- ✅ Completamente gratuito
- ✅ Muy preciso con distorsiones
- ✅ Fácil de implementar
- ✅ 1500 solicitudes/día (suficiente)

## Limitaciones de la API Gratuita

```
┌─────────────────────────────────────────┐
│     GEMINI API - FREE TIER              │
├─────────────────────────────────────────┤
│ 15 solicitudes por MINUTO               │
│ 1500 solicitudes por DÍA                │
│ Múltiples modelos disponibles           │
│ Acceso a todos los features             │
└─────────────────────────────────────────┘
```

**Para nuestro uso (scraping nocturno):**
- Procesamos ~20-30 captchas por ejecución
- Ejecutamos 1-2 veces por día
- = ~40-60 solicitudes/día
- = **Ampliamente dentro del límite libre**

## Problemas Comunes y Soluciones

### "Captcha no resuelto"
- Verifica tu API key en `resolver_captcha_gemini.py`
- El modelo puede fallar en captchas muy distorsionados (raros)
- Solución: `resolver_captcha_ollama.py` como fallback

### "Error: RESOURCE_EXHAUSTED"
- Agotaste el límite de 1500 req/día
- Espera hasta mañana o crea otra API key

### "Error: PERMISSION_DENIED"
- API key inválida o expirada
- Obtén una nueva en https://aistudio.google.com/app/apikey

## ¿Cómo Obtengo una API Key?

1. Ve a https://aistudio.google.com/app/apikey
2. Click en **"Create API Key"**
3. Selecciona o crea un proyecto
4. Copia la clave generada
5. Pégala en `resolver_captcha_gemini.py`:

```python
GEMINI_API_KEY = "AIzaSy..."  # Tu clave aquí
```

**Listo.** ¡No requiere tarjeta de crédito!

## Alternativa: Ollama (Local)

Si prefieres no enviar imágenes a Google, hay un resolvedor local:

```bash
# Instala Ollama desde: https://ollama.ai
ollama pull llama3.2-vision

# Luego ejecuta:
python scraper_ollama.py  # Versión con Ollama local
```

**Ventajas:**
- 🔒 Privacidad total (sin enviar imágenes)
- 💰 Gratuito
- 🚫 Sin límites de API

**Desventajas:**
- 🐢 Muy lento (1-3 minutos por captcha)
- 💾 Requiere 7-10GB RAM
- ⚙️ Setup más complejo

## Seguridad de la API Key

⚠️ **IMPORTANTE:**

Tu API key es como una contraseña. Si la compartes:
- ❌ Otros pueden usar tu cuota de Gemini
- ❌ Google cobrará si exceden límites
- ❌ Es riesgo de seguridad

**Mejores prácticas:**
```python
# ❌ MAL - API key en el código
GEMINI_API_KEY = "AIzaSy123456..."

# ✅ BIEN - En variable de entorno
import os
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
```

Más adelante puedes cambiar a variables de entorno para mayor seguridad.

## Cuándo Usar Cada Solución

```
¿Necesitas velocidad?
├─ SÍ → Usa Gemini API ⭐ (1-3 seg)
└─ NO → Usa Ollama local (privacidad)

¿Preocupado por privacidad?
├─ SÍ → Usa Ollama local
└─ NO → Usa Gemini API ⭐ (más rápido)

¿Necesitas máxima precisión?
├─ SÍ → Usa servicio comercial ($$$)
└─ NO → Usa Gemini API ⭐ (95%)
```

## Monitoreo y Debugging

El script imprime información detallada:

```
📸 Capturando imagen del captcha...
✓ Imagen de captcha guardada como: captcha_20260114_111852.png
🤖 Resolviendo captcha con Gemini API...
[1/3] Procesando imagen: captcha_20260114_111852.png
       Tamaño: 4.37 KB

[2/3] Enviando imagen a Gemini API...
       ✓ Respuesta recibida en 2.48 segundos

[3/3] Procesando respuesta...

============================================================
✓ CAPTCHA RESUELTO: ijx05t4f
============================================================
✓ Captcha rellenado automáticamente en el formulario
```

**Puedes revisar las imágenes capturadas** en la carpeta del proyecto:
- `captcha_20260114_111852.png`
- `captcha_20260114_111911.png`
- etc.

## Próximos Pasos

Ahora que tienes resolución automática de captchas:

1. ✅ **Scraping completamente automatizado**
2. 📊 Integrar MongoDB para guardar datos
3. 🔄 Usar `schedule` para ejecutar automáticamente cada noche
4. 📈 Escalar a múltiples palabras clave
5. 🌐 Crear panel web para visualizar datos

---

**¿Más información?** Lee [README.md](README.md)
