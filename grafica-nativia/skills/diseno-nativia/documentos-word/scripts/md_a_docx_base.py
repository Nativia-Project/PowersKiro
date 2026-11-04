"""
md_a_docx_base.py
=================
Conversor estable y reutilizable de Markdown a un .docx base con los estilos que
espera el script de marca Nativia (informe_docx_nativia.py del Power
grafica-nativia).

Este script es el PASO PREVIO a informe_docx_nativia.py. Produce un .docx
"neutro" (sin portada ni marca) con la estructura correcta: Title, Heading 1,
Heading 2, List Bullet, parrafos normales y tablas reales de Word. Luego ese
.docx se entrega a informe_docx_nativia.py, que agrega la portada, el indice y
los encabezados con la identidad Nativia. Separar los dos pasos evita el defecto
de improvisar el .docx base en cada corrida (parrafos partidos por el wrap a 80
columnas y tablas rotas en lineas sueltas).

Trazabilidad CRISP-DM:
  - Spec: 00-exploracion-datos-origen (Tarea 16.2).
  - Fase: 2 - Comprension de los Datos (informe ejecutivo de la exploracion).
  - Sub-etapa: generacion del documento ejecutivo (Requisito 11.1).
  - Falla: DPF (piloto). El conversor en si es generico y reutilizable.
  - Entrada: un archivo Markdown (--src), por ejemplo
    docs/00-exploracion-datos-origen/informe-ejecutivo-exploracion-origen.md.
  - Salida: un .docx base (--out) listo para informe_docx_nativia.py.

Reglas de conversion (pensadas para no repetir los defectos conocidos):
  - UNION DE LINEAS DE PARRAFO: las lineas consecutivas de texto que no estan
    separadas por una linea en blanco pertenecen al MISMO parrafo y se unen con
    un espacio. Un parrafo termina en una linea en blanco. Asi el wrap a 80
    columnas del Markdown no genera un parrafo por renglon.
  - ENCABEZADOS: el primer "# " va a Title; "## " va a Heading 1; "### " va a
    Heading 2.
  - VINETAS: las lineas que empiezan con "- " van a List Bullet; las lineas de
    continuacion indentadas se unen al mismo item.
  - TABLAS: los bloques Markdown con "|" y una fila separadora "|---|" se
    construyen como tablas reales de Word; la primera fila es cabecera; soporta
    2 o 3 columnas; se recortan los espacios de relleno de cada celda.
  - NEGRITAS: los pares **...** se traducen al caracter privado \ue000 (uno abre,
    el siguiente cierra) dentro de parrafos, vinetas y celdas, que es lo que
    informe_docx_nativia.py interpreta como negrita.
  - La cabecera del documento (Proyecto, Falla piloto, Fase, Fecha, Documento de
    respaldo) se conserva como parrafos normales.

Uso:
  python scripts/md_a_docx_base.py --src <informe>.md --out <base>.docx
"""
import argparse
import re

from docx import Document

# Caracter privado que informe_docx_nativia.py interpreta como limite de negrita.
NEGRITA_MARCADOR = "\ue000"

# Etiquetas de la cabecera del documento. Cada una abre un parrafo normal
# independiente; las lineas de continuacion (por el wrap a 80 columnas) se unen
# a la etiqueta en curso. Asi la cabecera se conserva como varios parrafos y no
# se fusiona en uno solo con la regla general de union de lineas.
ETIQUETAS_CABECERA = (
    "Proyecto:",
    "Falla piloto:",
    "Fase CRISP-DM:",
    "Fecha:",
    "Documento de respaldo:",
)


def es_inicio_campo_cabecera(linea):
    """Indica si la linea abre un campo de la cabecera del documento."""
    return any(linea.startswith(etq) for etq in ETIQUETAS_CABECERA)


def traducir_negritas(texto):
    """Convierte cada par **...** de Markdown en el marcador de negrita Nativia.

    Reemplaza la secuencia "**" por el caracter privado. El script del Power
    alterna negrita en cada aparicion del marcador (abre, cierra, abre, ...),
    por lo que basta con sustituir cada "**" por un marcador.
    """
    return texto.replace("**", NEGRITA_MARCADOR)


def normalizar_espacios(texto):
    """Colapsa espacios repetidos (que deja la union de lineas) en uno solo."""
    return re.sub(r" {2,}", " ", texto).strip()


def es_separador_tabla(linea):
    """Indica si la linea es la fila separadora de cabecera de una tabla (|---|)."""
    t = linea.strip()
    if not t.startswith("|"):
        return False
    celdas = [c.strip() for c in t.strip("|").split("|")]
    return all(re.fullmatch(r":?-{3,}:?", c) for c in celdas) and len(celdas) >= 1


def es_fila_tabla(linea):
    """Indica si la linea parece una fila de tabla Markdown (empieza con |)."""
    return linea.strip().startswith("|")


def partir_celdas(linea):
    """Separa una fila Markdown en celdas, recortando el relleno de cada una."""
    t = linea.strip()
    if t.startswith("|"):
        t = t[1:]
    if t.endswith("|"):
        t = t[:-1]
    return [c.strip() for c in t.split("|")]


