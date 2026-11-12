"""Verifica en NumPy/SciPy la cadena TX -> canal -> RX de los flujogramas grc/tx_fsk.grc y grc/rx_fsk.grc.

Usa los mismos parámetros (fs, baud, desviación, filtro, decimación) para comprobar, antes del laboratorio,
que el diseño demodula el mensaje con desplazamiento de frecuencia (típico del RTL-SDR) y ruido.
No sustituye la prueba con GNU Radio: la recuperación de reloj aquí es por muestreo en el centro del bit,
no el bloque Clock Recovery MM.

Uso:  py tools/verificar_cadena_fsk.py
"""
import numpy as np
from scipy import signal
from scipy.ndimage import uniform_filter1d

# ---- Parámetros (deben coincidir con los de los .grc: ver tools/generar_grc.py) ----
FS = 2_000_000       # Hz, muestreo SDR
BAUD = 2_000         # símbolos/s
DEV = 25_000         # Hz, desviación de frecuencia (±)
DECIM = 10           # decimación del filtro de canal
CUTOFF, TRANS = 60_000, 20_000
MENSAJE = "COEL"

def trama_bits(mensaje=MENSAJE):
    """Preámbulo 0xAA 0xAA + sincronía 0x2D 0xD4 + ASCII, MSB primero."""
    datos = bytes([0xAA, 0xAA, 0x2D, 0xD4]) + mensaje.encode()
    return np.array([(b >> i) & 1 for b in datos for i in range(7, -1, -1)], dtype=np.uint8)

def transmitir(bits):
    sps = FS//BAUD
    nrz = np.repeat(2.0*bits - 1.0, sps)                           # ±1
    fase = np.cumsum(2*np.pi*DEV/FS*nrz)                           # modulador de frecuencia (sensibilidad 2π·dev/fs)
    return 0.5*np.exp(1j*fase)

def canal(x, offset_hz, snr_db, rng):
    n = np.arange(len(x))
    x = x*np.exp(2j*np.pi*offset_hz*n/FS)                          # error de frecuencia entre osciladores
    pot = np.mean(np.abs(x)**2)
    sig = np.sqrt(pot/10**(snr_db/10)/2)                           # SNR en todo el ancho de banda de FS
    return x + sig*(rng.standard_normal(len(x)) + 1j*rng.standard_normal(len(x)))

def recibir(y, bits_ref):
    taps = signal.firwin(int(3.3*FS/TRANS)|1, CUTOFF, fs=FS, window='hamming')
    yd = signal.lfilter(taps, 1, y)[::DECIM]                       # filtro de canal + decimación
    fsd = FS/DECIM
    dem = np.angle(yd[1:]*np.conj(yd[:-1]))*fsd/(2*np.pi*DEV)       # Quadrature Demod, ganancia fsd/(2π·dev)
    dem = dem - uniform_filter1d(dem, size=int(fsd/BAUD*20))       # bloqueo de DC (quita el offset de frecuencia)
    spb = int(fsd/BAUD)
    # elegir la fase de muestreo con mayor "apertura de ojo"
    mejor = max(range(spb), key=lambda k: np.mean(np.abs(dem[k::spb])))
    simb = dem[mejor::spb]
    rx = (simb > 0).astype(np.uint8)
    # buscar la palabra de sincronía 0xAA 0xAA 0x2D 0xD4 para fijar el inicio de trama
    sync = bits_ref[:32]
    for i in range(len(rx)-len(bits_ref)):
        if np.array_equal(rx[i:i+32], sync):
            return rx[i:i+len(bits_ref)], simb
    return None, simb

def a_texto(bits):
    datos = bytes(int(''.join(map(str, bits[i:i+8])), 2) for i in range(32, len(bits), 8))
    return datos.decode(errors='replace')

if __name__ == "__main__":
    rng = np.random.default_rng(7)
    ref = trama_bits()
    tx = transmitir(np.tile(ref, 6))                              # la trama se repite (Repeat = Yes)
    print(f"fs={FS/1e6} Msps  baud={BAUD}  dev=±{DEV/1e3} kHz  índice h={2*DEV/BAUD:.1f}  Carson={(2*(DEV+BAUD/2))/1e3:.0f} kHz")
    print(f"{'offset [kHz]':>12} {'SNR [dB]':>9} {'BER':>8}  texto")
    for off, snr in [(0, 30), (15e3, 30), (-30e3, 30), (15e3, 10), (15e3, 0), (15e3, -5)]:
        rx, _ = recibir(canal(tx, off, snr, rng), np.tile(ref, 1))
        if rx is None:
            print(f"{off/1e3:12.0f} {snr:9} {'sin sync':>8}")
        else:
            ber = np.mean(rx != ref)
            print(f"{off/1e3:12.0f} {snr:9} {ber:8.4f}  {a_texto(rx)!r}")
