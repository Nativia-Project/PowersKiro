# PowersKiro

Repositorio de Powers de Kiro de Nativia. Cada Power vive en su propia carpeta en la raiz
y se instala en Kiro como "Custom Power".

## Powers disponibles

### 1. grafica-nativia

Aplica la identidad visual de marca Nativia (Cloud & IA) y estandares de usabilidad de la
industria (Nielsen, WCAG AA, Gestalt) a cualquier diseno o interfaz. Incluye la skill
`diseno-nativia`, los tokens de marca, los logos oficiales y las referencias de usabilidad.

## Como instalar un Power en Kiro

1. Clona o descarga este repositorio.
2. En Kiro, abre la pestana Powers.
3. Elige "Add Custom Power" y luego "Import from Local Folder".
4. Apunta a la carpeta del Power que quieras instalar (por ejemplo, `grafica-nativia`),
   NO a la raiz del repositorio.
5. El Power queda instalado y sus skills se activan solas cuando corresponde.

## Estructura de un Power

Cada carpeta de Power debe tener el `plugin.json` en su raiz. Esta es la estructura que
Kiro espera encontrar al importar:

```
grafica-nativia/
├── plugin.json                     # Manifiesto del Power (en la raiz de la carpeta)
├── POWER.md                        # Documentacion del Power
└── skills/
    └── diseno-nativia/
        ├── SKILL.md
        ├── references/
        └── assets/
```

Importante: al importar, se apunta a la carpeta del Power (la que contiene `plugin.json`),
no a una carpeta que la envuelva. Si el Power queda anidado un nivel de mas, Kiro no
encuentra las skills ni los assets.
