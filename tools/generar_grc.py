"""Genera los flujogramas de GNU Radio Companion (formato YAML de GRC 3.10) en grc/.

Uso:  py tools/generar_grc.py [MENSAJE]      (por defecto COEL; solo cambia el contenido de tx_fsk.grc)
Los parámetros están arriba para cambiarlos en un solo sitio (deben coincidir con tools/verificar_cadena_fsk.py).
"""
import os, sys, yaml

GRC_VERSION = "3.10.9.2"
OUT = os.path.join(os.path.dirname(__file__), "..", "grc")

# ---------------- parámetros del enlace ----------------
SAMP_RATE = 2_000_000
BAUD = 2_000
DEV = 25_000
FREQ = 433_920_000
MENSAJE = sys.argv[1] if len(sys.argv) > 1 else "COEL"   # py tools/generar_grc.py HOLA  (solo ASCII)
assert MENSAJE.isascii() and 1 <= len(MENSAJE) <= 32, "Use 1 a 32 caracteres ASCII (sin tildes ni ñ)"
DATOS = bytes([0xAA, 0xAA, 0x2D, 0xD4]) + MENSAJE.encode()           # preámbulo + sincronía + texto
BITS = [(b >> i) & 1 for b in DATOS for i in range(7, -1, -1)]
# -------------------------------------------------------

ST = dict(bus_sink=False, bus_source=False, bus_structure=None, rotation=0, state="enabled")

def blk(_n, id_, x, y, **params):
    return dict(name=_n, id=id_, parameters={k: str(v) for k, v in params.items()},
                states=dict(ST, coordinate=[x, y]))

def opciones(id_, titulo):
    return dict(parameters=dict(
        author="", catch_exceptions="True", category="[GRC Hier Blocks]", cmake_opt="", comment="",
        copyright="", description="", gen_cmake="On", gen_linking="dynamic", generate_options="qt_gui",
        hier_block_src_path=".:", id=id_, max_nouts="0", output_language="python", placement="(0,0)",
        qt_qss_theme="", realtime_scheduling="", run="True", run_command="{python} -u {filename}",
        run_options="prompt", sizing_mode="fixed", thread_safe_setters="", title=titulo,
        window_size="(1000,1000)"),
        states=dict(ST, coordinate=[8, 8]))

def escribir(nombre, id_, titulo, bloques, conexiones):
    nombres = {b["name"] for b in bloques}
    for a, _, b, _ in conexiones:                                       # comprobación estática de conexiones
        assert a in nombres and b in nombres, (a, b)
    doc = dict(options=opciones(id_, titulo), blocks=bloques,
               connections=[[a, str(pa), b, str(pb)] for a, pa, b, pb in conexiones],
               metadata=dict(file_format=1, grc_version=GRC_VERSION))
    ruta = os.path.join(OUT, nombre)
    with open(ruta, "w", encoding="utf8", newline="\n") as f:
        f.write(yaml.safe_dump(doc, sort_keys=False, allow_unicode=True))
    print("escrito", os.path.normpath(ruta))

def variables(x0=200):
    """Variables comunes."""
    return [
        blk("samp_rate", "variable", x0, 12, value=SAMP_RATE, comment="Muestreo SDR [Hz]"),
        blk("baud", "variable", x0+170, 12, value=BAUD, comment="Símbolos por segundo"),
        blk("dev", "variable", x0+300, 12, value=DEV, comment="Desviación de frecuencia ± [Hz]"),
        blk("freq", "variable", x0+430, 12, value=FREQ, comment="Portadora [Hz]"),
        blk("sps", "variable", x0+600, 12, value="int(samp_rate/baud)", comment="Muestras por bit"),
    ]

DURACION_CAPTURA = 5   # s de IQ que se guardan en tx.cfile / rx.cfile (a 2 Msps son 16 MB/s: 5 s = 80 MB)

