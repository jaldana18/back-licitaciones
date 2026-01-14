#!/usr/bin/env python3
"""
Script para limpiar archivos temporales generados durante el scraping.
- Elimina imágenes de captchas viejas
- Limpia cache de Python
- Mantiene el proyecto ordenado
"""

import os
import glob
from datetime import datetime, timedelta

# Colores para terminal
COLOR_VERDE = '\033[92m'
COLOR_ROJO = '\033[91m'
COLOR_AMARILLO = '\033[93m'
COLOR_RESET = '\033[0m'
COLOR_CYAN = '\033[36m'


def limpiar_captchas_viejos(dias=7):
    """Elimina imágenes de captchas más antiguas de X días"""
    print(f"\n{COLOR_CYAN}Limpiando captchas antiguos (> {dias} días)...{COLOR_RESET}")
    
    fecha_limite = datetime.now() - timedelta(days=dias)
    archivos_eliminados = 0
    
    for archivo in glob.glob('captcha_*.png'):
        try:
            # Obtener fecha de creación del archivo
            timestamp = os.path.getmtime(archivo)
            fecha_archivo = datetime.fromtimestamp(timestamp)
            
            if fecha_archivo < fecha_limite:
                os.remove(archivo)
                print(f"  {COLOR_ROJO}✗{COLOR_RESET} Eliminado: {archivo}")
                archivos_eliminados += 1
            else:
                print(f"  {COLOR_AMARILLO}⊕{COLOR_RESET} Mantenido: {archivo}")
        except Exception as e:
            print(f"  {COLOR_ROJO}✗{COLOR_RESET} Error al procesar {archivo}: {e}")
    
    if archivos_eliminados > 0:
        print(f"{COLOR_VERDE}✓ Se eliminaron {archivos_eliminados} captchas antiguos{COLOR_RESET}")
    else:
        print(f"{COLOR_VERDE}✓ No hay captchas antiguos para eliminar{COLOR_RESET}")


def limpiar_cache_python():
    """Elimina archivos de caché de Python"""
    print(f"\n{COLOR_CYAN}Limpiando caché de Python...{COLOR_RESET}")
    
    archivos_eliminados = 0
    
    # Eliminar archivos .pyc
    for archivo in glob.glob('**/__pycache__/*.pyc', recursive=True):
        try:
            os.remove(archivo)
            print(f"  {COLOR_ROJO}✗{COLOR_RESET} Eliminado: {archivo}")
            archivos_eliminados += 1
        except Exception as e:
            print(f"  {COLOR_ROJO}✗{COLOR_RESET} Error: {e}")
    
    # Eliminar carpetas __pycache__ vacías
    for carpeta in glob.glob('**/__pycache__', recursive=True):
        try:
            if not os.listdir(carpeta):  # Si está vacía
                os.rmdir(carpeta)
                print(f"  {COLOR_ROJO}✗{COLOR_RESET} Eliminada carpeta: {carpeta}")
                archivos_eliminados += 1
        except Exception as e:
            pass  # Ignorar si no está vacía
    
    if archivos_eliminados > 0:
        print(f"{COLOR_VERDE}✓ Se eliminaron {archivos_eliminados} archivos de caché{COLOR_RESET}")
    else:
        print(f"{COLOR_VERDE}✓ No hay caché para limpiar{COLOR_RESET}")


def mostrar_estadisticas():
    """Muestra estadísticas del proyecto"""
    print(f"\n{COLOR_CYAN}{'='*60}")
    print("ESTADÍSTICAS DEL PROYECTO")
    print(f"{'='*60}{COLOR_RESET}\n")
    
    # Contar imágenes de captcha
    captchas = glob.glob('captcha_*.png')
    tamaño_captchas = sum(os.path.getsize(f) for f in captchas) / 1024  # KB
    
    print(f"📸 Imágenes de captcha: {len(captchas)} ({tamaño_captchas:.2f} KB)")
    
    # Contar archivos Python
    scripts = glob.glob('*.py')
    print(f"🐍 Scripts Python: {len(scripts)}")
    
    # Contar archivos de documentación
    docs = glob.glob('*.md')
    print(f"📚 Documentación: {len(docs)} archivos")
    
    # Tamaño total del proyecto
    tamaño_total = sum(
        os.path.getsize(f) 
        for f in glob.glob('**/*', recursive=True) 
        if os.path.isfile(f)
    ) / 1024  # KB
    print(f"📦 Tamaño total: {tamaño_total:.2f} KB")


def main():
    print(f"\n{COLOR_CYAN}{'='*60}")
    print("UTILIDAD DE LIMPIEZA DEL PROYECTO")
    print(f"{'='*60}{COLOR_RESET}")
    
    # Mostrar menú
    print(f"\n{COLOR_CYAN}Opciones:{COLOR_RESET}")
    print("1. Limpiar captchas viejos (> 7 días)")
    print("2. Limpiar caché de Python")
    print("3. Limpiar todo")
    print("4. Ver estadísticas")
    print("5. Salir")
    
    while True:
        opcion = input(f"\n{COLOR_CYAN}Selecciona una opción (1-5):{COLOR_RESET} ").strip()
        
        if opcion == '1':
            dias = input(f"{COLOR_CYAN}¿Captchas más antiguos de cuántos días? (defecto: 7):{COLOR_RESET} ").strip()
            dias = int(dias) if dias.isdigit() else 7
            limpiar_captchas_viejos(dias)
            break
        
        elif opcion == '2':
            limpiar_cache_python()
            break
        
        elif opcion == '3':
            limpiar_captchas_viejos(7)
            limpiar_cache_python()
            break
        
        elif opcion == '4':
            mostrar_estadisticas()
            break
        
        elif opcion == '5':
            print(f"{COLOR_VERDE}Saliendo...{COLOR_RESET}")
            break
        
        else:
            print(f"{COLOR_ROJO}Opción inválida. Intenta de nuevo.{COLOR_RESET}")
    
    mostrar_estadisticas()
    print(f"\n{COLOR_VERDE}✓ Limpieza completada{COLOR_RESET}\n")


if __name__ == '__main__':
    main()
