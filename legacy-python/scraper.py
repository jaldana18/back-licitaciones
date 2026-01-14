import time
import os
import glob
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import config
from resolver_captcha_gemini import resolver_captcha_con_gemini


def limpiar_captchas_antiguos():
    """Elimina todos los captchas anteriores para mantener solo el nuevo"""
    captchas = glob.glob('captcha_*.png')
    for archivo in captchas:
        try:
            os.remove(archivo)
            print(f"🗑️  Eliminado captcha antiguo: {archivo}")
        except Exception as e:
            print(f"⚠ No se pudo eliminar {archivo}: {e}")


def aceptar_cookies(driver):
    """Función para aceptar el mensaje de cookies si aparece"""
    try:
        wait = WebDriverWait(driver, 10)
        btn_aceptar = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'cc-btn')))
        btn_aceptar.click()
        print("✓ Mensaje de cookies aceptado.")
    except Exception as e:
        print("⚠ No apareció el mensaje de cookies o ya fue aceptado.")


def guardar_captcha(driver):
    """Capturar y guardar la imagen del captcha"""
    try:
        # Primero limpiar captchas antiguos
        limpiar_captchas_antiguos()
        
        # Esperar a que la imagen del captcha esté presente y visible
        wait = WebDriverWait(driver, 10)
        captcha_img = wait.until(EC.visibility_of_element_located(
            (By.XPATH, '//img[contains(@src, "generadorCaptcha.php")]')
        ))
        
        # Pequeña pausa para asegurar que la imagen esté completamente cargada
        time.sleep(1)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')[:-3]  # Añadir milisegundos
        filename = f"captcha_{timestamp}.png"
        captcha_img.screenshot(filename)
        print(f"✓ Imagen de captcha guardada como: {filename}")
        return filename
    except Exception as e:
        print(f"✗ No se pudo guardar la imagen del captcha: {e}")
        return None


