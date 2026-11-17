# 04 · Guía para la exposición del Laboratorio 6

Tiempo sugerido: **10–12 minutos** + preguntas. Mensaje central en una frase:

> *"Transmitimos el texto COEL por radio con un HackRF, lo recibimos con un RTL-SDR en otro computador, lo recuperamos con un BER de 1.3·10⁻³, y antes simulamos en Python cómo el ruido daña estas modulaciones."*

---

## 1. Qué tienen y qué falta (sean honestos con el profesor)

| Pieza | Estado | Dónde está |
|---|---|---|
| Simulación Python FSK y 8-QAM | ✅ hecha y ejecutada | `notebooks/Modulacion_FSK.ipynb`, `Modulacion_QAM.ipynb`, figuras en `figures/` |
| Flujogramas GNU Radio TX/RX | ✅ funcionando (RX y enlace probados) | `grc/tx_fsk.grc`, `grc/rx_fsk.grc` |
| Constelación recibida | ✅ foto | su captura de pantalla |
| Mensaje decodificado "COEL", BER = 1.33·10⁻³ | ✅ captura de la terminal | su captura + `docs/02_bitacora.md` entrada 7 |
| Fotos del osciloscopio (M1a, M1b, M3) | ⚠️ **verificar si ya las tienen** | `figures/osciloscopio/` |
| Potencia y ancho de banda medidos (TX y RX) | ⚠️ **verificar** (necesita `tx.cfile` y `rx.cfile`) | `notebooks/Analisis_mediciones_SDR.ipynb` |
| Cuestionario (plano de eficiencia) | 🟡 esquema listo | `docs/01_plan_laboratorio.md` §5 |
| Conclusiones | 🟡 guion listo | §7 de esta guía |

**Regla:** si algo no está medido, no lo inventen. Digan "está planteado, el resultado teórico es X y falta medirlo".

---

## 2. Qué abrir ANTES de entrar (checklist de 10 minutos)

1. **Todo precargado, nada que escribir en vivo** salvo el decodificador.
2. Pestañas/ventanas abiertas, en este orden:
   1. `figures/` en el Explorador (imágenes para mostrar rápido).
   2. `Modulacion_FSK.ipynb` y `Modulacion_QAM.ipynb` ya ejecutados (se ven las gráficas sin correr nada).
   3. GNU Radio con `tx_fsk.grc` y `rx_fsk.grc` abiertos (solo para enseñar los bloques).
   4. Una terminal PowerShell en la carpeta donde está `rx_bits.bin` y `decodificar_bits.py`.
   5. La captura de la constelación y la de la terminal con "COEL".
   6. El repositorio: <https://github.com/Daniela6666/COEL_Lab6>
3. **Demostración en vivo segura:** ejecuten el decodificador sobre el `rx_bits.bin` **ya grabado**:
   ```bash
   py decodificar_bits.py rx_bits.bin COEL
   ```
   No dependen de que el radio funcione ese día. Si el profesor deja y hay equipos, transmitir en vivo es un extra, no el plan base.
4. Lleven las capturas también en un USB/nube por si falla el computador.

---

## 3. Orden de la exposición (qué mostrar y qué decir)

| # | Min | Mostrar | Decir (simple) |
|---|---|---|---|
| 1 | 1 | Título y objetivo | "Hicimos dos cosas: simular modulaciones digitales en Python y transmitir una de ellas con radio definida por software." |
| 2 | 3 | Notebook FSK: `fsk_01…05` (QPSK con ruido) | "Una modulación digital manda bits como puntos en un plano. El ruido ensancha los puntos y, si es mucho, un punto cae en la zona del vecino: error." |
| 3 | | `fsk_06…10` | "FSK es mandar un bit con una frecuencia y el otro con otra. Aquí 8 Hz es 0 y 16 Hz es 1. Construimos la señal juntando trozos de seno." |
| 4 | | Notebook QAM: `qam_01`, `qam_03`, `qam_07`, `qam_08` | "8-QAM usa dos anillos de 4 puntos: 8 símbolos, 3 bits por símbolo. Más bits por símbolo cabe en menos ancho de banda, pero el ruido la daña más fácil (anillos más juntos)." |
| 5 | 3 | `grc/tx_fsk.grc` | "Transmisor: bits del mensaje → cada bit dura 1000 muestras → modulador de frecuencia → HackRF. Frecuencia 433.92 MHz, 2000 baud, ±25 kHz." |
| 6 | | `grc/rx_fsk.grc` | "Receptor: RTL-SDR → filtro → demodulador (convierte frecuencia en voltaje) → quita el offset de frecuencia → reconoce los bits." |
| 7 | 2 | Captura de la constelación | "Dos grupos en −1 y +1: son los dos bits. Están separados y compactos, por eso casi no hay errores." |
| 8 | | Terminal con el decodificador ("COEL", BER) | "El mensaje llegó: COEL. De 26 684 tramas, 26 416 sin error (99 %). BER ≈ 1 bit malo de cada 750." |
| 9 | 1–2 | Fotos del osciloscopio (si las tienen) | "M1a el mensaje, M1b la FSK escalada a audio, M3 lo recuperado." |
| 10 | 1 | Potencia y ancho de banda | "Teóricamente 52 kHz (Carson). Medido: … (solo si lo tienen)." |
| 11 | 1 | Conclusiones (§7) | — |

