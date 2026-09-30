# Arquitectura del Sistema — andercal.visuals — Selector

```text
               +-----------------------------------+
               |        GUI Layer (CustomTkinter)  |
               |  - main_window.py                 |
               |  - preview_dialog.py              |
               +-----------------+-----------------+
                                 |
                                 v
               +-----------------+-----------------+
               |        Core Engine Layer          |
               |  - parser.py    (Extracción)      |
               |  - scanner.py   (Búsqueda)        |
               |  - validator.py (Comprobación)    |
               |  - mover.py     (Operaciones E/S) |
               +-----------------+-----------------+
                                 |
                                 v
               +-----------------+-----------------+
               |       Config & System Layer       |
               |  - settings.json / formats.json   |
               |  - pathlib / os (File System)     |
               +-----------------------------------+
```

## Descripción de Capas

1. **GUI Layer (Interfaz de usuario):** Responsable de la presentación visual, captura de eventos y diálogo con el usuario.
2. **Core Engine Layer (Motor de negocios):** Contiene la lógica pura desvinculada de la interfaz gráfica. Facilita las pruebas unitarias.
3. **Config & System Layer (Capa de persistencia y SO):** Encargada del almacenamiento de configuraciones JSON y el acceso seguro al sistema de archivos local.
