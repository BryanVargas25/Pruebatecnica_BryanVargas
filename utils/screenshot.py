"""
Utilidad para capturas de pantalla via Appium driver.
"""
import os
import time
from config.settings import SCREENSHOTS_DIR


def take_screenshot(driver, name: str) -> str:
    """
    Captura la pantalla de la app y guarda la imagen.

    Args:
        driver: Instancia del Appium WebDriver.
        name: Nombre descriptivo para el archivo.

    Returns:
        Ruta absoluta del archivo guardado.
    """
    os.makedirs(SCREENSHOTS_DIR, exist_ok=True)
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    filename = f"{name}_{timestamp}.png"
    filepath = os.path.join(SCREENSHOTS_DIR, filename)
    driver.save_screenshot(filepath)
    return filepath
