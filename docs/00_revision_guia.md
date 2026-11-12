# 00 · Revisión de la guía (Laboratorio No. 6 COEL)

Fuente: `guia/Guía laboratorio modulacion digital COEL.pdf` (16 páginas). Revisada el 2026-11-12.

## 1. Qué pide la guía

**Título:** Modulaciones digitales mediante SDR (TX con HackRF One, RX con NooElec RTL-SDR) y simuladas en Python.

| Bloque | Contenido | Entregable |
|---|---|---|
| Parte 1 (SDR, GNU Radio) | Elegir una técnica (FSK, MSK, GMSK, BPSK, M-PSK, M-QAM), portadora dentro del rango del HackRF y del receptor; modular un mensaje (nota, imagen o texto), transmitir, recibir, demodular, ver constelación | Flujogramas + capturas |
| Parte 1, pto. 3 y 5 | **Osciloscopio:** señal sin modular y modulada *antes de transmitir*; mensaje demodulado | Fotos/capturas del osciloscopio |
| Parte 2 (Python/Colab) | Cuaderno `Modulación_FSK`: constelación QPSK, ruido AWGN, ruido de fase, FSK (duplicar frecuencia, modulación, concatenación, `bfsk_modulate`); luego repetir los 10 pasos para una QAM (8-QAM o 16-QAM) | Cuadernos con gráficas |
| Cuestionario | Deducir la ecuación del plano de eficiencia de ancho de banda (Artés y Pérez, *Comunicaciones digitales*, cap. 9, p. 567) | Deducción |
| Análisis | (1) Ventajas y aplicaciones de la técnica elegida; (2) **medir potencia y ancho de banda TX y RX**; (3) conclusiones | Informe en la bitácora |
| Recomendaciones | Convertir el archivo a **.wav**; escribir cifras completas (sin abreviaturas) | — |
| Tiempo | 3 horas de laboratorio | — |

**Equipos:** HackRF One (solo hay 2 módulos, se solicita en el laboratorio), RTL-SDR asignado a cada grupo, osciloscopio, PC con GNU Radio 3.10 o 3.7 (de preferencia Windows 10).

**Tips de GNU Radio de la guía:** HackRF en Osmocom *Source* usa el argumento de dispositivo `hackrf=0`, en *Sink* `hackrf`; error `xterm is missing` es inofensivo; si no hay gráficas, *Options → Generate Options → QT GUI*; problemas de audio → revisar muestreo, diezmado, ganancias; drivers del fabricante; librerías wxPython/QT con `pip`.

**Figuras 1–5 (pp. 3–5):** ASK (File Source → Complex to Mag → Threshold → Scope), FSK/GFSK (Vector Source → Repeat → UChar to Float → Packet Encoder → GFSK Mod → Virtual Sink; RX: Virtual Source → GFSK Demod → Packet Decoder → Time Sink), PSK y QAM (Random Source → Short To Float/Throttle → QAM Mod → Constellation Sink).

## 2. Errores y ambigüedades de la guía (y cómo se resolvieron)

| # | Dónde | Problema | Solución adoptada |
|---|---|---|---|
| 1 | Parte 2, nombre del cuaderno | Se llama `Modulación_FSK` pero luego se pide repetirlo para QAM | Dos cuadernos: `Modulacion_FSK` y `Modulacion_QAM` (sin tilde, para evitar problemas de rutas) |
| 2 | Pasos 3–6 | Ejes "Sin(wc·t)" en X y "Cos(wc·t)" en Y: están invertidos (X = I = cos, Y = Q = sin) | Ejes rotulados **I** y **Q** |
| 3 | Paso 3 | Comentario "rango [0,4]": `randint(0,4)` da {0,1,2,3} | Comentario corregido |
| 4 | Paso 9 FSK | `linspace(0, .5, samp_rate*len_in_sec)` da 1000 muestras en 0.5 s ⇒ fs real de 2000 Hz | `int(samp_rate*0.5)` muestras |
| 5 | Paso 10 `bfsk_modulate` | `baud` se usa como *segundos por bit*; `samples_per_bit` es `float` y `np.linspace` lo rechaza en NumPy reciente; `np.append` en bucle es O(n²) | `baud` real (bit/s), entero, `np.concatenate`. Con `baud=1` reproduce el ejemplo |
| 6 | QAM paso 3–4 | Solo grafica 2 símbolos con leyenda "Magnitud 2.62/1.08" (no corresponden a las amplitudes 0.765 y 1.848); `noise_power=0.9` borra la constelación | Se grafican todos los símbolos de ambos anillos y se barre `noise_power` (0.05, 0.3, 0.9) |
| 7 | QAM paso 5 | Comentario dice "QPSK"; es QAM | Corregido |
| 8 | QAM paso 7 | El diccionario solo asigna **amplitud**; no codifica fase, por lo que 8 símbolos colapsan en 2 ondas distintas; usa `input()` (bloquea la ejecución automática) | Se conserva la versión de la guía y se añade la 8-QAM completa (1 bit → anillo, 2 bits Gray → fase), con modulador, demodulador coherente y BER |
| 9 | QAM paso 2 | Texto dice "cada símbolo con dos amplitudes" pero se grafican 2 anillos de 4 puntos: es la 8-QAM tipo *star* (potencia media = 2.0, verificada) | Documentado |
| 10 | Parte 1, pto. 3 | Pide ver la señal **modulada** en el osciloscopio "antes de transmitirla", pero a una portadora de cientos de MHz solo se ve con un osciloscopio de ancho de banda ≥ 500 MHz | Ver `01_plan_laboratorio.md` §3: se observan banda base y una FI/audio escalada; la portadora RF se verifica con espectro del SDR |
| 11 | Entregable | "Informe en la bitácora" sin formato | Plantilla en `docs/03_informe.md` |

## 3. Decisiones que el grupo debe confirmar

1. **Técnica de la Parte 1:** se propone **FSK** (los diagramas y el cuaderno de la guía son de FSK, y es la más sencilla de demodular con RTL-SDR).
2. **Técnica QAM de la Parte 2:** se propone **8-QAM** (usa los datos de la guía).
3. **Portadora:** se propone **433.92 MHz** (banda ISM; dentro del HackRF 1 MHz–6 GHz y del RTL-SDR ≈ 24–1766 MHz). Confirmar con el profesor.
4. **Modelo/ancho de banda del osciloscopio** disponible (define cómo se ve la señal, §3 del plan).
5. **Versión de GNU Radio** en los PC del laboratorio.
