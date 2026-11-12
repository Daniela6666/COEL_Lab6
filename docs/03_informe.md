# Informe — Laboratorio 6: Modulaciones digitales mediante SDR y Python

**Escuela Colombiana de Ingeniería Julio Garavito · Ingeniería Electrónica · COEL**
**Integrantes:** _(completar)_ · **Fecha:** _(completar)_ · **Técnica:** FSK (SDR) y 8-QAM (simulación)

## 1. Objetivos
Transmitir y recibir una señal modulada digitalmente con SDR; simular FSK y 8-QAM en Python/Colab; familiarizarse con GNU Radio.

## 2. Marco teórico (resumen propio)
_CPFSK, MSK, espectro de CPFSK (regla de Carson), CPM, desempeño en AWGN. Escribir con sus palabras y citar la guía y a Artés y Pérez._

## 3. Metodología
### 3.1 Simulación en Python (Colab)
Resumen de `Modulacion_FSK` y `Modulacion_QAM` (ver bitácora, entradas 4–5). Figuras: `figures/fsk_*.png`, `figures/qam_*.png`. Enlace Colab: _(completar)_.

### 3.2 Implementación SDR
- Portadora: _(completar)_ MHz; muestreo: _(completar)_ Msps; baud: _(completar)_; desviación: _(completar)_ Hz.
- Flujograma TX/RX (capturas): _(insertar)_.
- Montaje y atenuación: _(completar)_.

### 3.3 Mediciones con osciloscopio
Tabla de capturas M1a, M1b, M1c, M2, M3 con configuración (ver `01_plan_laboratorio.md` §3).

## 4. Resultados
### 4.1 Simulaciones
- Constelación QPSK sin ruido, con AWGN, con ruido de fase y ambos (figuras fsk_01–fsk_05). Discusión: a partir de `noise_power ≈ 0.5` la SER supera 15 %.
- FSK: duplicación de frecuencia, modulación `01`, `bfsk_modulate("010110")`.
- 8-QAM: constelación, efecto del ruido y de la fase, onda modulada, BER vs. ruido.

### 4.2 SDR
| Magnitud | TX | RX |
|---|---|---|
| Potencia [dBFS] | | |
| Potencia [dBm] (analizador) | | |
| BW −3 dB [kHz] | | |
| BW −20 dB [kHz] | | |
| OBW 99 % [kHz] | | |
| Carson teórico [kHz] | | |

Constelación recibida, mensaje transmitido vs. recuperado, BER observada.

## 5. Cuestionario
Deducción de la ecuación del plano de eficiencia de ancho de banda (esquema en `01_plan_laboratorio.md` §5): `Eb/N0 = (2^η − 1)/η`. _Completar con la deducción del libro (Artés y Pérez, p. 567)._

## 6. Análisis
1. Ventajas y aplicaciones del esquema elegido.
2. Potencia y ancho de banda TX/RX: comparación con la teoría y causas de diferencias.
3. Diferencias entre la simulación y la práctica.

## 7. Conclusiones
_(completar)_

## 8. Bibliografía
- Guía de laboratorio No. 6, COEL (ECI).
- Artés, A. y Pérez, F., *Comunicaciones digitales*, Pearson-Prentice Hall.
- GNU Radio, <https://www.gnuradio.org>; *Guided Tutorial Introduction*, <https://wiki.gnuradio.org/index.php/Guided_Tutorial_Introduction>.
- Laufer, C., *The Hobbyist's Guide to the RTL-SDR*, 3.ª ed.