def registro(lado, archivos, imports="", x0=200, y0=700):
    """Bloques comunes de registro: carpeta de la prueba, duración de captura, datos_de_la_prueba.txt.
    La carpeta es ~/lab6_pruebas/<nombre_prueba> (se crea sola). Cambiar nombre_prueba en cada corrida."""
    codigo = f'''def _valores():
    return (f"  Ganancia RF [dB]: {{tb.rf_gain}}\\n"
            f"  Ganancia IF [dB]: {{tb.if_gain}}\\n"
            f"  Ganancia BB [dB]: {{tb.bb_gain}}\\n"
            f"  Correccion de frecuencia [ppm]: {{tb.ppm}}\\n")
_inicio = _valores()
def _guardar_datos():
    with open(os.path.join(tb.carpeta, "datos_de_la_prueba.txt"), "w", encoding="utf-8") as f:
        f.write("Prueba: " + str(tb.nombre_prueba) + "\\n")
        f.write("Lado: {lado}\\n")
        f.write("Fecha y hora de inicio: " + _t0 + "\\n")
        f.write(f"Frecuencia de muestreo [Hz]: {{tb.samp_rate}}\\n")
        f.write(f"Frecuencia central [Hz]: {{tb.freq}}\\n")
        f.write(f"Baud: {{tb.baud}}\\n")
        f.write(f"Desviacion de frecuencia [Hz]: {{tb.dev}}\\n")
        f.write("Valores al iniciar:\\n" + _inicio)
        f.write("Valores al terminar (los deslizadores pueden haber cambiado):\\n" + _valores())
        f.write(f"Duracion de la captura IQ [s]: {{tb.duracion_captura}}\\n")
        f.write("Archivos: {archivos}\\n")
_t0 = time.strftime("%Y-%m-%d %H:%M:%S")
_guardar_datos()
atexit.register(_guardar_datos)
print("Archivos de la prueba en:", tb.carpeta)'''
    codigo = codigo.replace("tb.", "self.")   # GRC ejecuta el snippet como snipfcn(self): el flujograma se llama 'self'
    return [
        blk("nombre_prueba", "variable", x0, y0, value='"prueba01"',
            comment="CAMBIAR en cada corrida para no sobrescribir los archivos"),
        blk("carpeta", "variable", x0+200, y0,
            value='(lambda p: (os.makedirs(p, exist_ok=True), p)[1])(os.path.join(os.path.expanduser("~"), "lab6_pruebas", nombre_prueba))',
            comment="Carpeta de salida: C:/Users/<usuario>/lab6_pruebas/<nombre_prueba>"),
        blk("duracion_captura", "variable", x0+400, y0, value=DURACION_CAPTURA, comment="Segundos de IQ guardados"),
        blk("imports_registro", "import", x0+560, y0, imports="import os\nimport time\nimport atexit" + imports, comment=""),
        blk("snippet_datos", "snippet", x0+720, y0, section="main_after_init", priority=0, code=codigo,
            comment="Escribe datos_de_la_prueba.txt al iniciar y al terminar"),
    ]

