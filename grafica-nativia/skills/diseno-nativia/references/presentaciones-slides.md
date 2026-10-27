# Presentaciones y slides HTML (marca Nativia)

Guia para construir presentaciones de diapositivas en HTML con la identidad Nativia,
navegables con flechas. Recoge decisiones ya probadas para evitar repetir errores.
Complementa SKILL.md (tokens, paleta, tipografia) y las demas referencias.

> Todas las decisiones de color, tipografia y espaciado salen de assets/design-tokens.json.
> Esta guia solo anade patrones especificos del formato "slides".

## 1. Estructura base

- Un solo archivo index.html autocontenido (CSS en <style>, JS minimo en <script>).
- Cada diapositiva es una <section class="slide">; solo la activa lleva .active.
- Fuentes: Montserrat (titulos) + Inter (cuerpo) desde Google Fonts, coherentes con los tokens.
- Fondo por defecto blanco; portadas y transiciones de seccion en Azul Profundo (.slide.dark).

## 2. El logo en el encabezado: el aire del SVG (IMPORTANTE)

Los SVG de isotipo Nativia (assets/logos/isotipo-*.svg) tienen un lienzo cuadrado
~1500x1500 con mucho espacio vacio alrededor del dibujo (isotipo + texto centrados).

Consecuencia: si pones el <img> del logo "grande" por altura, gran parte es aire y
se ve pequeno aunque ocupe mucho espacio, empujando el contenido hacia abajo.

### Que NO hacer
- NO recortar el viewBox "a ojo" estimando coordenadas con regex sobre el SVG: los
  archivos tienen cientos de <path> de gradientes y matrix() que contaminan el calculo.
  Recortes mal calculados cortan el texto "NATIVIA" o descentran el isotipo.

### Que SI hacer (solucion robusta, sin tocar el SVG)
Recortar el aire vertical con CSS usando una caja mas ancha que alta y object-fit: cover.
Como el lienzo es cuadrado, al cubrir el ancho el dibujo se agranda y solo se recorta
arriba/abajo (donde solo hay aire), nunca los lados (donde esta el texto).

    .brand-mark img {
      width: 300px;          /* ancho de la caja */
      height: 150px;         /* alto menor que el ancho: recorta aire vertical */
      object-fit: cover;     /* el SVG cubre la caja; se recorta arriba/abajo */
      object-position: center 46%; /* ajuste fino del encuadre vertical */
      display: block;
    }

- Ajustar el encuadre SOLO con object-position (el % vertical), nunca cortando lados.
- Variante por fondo: logo a color / "fondo claro" sobre blanco; variante clara sobre Azul Profundo.
- Mantener el logo prominente: es el elemento de identidad principal, nunca diminuto.

## 3. Encabezado que no empuja el contenido

El encabezado va en posicion absoluta, fuera del flujo, para que el cuerpo se centre
respecto a toda la diapositiva y el logo no desplace el contenido. El logo va arriba a la
DERECHA (justify-content: flex-end). No se usa chip de seccion: el unico elemento del
encabezado es el logo. Las portadas y el cierre no llevan logo en el encabezado porque ya
tienen el isotipo grande como hero.

    .slide-head { position: absolute; top: clamp(20px,3vh,40px);
      left: clamp(48px,6vw,96px); right: clamp(48px,6vw,96px);
      display: flex; align-items: center; justify-content: flex-end; z-index: 3; }

El .slide reserva arriba un padding-top acorde al alto del logo para que el cuerpo
nunca quede debajo del encabezado:

    .slide { padding: clamp(165px,20vh,190px) clamp(48px,6vw,96px) clamp(24px,4vh,48px); }

Regla practica: padding-top ~= alto_logo + top_del_header + ~30px de aire.
Si cambias el alto del logo, recalcula este padding-top o el contenido "bajara".

## 4. Centrado vertical del contenido

El cuerpo centra su contenido en el espacio disponible y se limita en ancho para no
quedar pegado a los bordes en pantallas anchas:

    .slide-body { flex: 1; display: flex; flex-direction: column; justify-content: safe center;
      max-width: 1600px; width: 100%; margin: 0 auto; padding-bottom: 72px; }

