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
  - Se escribieron `data/mensaje_osciloscopio.wav` (estéreo: izquierdo NRZ = M1a, derecho FSK 6/12 kHz a 2000 baud = M1b) y `data/mensaje_qam.wav`.
  - 20 figuras en `figures/`.
- **Archivos:** `notebooks/Modulacion_FSK.ipynb`, `notebooks/Modulacion_QAM.ipynb`.

### Entrada 5 — Cuaderno de análisis de mediciones SDR
- **Cómo:** funciones para PSD (Welch), potencia en dBFS, ancho de banda −x dB y OBW 99 %. Se validó con una FSK sintética (1 Msps, 2 kbaud, Δf = ±25 kHz): BW −3 dB = 51.8 kHz, −20 dB = 57.1 kHz, OBW 99 % = 56.6 kHz (TX) y 59.6 kHz (RX con ruido); Carson = 52 kHz.
- **Bug encontrado y corregido:** el suavizado del espectro se hacía en dB con relleno de ceros, lo que subía los extremos y daba BW = 999.8 kHz. Ahora se suaviza en escala lineal.
- **Archivo:** `notebooks/Analisis_mediciones_SDR.ipynb`.

### Entrada 6 — Flujogramas de GNU Radio (generados, sin probar en GNU Radio)
- **Cómo:** `tools/generar_grc.py` escribe los `.grc` (YAML de GRC 3.10) con parámetros en un solo sitio: 2 Msps, 2000 baud, ±25 kHz, 433.92 MHz. Archivos: `grc/tx_fsk.grc` (HackRF), `grc/rx_fsk.grc` (RTL-SDR), `grc/audio_osciloscopio.grc` (M1a/M1b).
- **Verificación hecha:** GNU Radio **no está instalado** en este equipo, así que los `.grc` solo pasaron una comprobación estática (YAML válido, todas las conexiones apuntan a bloques existentes). **Deben abrirse en GNU Radio Companion y revisarse en el laboratorio** (nombres de parámetros de *Osmocom* y de los sumideros QT pueden variar entre versiones).
- **Verificación del diseño en NumPy:** `tools/verificar_cadena_fsk.py` simula TX → canal → RX con los mismos parámetros (filtro, decimación, ganancia del demodulador, bloqueo de DC). Decodifica "COEL" con BER = 0 con error de frecuencia de 0, +15 y −30 kHz y SNR de banda ancha de 30 a −5 dB. No prueba el bloque *Clock Recovery MM* (aquí se muestrea al centro del bit).
- **Cambio de parámetros:** el baud pasó de 10 000 a 2000 para que las relaciones con el audio de 48 kHz sean enteras (24 muestras por bit) y M1a/M1b/M3 se comparen al mismo baud. Carson = 52 kHz.

### Entrada 7 — Primer enlace TX→RX real (HackRF + RTL-SDR, dos computadores)
- **Fecha:** 2026-11-12 · **Configuración:** `tx_fsk.grc` en el PC del HackRF y `rx_fsk.grc` en el del RTL-SDR; 433.92 MHz, 2 Msps, 2000 baud, ±25 kHz. _(Completar: ganancias RF/IF del TX, ganancia del RX, ppm, distancia y antenas.)_
- **Observación:** la constelación del RX muestra dos grupos limpios en −1 y +1 (Q = 0 porque en FSK demodulada se grafica solo la componente real).
- **Decodificación** con `tools/decodificar_bits.py rx_bits.bin COEL`: 1 859 183 bits leídos (proporción de unos = 0.471), 26 684 tramas con sincronía, primer mensaje `'COEL'`, 26 416 tramas sin error (99.0 %), **BER = 1.33·10⁻³**.
- **Alcance de la cifra:** el BER se calcula solo sobre las tramas cuya sincronía se detectó; las tramas con la sincronía dañada no se cuentan, así que es una cota inferior del BER real.
- **Errores en el uso:** el primer intento falló porque `decodificar_bits.py` no estaba en la carpeta del Escritorio; se copió y funcionó.

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
| 7 | 2026-11-12 | | Primer enlace TX→RX y decodificación (BER 1.33e-3) | hecho |
| 8 | | | M1a/M1b osciloscopio | pendiente |
| 9 | | | M2/M3 osciloscopio | pendiente |
| 10 | | | Capturas IQ, potencia y ancho de banda | pendiente |
| 11 | | | Repetir con otra condición (otro baud o desviación) | pendiente |
