"""
Script principal para ejecutar las pruebas de la Calculadora de Windows.
Usa Appium + WinAppDriver. 
Ejecutar: python run_tests.py

Prerequisitos:
  1. WinAppDriver corriendo en http://127.0.0.1:4723
  2. pip install -r requirements.txt
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pages.calculator_page import CalculatorPage
from utils.screenshot import take_screenshot
from utils.bug_report import BugReportPDF
from config.settings import EXPECTED_MODE, EXPECTED_MODE_EN, EXPECTED_MODE_ALT


def log(step: str, desc: str):
    print(f"\n{'='*60}")
    print(f"  PASO {step}: {desc}")
    print(f"{'='*60}")


def result(ok: bool, msg: str):
    print(f"  [{'PASS' if ok else 'FAIL'}] {msg}")


def main():
    print("\n" + "=" * 60)
    print("  AUTOMATIZACION - CALCULADORA DE WINDOWS")
    print("  Appium + WinAppDriver | Bryan Vargas")
    print("=" * 60)

    calc = CalculatorPage()
    ok = True

    try:
        # ── Iniciar Calculadora ────────────────────────────────
        log("1", "Iniciar la Calculadora via Appium + WinAppDriver de Windows")
        calc.launch()
        result(True, "Calculadora iniciada correctamente.")
        take_screenshot(calc.driver, "paso1_inicio")

        # ── Test #1: Modo Estándar ─────────────────────────────
        log("2", "Test #1 - Verificar modo Estandar")
        mode = calc.get_mode()
        is_std = any(m.lower() in mode.lower() for m in [EXPECTED_MODE, EXPECTED_MODE_EN, EXPECTED_MODE_ALT])
        result(is_std, f"Modo detectado: '{mode}'")
        take_screenshot(calc.driver, "paso2_modo")
        if not is_std:
            ok = False

        # ── Test #2: 9 + 3 = 12 y Clear ───────────────────────
        log("3", "Test #2 - Realizar 9 + 3 = y validar resultado 12")
        res = calc.perform_operation(9, "+", 3)
        is_12 = "12" in res
        result(is_12, f"Display: '{res}'")
        take_screenshot(calc.driver, "paso3_suma")
        if not is_12:
            ok = False

        calc.press_clear()
        cleared = calc.get_display_text()
        is_clear = "0" in cleared
        result(is_clear, f"Display despues de Clear: '{cleared}'")
        take_screenshot(calc.driver, "paso3_clear")
        if not is_clear:
            ok = False

        # ── Test #3: 5 / 0 → Error ────────────────────────────
        log("4", "Test #3 - Realizar 5 / 0 = y validar error")
        calc.perform_operation(5, "/", 0)
        has_err = calc.display_shows_error()
        dtxt = calc.get_display_text()
        result(has_err, f"Display: '{dtxt}'")
        take_screenshot(calc.driver, "paso4_div5_0")
        if not has_err:
            ok = False

        # ── Test #4: 6 / 0 → Validar resultado 0 ──────────────
        log("5", "Test #4 - Realizar 6 / 0 = y validar que muestre 0")
        calc.press_clear()
        calc.perform_operation(6, "/", 0)
        ss_path = take_screenshot(calc.driver, "paso5_div6_0")
        dtxt = calc.get_display_text()
        is_zero = dtxt.strip().replace(",", "").replace(".", "") == "0"
        result(is_zero, f"Display: '{dtxt}'")

        if not is_zero:
            ok = False
            print("\n  >> Prueba fallo. Generando reporte de bug en PDF...")
            report = BugReportPDF()
            pdf = report.generate(
                title="Division 6/0 no muestra resultado 0",
                description=(
                    "Al realizar 6 / 0 en la Calculadora de Windows, "
                    "se esperaba '0' como resultado. "
                    f"El display muestra: '{dtxt}'."
                ),
                steps_to_reproduce=[
                    "Abrir la Calculadora via Appium + WinAppDriver.",
                    "Verificar modo Estandar.",
                    "Presionar Clear (C).",
                    "Ingresar: 6 / 0 =",
                    "Observar el resultado en el display.",
                ],
                expected_result="El display muestra '0'.",
                actual_result=f"El display muestra: '{dtxt}'.",
                screenshot_path=ss_path,
                severity="Media",
                priority="Alta",
            )
            print(f"  >> Reporte PDF: {pdf}")

    except Exception as e:
        print(f"\n  [ERROR] {e}")
        try:
            take_screenshot(calc.driver, "error_general")
        except Exception:
            pass
        ok = False

    finally:
        log("6", "Cerrar la Calculadora")
        calc.close()
        result(True, "Calculadora cerrada.")

    print(f"\n{'='*60}")
    print(f"  RESULTADO FINAL: {'TODAS PASARON' if ok else 'ALGUNAS FALLARON'}")
    print(f"{'='*60}\n")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