El padding-bottom deja aire para la barra de navegacion inferior.

IMPORTANTE: el centrado usa `safe center`, NO `center` a secas. Con contenido que cabe,
`safe center` lo centra igual que `center`. Pero cuando el contenido es mas alto que la
slide (p. ej. una Carta Gantt con varias fases expandidas, o una slide con muchas tarjetas),
`center` recorta por arriba y por abajo y el scroll NO alcanza la parte superior (bug clasico
de flexbox centrado + overflow). `safe center` alinea al inicio en ese caso, para que nada se
corte y el scroll funcione.

Y para que ese scroll exista, el `.slide` debe permitir desborde vertical:

    .slide { ...; overflow-y: auto; }

Asi, si una slide tiene mas contenido del que cabe en pantalla, se puede bajar con scroll
(rueda, barra, teclas) para verlo completo, en vez de quedar contenido inalcanzable fuera de
la vista. Las dos piezas van juntas: `overflow-y: auto` en `.slide` + `safe center` en
`.slide-body`. En impresion (`@media print`) el `.slide-body` usa `justify-content: flex-start`
o `center` y cada slide larga se parte en varias paginas (el PDF no scrollea).

## 5. Portada y cierre (sin logo de encabezado)

- La portada NO lleva logo ni encabezado (el head queda vacio o se omite). Lleva el isotipo grande
  centrado en el cuerpo. Dale una clase propia (.cover-slide) y recupera el
  padding-top normal, porque no hay logo arriba que compensar.
- El cierre recomendado: una sola diapositiva con el isotipo grande centrado y un
  texto corto ("Dudas?"). Sin encabezado ni mas elementos.

    .slide.cover-slide { padding-top: clamp(28px,4.5vh,56px); }
    .slide.closing { justify-content: center; align-items: center; }
    .closing-logo { width: clamp(340px,42vw,620px); max-height: 62vh; height: auto; }

Para el isotipo grande de portada/cierre SI se usa el SVG completo (sin recorte CSS),
porque ahi el aire alrededor no molesta: va centrado y con espacio propio.

## 6. Navegacion por flechas (controles semitransparentes abajo)

- Barra fija centrada en la parte inferior, semitransparente, que se opaca al pasar el mouse.
- Botones tactiles >= 44px (WCAG), con foco visible (:focus-visible en Naranja de marca).
- Soportar teclado (izquierda/derecha, espacio, Home/End) y swipe tactil.
- Barra de progreso fina arriba en Naranja Vibrante.
- El contador de diapositivas se calcula solo con slides.length: asi agregar o quitar
  diapositivas no obliga a tocar el numero.

    .nav { position: fixed; left: 50%; bottom: 22px; transform: translateX(-50%);
      background: rgba(10,42,67,0.28); backdrop-filter: blur(8px);
      border: 1px solid rgba(255,255,255,0.18); border-radius: 9999px; opacity: 0.55; }
    .nav:hover { opacity: 1; }
    .nav button { width: 44px; height: 44px; border-radius: 9999px; }
    .nav button:hover { background: var(--naranja); }

## 7. Densidad: contenido grande y legible a distancia

Una presentacion se ve a distancia y proyectada: el texto debe ser mayor que en una web.
El error tipico es texto chico "nadando" en una slide con mucho aire vacio. El contenido
debe LLENAR la slide, no flotar perdido en el centro.

Escala minima (sube tamanos antes de estirar el layout o dejar aire):
- Titulos h2: clamp(2rem, 4.2vw, 3.2rem).
- Texto de apoyo (.lead) y listas (ul.clean): clamp(1.15rem, 1.7vw, 1.5rem).
- Cuerpo de tarjetas, pasos y descripciones: --fs-lg como minimo (NUNCA --fs-base ni menos).
- Titulos de tarjeta / paso: --fs-xl o --fs-2xl.
- Notas al pie (.note): --fs-lg. La fuente al pie puede ser discreta, pero legible.
- Items de agenda (.l): --fs-2xl; el numero (.t) en circulo de 56px.
- Tarjetas con padding generoso (--sp-8 a --sp-12); badges/iconos numericos >= 48-56px.

