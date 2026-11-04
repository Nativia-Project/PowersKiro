"""Arma el logo horizontal Nativia sobre fondo oscuro a partir del logo oficial a color.

Toma isotipo-color.png (version vertical sobre blanco) y produce un PNG transparente con:
- la N con su cinta en azul de marca (azulAcento #3075A9) y las alas naranjas originales,
- el texto NATIVIA / CLOUD & IA en blanco, a la derecha de la N.
"""
import sys
import numpy as np
from PIL import Image

src, dst = sys.argv[1], sys.argv[2]
AZUL = np.array([0x30, 0x75, 0xA9], float)

im = Image.open(src).convert('RGBA')
bg = Image.new('RGBA', im.size, (255, 255, 255, 255))
bg.alpha_composite(im)
a = np.asarray(bg.convert('RGB')).astype(float)


def bbox(m):
    ys, xs = np.where(m)
    return ys.min(), ys.max() + 1, xs.min(), xs.max() + 1


def recolor(reg, color_oscuro):
    r, g, b = reg[..., 0], reg[..., 1], reg[..., 2]
    lum = 0.3 * r + 0.59 * g + 0.11 * b
    naranja = (r - b) > 50
    out = np.zeros(reg.shape[:2] + (4,))
    # pixeles no naranjas: color destino con alfa segun cuan lejos estan del blanco
    oscuro = lum[~naranja & (lum < 200)]
    ref = np.percentile(oscuro, 5) if oscuro.size else 40
    out[..., :3] = color_oscuro
    out[..., 3] = np.clip((255 - lum) / (255 - ref), 0, 1) * 255
    # naranjas: color original, alfa segun distancia al blanco por el canal azul
    ao = np.clip((255 - b) / (255 - 40), 0, 1)
    out[naranja, :3] = reg[naranja]
    out[naranja, 3] = (ao * 255)[naranja]
    return Image.fromarray(out.astype('uint8'), 'RGBA')


no_blanco = a.min(axis=2) < 245
# la N ocupa la parte superior del dibujo; el texto, la inferior (separadas por filas en blanco)
filas = np.where(no_blanco.any(axis=1))[0]
corte = None
for y in range(filas.min() + 200, filas.max()):
    if not no_blanco[y].any():
        corte = y
        break
y0, y1, x0, x1 = bbox(no_blanco[:corte])
glifo = recolor(a[y0:y1, x0:x1], AZUL)
t = no_blanco.copy(); t[:corte] = False
y0, y1, x0, x1 = bbox(t)
texto = recolor(a[y0:y1, x0:x1], np.array([255, 255, 255], float))

# composicion horizontal: el bloque de texto mide ~60 por ciento del alto de la N
gh = glifo.height
th = int(gh * 0.60)
texto = texto.resize((int(texto.width * th / texto.height), th), Image.LANCZOS)
gap = int(gh * 0.10)
lienzo = Image.new('RGBA', (glifo.width + gap + texto.width, gh), (0, 0, 0, 0))
lienzo.alpha_composite(glifo, (0, 0))
lienzo.alpha_composite(texto, (glifo.width + gap, (gh - th) // 2))
lienzo.save(dst)
print('ok', lienzo.size)