def leer_bloques(lineas):
    """Agrupa las lineas del Markdown en bloques logicos.

    Cada bloque es una tupla (tipo, datos):
      - ("title", texto)        primer "# "
      - ("h1", texto)           "## "
      - ("h2", texto)           "### "
      - ("bullet", texto)       item de lista "- " (con continuaciones unidas)
      - ("parrafo", texto)      parrafo normal (lineas unidas con espacio)
      - ("tabla", [filas])      tabla real; filas es lista de listas de celdas

    La union de lineas de parrafo es el nucleo que evita los parrafos partidos.
    """
    bloques = []
    i = 0
    n = len(lineas)
    title_emitido = False

    while i < n:
        linea = lineas[i]
        bruta = linea.rstrip("\n")
        strip = bruta.strip()

        # Linea en blanco: cierra cualquier parrafo en curso.
        if not strip:
            i += 1
            continue

        # Tabla: fila que empieza con | seguida (en la linea siguiente) de un
        # separador |---|. Se consumen todas las filas contiguas.
        if es_fila_tabla(bruta) and i + 1 < n and es_separador_tabla(lineas[i + 1]):
            cabecera = partir_celdas(bruta)
            filas = [cabecera]
            i += 2  # saltar cabecera y separador
            while i < n and es_fila_tabla(lineas[i]):
                if es_separador_tabla(lineas[i]):
                    i += 1
                    continue
                filas.append(partir_celdas(lineas[i].rstrip("\n")))
                i += 1
            bloques.append(("tabla", filas))
            continue

        # Encabezados.
        if strip.startswith("### "):
            bloques.append(("h2", strip[4:].strip()))
            i += 1
            continue
        if strip.startswith("## "):
            bloques.append(("h1", strip[3:].strip()))
            i += 1
            continue
        if strip.startswith("# "):
            texto = strip[2:].strip()
            if not title_emitido:
                bloques.append(("title", texto))
                title_emitido = True
            else:
                bloques.append(("h1", texto))
            i += 1
            continue

        # Vineta: "- " al inicio. Se unen las lineas de continuacion, es decir
        # las lineas siguientes que no estan en blanco, no abren otra vineta y
        # no inician un encabezado o una tabla.
        if strip.startswith("- "):
            partes = [strip[2:].strip()]
            i += 1
            while i < n:
                sig = lineas[i].rstrip("\n")
                sig_strip = sig.strip()
                if not sig_strip:
                    break
                if sig_strip.startswith(("- ", "#", "## ", "### ")) or es_fila_tabla(sig):
                    break
                partes.append(sig_strip)
                i += 1
            bloques.append(("bullet", normalizar_espacios(" ".join(partes))))
            continue

        # Bloque de campos de cabecera: si la linea abre un campo conocido
        # (Proyecto:, Falla piloto:, ...), se emite un parrafo normal por campo.
        # Las lineas de continuacion partidas por el wrap a 80 columnas se unen
        # al campo en curso. Asi la cabecera se conserva como varios parrafos
        # normales legibles y no se fusiona en una sola oracion con la regla
        # general de union de lineas.
        if es_inicio_campo_cabecera(strip):
            while i < n:
                cur = lineas[i].rstrip("\n").strip()
                if not cur or not es_inicio_campo_cabecera(cur):
                    break
                partes = [cur]
                i += 1
                while i < n:
                    sig_strip = lineas[i].rstrip("\n").strip()
                    if not sig_strip:
                        break
                    if (
                        es_inicio_campo_cabecera(sig_strip)
                        or sig_strip.startswith(("- ", "#", "## ", "### "))
                        or es_fila_tabla(lineas[i])
                    ):
                        break
                    partes.append(sig_strip)
                    i += 1
                bloques.append(("parrafo", normalizar_espacios(" ".join(partes))))
            continue

        # Parrafo normal: se unen todas las lineas contiguas hasta una linea en
        # blanco, un encabezado, una vineta o una tabla.
        partes = [strip]
        i += 1
        while i < n:
            sig = lineas[i].rstrip("\n")
            sig_strip = sig.strip()
            if not sig_strip:
                break
            if sig_strip.startswith(("- ", "#", "## ", "### ")) or es_fila_tabla(sig):
                break
            partes.append(sig_strip)
            i += 1
        bloques.append(("parrafo", normalizar_espacios(" ".join(partes))))

    return bloques


def construir_tabla(doc, filas):
    """Crea una tabla real de Word a partir de las filas (lista de listas)."""
    columnas = max(len(f) for f in filas)
    tabla = doc.add_table(rows=len(filas), cols=columnas)
    tabla.style = "Table Grid"
    for r, fila in enumerate(filas):
        for c in range(columnas):
            valor = fila[c] if c < len(fila) else ""
            celda = tabla.cell(r, c)
            celda.text = ""  # limpiar el parrafo por defecto
            celda.paragraphs[0].add_run(traducir_negritas(valor))
    return tabla


def convertir(src, out):
    """Lee el Markdown de src y escribe el .docx base en out."""
    with open(src, encoding="utf-8") as fh:
        lineas = fh.readlines()

    bloques = leer_bloques(lineas)
    doc = Document()

    for tipo, datos in bloques:
        if tipo == "title":
            doc.add_paragraph(traducir_negritas(datos), style="Title")
        elif tipo == "h1":
            doc.add_paragraph(traducir_negritas(datos), style="Heading 1")
        elif tipo == "h2":
            doc.add_paragraph(traducir_negritas(datos), style="Heading 2")
        elif tipo == "bullet":
            doc.add_paragraph(traducir_negritas(datos), style="List Bullet")
        elif tipo == "tabla":
            construir_tabla(doc, datos)
        else:  # parrafo
            doc.add_paragraph(traducir_negritas(datos))

    doc.save(out)
    return len(bloques)


def main():
    ap = argparse.ArgumentParser(
        description="Convierte un Markdown a un .docx base para informe_docx_nativia.py"
    )
    ap.add_argument("--src", required=True, help="Archivo Markdown de entrada")
    ap.add_argument("--out", required=True, help="Archivo .docx base de salida")
    args = ap.parse_args()
    n = convertir(args.src, args.out)
    print("Bloques convertidos:", n)
    print("Salida:", args.out)


if __name__ == "__main__":
    main()
