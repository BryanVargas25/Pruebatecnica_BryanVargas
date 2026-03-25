"""
Page Object Model para la Calculadora de Windows.
Usa Appium + WinAppDriver para interactuar con la UI.
"""
import time
from appium import webdriver
from selenium.webdriver.common.by import By
from config.settings import WINAPPDRIVER_URL, CALCULATOR_CAPS, IMPLICIT_WAIT


class CalculatorPage:
    """Page Object que representa la Calculadora de Windows via Appium."""

    # ── Locators (AccessibilityId / AutomationId) ──────────────
    DISPLAY = "CalculatorResults"
    HEADER = "Header"
    NAV_BUTTON = "TogglePaneButton"

    # Botones numéricos
    NUM_BUTTONS = {i: f"num{i}Button" for i in range(10)}

    # Operadores
    BTN_PLUS = "plusButton"
    BTN_MINUS = "minusButton"
    BTN_MULTIPLY = "multiplyButton"
    BTN_DIVIDE = "divideButton"
    BTN_EQUALS = "equalButton"
    BTN_CLEAR = "clearButton"
    BTN_CLEAR_ENTRY = "clearEntryButton"

    def __init__(self):
        self.driver = None

    # ── Ciclo de vida ──────────────────────────────────────────

    def launch(self):
        """Inicia la Calculadora mediante Appium + WinAppDriver."""
        self.driver = webdriver.Remote(
            command_executor=WINAPPDRIVER_URL,
            desired_capabilities=CALCULATOR_CAPS,
        )
        self.driver.implicitly_wait(IMPLICIT_WAIT)

    def close(self):
        """Cierra la sesión de Appium y la calculadora."""
        if self.driver:
            self.driver.quit()

    def take_screenshot(self, filepath: str):
        """Captura pantalla de la ventana de la calculadora."""
        if self.driver:
            self.driver.save_screenshot(filepath)

    # ── Consultas ──────────────────────────────────────────────

    def get_mode(self) -> str:
        """Retorna el modo actual de la calculadora."""
        try:
            header = self.driver.find_element_by_accessibility_id(self.HEADER)
            return header.text
        except Exception:
            try:
                nav = self.driver.find_element_by_accessibility_id(self.NAV_BUTTON)
                return nav.text
            except Exception:
                return self._get_title_mode()

    def _get_title_mode(self) -> str:
        """Extrae el modo desde el título de la ventana."""
        title = self.driver.title or ""
        for mode in ["Estándar", "Standard", "Científica", "Scientific",
                     "Calculadora", "Calculator"]:
            if mode.lower() in title.lower():
                return mode
        return title

    def get_display_text(self) -> str:
        """Retorna el texto limpio del display."""
        display = self.driver.find_element_by_accessibility_id(self.DISPLAY)
        raw = display.text.strip()
        for prefix in ["Display is", "La pantalla muestra", "El resultado es",
                     "Se muestra"]:
            if raw.startswith(prefix):
                raw = raw[len(prefix):].strip()
        return raw

    # ── Acciones sobre botones ─────────────────────────────────

    def _click(self, auto_id: str):
        """Clic en un elemento por AccessibilityId."""
        self.driver.find_element_by_accessibility_id(auto_id).click()
        time.sleep(0.3)

    def press_number(self, number: int):
        self._click(self.NUM_BUTTONS[number])

    def press_plus(self):
        self._click(self.BTN_PLUS)

    def press_minus(self):
        self._click(self.BTN_MINUS)

    def press_multiply(self):
        self._click(self.BTN_MULTIPLY)

    def press_divide(self):
        self._click(self.BTN_DIVIDE)

    def press_equals(self):
        self._click(self.BTN_EQUALS)

    def press_clear(self):
        self._click(self.BTN_CLEAR)

    # ── Operaciones de alto nivel ──────────────────────────────

    def perform_operation(self, num1: int, operator: str, num2: int) -> str:
        """
        Ejecuta una operación aritmética y retorna el texto del display.
        """
        op_map = {
            "+": self.press_plus,
            "-": self.press_minus,
            "*": self.press_multiply,
            "/": self.press_divide,
        }

        for digit in str(num1):
            self.press_number(int(digit))

        op_map[operator]()

        for digit in str(num2):
            self.press_number(int(digit))

        self.press_equals()
        time.sleep(0.5)
        return self.get_display_text()

    def display_shows_error(self) -> bool:
        """Verifica si el display muestra un error de división por cero."""
        text = self.get_display_text().lower()
        error_msgs = [
            "cannot divide by zero",
            "no se puede dividir entre cero",
            "result is undefined",
            "el resultado no está definido",
        ]
        return any(msg in text for msg in error_msgs)
