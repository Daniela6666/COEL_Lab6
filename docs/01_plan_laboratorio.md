# 01 · Plan paso a paso del laboratorio

Parámetros propuestos (confirmar, ver `00_revision_guia.md` §3): **FSK binaria**, portadora **433.92 MHz**, mensaje de texto ASCII ("COEL" + nombre del grupo), 3 h de laboratorio.

## 0. Reparto de roles (trabajo colaborativo)

| Rol | Responsabilidad | Entrega |
|---|---|---|
| **A · Simulación** | Cuadernos Python/Colab (ya preparados), correr y explicar cada celda | `notebooks/*.ipynb`, `figures/` |
| **B · GNU Radio TX** | Flujograma de transmisión + HackRF | `grc/tx_fsk.grc`, capturas del flujograma |
| **C · GNU Radio RX** | Flujograma de recepción + RTL-SDR, constelación | `grc/rx_fsk.grc` |
| **D · Instrumentación** | Osciloscopio y medición de potencia/ancho de banda; llenar `data/mediciones/` | fotos, CSV |
| **E · Informe** | Bitácora, cuestionario, análisis, conclusiones | `docs/02_bitacora.md`, `docs/03_informe.md` |

Con 3 integrantes: A+E, B+C, D. Cada cambio se registra en la bitácora y se hace *commit* con el rol en el mensaje.

## 1. Antes del laboratorio (≈ 1 h, sin equipos)

1. Leer los temas: CPFSK, MSK, características espectrales, CPM (guía p. 2).
2. Abrir `notebooks/Modulacion_FSK.ipynb` y `Modulacion_QAM.ipynb` en VS Code (extensión *Jupyter*; para Colab, ver README) y ejecutar todas las celdas. Guardar las gráficas.
3. Instalar GNU Radio 3.10 (o 3.7), driver del HackRF (`hackrf_info` debe listar el dispositivo) y del RTL-SDR (Zadig, driver WinUSB). Probar `rtl_test`.
4. Calcular con la regla de Carson el ancho de banda esperado: `B ≈ 2(Δf + Rb/2)`. Con Δf = 25 kHz y Rb = 10 kbaud ⇒ **60 kHz** (valor ya usado en `Analisis_mediciones_SDR`).
5. Preparar los bits: ASCII del mensaje (`COEL` = 01000011 01001111 01000101 01001100).

## 2. Durante el laboratorio

### Fase 1 — Banda base y modulación en GNU Radio (≈ 40 min)

1. **Flujograma TX (Fig. 2 de la guía):** *Vector Source* (bits del mensaje, *Repeat* = Yes) → *Repeat* (interpolación = muestras por bit) → *UChar To Float* → *GFSK Mod* o *Frequency Mod* (sensibilidad = 2π·Δf/fs) → *Throttle* → *QT GUI Time Sink* y *QT GUI Frequency Sink* → *Osmocom Sink* (`hackrf`).
   - `samp_rate` = 2 Msps; frecuencia = 433.92 MHz; ganancia RF = 0 (sin amplificador), IF = 0–16 dB al inicio.
2. **Primer punto de medición con osciloscopio — ver §3, punto M1.**
3. **Flujograma RX:** *Osmocom Source* (`rtl=0`) → *Low Pass Filter* (corte ≈ 40 kHz) → *Quadrature Demod* → *Clock Recovery MM* → *Binary Slicer* → *QT GUI Time Sink / Constellation Sink* y archivo (*File Sink*).
4. Sin transmitir aún: comprobar con el RTL-SDR que el espectro del canal esté libre (*Frequency Sink*).

### Fase 2 — Transmisión y recepción (≈ 50 min)

> **Seguridad y cumplimiento:** transmitir con la potencia mínima, **salida del HackRF por cable coaxial con atenuador de 30–40 dB** hacia el RTL-SDR (nunca conectar la salida del HackRF directa al RTL-SDR: máx. entrada ≈ −10 dBm). Si se usa antena, mantener TX Amp apagado y distancia corta. Confirmar con el profesor la banda permitida.

5. Arrancar primero RX, luego TX. Ajustar ganancias hasta ver dos lóbulos de FSK separados en el espectro.
6. Verificar en la RX: constelación (los puntos se agrupan en 2 clústeres al tomar la salida del discriminador), mensaje decodificado = mensaje transmitido. Registrar BER observada.
7. **Segundo punto de medición con osciloscopio — M3** (mensaje demodulado).
8. Capturar 10 s de IQ en TX y RX (*File Sink*, `complex64`) y guardar en `data/mediciones/tx.cfile`, `rx.cfile` (no se versionan, ver `.gitignore`).

### Fase 3 — Mediciones de potencia y ancho de banda (≈ 30 min)

9. Con `Analisis_mediciones_SDR.ipynb`: potencia (dBFS), ancho de banda −3 dB, −20 dB y OBW 99 % de TX y RX; comparar con Carson.
10. Medidas absolutas: potencia de salida en el conector (analizador/osciloscopio con FFT) — M2 del §3. Anotar en `data/mediciones/mediciones_plantilla.csv`.
11. Repetir con una segunda condición (p. ej. otra desviación Δf o baud) para tener comparación en el informe.

### Fase 4 — Python/Colab (≈ 30 min si ya se trabajó antes)
12. Subir los `.ipynb` a Colab (`colab.research.google.com` → Archivo → Subir) y ejecutar; verificar que no hay errores. Guardar el enlace en el informe.

## 3. Puntos de medición con osciloscopio (qué, dónde y por qué)

La guía exige ver las señales sin modular, moduladas y el mensaje demodulado. El HackRF no tiene salida analógica de la banda base; la visualización depende del ancho de banda (BW) del osciloscopio:

