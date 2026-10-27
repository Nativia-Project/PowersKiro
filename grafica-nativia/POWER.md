---
name: "grafica-nativia"
displayName: "Gráfica Nativia"
description: "Aplica la identidad visual de marca Nativia (Cloud & IA) y estándares de usabilidad de la industria (Nielsen, WCAG AA, Gestalt) a cualquier diseño o interfaz. Úsala al crear o revisar UI, componentes, landings, dashboards, presentaciones o piezas gráficas, para que el resultado siga la marca y NO sea un diseño genérico de IA."
keywords: ["nativia", "diseño", "design", "marca", "branding", "ui", "ux", "usabilidad", "wcag", "accesibilidad", "dashboard", "landing", "componentes", "identidad visual", "cloud", "ia"]
author: "Nativia"
version: "1.2.0"
license: "UNLICENSED"
---

# Gráfica Nativia

Power que empaqueta la identidad visual oficial de **Nativia - Cloud & IA** junto con estándares de
usabilidad de la industria, para que cualquier diseño generado respete la marca y evite el look
genérico de IA.

## Qué incluye

- **Skill `diseno-nativia`** — reglas de marca + usabilidad, activada automáticamente al pedir diseño.
- **Tokens de marca** (`design-tokens.json`) — paleta, tipografía, espaciado y radios oficiales,
  extraídos del Manual de Identidad Visual Nativia V2.
- **Logos** (`assets/logos/`) — isotipo en variantes para fondo claro y oscuro, con y sin fondo (SVG + PNG).
- **Referencias de usabilidad** — heurísticas de Nielsen, leyes de UX, Gestalt y WCAG 2.1 AA.
- **Catálogo anti-genérico** — los "tells" de diseño IA a evitar activamente.

## Estructura

```
grafica-nativia/
├── POWER.md                        # Este manifiesto + documentación
├── plugin.json                     # Manifiesto Agent Plugins
└── skills/
    └── diseno-nativia/
        ├── SKILL.md                # Reglas, resumen de marca y checklist
        ├── references/
        │   ├── principios-usabilidad.md
        │   └── anti-generico-ia.md
        └── assets/
            ├── design-tokens.json  # Marca real (colores, tipografía, escalas)
            └── logos/              # Isotipo Nativia (SVG/PNG, por fondo)
```

## Marca Nativia (resumen)

- **Paleta**: Azul Profundo `#0A2A43` (principal), escala azul `#164264` / `#225B86` / `#3075A9`,
  Naranja Vibrante `#F39221` (acento/CTA, escaso), Gris Corporativo `#58595B` (texto secundario).
- **Tipografía**: geométrica (tipo Montserrat/Gotham) para títulos; humanista para cuerpo.
- **Aplicación**: fondos blancos por defecto; Azul Profundo en portadas/paneles; Naranja solo acción.

## Cómo usar

1. Instala el Power desde la pestaña **Powers → Add Custom Power → Import from Local Folder**,
   apuntando a esta carpeta.
2. Pide un diseño ("crea una landing", "revisa esta UI", "arma un dashboard"): la skill se activa sola.
3. Kiro cargará los tokens, aplicará las reglas de marca y usabilidad, y usará los logos reales.

## Límite honesto

Asegura las bases de marca y usabilidad y elimina los defaults genéricos obvios; no garantiza por sí
solo un diseño excelente (eso depende del contexto y del criterio humano). La conformidad WCAG plena
requiere pruebas manuales con tecnología de asistencia.
