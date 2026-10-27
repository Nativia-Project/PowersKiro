---
name: "grafica-nativia"
displayName: "Gru{00E1}fica Nativia v1.4.0"
description: "v1.4.0 u{00B7} v1.4.0 Â· Aplica la identidad visual de marca Nativia (Cloud & IA) y estÃ¡ndares de usabilidad de la industria (Nielsen, WCAG AA, Gestalt) a cualquier diseÃ±o o interfaz. Ãšsala al crear o revisar UI, componentes, landings, dashboards, presentaciones o piezas grÃ¡ficas, para que el resultado siga la marca y NO sea un diseÃ±o genÃ©rico de IA."
keywords: ["nativia", "diseÃ±o", "design", "marca", "branding", "ui", "ux", "usabilidad", "wcag", "accesibilidad", "dashboard", "landing", "componentes", "identidad visual", "cloud", "ia"]
author: "Nativia"
version: "1.4.0"
license: "UNLICENSED"
---

# GrÃ¡fica Nativia

Power que empaqueta la identidad visual oficial de **Nativia - Cloud & IA** junto con estÃ¡ndares de
usabilidad de la industria, para que cualquier diseÃ±o generado respete la marca y evite el look
genÃ©rico de IA.

## QuÃ© incluye

- **Skill `diseno-nativia`** â€” reglas de marca + usabilidad, activada automÃ¡ticamente al pedir diseÃ±o.
- **Tokens de marca** (`design-tokens.json`) â€” paleta, tipografÃ­a, espaciado y radios oficiales,
  extraÃ­dos del Manual de Identidad Visual Nativia V2.
- **Logos** (`assets/logos/`) â€” isotipo en variantes para fondo claro y oscuro, con y sin fondo (SVG + PNG).
- **Plantillas de presentaciÃ³n** (`assets/plantillas/`) â€” `deck-base.html` (deck navegable con
  portada, agenda, header de logo, nav inferior, barra de progreso y bloque de impresiÃ³n a PDF) y
  `deck-seguimiento.html` (variante para reuniones de seguimiento con Carta Gantt). Incluyen sus
  logos en `assets/plantillas/assets/`. Son el punto de partida para construir cualquier deck.
- **Referencias de usabilidad** â€” heurÃ­sticas de Nielsen, leyes de UX, Gestalt y WCAG 2.1 AA.
- **CatÃ¡logo anti-genÃ©rico** â€” los "tells" de diseÃ±o IA a evitar activamente.

## Estructura

```
grafica-nativia/
â”œâ”€â”€ POWER.md                        # Este manifiesto + documentaciÃ³n
â”œâ”€â”€ plugin.json                     # Manifiesto Agent Plugins
â””â”€â”€ skills/
    â””â”€â”€ diseno-nativia/
        â”œâ”€â”€ SKILL.md                # Reglas, resumen de marca y checklist
        â”œâ”€â”€ references/
        â”‚   â”œâ”€â”€ principios-usabilidad.md
        â”‚   â”œâ”€â”€ presentaciones-slides.md
        â”‚   â””â”€â”€ anti-generico-ia.md
        â””â”€â”€ assets/
            â”œâ”€â”€ design-tokens.json  # Marca real (colores, tipografÃ­a, escalas)
            â”œâ”€â”€ logos/              # Isotipo Nativia (SVG/PNG, por fondo)
            â””â”€â”€ plantillas/         # Plantillas de deck (base y seguimiento) + sus logos
                â”œâ”€â”€ deck-base.html
                â”œâ”€â”€ deck-seguimiento.html
                â””â”€â”€ assets/         # logo-claro.svg, logo-oscuro.svg, isotipo-color.png
```

## Marca Nativia (resumen)

- **Paleta**: Azul Profundo `#0A2A43` (principal), escala azul `#164264` / `#225B86` / `#3075A9`,
  Naranja Vibrante `#F39221` (acento/CTA, escaso), Gris Corporativo `#58595B` (texto secundario).
- **TipografÃ­a**: geomÃ©trica (tipo Montserrat/Gotham) para tÃ­tulos; humanista para cuerpo.
- **AplicaciÃ³n**: fondos blancos por defecto; Azul Profundo en portadas/paneles; Naranja solo acciÃ³n.

## CÃ³mo usar

1. Instala el Power desde la pestaÃ±a **Powers â†’ Add Custom Power â†’ Import from Local Folder**,
   apuntando a esta carpeta.
2. Pide un diseÃ±o ("crea una landing", "revisa esta UI", "arma un dashboard"): la skill se activa sola.
3. Kiro cargarÃ¡ los tokens, aplicarÃ¡ las reglas de marca y usabilidad, y usarÃ¡ los logos reales.

## LÃ­mite honesto

Asegura las bases de marca y usabilidad y elimina los defaults genÃ©ricos obvios; no garantiza por sÃ­
solo un diseÃ±o excelente (eso depende del contexto y del criterio humano). La conformidad WCAG plena
requiere pruebas manuales con tecnologÃ­a de asistencia.