if __name__ == "__main__":
    # Configuración de Selenium
    chrome_options = Options()
    chrome_options.add_experimental_option('detach', True)

    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        driver.get(config.BASE_URL)
        print(f"🔍 Navegando a: {config.BASE_URL}\n")

        # Aceptar cookies
        aceptar_cookies(driver)
        time.sleep(1)

        # Esperar a que el campo de palabra clave esté presente
        print("⏳ Esperando campo de búsqueda...")
        wait = WebDriverWait(driver, 20)
        campo_palabra = wait.until(EC.presence_of_element_located((By.ID, 'txtPalabrasClaves')))
        campo_palabra.click()
        campo_palabra.clear()
        campo_palabra.send_keys(config.KEYWORD)
        print(f"✓ Palabra clave '{config.KEYWORD}' ingresada\n")
        time.sleep(1)

        # Capturar captcha
        print("📸 Capturando imagen del captcha...")
        image_path = guardar_captcha(driver)
        time.sleep(2)

        # Resolver captcha con Gemini API
        if image_path:
            print("🤖 Resolviendo captcha con Gemini API...")
            captcha_text = resolver_captcha_con_gemini(image_path)
            
            if captcha_text:
                print(f"✓ Captcha resuelto: {captcha_text}\n")
                
                # Rellenar el campo del captcha
                try:
                    campo_captcha = driver.find_element(By.ID, 'image')
                    campo_captcha.clear()
                    campo_captcha.send_keys(captcha_text)
                    print("✓ Captcha rellenado automáticamente en el formulario\n")
                    time.sleep(1)
                except Exception as e:
                    print(f"✗ No se pudo rellenar el campo del captcha: {e}")
                    input("⏱ Ingresa el captcha manualmente y presiona ENTER...")
            else:
                print("✗ No se pudo resolver el captcha automáticamente")
                input("⏱ Ingresa el captcha manualmente y presiona ENTER...")
        else:
            input("⏱ Ingresa el captcha manualmente y presiona ENTER...")

        # Hacer clic en el enlace de buscar (el <a> con onclick="botonBuscar()").
        # Ejecutamos la función JS directamente para garantizar que se llame al handler correcto.
        print("🔎 Haciendo clic en el botón de búsqueda (ejecutando botonBuscar() vía JS)...")
        try:
            driver.execute_script("if(typeof botonBuscar === 'function'){ botonBuscar(); } else { var a = document.querySelector(\"a.toolbarbotones[onclick*='botonBuscar']\"); if(a) a.click(); }")
            print("✓ Se ejecutó botonBuscar() vía JavaScript.")
        except Exception:
            try:
                buscar_enlace = driver.find_element(By.XPATH, "//a[contains(@onclick,'botonBuscar')]")
                driver.execute_script("arguments[0].scrollIntoView(true);", buscar_enlace)
                buscar_enlace.click()
            except Exception:
                try:
                    buscar_img = driver.find_element(By.XPATH, "//a[contains(@onclick,'botonBuscar')]//img")
                    driver.execute_script("arguments[0].scrollIntoView(true);", buscar_img)
                    buscar_img.click()
                except Exception:
                    try:
                        buscar_btn = driver.find_element(By.ID, 'btnBuscar')
                        driver.execute_script("arguments[0].scrollIntoView(true);", buscar_btn)
                        buscar_btn.click()
                    except Exception as e:
                        print(f"✗ No se pudo hacer clic en el botón de búsqueda: {e}")

        # Esperar a que se cargue la tabla de resultados
        print("⏳ Esperando resultados de búsqueda...")
        time.sleep(5)

        # Extraer la tabla de resultados
        rows = driver.find_elements(By.XPATH, '//div[@id="divProcesos"]//tr')[1:]
        procesos = []
        filas_ignoradas = 0

        for row in rows:
            cols = row.find_elements(By.TAG_NAME, 'td')
            if not cols or len(cols) < 7:
                filas_ignoradas += 1
                print(f"⚠ Fila ignorada (columnas encontradas: {len(cols) if cols else 0})")
                continue

            codigo = cols[0].text.strip()
            entidad = cols[1].text.strip()
            objeto = cols[2].text.strip()
            estado = cols[3].text.strip()
            provincia = cols[4].text.strip()
            presupuesto = cols[5].text.strip()
            fecha = cols[6].text.strip()
            procesos.append({
                'codigo': codigo,
                'entidad': entidad,
                'objeto': objeto,
                'estado': estado,
                'provincia': provincia,
                'presupuesto': presupuesto,
                'fecha': fecha
            })

        if filas_ignoradas:
            print(f"\n⚠ Se ignoraron {filas_ignoradas} filas incompletas al parsear la tabla.")

        print(f"\n{'='*70}")
        print(f"✅ BÚSQUEDA COMPLETADA")
        print(f"{'='*70}")
        
        if len(procesos) == 0:
            print(f"\n⚠️  NO SE ENCONTRARON REGISTROS para la palabra clave '{config.KEYWORD}'")
            print(f"\nPosibles razones:")
            print(f"  • La palabra clave no tiene resultados en el sitio")
            print(f"  • El captcha no se resolvió correctamente")
            print(f"  • Intenta cambiar la palabra clave en config.py")
            print(f"\n💡 Sugerencia: Prueba con palabras más comunes como 'construcción', 'servicios', etc.")
            
            # Pausa adicional para ver la página vacía
            print(f"\n⏳ Manteniendo navegador abierto por 10 segundos para verificar...")
            time.sleep(10)
        else:
            print(f"\n✅ Se encontraron {len(procesos)} registros:")
            print(f"{'='*70}")
            for i, p in enumerate(procesos, 1):
                print(f"\n{i}. {p['codigo']}")
                print(f"   Entidad:    {p['entidad']}")
                print(f"   Objeto:     {p['objeto']}")
                print(f"   Estado:     {p['estado']}")
                print(f"   Provincia:  {p['provincia']}")
                print(f"   Presupuesto: {p['presupuesto']}")
                print(f"   Fecha:      {p['fecha']}")
            print(f"\n{'='*70}")
            
            # Pausa para revisar los resultados
            print(f"\n⏳ Manteniendo navegador abierto por 10 segundos para revisar resultados...")
            time.sleep(10)

    except Exception as e:
        print(f"\n✗ Error durante el scraping: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        print("\n✓ Navegador cerrado.")
        driver.quit()

