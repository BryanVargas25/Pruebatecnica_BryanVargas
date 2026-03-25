"""
Generador de reportes de bug en PDF.
Opcion (d) del flujo de pruebas.
"""
import os
import time
from fpdf import FPDF
from config.settings import REPORTS_DIR


def _safe(text: str) -> str:
    """Reemplaza caracteres no soportados por Helvetica."""
    replacements = {
        "\u00e1": "a", "\u00e9": "e", "\u00ed": "i",
        "\u00f3": "o", "\u00fa": "u", "\u00f1": "n",
        "\u00c1": "A", "\u00c9": "E", "\u00cd": "I",
        "\u00d3": "O", "\u00da": "U", "\u00d1": "N",
        "\u00fc": "u", "\u00dc": "U",
        "\u2018": "'", "\u2019": "'", "\u201c": '"', "\u201d": '"',
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text.encode("latin-1", errors="replace").decode("latin-1")


class BugReportPDF:
    """Genera un PDF con los detalles de un bug encontrado."""

    def __init__(self):
        self.pdf = None

    def generate(
        self,
        title: str,
        description: str,
        steps_to_reproduce: list[str],
        expected_result: str,
        actual_result: str,
        screenshot_path: str = None,
        severity: str = "Alta",
        priority: str = "Alta",
    ) -> str:
        """
        Genera el PDF del reporte de bug.

        Returns:
            Ruta absoluta del PDF generado.
        """
        os.makedirs(REPORTS_DIR, exist_ok=True)
        self.pdf = FPDF()
        self.pdf.set_auto_page_break(auto=True, margin=15)
        self.pdf.add_page()

        # Titulo del reporte
        self.pdf.set_font("Helvetica", "B", 18)
        self.pdf.cell(0, 15, "Reporte de Bug", new_x="LMARGIN", new_y="NEXT", align="C")
        self.pdf.ln(5)

        # Informacion general
        self._add_field("Titulo", _safe(title))
        self._add_field("Severidad", severity)
        self._add_field("Prioridad", priority)
        self._add_field("Fecha", time.strftime("%Y-%m-%d %H:%M:%S"))
        self._add_field("Reportado por", "Automatizacion QA - Bryan Vargas")
        self.pdf.ln(5)

        # Descripcion
        self._add_section("Descripcion", _safe(description))

        # Pasos para reproducir
        self.pdf.set_font("Helvetica", "B", 12)
        self.pdf.cell(0, 10, "Pasos para Reproducir:", new_x="LMARGIN", new_y="NEXT")
        self.pdf.set_font("Helvetica", "", 11)
        for i, step in enumerate(steps_to_reproduce, 1):
            self.pdf.set_x(self.pdf.l_margin)
            self.pdf.multi_cell(
                self.pdf.w - self.pdf.l_margin - self.pdf.r_margin,
                7,
                _safe(f"  {i}. {step}"),
            )
        self.pdf.ln(3)

        # Resultado esperado vs actual
        self._add_section("Resultado Esperado", _safe(expected_result))
        self._add_section("Resultado Actual", _safe(actual_result))

        # Captura de pantalla
        if screenshot_path and os.path.exists(screenshot_path):
            self.pdf.ln(5)
            self.pdf.set_font("Helvetica", "B", 12)
            self.pdf.cell(0, 10, "Captura de Pantalla:", new_x="LMARGIN", new_y="NEXT")
            try:
                img_w = self.pdf.w - 2 * self.pdf.l_margin
                self.pdf.image(screenshot_path, w=img_w)
            except Exception as e:
                self.pdf.set_font("Helvetica", "I", 10)
                self.pdf.cell(0, 10, f"(No se pudo insertar la imagen: {e})")

        # Guardar
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"bug_report_{timestamp}.pdf"
        filepath = os.path.join(REPORTS_DIR, filename)
        self.pdf.output(filepath)
        return filepath

    def _add_field(self, label: str, value: str):
        self.pdf.set_font("Helvetica", "B", 11)
        self.pdf.cell(45, 8, f"{label}:")
        self.pdf.set_font("Helvetica", "", 11)
        self.pdf.cell(0, 8, _safe(value), new_x="LMARGIN", new_y="NEXT")

    def _add_section(self, title: str, content: str):
        self.pdf.set_font("Helvetica", "B", 12)
        self.pdf.set_x(self.pdf.l_margin)
        self.pdf.cell(0, 10, f"{_safe(title)}:", new_x="LMARGIN", new_y="NEXT")
        self.pdf.set_font("Helvetica", "", 11)
        self.pdf.set_x(self.pdf.l_margin)
        self.pdf.multi_cell(
            self.pdf.w - self.pdf.l_margin - self.pdf.r_margin,
            7,
            _safe(content),
        )
        self.pdf.ln(3)