| Punto | Qué se mide | Dónde se conecta | Por qué | Configuración sugerida |
|---|---|---|---|---|
| **M1a** | **Mensaje sin modular** (bits NRZ) | Salida de audio/DAC del PC (*Audio Sink* con el vector de bits como señal) o generador de funciones con la misma secuencia | Pto. 3 de la guía: señal sin modular; referencia de temporización | Escala: 1 V/div; base de tiempo: ≈ 1 bit/div (10 kbaud ⇒ 100 µs/div; 100 baud ⇒ 10 ms/div); disparo por flanco |
| **M1b** | **Señal modulada FSK** antes de transmitir | Misma salida de audio, con FSK a **tonos de audio** (1 kHz / 2 kHz, baud 100) — la versión del cuaderno `Modulacion_FSK` (archivo `data/mensaje_fsk.wav`) | Pto. 3: ver la modulada. Una portadora de 433.92 MHz no es visible en un osciloscopio de < 500 MHz de BW; la versión escalada muestra la misma morfología (dos frecuencias según el bit) | 0.5 V/div; 2 ms/div; mostrar los cambios de frecuencia en cada bit |
| **M1c** *(opcional si BW ≥ 1 GHz)* | Portadora RF modulada a 433.92 MHz | Salida del HackRF con atenuador de 20–30 dB hacia el canal 50 Ω del osciloscopio | Ver la RF real | 50 Ω; 1 µs/div (se ve la portadora, no los bits) |
| **M2** | **Potencia y espectro de TX** | Mismo punto que M1c con función FFT (o analizador de espectro) | Análisis 2: potencia y ancho de banda transmitido en dBm absolutos (el SDR solo da dBFS) | Centro 433.92 MHz, span 200 kHz, RBW 1 kHz |
| **M3** | **Mensaje demodulado** | Salida de audio del PC con la señal recuperada (*Audio Sink* en el flujograma RX tras el *Binary Slicer*) | Pto. 5: comparar el mensaje recuperado con M1a (misma secuencia, retardo y forma) | Mismos ajustes que M1a, canal 2 del osciloscopio para superponer con M1a si se tiene doble canal |

Registrar para cada captura: modelo del osciloscopio, BW, escala vertical/horizontal, sonda (1x/10x), disparo, nombre del archivo de imagen. Guardar en `figures/osciloscopio/`.

**Qué esperar:** M1a es una onda cuadrada NRZ; M1b muestra periodos cortos cuando el bit es 1 (2 kHz) y largos cuando es 0 (1 kHz); M3 reproduce M1a con retardo (latencia de buffers de GNU Radio, típica de decenas a cientos de ms) y ligera distorsión de flancos.

## 4. Parte de Python (ya hecha, solo reproducir)

| Paso de la guía | Celda | Figura generada |
|---|---|---|
| 3–6 Constelación QPSK, AWGN, ruido de fase | `Modulacion_FSK` | `fsk_01…fsk_05` |
| 7–8 Duplicar frecuencia y modular | `Modulacion_FSK` | `fsk_06…fsk_08` |
| 9–10 FSK por concatenación y `bfsk_modulate` | `Modulacion_FSK` | `fsk_09`, `fsk_10` |
| 8-QAM pasos 1–7 | `Modulacion_QAM` | `qam_01…qam_07` |
| Demodulación 8-QAM y BER | `Modulacion_QAM` | `qam_08` |
| Exportación .wav | ambos | `data/mensaje_*.wav` |

## 5. Cuestionario — plano de eficiencia de ancho de banda

Esquema de la deducción (verificar con Artés y Pérez, cap. 9, p. 567):

1. Capacidad de Shannon: `C = B·log2(1 + S/N)`. Para operar a tasa `Rb ≤ C`, eficiencia espectral `η = Rb/B ≤ log2(1 + S/N)`.
2. Con `S = Eb·Rb`, `N = N0·B`: `S/N = (Eb/N0)·(Rb/B) = (Eb/N0)·η`.
3. En el límite `Rb = C`: `η = log2(1 + η·Eb/N0)`, de donde
   **`Eb/N0 = (2^η − 1)/η`** (frontera de capacidad del plano η vs. Eb/N0).
4. Para `η → 0`: `Eb/N0 → ln 2 = −1.59 dB` (límite de Shannon).
5. Puntos de las modulaciones: `η = log2(M)/(1+α)` con roll-off α (para M-QAM y M-PSK) y para FSK ortogonal `η = 2·log2(M)/M`. Se ubican al `Pb = 10⁻⁵`, con `Eb/N0` requerido por cada esquema.

## 6. Análisis y conclusiones (guion)

1. **Ventajas/aplicaciones de FSK:** envolvente constante (amplificadores clase C), robustez al ruido y al desvanecimiento, demodulación no coherente simple; usada en telemetría ISM, módems, pagers, mandos a distancia, LoRa/GFSK (Bluetooth). Contrastar con 8-QAM: mayor eficiencia espectral, menor robustez, necesita linealidad y recuperación coherente.
2. **Mediciones:** tabla TX/RX de potencia, BW −3 dB, −20 dB y OBW; comparar con Carson; explicar diferencias (ruido de piso, filtro del RTL-SDR de ≈ 2.4 MHz, ganancias).
3. **Conclusiones:** relacionar simulación (efecto del ruido en la constelación, SER/BER) con lo medido.

## 7. Cronograma

| Tiempo | Actividad |
|---|---|
| Antes del lab | Pasos de §1 |
| 0:00–0:40 | Fase 1 |
| 0:40–1:30 | Fase 2 |
| 1:30–2:00 | Fase 3 |
| 2:00–2:30 | Fase 4 y repetición de mediciones |
| 2:30–3:00 | Orden de archivos, *commit*, revisión cruzada |
| Después | Informe (`03_informe.md`) |
