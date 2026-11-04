# Documentos Word (.docx) con formato Nativia

Alcance: SOLO documentos Word (informes, documentos ejecutivos, minutas en .docx).
Las presentaciones HTML NO se rigen por este apartado: siguen usando
`assets/plantillas/` y `references/presentaciones-slides.md` sin cambios.

## Contenido de esta carpeta

```
documentos-word/
├── README.md                          # Este documento (reglas de Word)
├── scripts/
│   ├── informe_docx_nativia.py        # Aplica el formato Nativia a un .docx
│   └── logo_horizontal_sobre_azul.py  # Regenera el logo de portada desde el logo oficial
└── assets/
    ├── logo-portada-sobre-azul.png    # Logo horizontal para la portada (fondo Azul Profundo)
    └── glifo-encabezado.png           # N a color para el encabezado de paginas interiores
```

## Uso

Requisitos: python-docx y lxml. Opcional: LibreOffice (`soffice`) y `pdftotext` para que el
indice salga con los numeros de pagina reales.

```
python documentos-word/scripts/informe_docx_nativia.py --src entrada.docx --out salida.docx \
  --kicker "INFORME EJECUTIVO  |  FASE 2" \
  --titulo "Titulo del documento" \
  --subtitulo "Proyecto o cliente" \
  --detalle "Linea de contexto" \
  --dato "Fecha=2026-11-03" --dato "Respaldo=ruta o referencia"
```

El .docx de entrada debe usar los estilos Title, Heading 1, Heading 2, List Bullet y tablas.

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