Regla de verificacion: si al abrir la slide el contenido se ve pequeno respecto al marco y
sobra blanco arriba/abajo, sube tamanos y padding antes de darla por buena. Preferir pocas
slides con contenido grande y respirado, a muchas con texto chico.

## 7bis. Si usas un layout, incluye SU CSS (leccion aprendida)

Cada patron (agenda, tarjetas, metrics, pricing, pasos) depende de reglas CSS concretas.
Si partes de la plantilla real y la editas, ya vienen todas. Pero si reescribes o recortas
el bloque <style>, DEBES incluir el CSS de cada clase que uses en el markup.

Sintoma del error: el markup de un layout (ej. .agenda con .agenda-item/.t/.l/.go) aparece
como texto plano roto: numeros pegados al texto, sin circulos, sin tarjetas, sin espaciado,
y el texto auxiliar (.go "Ir ->") pegado al titulo. Significa que falta su CSS.

Prevencion:
- Parte del archivo real de la plantilla y edita sobre el; no reconstruyas el <style> de memoria.
- Si reconstruyes el <style>, antes de dar por lista la presentacion verifica que CADA clase
  usada en el HTML tenga su regla en el CSS (agenda, map/pasos, metrics, pricing, logos, etc.).

## 7ter. El indice / agenda debe ser NAVEGABLE por clic

La slide de indice o agenda no es solo decorativa: cada item salta a su seccion al hacer clic
o Enter. No basta con una lista numerada estatica.

Como se hace:
- Cada item lleva data-goto="N" (indice 0-based de la slide destino), role="link" y tabindex="0".
- El contenedor marca que es navegable (p. ej. clase .agenda o .nav-list) para el CSS de
  cursor/hover/foco.
- El script engancha el clic y Enter: querySelectorAll('[data-goto]') -> addEventListener click
  y keydown (Enter/Espacio) que llaman a go(N). Sin ese JS, los data-goto no hacen nada.

Sintoma del error: haces clic en un item del indice y no pasa nada. Falta el JS que engancha los
data-goto, o el item no tiene cursor/hover (falta la clase navegable y su CSS).

## 7quater. Jerarquia titulo / kicker (NO invertir)

El nombre de la seccion va en el titulo grande (h2); la frase descriptiva o el contexto van en
el kicker chico de arriba. Nunca al reves. Ejemplo correcto: kicker "Quien hace que" (chico) +
h2 "Compromisos" (grande). Incorrecto: kicker "Compromisos" + h2 "Quien hace que". Si el titulo
grande dice una frase y el nombre de la seccion quedo arriba en chico, estan invertidos.

## 7quinquies. Carta Gantt para planificacion (seguimientos)

Para mostrar la planificacion de un proyecto en una reunion de seguimiento, usar una Carta Gantt
estilo Nativia en vez de un timeline vertical:
- Cuadricula: encabezado con nº de semana + fechas (Azul Profundo, texto legible blanco/azul claro).
- Filas por fase, barra posicionada en sus semanas con grid-column (numeros literales, no calc con
  variables en grid-column: es fragil). Columna de etiqueta proporcional (fr), no ancho fijo en px,
  o las semanas se comprimen y no se ven.
- Colores de marca: azul medio = completado, azul acento = en curso, gris azulado = planificado,
  naranja = hito. Linea vertical "HOY" en la semana actual.
- Fases expandibles (clic en triangulo) que muestran sus actividades como sub-filas con vineta de
  estado. La fase en curso expandida por defecto. No omitir actividades.
- Partir en varias slides si no cabe; cada slide repite su encabezado de semanas (para PDF).

## 8. Diagramas (ej. jerarquias)

Para jerarquias tipo "una agrupacion contiene varios elementos" (p. ej. una OU con varias
cuentas), representar cada rama en su propia columna con sus hijos debajo, unidos por
conectores. No colgar hijos de una sola rama: se entiende mal la relacion "uno a muchos".

## 9. Logos grandes de marca: usar los reales

Para el isotipo protagonista (portada/cierre) usar los SVG reales de assets/logos/.
En un proyecto, copiarlos a una carpeta local assets/ y referenciarlos por ruta relativa
(los SVG son pesados; evitar incrustarlos inline en cada diapositiva).

