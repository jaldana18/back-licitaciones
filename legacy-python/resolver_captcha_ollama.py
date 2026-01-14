import ollama
import base64
import os
import time

def resolver_captcha_con_ollama(ruta_imagen):
    """
    Resuelve un captcha usando Ollama con llama3.2-vision localmente.
    """
    print(f"Procesando imagen: {ruta_imagen}")
    print(f"Tamaño del archivo: {os.path.getsize(ruta_imagen) / 1024:.2f} KB")
    
    # Verificar que Ollama esté corriendo
    print("\n[1/4] Verificando conexión con Ollama...")
    try:
        ollama.list()
        print("✓ Conexión con Ollama establecida")
    except Exception as e:
        print(f"✗ Error conectando con Ollama: {e}")
        print("Asegúrate de que Ollama esté corriendo (debería iniciarse automáticamente)")
        return None
    
    # Crear el prompt para el modelo
    prompt = """Analiza esta imagen y extrae únicamente el texto que aparece en ella. 
Devuelve SOLO las letras o números que ves, sin puntos, sin espacios extras, sin explicaciones.
Por ejemplo, si ves "abc123", responde solamente: abc123"""
    
    print("\n[2/4] Preparando imagen...")
    time.sleep(0.5)
    
    print("\n[3/4] Enviando imagen a Ollama (llama3.2-vision)...")
    print("⏳ Esto puede tardar 1-3 minutos en CPU (Ryzen 5 3600)...")
    print("   Nota: Tu RX 580 no se usa porque Ollama en Windows solo soporta NVIDIA CUDA por defecto")
    
    inicio = time.time()
    
    try:
        # Llamar al modelo de Ollama con la imagen
        response = ollama.chat(
            model='llama3.2-vision',
            messages=[{
                'role': 'user',
                'content': prompt,
                'images': [ruta_imagen]  # Ollama acepta rutas directamente
            }]
        )
        
        tiempo_transcurrido = time.time() - inicio
        print(f"\n✓ Respuesta recibida en {tiempo_transcurrido:.2f} segundos")
        
        print("\n[4/4] Procesando respuesta...")
        # Extraer el texto de la respuesta
        texto_captcha = response['message']['content'].strip()
        
        print(f"\n✓ Captcha resuelto: {texto_captcha}")
        print(f"\nRespuesta completa del modelo:\n{response['message']['content']}")
        return texto_captcha
        
    except Exception as e:
        print(f"\n✗ Error al resolver captcha: {e}")
        import traceback
        traceback.print_exc()
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
    
    texto_captcha = resolver_captcha_con_ollama(ruta_completa)
    
    if texto_captcha:
        print(f"\n✓ Texto del captcha listo para usar: {texto_captcha}")
    else:
        print("\nNo se pudo resolver el captcha.")