# =================== TX: HackRF ===================
def tx():
    b = variables()
    b += registro("TX (HackRF)", "tx.cfile (IQ transmitido), datos_de_la_prueba.txt")
    b += [
        blk("bb_gain", "variable", 760, 80, value=20, comment="Ganancia BB del HackRF [dB]"),
        blk("ppm", "variable", 900, 80, value=0, comment="Correccion de frecuencia del HackRF [ppm]"),
        blk("captura_head", "blocks_head", 1520, 360, type="complex", num_items="int(samp_rate*duracion_captura)",
            vlen=1, affinity="", alias="", maxoutbuf=0, minoutbuf=0, comment="Limita la grabacion a duracion_captura s"),
        blk("archivo_tx", "blocks_file_sink", 1720, 360, file='carpeta + "/tx.cfile"', type="complex", vlen=1,
            append="False", unbuffered="False", affinity="", alias="", comment="IQ enviado al HackRF"),
        blk("mensaje_bits", "variable", 200, 80, value=BITS,
            comment=f"Preámbulo 0xAA 0xAA, sincronía 0x2D 0xD4 y texto ASCII '{MENSAJE}'"),
        blk("rf_gain", "variable_qtgui_range", 560, 80, label="Ganancia RF (TX amp) [dB]", gui_hint="",
            min_len=200, orient="QtCore.Qt.Horizontal", rangeType="float", start=0, stop=14, step=14,
            value=0, widget="counter_slider", comment="0 = amplificador apagado. Dejar en 0."),
        blk("if_gain", "variable_qtgui_range", 560, 150, label="Ganancia IF (TX VGA) [dB]", gui_hint="",
            min_len=200, orient="QtCore.Qt.Horizontal", rangeType="float", start=0, stop=47, step=1,
            value=0, widget="counter_slider", comment="Subir de a poco; con atenuador de 30-40 dB en el cable"),
        blk("fuente", "blocks_vector_source_x", 40, 260, type="byte", vector="mensaje_bits", repeat="True",
            tags="[]", vlen=1, maxoutbuf=0, minoutbuf=0, affinity="", alias="", comment="Mensaje repetido"),
        blk("repetir", "blocks_repeat", 260, 260, type="byte", interp="sps", vlen=1, affinity="", alias="",
            maxoutbuf=0, minoutbuf=0, comment="Cada bit dura sps muestras (NRZ)"),
        blk("a_float", "blocks_char_to_float", 450, 260, scale=1, vlen=1, affinity="", alias="",
            maxoutbuf=0, minoutbuf=0),
        blk("centrar", "blocks_add_const_vxx", 640, 260, type="float", const=-0.5, vlen=1, affinity="",
            alias="", maxoutbuf=0, minoutbuf=0, comment="0/1 -> -0.5/+0.5"),
        blk("bipolar", "blocks_multiply_const_vxx", 840, 260, type="float", const=2, vlen=1, affinity="",
            alias="", maxoutbuf=0, minoutbuf=0, comment="-> -1/+1 (NRZ bipolar, punto M1a)"),
        blk("modulador_fm", "analog_frequency_modulator_fc", 1040, 260, sensitivity="2*3.141592653589793*dev/samp_rate",
            affinity="", alias="", maxoutbuf=0, minoutbuf=0, comment="Desviacion = ±dev para entrada ±1"),
        blk("amplitud", "blocks_multiply_const_vxx", 1300, 260, type="complex", const=0.5, vlen=1, affinity="",
            alias="", maxoutbuf=0, minoutbuf=0, comment="Margen frente a la saturación del DAC"),
        blk("hackrf", "osmosdr_sink", 1520, 240, args="hackrf", freq0="freq", gain0="rf_gain", if_gain0="if_gain",
            bb_gain0="bb_gain", corr0="ppm", bw0=0, sample_rate="samp_rate", nchan=1, type="fc32",
            clock_source0="", sync="", num_mboards=1, affinity="", alias="",
            comment="HackRF One (argumento 'hackrf' segun la guia)"),
        blk("espectro_tx", "qtgui_freq_sink_x", 1300, 420, name='"Espectro TX"', type="complex", bw="samp_rate",
            fc="freq", fftsize=2048, wintype="window.WIN_BLACKMAN_hARRIS", average=0.2, nconnections=1,
            showports="False", update_time=0.1, gui_hint="", comment="Verificar los dos lóbulos de FSK"),
        blk("tiempo_nrz", "qtgui_time_sink_x", 840, 420, name='"Bits NRZ (M1a)"', type="float", nconnections=1,
            size="int(sps*16)", srate="samp_rate", ymin=-1.5, ymax=1.5, update_time=0.1, gui_hint="",
            tr_mode="qtgui.TRIG_MODE_FREE", tr_slope="qtgui.TRIG_SLOPE_POS", tr_level=0, tr_delay=0,
            tr_chan=0, tr_tag='""', autoscale="False", grid="True"),
    ]
    c = [("fuente", 0, "repetir", 0), ("repetir", 0, "a_float", 0), ("a_float", 0, "centrar", 0),
         ("centrar", 0, "bipolar", 0), ("bipolar", 0, "modulador_fm", 0), ("bipolar", 0, "tiempo_nrz", 0),
         ("modulador_fm", 0, "amplitud", 0), ("amplitud", 0, "hackrf", 0), ("amplitud", 0, "espectro_tx", 0),
         ("amplitud", 0, "captura_head", 0), ("captura_head", 0, "archivo_tx", 0)]
    escribir("tx_fsk.grc", "tx_fsk", "TX FSK - HackRF", b, c)

