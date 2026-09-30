# Reglas de Negocio — andercal.visuals — Selector

- **RN-001 (Identificador único):** Una fotografía será identificada primariamente por un código numérico de 4 dígitos extraído del nombre del archivo o del texto de entrada.
- **RN-002 (Extensiones explícitas):** El sistema procesará únicamente las extensiones de archivo que el usuario haya seleccionado en la interfaz. No se asumirá arbitrariamente una extensión si no fue marcada.
- **RN-003 (Sidecar XMP):** Para las extensiones XMP, el sistema buscará tanto la convención simple (`<nombre>.xmp`) como la convención doble (`<nombre>.<ext_raw>.xmp`).
- **RN-004 (Inhabilitación por inconsistencia):** El botón de ejecución (`Copiar` / `Mover`) permanecerá deshabilitado o requerirá confirmación explícita si existen códigos solicitados sin archivos correspondientes en las extensiones seleccionadas.
- **RN-005 (Destino seguro):** Los archivos procesados se almacenarán exclusivamente en una subcarpeta llamada `Seleccionadas/` dentro de la carpeta de trabajo.
- **RN-006 (Protección anti-sobrescritura):** Si un archivo ya existe en el destino, el sistema advertirá y renombrará o solicitará confirmación antes de proceder.
