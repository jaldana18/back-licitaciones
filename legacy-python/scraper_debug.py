"""
Script de debugging para verificar por qué no hay resultados.
Captura el HTML de la tabla de resultados para análisis.
"""

import time
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import config
from resolver_captcha_gemini import resolver_captcha_con_gemini


def aceptar_cookies(driver):
    """Aceptar cookies"""
    try:
        wait = WebDriverWait(driver, 10)
        btn_aceptar = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'cc-btn')))
        btn_aceptar.click()
        print("✓ Cookies aceptadas")
    except:
        print("⚠ No hay banner de cookies")


def guardar_html(driver, filename):
    """Guarda el HTML de la página para análisis"""
    html = driver.page_source
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"✓ HTML guardado en: {filename}")
    return len(html)


if __name__ == "__main__":
    chrome_options = Options()
    chrome_options.add_experimental_option('detach', True)
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        print(f"🔍 Navegando a: {config.BASE_URL}\n")
        driver.get(config.BASE_URL)
        time.sleep(3)
        
        # Aceptar cookies
        aceptar_cookies(driver)
        time.sleep(1)
        
        # Llenar formulario
        print("📝 Rellenando formulario...")
        wait = WebDriverWait(driver, 20)
        campo = wait.until(EC.presence_of_element_located((By.ID, 'txtPalabrasClaves')))
        campo.send_keys(config.KEYWORD)
        print(f"✓ Palabra clave: {config.KEYWORD}")
        time.sleep(1)
        
        # Capturar y resolver captcha
        print("📸 Capturando y resolviendo captcha...")
        try:
            captcha = wait.until(EC.visibility_of_element_located(
                (By.XPATH, '//img[contains(@src, "generadorCaptcha.php")]')
            ))
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')[:-3]
            filename = f"debug_captcha_{timestamp}.png"
            captcha.screenshot(filename)
            print(f"✓ Captcha guardado: {filename}")
            
            # Resolver
            captcha_text = resolver_captcha_con_gemini(filename)
            if captcha_text:
                print(f"✓ Captcha resuelto: {captcha_text}")
                campo_img = driver.find_element(By.ID, 'image')
                campo_img.send_keys(captcha_text)
                print("✓ Captcha rellenado")
                time.sleep(1)
        except Exception as e:
            print(f"✗ Error con captcha: {e}")
            input("Ingresa el captcha manualmente y presiona ENTER...")
        
        # Click en buscar
        print("🔎 Buscando...")
        buscar_btn = driver.find_element(By.ID, 'btnBuscar')
        buscar_btn.click()
        
        # Esperar y capturar HTML antes de extraer
        print("⏳ Esperando resultados...")
        time.sleep(8)
        
        # Guardar HTML completo para análisis
        html_size = guardar_html(driver, 'debug_pagina_resultados.html')
        print(f"  Tamaño HTML: {html_size:,} bytes")
        
        # Intentar extraer tabla
        print("\n📊 Analizando tabla de resultados...")
        try:
            div_procesos = driver.find_element(By.XPATH, '//div[@id="divProcesos"]')
            print(f"✓ Div encontrado")
            
            # Obtener todas las filas
            rows = div_procesos.find_elements(By.XPATH, './/tr')
            print(f"✓ Total de filas (incluyendo encabezado): {len(rows)}")
            
            if len(rows) <= 1:
                print("\n⚠️  LA TABLA ESTÁ VACÍA O NO TIENE REGISTROS")
                print("\nPosibles causas:")
                print("  1. No hay resultados para esta palabra clave")
                print("  2. El captcha es incorrecto")
                print("  3. El sitio tiene restricciones anti-bot")
                print(f"\n📄 Revisa debug_pagina_resultados.html para ver el HTML")
                print("   Busca por 'divProcesos' para ver qué hay en la tabla")
            else:
                print(f"\n✅ Se encontraron {len(rows) - 1} registros")
                # Mostrar primeros registros
                for i, row in enumerate(rows[1:6]):  # Mostrar 5 primeros
                    cols = row.find_elements(By.TAG_NAME, 'td')
                    if cols:
                        print(f"\nRegistro {i+1}:")
                        print(f"  Código: {cols[0].text[:30]}")
                        print(f"  Entidad: {cols[1].text[:40]}")
                        print(f"  Objeto: {cols[2].text[:40]}")
        except Exception as e:
            print(f"✗ Error al extraer tabla: {e}")
            print(f"\n📄 Revisa debug_pagina_resultados.html manualmente")
        
        # Información adicional
        print("\n" + "="*70)
        print("INFORMACIÓN DE DEPURACIÓN:")
        print("="*70)
        print(f"URL actual: {driver.current_url}")
        print(f"Título: {driver.title}")
        print(f"\nArchivos generados:")
        print(f"  1. debug_pagina_resultados.html - HTML completo de la página")
        print(f"  2. debug_captcha_*.png - Imagen del captcha usado")
        
        print("\n⏳ Manteniendo navegador abierto por 15 segundos...")
        time.sleep(15)
        
    except Exception as e:
        print(f"\n✗ Error general: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        print("\n✓ Cerrando navegador")
        driver.quit()