---

## 4. Explicación muy simple de todo

- **Modulación digital:** poner bits en una onda. Cambiar *frecuencia* (FSK), *fase* (PSK) o *amplitud y fase* (QAM).
- **FSK:** un bit 0 y un bit 1 son dos frecuencias distintas. Como cantar una nota grave para 0 y una aguda para 1.
- **QAM:** combinar amplitud y fase. La constelación son los puntos posibles.
- **SDR (radio definida por software):** radio donde el procesamiento (filtros, modulación) lo hace el computador, no circuitos fijos. HackRF **transmite**; RTL-SDR (NooElec) **solo recibe**.
- **GNU Radio:** programa de bloques para construir esos procesamientos.
- **Constelación:** gráfico de los valores recibidos. Cada grupo es un símbolo. Más ruido = grupos más grandes.
- **Ruido AWGN:** ruido "blanco" que se suma. **Ruido de fase:** el oscilador tiembla y gira los puntos.
- **Baud (2000):** símbolos por segundo. En FSK binaria = bits por segundo.
- **Desviación (±25 kHz):** cuánto se aleja la frecuencia de la portadora para cada bit.
- **Ancho de banda (Carson):** `B ≈ 2(Δf + baud/2) = 2(25 000 + 1 000) = 52 kHz`.
- **Portadora 433.92 MHz:** banda ISM, de uso libre de baja potencia, dentro del rango del HackRF y del RTL-SDR.
- **Preámbulo y sincronía:** el mensaje va precedido de `0xAA 0xAA 0x2D 0xD4`. El preámbulo alterna 1010… para que el receptor se ajuste; la sincronía marca dónde empieza el texto.
- **BER:** fracción de bits recibidos mal. 1.33·10⁻³ ≈ 1 de cada 750.
- **ppm / bloqueo de DC:** los osciladores del HackRF y del RTL-SDR no son idénticos; esa diferencia corre la frecuencia. El filtro DC Blocker del receptor la compensa.
- **Osciloscopio:** no se ve la portadora (433 MHz es muy alta para el osciloscopio del laboratorio), por eso se muestra una FSK escalada a audio (6 kHz/12 kHz) con los mismos bits.

---

## 5. Preguntas probables y respuestas cortas

**¿Por qué FSK?** Es simple, resistente al ruido y no necesita recuperar la fase de la portadora. Es la que usan mandos, módems y LoRa/GFSK.

**¿Por qué la constelación tiene solo dos puntos y Q = 0?** Porque la FSK demodulada es un número real (±1); no hay componente de cuadratura. La graficamos con Q = 0.

**¿Qué significa el BER de 1.33·10⁻³?** Cerca de 1 bit erróneo cada 750. Solo cuenta las tramas donde se encontró la sincronía, así que el real puede ser algo mayor.

**¿Cómo saben que lo recibido viene de su transmisor?** Se vio el mensaje exacto "COEL" con preámbulo en miles de tramas. La prueba definitiva es apagar el TX (debe desaparecer la sincronía) o transmitir otra palabra (`py tools/generar_grc.py HOLA`) y recibir esa.

**¿Por qué el RTL-SDR solo recibe y el HackRF transmite?** El RTL-SDR es un receptor de TV adaptado, no tiene transmisor. El HackRF es *half-duplex*: transmite o recibe.

**¿Por qué 2000 baud y ±25 kHz?** Con 2 Msps hay 1000 muestras por bit y con audio de 48 kHz hay 24 muestras por bit (números enteros, fácil de comparar). El índice de modulación es h = 2Δf/baud = 25, muy ancho, lo que da margen frente al error de frecuencia del RTL-SDR.

