# Registro de Cambios (Changelog) — andercal.visuals — Selector

Todos los cambios notables de este proyecto serán documentados en este archivo.
El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/) y este proyecto adhiere a [Semantic Versioning](https://semver.org/lang/es/).

---

## [1.0.0] - 2026-09-30

### ✨ Añadido
- **Motor Central (`src/core/`):**
  - Extractor inteligente de códigos de 4 dígitos (`parser.py`) con filtrado automático de fechas (`9/28/2026`, `2026-09-28`).
  - Escáner de carpetas (`scanner.py`) con soporte multiformato RAW (CR3, CR2, NEF, ARW, DNG, etc.) y sidecars XMP simples y dobles (`.CR3.xmp`).
  - Validador de diagnóstico (`validator.py`) con detección de faltantes, ambigüedades y cálculo de procesabilidad parcial.
  - Gestor de transferencia (`mover.py`) con soporte de Copiar/Mover, preservación de metadatos (`shutil.copy2`), creación automática de `/Seleccionadas` y sufijos incrementales anti-sobrescritura (`_1`).

- **Capa de Configuración (`src/config/`):**
  - Persistencia en JSON (`settings.json` y `formats.json`) para recordar la última carpeta y preferencias de extensiones.
  - Función de adición de extensiones personalizadas por el usuario (`add_custom_format`) en tiempo real.

- **Interfaz Gráfica Moderna (`src/gui/`):**
  - Desarrollada en **CustomTkinter** con tema oscuro y centrado dinámico de pantalla.
  - Panel interactivo para pegar listas, explorar carpetas y agregar extensiones personalizadas.
  - Modal de Vista Previa (`preview_dialog.py`) con desglose de archivos a procesar y advertencias de faltantes omitidos.

- **Pruebas Automatizadas (`tests/`):**
  - Suite de integración unificada con `pytest` alcanzando 100% de cobertura del motor central.

- **Empaquetado:**
  - Compilación a ejecutable nativo de Windows `dist/andercal.visuals - Selector.exe` mediante `PyInstaller`.

- **Control de Versiones y Documentación:**
  - Repositorio oficial conectado en GitHub: `https://github.com/anderscal/andercal-visuals-selector.git`.
  - Bitácora de aprendizaje continua en `APRENDIDO.txt`.
