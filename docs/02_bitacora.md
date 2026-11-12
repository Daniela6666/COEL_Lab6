# 02 · Bitácora de trabajo

Formato: fecha · quién · qué se hizo · cómo · resultado · archivos. Una entrada por actividad; se hace un *commit* por entrada.

## 2026-11-12 · Preparación (asistida por Claude Code)

### Entrada 1 — Revisión de la guía
- **Cómo:** la guía es un PDF de 16 páginas. Se extrajo el texto con `pypdf` y se revisaron las figuras de las páginas 3–5 renderizadas con `pymupdf`.
- **Resultado:** resumen de requisitos y 11 observaciones/errores de la guía en `docs/00_revision_guia.md`.

### Entrada 2 — Plan del laboratorio
- **Cómo:** se organizó en roles, fases, puntos de medición con osciloscopio (M1–M3) y cuestionario.
- **Resultado:** `docs/01_plan_laboratorio.md`.
- **Pendiente de confirmar:** técnica, portadora, ancho de banda del osciloscopio, versión de GNU Radio.

### Entrada 3 — Estructura del repositorio y entorno
- **Cómo:** carpetas `guia/ docs/ notebooks/ figures/ data/`; `git init`, rama `main`. Python 3.12.10, `numpy 2.5.4`, `scipy 1.18.1`, `matplotlib 3.11.2`, `jupyterlab`.
- **Archivos:** `README.md`, `.gitignore`, `requirements.txt`.

### Entrada 4 — Cuadernos Python (Parte 2 de la guía)
- **Cómo:** se transcribió el código de la guía a `.ipynb` (formato compatible con Colab), con comentarios por línea, corrigiendo los errores listados en `00_revision_guia.md` §2 (marcados **[CORRECCIÓN]** en las celdas). Se ejecutó con `jupyter nbconvert --execute` para validar y guardar salidas. Semilla `np.random.seed(42)`.
- **Resultados verificados:**
  - SER de QPSK vs. `noise_power`: 0.01→0.0000, 0.1→0.0013, 0.5→0.150, 1→0.297, 2→0.420.
  - 8-QAM: potencia media de la constelación = 2.0002; BER del modulador/demodulador coherente: σ=0→0, 5→0.0017, 10→0.0675, 20→0.223, 40→0.350.
  - Se escribieron `data/mensaje_fsk.wav` (tonos 1 kHz/2 kHz, 100 baud) y `data/mensaje_qam.wav`, que se usan como fuente en el osciloscopio (M1b).
  - 20 figuras en `figures/`.
- **Archivos:** `notebooks/Modulacion_FSK.ipynb`, `notebooks/Modulacion_QAM.ipynb`.

### Entrada 5 — Cuaderno de análisis de mediciones SDR
- **Cómo:** funciones para PSD (Welch), potencia en dBFS, ancho de banda −x dB y OBW 99 %. Se validó con una FSK sintética (1 Msps, 10 kbaud, Δf = ±25 kHz): BW −3 dB = 52.0 kHz, −20 dB = 65.4 kHz, OBW 99 % = 73.2 kHz (TX) y 78.6 kHz (RX con ruido); Carson = 60 kHz.
- **Bug encontrado y corregido:** el suavizado del espectro se hacía en dB con relleno de ceros, lo que subía los extremos y daba BW = 999.8 kHz. Ahora se suaviza en escala lineal.
- **Archivo:** `notebooks/Analisis_mediciones_SDR.ipynb`.

## Plantilla para entradas del laboratorio

```
### Entrada N — título
- Fecha/hora · Integrante:
- Objetivo:
- Configuración (equipo, parámetros, flujograma):
- Procedimiento:
- Resultado / medición (valores con unidades, cifras completas):
- Archivos (fotos, .grc, .cfile):
- Observaciones:
```

## Registro del laboratorio (completar)

| Entrada | Fecha | Integrante | Actividad | Estado |
|---|---|---|---|---|
| 6 | | | Flujograma TX GNU Radio | pendiente |
| 7 | | | Flujograma RX GNU Radio | pendiente |
| 8 | | | M1a/M1b osciloscopio | pendiente |
| 9 | | | Transmisión y recepción | pendiente |
| 10 | | | M2/M3 osciloscopio | pendiente |
| 11 | | | Potencia y ancho de banda | pendiente |
