# Principios de usabilidad de la industria

Estándares de referencia para que cualquier diseño de Nativia sea usable, no solo "bonito".
Cargar bajo demanda cuando se diseñe UI o se revise una interfaz.

## 10 heurísticas de Nielsen (Nielsen Norman Group)

1. **Visibilidad del estado del sistema** — el usuario siempre sabe qué está pasando
   (loaders, confirmaciones, estados activos). Nada de acciones mudas.
2. **Correspondencia con el mundo real** — lenguaje y conceptos del usuario, no jerga técnica.
3. **Control y libertad del usuario** — salidas claras, deshacer/cancelar, no callejones sin salida.
4. **Consistencia y estándares** — mismos patrones en toda la app; respetar convenciones de plataforma.
5. **Prevención de errores** — evitar que el error ocurra (validación, confirmaciones en acciones destructivas) mejor que solo reportarlo.
6. **Reconocer antes que recordar** — mostrar opciones visibles; no obligar a memorizar.
7. **Flexibilidad y eficiencia** — atajos para expertos sin estorbar a novatos.
8. **Diseño estético y minimalista** — cada elemento compite por atención; quitar lo que no aporta.
9. **Ayudar a reconocer y recuperarse de errores** — mensajes en lenguaje claro, con causa y solución.
10. **Ayuda y documentación** — accesible cuando se necesita, orientada a la tarea.

## Leyes de UX aplicables

- **Ley de Hick** — a más opciones, más tiempo de decisión. Reducir y agrupar opciones.
- **Ley de Fitts** — objetivos (botones) más grandes y cercanos = más fáciles de alcanzar.
  CTA principales con área de toque mínima 44x44px (táctil).
- **Ley de Jakob** — los usuarios esperan que tu producto funcione como los que ya conocen.
  No reinventar patrones estándar sin razón.
- **Ley de Miller** — ~7±2 elementos en memoria de trabajo. Chunkear información.
- **Umbral de Doherty** — respuesta del sistema < 400ms mantiene al usuario en flujo. Feedback inmediato.

## Principios de Gestalt (organización visual)

- **Proximidad** — elementos cercanos se perciben como grupo. Agrupar por espaciado, no por líneas.
- **Similitud** — elementos parecidos se perciben relacionados. Consistencia en botones, tarjetas.
- **Cierre / continuidad** — el ojo completa formas y sigue líneas. Guiar el recorrido visual.
- **Figura-fondo** — contraste claro entre contenido y fondo.
- **Jerarquía visual** — tamaño, peso, color y posición dirigen la atención en orden intencional.

## Accesibilidad (WCAG 2.1 AA — mínimo exigible)

- **Contraste**: texto normal ≥ 4.5:1, texto grande (≥18.66px bold / 24px) ≥ 3:1.
  El Azul Profundo (#0A2A43) sobre blanco cumple de sobra; verificar Naranja/Gris según uso.
- **No depender solo del color** — estados y errores con icono + texto, no solo tinte.
- **Foco visible** — todo elemento interactivo con indicador de foco claro (teclado).
- **Objetivos táctiles** ≥ 44x44px.
- **Texto alternativo** en imágenes/iconos informativos; `alt=""` en decorativos.
- **Estructura semántica** — headings jerárquicos (h1→h2→h3), landmarks, labels en formularios.
- **Navegable por teclado** — orden lógico de tabulación, sin trampas de foco.

> Nota de alcance: WCAG AA se valida con revisión automática + pruebas manuales con tecnología
> de asistencia (lectores de pantalla). La skill asegura las bases de diseño; la conformidad
> plena requiere testing dedicado.

## Checklist mínimo antes de dar por bueno un diseño

- [ ] Jerarquía visual clara (se entiende qué es primario/secundario en 3 segundos).
- [ ] Contraste WCAG AA verificado en texto y controles.
- [ ] Estados definidos: default, hover, focus, active, disabled, loading, error, vacío.
- [ ] Objetivos táctiles ≥ 44px; espaciado por la escala, no arbitrario.
- [ ] Feedback de sistema en toda acción (nada mudo).
- [ ] Navegable por teclado con foco visible.
- [ ] Mensajes de error con causa + solución, en lenguaje claro.
