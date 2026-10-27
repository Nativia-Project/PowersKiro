---
name: diseno-nativia
description: Aplica la identidad visual de marca Nativia (Cloud & IA) y estándares de usabilidad de la industria (Nielsen, WCAG AA, Gestalt) a cualquier diseño o interfaz. Úsala al crear o revisar UI, componentes, landings, dashboards, presentaciones o piezas gráficas, para que el resultado siga la marca y NO sea un diseño genérico de IA.
---

# Diseño Nativia: marca + usabilidad

Skill para producir diseños que (1) respetan la identidad visual oficial de **Nativia - Cloud & IA**
y (2) cumplen estándares de usabilidad de la industria. Objetivo explícito: **evitar el look
genérico de IA** y anclar cada decisión en marca o en un principio de usabilidad.

Aplica a UI web/app, componentes, landings, dashboards, y también presentaciones y piezas gráficas.

## Cómo usar esta skill (procedimiento)

1. **Antes de diseñar**, cargar los tokens de marca desde `assets/design-tokens.json`
   (relativo a esta carpeta de skill). Usar SOLO esos colores, tipografía y escalas. No inventar paleta.
2. Si el trabajo es UI/interacción, revisar también
   `references/principios-usabilidad.md` (heurísticas, leyes UX, WCAG, Gestalt).
3. Tener presente `references/anti-generico-ia.md` y evitar activamente cada "tell".
4. Si el trabajo es una presentacion o slides HTML navegables:
   - PARTIR SIEMPRE de la plantilla incluida en el Power: `assets/plantillas/deck-base.html`
     (o `assets/plantillas/deck-seguimiento.html` para reuniones de seguimiento con Carta Gantt).
     NO reconstruir el andamiaje de memoria. La plantilla ya trae: tokens, estilos, header con
     logo arriba a la derecha, portada con isotipo grande, agenda navegable, barra de navegacion
     inferior centrada, barra de progreso en Naranja, bloque @media print para exportar a PDF y
     el motor de navegacion (flechas, teclado, swipe, contador automatico). Copiar la plantilla y
     verter el contenido dentro de su estructura; no inventar un andamiaje propio.
   - Los logos que la plantilla referencia viajan en `assets/plantillas/assets/` (logo-claro.svg,
     logo-oscuro.svg, isotipo-color.png). Al copiar la plantilla a una presentacion concreta,
     ajustar la ruta relativa de `../assets/logo-*.svg` segun donde quede el HTML.
   - Revisar tambien `references/presentaciones-slides.md` (manejo del logo y su aire con
     object-fit: cover, encabezado absoluto que no empuja el contenido, centrado vertical,
     navegacion por flechas, portada y cierre con isotipo grande, agenda navegable, PDF).
4. Para logos, usar los archivos reales en `assets/logos/` (incluidos en este Power):
   - `isotipo-fondo-claro.svg` / `isotipo-sinfondo-claro.svg` → sobre fondo claro (blanco).
   - `isotipo-fondo-oscuro.svg` / `isotipo-sinfondo-oscuro.svg` → sobre fondo oscuro (Azul Profundo).
   - Preferir SVG; usar la variante "sinfondo" cuando se quiera integrar sin recuadro.
5. **Antes de entregar**, correr el checklist de cierre (abajo).

> Todas las rutas (`references/`, `assets/`) son relativas a esta carpeta de skill, que viaja
> dentro del Power. No dependen de rutas absolutas de ninguna máquina en particular.

## Marca Nativia (resumen; valores exactos en design-tokens.json)

**Paleta** (extraída del Manual de Identidad Visual Nativia V2):
- Azul Profundo `#0A2A43` — principal: títulos, autoridad, tecnología.
- Escala azul del logo: `#164264`, `#225B86`, `#3075A9` — secciones, enlaces, estados.
- Naranja Vibrante `#F39221` — acento e innovación. **Solo** CTA/acción y destacados puntuales.
- Gris Corporativo `#58595B` — textos secundarios y subtítulos.
- Blanco — fondo por defecto (limpieza visual).

**Tipografía**:
- Primaria (títulos/marca): sans-serif **geométrica** (tipo Montserrat/Gotham), Bold/Extra-Bold.
- Secundaria (cuerpo/eslogan): sans-serif **humanista**, Light/Regular, Medium en subtítulos.

**Aplicación**:
- Jerarquía: títulos en Azul Profundo, destacados en Naranja, lectura en Gris.
- Fondos blancos por defecto; Azul Profundo solo en portadas/transiciones.

## Reglas duras (no negociables)

1. **Paleta cerrada**: solo colores de `design-tokens.json`. El Naranja es escaso (acción/acento),
   nunca color de fondo masivo ni de texto largo.
2. **Sin clichés de IA**: nada de gradientes morados, todo-centrado, radios uniformes en todo,
   emojis como iconos, microcopy vacío. Ver `anti-generico-ia.md`.
3. **Jerarquía tipográfica real**: usar la escala de tokens; jerarquía por tamaño Y peso, no 2 tamaños.
4. **Accesibilidad WCAG AA**: contraste ≥ 4.5:1 en texto; foco visible; objetivos táctiles ≥ 44px;
   no comunicar solo con color.
5. **Estados completos**: todo elemento interactivo define default/hover/focus/active/disabled/
   loading; y las vistas definen estado vacío y de error.
6. **Justificación**: cada decisión visual se ancla en marca o en un principio de usabilidad.

## Checklist de cierre (verificar antes de entregar)

- [ ] Colores solo de la paleta Nativia; Naranja usado con moderación y solo para acción/acento.
- [ ] Tipografía: geométrica en títulos, humanista en cuerpo; escala aplicada.
- [ ] Jerarquía visual clara (primario/secundario evidente).
- [ ] Contraste WCAG AA verificado; foco visible; táctiles ≥ 44px; no solo-color.
- [ ] Estados definidos (hover/focus/active/disabled/loading/vacío/error).
- [ ] Ningún "tell" de IA de `anti-generico-ia.md`.
- [ ] Logo correcto (SVG; variante según fondo) si aplica.
- [ ] Cada decisión tiene justificación de marca o usabilidad.

## Límite honesto

Esta skill asegura las bases de marca y usabilidad y elimina los defaults genéricos obvios. No
garantiza por sí sola un diseño excelente: eso depende del contexto del producto y de criterio
humano. Y la conformidad WCAG plena requiere pruebas manuales con tecnología de asistencia.
