"""
Suite de pruebas automatizadas para la Calculadora de Windows.
Utiliza Appium + WinAppDriver con patrón POM.

Autor: Bryan Vargas
"""
import pytest
from utils.screenshot import take_screenshot
from utils.bug_report import BugReportPDF
from config.settings import EXPECTED_MODE, EXPECTED_MODE_EN, EXPECTED_MODE_ALT


class TestCalculadoraWindows:
    """Tests automatizados de la Calculadora de Windows."""

    # ── Test #1: Verificar modo Estándar ───────────────────────

    def test_01_modo_estandar(self, calculator):
        """Verifica que la calculadora inicia en modo Estándar."""
        mode = calculator.get_mode()
        take_screenshot(calculator.driver, "test01_modo_estandar")
        assert any(
            expected.lower() in mode.lower()
            for expected in [EXPECTED_MODE, EXPECTED_MODE_EN, EXPECTED_MODE_ALT]
        ), f"Se esperaba modo '{EXPECTED_MODE}', pero se encontro: '{mode}'"

    # ── Test #2: Operación 9 + 3 = 12 y Clear ─────────────────

    def test_02_suma_9_mas_3(self, calculator):
        """Realiza 9 + 3, valida resultado 12 y limpia."""
        result = calculator.perform_operation(9, "+", 3)
        take_screenshot(calculator.driver, "test02_suma_9_mas_3")
        assert "12" in result, (
            f"Se esperaba '12' en el display, pero se encontro: '{result}'"
        )
        # Limpiar la operación (Clear)
        calculator.press_clear()
        cleared = calculator.get_display_text()
        take_screenshot(calculator.driver, "test02_clear")
        assert "0" in cleared, (
            f"Despues de Clear se esperaba '0', pero se encontro: '{cleared}'"
        )

    # ── Test #3: División 5 / 0 → Error ────────────────────────

    def test_03_division_5_entre_0_error(self, calculator):
        """Realiza 5 / 0 y valida mensaje de error."""
        calculator.perform_operation(5, "/", 0)
        take_screenshot(calculator.driver, "test03_div_5_entre_0")
        assert calculator.display_shows_error(), (
            "Se esperaba 'Cannot divide by zero', "
            f"pero el display muestra: '{calculator.get_display_text()}'"
        )

    # ── Test #4: División 6 / 0 → Validar resultado 0 ─────────

    def test_04_division_6_entre_0_resultado_cero(self, calculator):
        """
        Realiza 6 / 0 y valida que el display muestre '0'.
        Si falla, genera un reporte de bug en PDF con captura de pantalla.
        """
        calculator.press_clear()
        calculator.perform_operation(6, "/", 0)
        screenshot_path = take_screenshot(calculator.driver, "test04_div_6_entre_0")
        display_text = calculator.get_display_text()

        test_passed = display_text.strip().replace(",", "").replace(".", "") == "0"

        if not test_passed:
            # Generar reporte de bug en PDF (opción d)
            report = BugReportPDF()
            pdf_path = report.generate(
                title="Division 6/0 no muestra resultado 0",
                description=(
                    "Al realizar la operacion 6 / 0 en la Calculadora de Windows, "
                    "se esperaba que el display mostrara '0' como resultado. "
                    f"Sin embargo, el display muestra: '{display_text}'."
                ),
                steps_to_reproduce=[
                    "Abrir la Calculadora de Windows via Appium + WinAppDriver.",
                    "Verificar que esta en modo Estandar.",
                    "Presionar Clear (C) para limpiar el display.",
                    "Ingresar: 6 / 0 =",
                    "Observar el resultado en el display.",
                ],
                expected_result="El display muestra '0'.",
                actual_result=f"El display muestra: '{display_text}'.",
                screenshot_path=screenshot_path,
                severity="Media",
                priority="Alta",
            )
            print(f"\n[BUG REPORT] PDF generado en: {pdf_path}")

            pytest.fail(
                f"Se esperaba '0' en el display, pero se encontro: '{display_text}'. "
                f"Reporte de bug generado en: {pdf_path}"
            )
