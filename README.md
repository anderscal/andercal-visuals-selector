# andercal.visuals — Selector

**Selector** es una aplicación de escritorio para Windows desarrollada en **Python** con **CustomTkinter**, diseñada para la localización, verificación y traslado automatizado de archivos fotográficos (RAW y sidecars XMP) asociados a listados de códigos numéricos de fotografía.

---

## 📌 Características Principales

- 🔍 **Extracción inteligente de códigos:** Extrae identificadores de 4 dígitos a partir de texto sucio, tablas, nombres de archivo o listas.
- ⚙️ **Formatos configurables:** Soporte para múltiples formatos RAW (CR3, CR2, NEF, ARW, DNG, RAF, etc.) y sidecars XMP simples (`foto.xmp`) y dobles (`foto.CR3.xmp`).
- 🛡️ **Verificación estricta:** Diagnóstico en tiempo real antes de cualquier movimiento (conteo de recibidos, encontrados, faltantes y colisiones).
- 👁️ **Vista previa previa a la ejecución:** Confirmación visual antes de mover o copiar archivos hacia la carpeta `/Seleccionadas`.
- 💾 **Persistencia local:** Recuerda la última carpeta utilizada y las preferencias de formatos en archivos JSON locales.

---

## 📁 Estructura del Proyecto

```text
.
├── src/            # Código fuente de la aplicación (core, gui, config)
├── config/         # Archivos de configuración JSON (formats.json, settings.json)
├── docs/           # Documentación técnica del proyecto
├── tests/          # Pruebas automatizadas con pytest
├── assets/         # Recursos gráficos (iconos, temas)
├── README.md       # Presentación principal del repositorio
├── APRENDIDO.txt   # Bitácora de aprendizaje y conceptos técnicos
└── .gitignore      # Archivos excluidos del control de versiones
```

---

## 🚀 Requisitos e Instalación

### Requisitos previos
- **Python 3.10** o superior
- **Git**

### Instalación
```bash
# Instalar dependencias
pip install -r requirements.txt
```

---

## ✒️ Autor

- **Anderscal** ([@calderonanderson78@gmail.com](mailto:calderonanderson78@gmail.com)) — *fotografía & desarrollo de software*.
