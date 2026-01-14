from google import genai
from google.genai import types
from google.genai import errors as genai_errors
from PIL import Image
import os
import time

# Configurar la API key
GEMINI_API_KEY = "AIzaSyBn46Y2tIyymWvWMgsBM0HZWoMFS5NMzxc"
client = genai.Client(api_key=GEMINI_API_KEY)

def resolver_captcha_con_gemini(ruta_imagen):
    """
    Resuelve un captcha usando Google Gemini API (visión).
    """
    print(f"[1/3] Procesando imagen: {ruta_imagen}")
    print(f"       Tamaño: {os.path.getsize(ruta_imagen) / 1024:.2f} KB")
    
    # Cargar la imagen
    with open(ruta_imagen, 'rb') as img_file:
        imagen_bytes = img_file.read()

    # Prompt para extraer texto del captcha
    prompt = """Analiza esta imagen y extrae ÚNICAMENTE el texto que aparece en ella.
Responde SOLO con las letras o números que ves, sin espacios extras, sin puntos, sin explicaciones adicionales.
Si ves "abc123", responde solamente: abc123"""

    max_intentos = 4
    backoff_base = 1

    for intento in range(1, max_intentos + 1):
        try:
            print(f"\n[2/3] Enviando imagen a Gemini API... (intento {intento}/{max_intentos})")
            inicio = time.time()
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=[
                    types.Part.from_bytes(data=imagen_bytes, mime_type='image/png'),
                    prompt
                ]
            )
            tiempo = time.time() - inicio

            print(f"       ✓ Respuesta recibida en {tiempo:.2f} segundos")
            print("\n[3/3] Procesando respuesta...")
            texto_captcha = response.text.strip()

            print(f"\n{'='*60}")
            print(f"✓ CAPTCHA RESUELTO: {texto_captcha}")
            print(f"{'='*60}")
            return texto_captcha

        except Exception as e:
            print(f"\n✗ Error al resolver captcha (intento {intento}): {e}")
            import traceback
            traceback.print_exc()

            # Si es un error de servidor (p.ej. 503), reintentar con backoff
            if isinstance(e, genai_errors.ServerError) or '503' in str(e):
                if intento < max_intentos:
                    wait = backoff_base * (2 ** (intento - 1))
                    print(f"Reintentando en {wait} segundos...")
                    time.sleep(wait)
                    continue
                else:
                    print("Se alcanzó el máximo de reintentos en Gemini.")
            # Para otros errores o si no quedan reintentos, intentar fallback
            break

    # Fallback: intentar resolver con Ollama si está disponible
    try:
        print("\nIntentando fallback con Ollama (si está disponible)...")
        from resolver_captcha_ollama import resolver_captcha_con_ollama
        return resolver_captcha_con_ollama(ruta_imagen)
    except Exception as e:
        print(f"✗ Fallback con Ollama no disponible o falló: {e}")
        return None

if __name__ == "__main__":
    # Buscar la última imagen de captcha guardada
    captcha_files = [f for f in os.listdir('.') if f.startswith('captcha_') and f.endswith('.png')]
    captcha_files.sort(reverse=True)
    
    if not captcha_files:
        print("No se encontró ninguna imagen de captcha en la carpeta actual.")
        exit(1)
    
    captcha_img = captcha_files[0]
    ruta_completa = os.path.abspath(captcha_img)
    print(f"Usando la imagen: {captcha_img}\n")
    
    texto_captcha = resolver_captcha_con_gemini(ruta_completa)
    
    if texto_captcha:
        print(f"\nTexto del captcha listo para usar en el formulario: {texto_captcha}")
    else:
        print("\nNo se pudo resolver el captcha.")
