"""
Configuración global del proyecto de automatización.
Appium + WinAppDriver para la Calculadora de Windows.
"""
import os

# Rutas del proyecto
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCREENSHOTS_DIR = os.path.join(BASE_DIR, "screenshots")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")

# WinAppDriver
WINAPPDRIVER_URL = "http://127.0.0.1:4723"

# Desired Capabilities para la Calculadora de Windows
CALCULATOR_CAPS = {
    "app": "Microsoft.WindowsCalculator_8wekyb3d8bbwe!App",
    "platformName": "Windows",
    "deviceName": "WindowsPC",
    "automationName": "Windows",
}

# Timeouts (segundos)
IMPLICIT_WAIT = 5

# Modo esperado
EXPECTED_MODE = "Estándar"
EXPECTED_MODE_EN = "Standard"
EXPECTED_MODE_ALT = "Calculadora"
