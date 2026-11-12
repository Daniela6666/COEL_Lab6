"""Decodifica el archivo de bits que guarda rx_fsk.grc (rx_bits.bin) y mide los errores.

Cada byte del archivo es un bit (0 o 1). Busca la sincronía 0xAA 0xAA 0x2D 0xD4, lee el mensaje que sigue
y compara con el transmitido. Prueba también la polaridad invertida (según el signo del demodulador).

Uso:  py tools/decodificar_bits.py ruta/rx_bits.bin [MENSAJE_ESPERADO]
"""
import sys
import numpy as np

SYNC = [int(b) for b in format(0xAA, "08b")*2 + format(0x2D, "08b") + format(0xD4, "08b")]

def a_bytes(bits):
    n = len(bits)//8*8
    return bytes(int("".join(map(str, bits[i:i+8])), 2) for i in range(0, n, 8))

def buscar(bits, esperado):
    L = 32 + 8*len(esperado)
    tramas = []
    for i in range(len(bits) - L + 1):
        if bits[i:i+32] == SYNC:
            tramas.append(bits[i:i+L])
    return tramas

if __name__ == "__main__":
    ruta = sys.argv[1]
    esperado = sys.argv[2] if len(sys.argv) > 2 else "COEL"
    raw = np.fromfile(ruta, dtype=np.uint8)
    print(f"{len(raw)} bits leídos; proporción de unos = {raw.mean():.3f}")
    for nombre, b in [("normal", raw), ("invertida", 1 - raw)]:
        tramas = buscar([int(x) for x in b], esperado)
        print(f"polaridad {nombre}: {len(tramas)} tramas con sincronía")
        if tramas:
            ref = [int(x) for x in format(int.from_bytes(bytes([0xAA, 0xAA, 0x2D, 0xD4]) + esperado.encode(), "big"),
                                        f"0{32 + 8*len(esperado)}b")]
            errores = [sum(x != y for x, y in zip(t, ref)) for t in tramas]
            ok = sum(e == 0 for e in errores)
            texto = a_bytes(tramas[0][32:]).decode(errors="replace")
            print(f"  primer mensaje: {texto!r} | tramas sin error: {ok}/{len(tramas)} | "
                  f"BER = {sum(errores)/(len(ref)*len(tramas)):.2e}")
            break
    else:
        print("No se encontró la sincronía: revisar ppm, ganancias o polaridad.")