# =================== RX: RTL-SDR ===================
def rx():
    b = variables()
    b += registro("RX (RTL-SDR)", "rx.cfile (IQ recibido), rx_bits.bin (bits decodificados), datos_de_la_prueba.txt",
                  imports="\nimport math")
    b += [
        blk("if_gain", "variable", 760, 80, value=20, comment="Ganancia IF del RTL-SDR [dB]"),
        blk("bb_gain", "variable", 900, 80, value=20, comment="Ganancia BB del RTL-SDR [dB]"),
        blk("captura_head", "blocks_head", 260, 540, type="complex", num_items="int(samp_rate*duracion_captura)",
            vlen=1, affinity="", alias="", maxoutbuf=0, minoutbuf=0, comment="Limita la grabacion a duracion_captura s"),
        blk("archivo_rx", "blocks_file_sink", 460, 540, file='carpeta + "/rx.cfile"', type="complex", vlen=1,
            append="False", unbuffered="False", affinity="", alias="", comment="IQ recibido (2 Msps, antes de filtrar)"),
        blk("decim", "variable", 200, 80, value=10, comment="Decimación del filtro de canal"),
        blk("fs_dec", "variable", 330, 80, value="samp_rate//decim", comment="Muestreo tras decimar"),
        blk("sps_dec", "variable", 480, 80, value="fs_dec/baud", comment="Muestras por bit tras decimar"),
        blk("rf_gain", "variable_qtgui_range", 640, 80, label="Ganancia RF RTL [dB]", gui_hint="", min_len=200,
            orient="QtCore.Qt.Horizontal", rangeType="float", start=0, stop=49.6, step=0.1, value=20,
            widget="counter_slider"),
        blk("ppm", "variable_qtgui_range", 640, 150, label="Corrección de frecuencia [ppm]", gui_hint="",
            min_len=200, orient="QtCore.Qt.Horizontal", rangeType="float", start=-60, stop=60, step=0.1,
            value=0, widget="counter_slider", comment="Ajustar hasta centrar los lóbulos del espectro"),
        blk("rtl", "osmosdr_source", 40, 260, args='"rtl=0"', freq0="freq", gain0="rf_gain", if_gain0="if_gain",
            bb_gain0="bb_gain", bw0=0, corr0="ppm", sample_rate="samp_rate", nchan=1, type="fc32", gain_mode0="False",
            dc_offset_mode0=0, iq_balance_mode0=0, clock_source0="", sync="", num_mboards=1, affinity="",
            alias="", maxoutbuf=0, minoutbuf=0, comment="RTL-SDR NooElec"),
        blk("filtro_canal", "low_pass_filter", 260, 260, type="fir_filter_ccf", decim="decim", gain=1,
            samp_rate="samp_rate", cutoff_freq="2*dev+baud+10000", width=20000, win="window.WIN_HAMMING",
            beta=6.76, affinity="", alias="", maxoutbuf=0, minoutbuf=0,
            comment="Corte = 2*dev + baud + margen para el offset del RTL"),
        blk("demod_fm", "analog_quadrature_demod_cf", 520, 260, gain="fs_dec/(2*math.pi*dev)", affinity="",
            alias="", maxoutbuf=0, minoutbuf=0, comment="Salida normalizada: ±1 = ±dev"),
        blk("sin_dc", "dc_blocker_xx", 760, 260, type="ff", length="int(sps_dec*20)", long_form="True",
            affinity="", alias="", maxoutbuf=0, minoutbuf=0, comment="Quita el error de frecuencia (RTL vs HackRF)"),
        blk("reloj", "digital_clock_recovery_mm_xx", 980, 260, type="float", omega="sps_dec",
            gain_omega="0.25*0.175*0.175", mu=0.5, gain_mu=0.175, omega_relative_limit=0.005, affinity="",
            alias="", maxoutbuf=0, minoutbuf=0),
        blk("decisor", "digital_binary_slicer_fb", 1240, 260, affinity="", alias="", maxoutbuf=0, minoutbuf=0),
        blk("archivo_bits", "blocks_file_sink", 1460, 260, file='carpeta + "/rx_bits.bin"', type="byte", vlen=1, append="False",
            unbuffered="True", affinity="", alias="", comment="Bits decodificados"),
        blk("a_complejo", "blocks_float_to_complex", 1240, 400, vlen=1, affinity="", alias="", maxoutbuf=0,
            minoutbuf=0, comment="Parte imaginaria sin conectar = 0"),
        blk("constelacion", "qtgui_const_sink_x", 1460, 400, name='"Constelación (símbolos FSK)"', size=1024,
            nconnections=1, type="complex", gui_hint="", update_time=0.1, xmin=-2, xmax=2, ymin=-2, ymax=2,
            axislabels="True", grid="True", comment="Dos grupos en I = -1 y +1"),
        blk("espectro_rx", "qtgui_freq_sink_x", 260, 400, name='"Espectro RX"', type="complex", bw="samp_rate",
            fc="freq", fftsize=2048, wintype="window.WIN_BLACKMAN_hARRIS", average=0.2, nconnections=1,
            showports="False", update_time=0.1, gui_hint=""),
        blk("tiempo_demod", "qtgui_time_sink_x", 760, 400, name='"Salida del demodulador"', type="float",
            nconnections=1, size="int(sps_dec*16)", srate="fs_dec", ymin=-2, ymax=2, update_time=0.1,
            gui_hint="", tr_mode="qtgui.TRIG_MODE_AUTO", tr_slope="qtgui.TRIG_SLOPE_POS", tr_level=0,
            tr_delay=0, tr_chan=0, tr_tag='""', autoscale="False", grid="True"),
        blk("a_audio", "rational_resampler_xxx", 760, 540, type="fff", interp=6, decim=25, taps="",
            fractional_bw=0, affinity="", alias="", maxoutbuf=0, minoutbuf=0,
            comment="200 kHz -> 48 kHz para el osciloscopio (M3)"),
        blk("audio_m3", "audio_sink", 1000, 540, samp_rate=48000, device_name='""', ok_to_block="True",
            num_inputs=1, affinity="", alias="", comment="M3: mensaje demodulado al osciloscopio"),
    ]
    c = [("rtl", 0, "filtro_canal", 0), ("rtl", 0, "espectro_rx", 0), ("filtro_canal", 0, "demod_fm", 0),
         ("demod_fm", 0, "sin_dc", 0), ("sin_dc", 0, "reloj", 0), ("sin_dc", 0, "tiempo_demod", 0),
         ("sin_dc", 0, "a_audio", 0), ("a_audio", 0, "audio_m3", 0), ("reloj", 0, "decisor", 0),
         ("reloj", 0, "a_complejo", 0), ("a_complejo", 0, "constelacion", 0), ("decisor", 0, "archivo_bits", 0),
         ("rtl", 0, "captura_head", 0), ("captura_head", 0, "archivo_rx", 0)]
    escribir("rx_fsk.grc", "rx_fsk", "RX FSK - RTL-SDR", b, c)

