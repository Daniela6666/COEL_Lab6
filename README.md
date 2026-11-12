# Lab 6 COEL — Modulaciones digitales (SDR + Python)

Escuela Colombiana de Ingeniería Julio Garavito · Ingeniería Electrónica.
Guía: `guia/Guía laboratorio modulacion digital COEL.pdf`.

| Carpeta | Contenido |
|---|---|
| `docs/00_revision_guia.md` | Resumen de la guía y errores encontrados |
| `docs/01_plan_laboratorio.md` | Plan paso a paso, roles y puntos de osciloscopio |
| `docs/02_bitacora.md` | Bitácora (qué, cómo, resultado) |
| `docs/03_informe.md` | Plantilla del informe |
| `notebooks/` | `Modulacion_FSK`, `Modulacion_QAM`, `Analisis_mediciones_SDR` (.ipynb, compatibles con Colab) |
| `grc/` | Flujogramas de GNU Radio (TX HackRF, RX RTL-SDR, audio para osciloscopio) |
| `tools/` | `generar_grc.py` (regenera los `.grc`) y `verificar_cadena_fsk.py` (simula la cadena TX→RX) |
| `figures/` | Gráficas generadas por los cuadernos (y `osciloscopio/` para fotos) |
| `data/` | `.wav` de los mensajes; `mediciones/` para capturas IQ y CSV |

## Cómo ejecutar
**VS Code local:** `py -m pip install -r requirements.txt`, abrir un `.ipynb` y elegir el kernel de Python.
**Colab desde VS Code:** instalar las extensiones *Jupyter* y *Google Colab* y elegir *Colab* como kernel; o subir el `.ipynb` en <https://colab.research.google.com>. En Colab el cuaderno corre igual (no guarda figuras, solo las muestra).

## Flujo colaborativo
Rama por integrante (`rol-nombre`), un *commit* por entrada de bitácora, revisión cruzada antes de unir a `main`. Las capturas IQ grandes (`*.cfile`) no se versionan.