## Checklist especifico de slides

- [ ] Logo del encabezado arriba a la DERECHA, grande y sin aire (object-fit: cover), sin cortar texto.
- [ ] Sin chip de seccion en el encabezado (el logo es el unico elemento).
- [ ] Encabezado absoluto; contenido centrado vertical y no "caido" hacia abajo.
- [ ] padding-top del .slide recalculado si cambia el alto del logo.
- [ ] Portada sin logo de encabezado; isotipo grande en el cuerpo.
- [ ] Cierre con solo isotipo grande + texto corto.
- [ ] Navegacion por flechas (teclado + clic + swipe), tactiles >= 44px, foco visible.
- [ ] Contador automatico con slides.length.
- [ ] Indice/agenda navegable: cada item salta a su seccion al hacer clic o Enter (data-goto + JS).
- [ ] Boton flotante para volver al indice/agenda presente en cada slide (oculto en portada,
      indice y cierre), con tecla M y foco visible.
- [ ] Texto grande y legible a distancia; el contenido llena la slide, no flota en el centro.
- [ ] Cada layout usado tiene su CSS en el <style> (agenda, pasos, metrics, pricing no rotos).
- [ ] Cuerpo de tarjetas/pasos/notas >= --fs-lg; items de agenda en --fs-2xl.
- [ ] Todo el color/tipografia desde los tokens; Naranja solo como acento.

## 10. Exportar la presentaciÃ³n a PDF (una slide por pÃ¡gina)

Las slides viven apiladas (position absolute, solo la activa visible), asi que al imprimir
sale una sola. Para exportar TODAS en un PDF, una por pagina, agregar un bloque @media print.

### Instrucciones para el usuario (Chrome/Edge/Brave)
1. Abrir el HTML, Ctrl+P, Destino = Guardar como PDF.
2. Mas opciones: Tamano del papel = Tabloid (el que mejor calza 16:9), Paginas por hoja = 1,
   Margenes = Predeterminado.
3. Activar "Graficos en segundo plano" (si no, los fondos azules/naranjas no se imprimen).

### Bloque @media print (probado). Va dentro del <style>, antes de </style>:

    @media print {
      @page { size: landscape; margin: 0; }
      html, body { height: auto !important; overflow: visible !important; background: #fff !important; }
      .deck { position: static !important; width: auto !important; height: auto !important; display: block !important; }
      .slide {
        position: relative !important; display: flex !important; flex-direction: column !important;
        justify-content: center !important; opacity: 1 !important; inset: auto !important;
        width: 100% !important; height: 100vh !important; box-sizing: border-box !important;
        padding: 5vh 6vw !important; margin: 0 !important; overflow: hidden !important;
        page-break-after: always !important; break-after: page !important;
        page-break-inside: avoid !important; break-inside: avoid !important;
      }
      .slide:last-of-type { page-break-after: auto !important; break-after: auto !important; }
      .slide-head { position: absolute !important; top: 3vh !important; left: 6vw !important; right: 6vw !important; align-items: center !important; }
      .brand-mark img { width: 200px !important; height: 88px !important; object-fit: cover !important; object-position: center 46% !important; }
      .slide-body { padding-top: 9vh !important; padding-bottom: 3vh !important; max-width: 100% !important; justify-content: center !important; }
      .nav, .menu-btn, .progress, .hint { display: none !important; }
      * { -webkit-print-color-adjust: exact !important; print-color-adjust: exact !important; }
    }

### Claves (lecciones aprendidas)
- El logo se corta si object-fit: contain muestra todo el aire del SVG, o si queda pegado al
  borde superior. Solucion: object-fit: cover en caja ~200x88 (recorta solo el aire, no el texto).
- El contenido queda "muy abajo" si el padding-top de impresion es grande (ej. 17vh). Bajarlo a
  ~9vh y dejar que .slide-body centre con justify-content: center (igual que en pantalla).
- Sin "Graficos en segundo plano" activo, los fondos .slide.dark salen en blanco.
- Tabloid calza mejor que Letter/A4 para 16:9; landscape se fuerza con @page { size: landscape }.






