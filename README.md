# Automatización QA - Calculadora de Windows

Automatización con Appium + WinAppDriver para validar operaciones aritméticas y manejo de errores en la Calculadora de Windows, usando patrón Page Object Model (POM).

**Autor:** Bryan Vargas
**Propósito:** Prueba técnica - Vacante QA

---

## Estructura del Proyecto (POM)

```
├── config/
│   └── settings.py          # Configuración (capabilities, URLs, timeouts)
├── pages/
│   └── calculator_page.py   # Page Object de la Calculadora (Appium)
├── tests/
│   └── test_calculator.py   # Suite de 4 tests con pytest
├── utils/
│   ├── screenshot.py        # Capturas de pantalla via Appium
│   └── bug_report.py        # Generador de reportes de bug en PDF
├── screenshots/              # Capturas generadas durante ejecución
├── reports/                  # Reportes PDF de bugs
├── conftest.py               # Fixture de sesión Appium para pytest
├── run_tests.py              # Script de ejecución directa
├── requirements.txt          # Dependencias
└── README.md
```

## Prerequisitos

1. **Windows 10/11** con la Calculadora de Windows instalada
2. **Python 3.10+**
3. **WinAppDriver v1.2.1** instalado y corriendo:
   - Descargar de: https://github.com/microsoft/WinAppDriver/releases/tag/v1.2.1
   - Ejecutar el instalador `.msi` como administrador
   - La ruta de instalación puede variar:
     - `C:\Program Files\Windows Application Driver\`
     - `C:\Program Files (x86)\Windows Application Driver\`
   - Habilitar **Modo de desarrollador** en Windows:
     - Configuración → Actualización y seguridad → Para programadores → Modo de desarrollador
     - O via registro (como administrador):
       ```
       reg add HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\AppModelUnlock /v AllowDevelopmentWithoutDevLicense /t REG_DWORD /d 1 /f
       ```
   - Ejecutar WinAppDriver como administrador:
     ```
     "C:\Program Files (x86)\Windows Application Driver\WinAppDriver.exe"
     ```
     Debe mostrar: `Windows Application Driver listening for requests at: http://127.0.0.1:4723`

## Nota de Compatibilidad

WinAppDriver v1.2.1 utiliza el protocolo **JSON Wire Protocol (JSONWP)**, por lo que requiere versiones específicas de Selenium y Appium:

| Dependencia | Versión requerida | Motivo |
|-------------|-------------------|--------|
| Appium-Python-Client | 1.3.0 | Soporte JSONWP + `desired_capabilities` |
| selenium | 3.141.0 | Protocolo JSONWP nativo |
| urllib3 | 1.26.x | Compatibilidad con Selenium 3 |

Las versiones más recientes (Selenium 4+, Appium-Python-Client 2+) usan el protocolo W3C WebDriver, que **no es compatible** con WinAppDriver 1.2.1.

## Instalación

```bash
# Crear entorno virtual (recomendado)
python -m venv venv
venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

## Ejecución

**Importante:** WinAppDriver debe estar corriendo como administrador antes de ejecutar las pruebas.

### Opción 1: Script directo (recomendado para demo)

```bash
python run_tests.py
```

### Opción 2: Con pytest

```bash
# Ejecución básica
pytest tests/test_calculator.py -v

# Con reporte HTML
pytest tests/test_calculator.py -v --html=reports/test_report.html
```

## Tests Implementados

| Test | Acción | Resultado esperado |
|------|--------|--------------------|
| #1 | Iniciar Calculadora | Modo "Estándar" / "Calculadora" activo |
| #2 | 9 + 3 = | Display muestra "12", luego Clear muestra "0" |
| #3 | 5 / 0 = | Display muestra "No se puede dividir entre cero" |
| #4 | 6 / 0 = | Valida si muestra "0" (genera bug report PDF al fallar) |

### Soporte de idioma

La calculadora se adapta al idioma del sistema operativo. Los tests validan tanto mensajes en español como en inglés:

- Modo: "Estándar" / "Standard" / "Calculadora" / "Calculator"
- Error: "No se puede dividir entre cero" / "Cannot divide by zero"
- Display: "Se muestra" / "Display is" / "La pantalla muestra"

## Reporte de Bug (Test #4)

El Test #4 está diseñado para fallar intencionalmente: la calculadora muestra "No se puede dividir entre cero" en lugar de "0". Al fallar, se genera automáticamente un PDF en `reports/` con:

- Título, severidad y prioridad
- Pasos detallados para reproducir
- Resultado esperado vs actual
- Captura de pantalla del momento del fallo

Los caracteres especiales del español (á, é, í, ó, ú, ñ) se normalizan automáticamente para compatibilidad con la fuente Helvetica del PDF.

## Stack Tecnológico

| Tecnología | Versión | Uso |
|------------|---------|-----|
| Python | 3.10+ | Lenguaje principal |
| Appium-Python-Client | 1.3.0 | Framework de automatización |
| WinAppDriver | 1.2.1 | Driver de Windows para Appium |
| Selenium WebDriver | 3.141.0 | API de interacción (via Appium) |
| pytest | 9.x | Framework de pruebas |
| fpdf2 | 2.8.x | Generación de reportes PDF |
| Pillow | 12.x | Procesamiento de imágenes |
