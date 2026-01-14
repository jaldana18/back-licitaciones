# 🚀 Guía de Inicio Rápido

## En 3 pasos estarás scrapeando licitaciones

### 1️⃣ Instalación (1 minuto)

```bash
pip install -r requirements.txt
```

### 2️⃣ Verificar Setup (30 segundos)

```bash
python verificar_setup.py
```

Deberías ver `✓ TODAS LAS VERIFICACIONES PASARON CORRECTAMENTE`

### 3️⃣ Ejecutar Scraper (2 minutos)

```bash
python scraper.py
```

**¿Eso es todo!** El scraper hará automáticamente:
- 🌐 Abre el sitio web
- 🍪 Acepta cookies
- 📝 Completa el formulario con tu palabra clave
- 📸 Captura la imagen del captcha
- 🤖 **RESUELVE AUTOMÁTICAMENTE el captcha con Gemini API** ← ¡LA MAGIA!
- 🔍 Busca las licitaciones
- 📊 Extrae y muestra los resultados

## ⚙️ Configuración Mínima

Edita `config.py` y cambiar esta línea:

```python
KEYWORD = "tu_palabra_clave"  # Cambiar esto
```

Ejemplo: `KEYWORD = "construcción"` o `KEYWORD = "servicios"`

## 🆘 Solución de Problemas

### "No module named 'selenium'"
```bash
pip install selenium
```

### "No module named 'google.genai'"
```bash
pip install google-genai
```

### "El captcha no se resuelve"
Verifica que:
1. Tu API key de Gemini sea correcta en `resolver_captcha_gemini.py`
2. Tengas conexión a internet
3. No hayas agotado tu límite de API (1500 req/día)

### "Chrome se abre y se cierra inmediatamente"
Instala Chrome desde: https://www.google.com/chrome/

## 📊 ¿Qué datos extrae?

Por cada licitación encontrada, el scraper extrae:

- **Código**: CP-2024-001
- **Entidad**: Municipalidad de Quito
- **Objeto**: Construcción de camino rural
- **Estado**: ACTIVO, CERRADO, EN PROCESO
- **Provincia**: Pichincha, Guayas, etc.
- **Presupuesto**: Monto estimado
- **Fecha**: Fecha de publicación

## 🔐 Seguridad de la API Key

Tu API key de Gemini está en `resolver_captcha_gemini.py`. 

⚠️ **NO la compartas públicamente** - puede ser usada sin autorización.

## 🎯 Próximos pasos

Cuando estés listo para más:

1. **MongoDB**: Edita `MONGO_URI` en `config.py` para guardar datos
2. **Múltiples palabras clave**: Modifica `config.py` para usar una lista
3. **Automatización**: Usa `schedule` library para ejecutar cada noche
4. **Detalles**: Extrae información adicional de cada licitación

## 📚 Documentación completa

Lee [README.md](README.md) para documentación completa.

---

¿Necesitas ayuda? Revisa `README.md` o ejecuta `python verificar_setup.py` para diagnosticar.