# =================== Osciloscopio: audio M1a/M1b ===================
def audio():
    b = [
        blk("fs_audio", "variable", 200, 12, value=48000, comment="Muestreo de audio"),
        blk("wav", "blocks_wavfile_source", 40, 200, file='"../data/mensaje_osciloscopio.wav"', nchan=2,
            repeat="True", norm="False", affinity="", alias="", maxoutbuf=0, minoutbuf=0,
            comment="Canal izq.: bits NRZ (M1a). Canal der.: FSK en audio (M1b)"),
        blk("audio_out", "audio_sink", 320, 200, samp_rate="fs_audio", device_name='""', ok_to_block="True",
            num_inputs=2, affinity="", alias="", comment="Salida de la tarjeta de sonido hacia el osciloscopio"),
        blk("vista", "qtgui_time_sink_x", 320, 340, name='"Vista previa (izq=NRZ, der=FSK)"', type="float",
            nconnections=2, size=2048, srate="fs_audio", ymin=-1.2, ymax=1.2, update_time=0.1, gui_hint="",
            tr_mode="qtgui.TRIG_MODE_FREE", tr_slope="qtgui.TRIG_SLOPE_POS", tr_level=0, tr_delay=0,
            tr_chan=0, tr_tag='""', autoscale="False", grid="True"),
    ]
    c = [("wav", 0, "audio_out", 0), ("wav", 1, "audio_out", 1), ("wav", 0, "vista", 0), ("wav", 1, "vista", 1)]
    escribir("audio_osciloscopio.grc", "audio_osciloscopio", "Audio para osciloscopio (M1a y M1b)", b, c)

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    tx(); rx(); audio()
