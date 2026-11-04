# Documentos Word (.docx) con formato Nativia

Alcance: SOLO documentos Word (informes, documentos ejecutivos, minutas en .docx).
Las presentaciones HTML NO se rigen por este apartado: siguen usando
`assets/plantillas/` y `references/presentaciones-slides.md` sin cambios.

## Contenido de esta carpeta

```
documentos-word/
├── README.md                          # Este documento (reglas de Word)
├── scripts/
│   ├── md_a_docx_base.py              # Convierte un Markdown a .docx base (paso previo)
│   ├── informe_docx_nativia.py        # Aplica el formato Nativia a un .docx
│   └── logo_horizontal_sobre_azul.py  # Regenera el logo de portada desde el logo oficial
└── assets/
    ├── logo-portada-sobre-azul.png    # Logo horizontal para la portada (fondo Azul Profundo)
    └── glifo-encabezado.png           # N a color para el encabezado de paginas interiores
```

## Uso

Requisitos: python-docx y lxml. Opcional: LibreOffice (`soffice`) y `pdftotext` para que el
indice salga con los numeros de pagina reales.

El punto de partida recomendado es un archivo Markdown. El flujo de documentos Word tiene dos
pasos encadenados: primero se genera un .docx base a partir del Markdown y luego se aplica el
formato Nativia sobre ese .docx base.

Paso 1. Generar el .docx base desde el Markdown con el conversor:

```
python documentos-word/scripts/md_a_docx_base.py --src documento.md --out base.docx
```

Paso 2. Aplicar el formato Nativia al .docx base:

```
python documentos-word/scripts/informe_docx_nativia.py --src base.docx --out salida.docx \
  --kicker "INFORME EJECUTIVO  |  FASE 2" \
  --titulo "Titulo del documento" \
  --subtitulo "Proyecto o cliente" \
  --detalle "Linea de contexto" \
  --dato "Fecha=2026-11-03" --dato "Respaldo=ruta o referencia"
```

El conversor del paso 1 produce exactamente los estilos que el paso 2 espera (Title, Heading 1,
Heading 2, List Bullet y tablas) y traduce los pares de negrita del Markdown (dobles asteriscos)
al marcador interno que el script de marca resalta. De este modo se evita el defecto de construir
el .docx base a mano en cada ocasion, que partia los parrafos (una linea por renglon) y rompia
las tablas.

Si ya se dispone de un .docx con los estilos correctos, se puede entrar directamente al paso 2.
El .docx de entrada del paso 2 debe usar los estilos Title, Heading 1, Heading 2, List Bullet y
tablas.

## Reglas del formato (implementadas en el script)

### Portada
- Pagina completa en Azul Profundo #0A2A43. El fondo es un rectangulo (forma de Word, no
  imagen ni tabla) anclado a la esquina de la hoja, del tamano exacto de la pagina y detras del
  texto. El texto de la portada es real y editable. No usar tablas para la portada: varios
  visores ignoran su ancho y sus margenes de celda.
- Logo: `assets/logo-portada-sobre-azul.png`, version horizontal: la N con su cinta en azul de
  marca #3075A9 y alas naranjas, y NATIVIA / CLOUD & IA en blanco a la derecha. La cinta de la N
  conserva siempre el azul; no se vuelve blanca. Se regenera con
  `scripts/logo_horizontal_sobre_azul.py ../assets/logos/isotipo-color.png salida.png`.
- Titulo, subtitulo y valores de los datos en blanco. La etiqueta superior y las etiquetas de
  los datos (FECHA, RESPALDO, etc.) en Naranja #F39221, como acento. Linea Naranja bajo el titulo.

### Paginas interiores
- Fondo blanco. Encabezado con `assets/glifo-encabezado.png` y filete azul; pie con numero de
  pagina. La portada cuenta como pagina 1.
- Indice en la pagina 2 y encabezados numerados (1., 1.1), obligatorios en todo documento. El
  script numera los Heading 1 y 2 que no traigan numero y genera el indice con campo TOC, puntos
  guia y numeros de pagina reales. Sin LibreOffice, el indice queda sin numeros hasta actualizar
  el campo en Word (clic derecho, Actualizar campo).

### Colores y tipografia
- Titulos, subtitulos, titulo del indice y encabezados de parrafo en negrita (por ejemplo
  "Telemetria. ..."): Azul Profundo #0A2A43, Montserrat Bold.
- Cuerpo de texto, vinetas y celdas de tablas: negro de lectura #1A1A1A, Inter.
- Tablas: cabecera Azul Profundo con texto blanco, filas alternadas en tinte azul claro, la
  cabecera se repite si la tabla cruza de pagina y las filas no se parten.

### Ortografia y compatibilidad
- Ortografia correcta en espanol en todo el documento, con tildes y enie. Si el texto fuente
  viene sin tildes, se corrige antes de generar el .docx: el script no corrige ortografia.
- El documento se marca con idioma es-CL para el corrector de Word.
- El script reordena las propiedades XML segun el esquema de Word (Word ignora las que quedan
  fuera de orden). Verificar el resultado abriendo el archivo en Word, no solo en LibreOffice.
- Los numeros van en digitos, no escritos como palabras (por ejemplo 9 sensores, no nueve
  sensores), en particular los conteos, cantidades, cifras, porcentajes y datos. Las expresiones
  fijas del lenguaje pueden mantener la palabra cuando el digito resulte forzado. El script no
  reescribe numeros: el texto fuente ya debe venir en digitos.
- Los numeros que son cifras o datos van en negrita en el cuerpo del documento (prosa, vinetas y
  celdas de tablas): conteos, cantidades, porcentajes, montos y valores. No se ponen en negrita
  los numeros de titulos y encabezados, la numeracion de secciones, los numeros de pagina ni los
  identificadores tecnicos que incluyan digitos (por ejemplo bank 1, us-east-1, un
  diagnostic_id). El resaltado en negrita del cuerpo se expresa en el texto fuente con el
  marcador que el script interpreta; el script no decide por si solo que numeros resaltar.
## Reglas del conversor md_a_docx_base.py

- Une en un mismo parrafo las lineas de texto consecutivas que no esten separadas por una linea
  en blanco, de modo que se evita el parrafo por renglon propio del ajuste a 80 columnas.
- El primer encabezado de nivel 1 del Markdown se asigna al estilo Title; los encabezados de
  nivel posterior se asignan a Heading 1 y Heading 2 segun su jerarquia.
- Las vinetas del Markdown se asignan al estilo List Bullet.
- Los bloques de tabla Markdown se construyen como tablas reales de Word de dos o tres columnas,
  con su fila de cabecera.
- Los pares de negrita del Markdown (dobles asteriscos) se traducen al marcador que interpreta
  informe_docx_nativia.py para resaltar el texto.
- La cabecera del documento (lineas de Proyecto, Falla, Fase, Fecha y Documento de respaldo) se
  conserva como parrafos normales.