**¿Por qué usaron atenuador / antenas cortas / ganancia baja?** El RTL-SDR se satura con señales fuertes (máx. ≈ −10 dBm) y hay que transmitir con la mínima potencia por norma. (Digan solo lo que realmente hicieron con el montaje.)

**¿Qué diferencia hay entre simulación y práctica?** En la simulación el ruido y la fase se ponen a mano; en la práctica aparecen el error de frecuencia entre equipos, la saturación de ganancias y el sincronismo.

**¿Qué es el ruido de fase y qué le hace a QPSK/QAM?** Gira los puntos alrededor del origen; puede mandarlos al cuadrante de otro símbolo. Afecta más a la QAM por tener símbolos de distinta amplitud muy juntos.

**¿Qué modulación elegirían y por qué?** FSK/GFSK si se prioriza robustez, bajo costo y potencia; QAM si se prioriza velocidad y se tiene buena señal (módems, Wi-Fi, TV digital).

**Cuestionario: ¿qué es el plano de eficiencia de ancho de banda?** Gráfico de η = Rb/B (bit/s por Hz) contra Eb/N0. La frontera de Shannon es `Eb/N0 = (2^η − 1)/η`; cuando η→0 llega a −1.59 dB. Cada modulación es un punto: M-QAM tiene η = log₂M/(1+α) y FSK ortogonal η = 2log₂M/M (la FSK gasta ancho de banda a cambio de requerir menos Eb/N0).

**¿Por qué corrigieron el código de la guía?** Porque tenía errores: `bfsk_modulate` no corre en NumPy actual, los ejes I/Q estaban invertidos, la tasa de muestreo del paso 9 estaba mal y el 8-QAM solo codificaba amplitud (la lista completa está en `docs/00_revision_guia.md`).

**¿Qué problemas tuvieron?** Drivers WinUSB del RTL-SDR (se resolvió con Zadig), el HackRF ya lo reconocía Windows, y un error `NameError` al generar el archivo de datos en GNU Radio (se corrigió usando `self`). Contarlo bien suma: muestra trabajo real.

---

## 6. Archivos que deben llevar / mostrar

**Carpeta del repositorio** `Lab6_Modulacion` (también en GitHub):
1. `notebooks/Modulacion_FSK.ipynb`, `Modulacion_QAM.ipynb` (ejecutados).
2. `notebooks/Analisis_mediciones_SDR.ipynb`.
3. `grc/tx_fsk.grc`, `grc/rx_fsk.grc`, `grc/audio_osciloscopio.grc`.
4. `docs/00_revision_guia.md`, `01_plan_laboratorio.md`, `02_bitacora.md`, `03_informe.md`.
5. `figures/` (20 imágenes de simulación).
6. `data/mensaje_osciloscopio.wav`.

**De la práctica (fuera del repo o por agregar):** captura de la constelación, captura del decodificador, `rx_bits.bin`, `tx.cfile` y `rx.cfile` si los lograron, `datos_de_la_prueba.txt`, fotos del osciloscopio.

---

## 7. Conclusiones (para decir al cierre)

1. Se logró transmitir y recibir por radio un mensaje FSK de texto y recuperarlo con BER ≈ 1.3·10⁻³.
2. La simulación en Python mostró cómo el ruido AWGN y el ruido de fase ensanchan la constelación hasta producir errores de decisión; en la práctica se vio lo mismo en la separación de los dos grupos.
3. FSK sacrifica ancho de banda (≈ 52 kHz para 2 kbit/s) a cambio de robustez; la QAM es más eficiente espectralmente pero más sensible al ruido.
4. Las diferencias entre equipos (error de frecuencia entre osciladores) deben compensarse en el receptor.
5. Trabajo futuro: medir potencia y ancho de banda en TX y RX con más condiciones de ganancia y distancia.

---

## 8. Si algo falla mañana (plan B)

| Falla | Qué hacer |
|---|---|
| El radio o GNU Radio no arranca | Mostrar las capturas y ejecutar el decodificador sobre `rx_bits.bin` grabado |
| No funciona `py` | Probar `python` |
| El notebook no corre | Mostrar las figuras de `figures/` o abrir el notebook ya ejecutado en GitHub (se ve con gráficas) |
| No hay fotos del osciloscopio | Mostrar `fsk_11_mensaje_audio.png` (lo que debería verse) y decir que se mide con `audio_osciloscopio.grc` |
| No hay mediciones de potencia/ancho de banda | Mostrar `sdr_01_espectro_tx_rx.png` (validado con señal sintética: BW −3 dB = 51.8 kHz vs. Carson 52 kHz) y decir que falta medir en radio |
