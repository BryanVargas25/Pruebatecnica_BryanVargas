"""
Configuración global de pytest.
Fixture compartido para la sesión de Appium + WinAppDriver.
"""
import sys
import os
import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pages.calculator_page import CalculatorPage


@pytest.fixture(scope="session")
def calculator():
    """
    Fixture de sesión: inicia la Calculadora via Appium/WinAppDriver
    antes de todos los tests y la cierra al finalizar.
    """
    calc = CalculatorPage()
    calc.launch()
    yield calc
    calc.close()
