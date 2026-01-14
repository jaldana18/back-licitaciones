#!/usr/bin/env python3
"""
Script de verificación de requisitos.
Verifica que todas las dependencias están instaladas correctamente.
"""

import sys
from importlib import import_module

# Lista de dependencias requeridas
DEPENDENCIAS = {
    'selenium': 'Web scraping y automatización de navegador',
    'google.genai': 'API de Google Gemini para OCR',
    'PIL': 'Procesamiento de imágenes (Pillow)',
    'pymongo': 'Conexión a MongoDB',
    'pandas': 'Manipulación de datos',
}

# Colores para terminal
COLOR_VERDE = '\033[92m'
COLOR_ROJO = '\033[91m'
COLOR_AMARILLO = '\033[93m'
COLOR_RESET = '\033[0m'
COLOR_CYAN = '\033[36m'


def verificar_dependencias():
    """Verifica que todas las dependencias estén instaladas"""
    
    print(f"\n{COLOR_CYAN}{'='*60}")
    print("VERIFICACIÓN DE DEPENDENCIAS")
    print(f"{'='*60}{COLOR_RESET}\n")
    
    todas_ok = True
    
    for modulo, descripcion in DEPENDENCIAS.items():
        try:
            import_module(modulo)
            print(f"{COLOR_VERDE}✓{COLOR_RESET} {modulo:<20} - {descripcion}")
        except ImportError:
            print(f"{COLOR_ROJO}✗{COLOR_RESET} {modulo:<20} - {descripcion}")
            todas_ok = False
    
    # Verificar archivos de configuración
    print(f"\n{COLOR_CYAN}{'='*60}")
    print("VERIFICACIÓN DE ARCHIVOS DE CONFIGURACIÓN")
    print(f"{'='*60}{COLOR_RESET}\n")
    
    import os
    archivos_requeridos = {
        'config.py': 'Configuración del proyecto',
        'scraper.py': 'Script principal de scraping',
        'resolver_captcha_gemini.py': 'Resolvedor de captchas con Gemini',
        'requirements.txt': 'Lista de dependencias',
    }
    
    for archivo, descripcion in archivos_requeridos.items():
        if os.path.exists(archivo):
            print(f"{COLOR_VERDE}✓{COLOR_RESET} {archivo:<30} - {descripcion}")
        else:
            print(f"{COLOR_ROJO}✗{COLOR_RESET} {archivo:<30} - {descripcion}")
            todas_ok = False
    
    # Verificar API key de Gemini
    print(f"\n{COLOR_CYAN}{'='*60}")
    print("VERIFICACIÓN DE CONFIGURACIÓN")
    print(f"{'='*60}{COLOR_RESET}\n")
    
    try:
        import config
        
        # Verificar KEYWORD
        if hasattr(config, 'KEYWORD') and config.KEYWORD:
            print(f"{COLOR_VERDE}✓{COLOR_RESET} KEYWORD configurado: '{config.KEYWORD}'")
        else:
            print(f"{COLOR_AMARILLO}⚠{COLOR_RESET} KEYWORD no configurado (usar valor por defecto)")
        
        # Verificar BASE_URL
        if hasattr(config, 'BASE_URL') and config.BASE_URL:
            print(f"{COLOR_VERDE}✓{COLOR_RESET} BASE_URL configurado")
        else:
            print(f"{COLOR_ROJO}✗{COLOR_RESET} BASE_URL no configurado")
            todas_ok = False
        
        # Verificar MONGO_URI (opcional)
        if hasattr(config, 'MONGO_URI'):
            if 'mongodb+srv://' in config.MONGO_URI:
                print(f"{COLOR_VERDE}✓{COLOR_RESET} MONGO_URI configurado para MongoDB Atlas")
            else:
                print(f"{COLOR_AMARILLO}⚠{COLOR_RESET} MONGO_URI no configurado (MongoDB no está configurado)")
        
    except ImportError as e:
        print(f"{COLOR_ROJO}✗{COLOR_RESET} Error importando config.py: {e}")
        todas_ok = False
    
    # Verificar API key de Gemini
    try:
        import resolver_captcha_gemini
        
        if hasattr(resolver_captcha_gemini, 'GEMINI_API_KEY'):
            api_key = resolver_captcha_gemini.GEMINI_API_KEY
            if api_key and api_key.startswith('AIzaSy'):
                print(f"{COLOR_VERDE}✓{COLOR_RESET} GEMINI_API_KEY configurado correctamente")
            else:
                print(f"{COLOR_ROJO}✗{COLOR_RESET} GEMINI_API_KEY inválido")
                todas_ok = False
        else:
            print(f"{COLOR_ROJO}✗{COLOR_RESET} GEMINI_API_KEY no encontrado")
            todas_ok = False
    except Exception as e:
        print(f"{COLOR_AMARILLO}⚠{COLOR_RESET} No se pudo verificar GEMINI_API_KEY: {e}")
    
    # Resultado final
    print(f"\n{COLOR_CYAN}{'='*60}")
    if todas_ok:
        print(f"{COLOR_VERDE}✓ TODAS LAS VERIFICACIONES PASARON CORRECTAMENTE{COLOR_RESET}")
        print(f"{COLOR_VERDE}El proyecto está listo para ejecutar:{COLOR_RESET}")
        print(f"{COLOR_VERDE}  python scraper.py{COLOR_RESET}")
    else:
        print(f"{COLOR_ROJO}✗ ALGUNAS VERIFICACIONES FALLARON{COLOR_RESET}")
        print(f"{COLOR_ROJO}Por favor, revisa los errores arriba e instala las dependencias faltantes.{COLOR_RESET}")
        print(f"{COLOR_ROJO}Ejecuta: pip install -r requirements.txt{COLOR_RESET}")
    print(f"{'='*60}\n{COLOR_RESET}")
    
    return todas_ok


if __name__ == '__main__':
    exito = verificar_dependencias()
    sys.exit(0 if exito else 1)
