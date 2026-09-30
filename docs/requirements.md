# Requisitos del Sistema — andercal.visuals — Selector

## Requisitos Funcionales (RF)

- **RF-001:** El sistema deberá permitir al usuario seleccionar una carpeta de origen mediante un explorador de archivos.
- **RF-002:** El sistema deberá permitir al usuario pegar texto con nombres de archivo, rutas, tablas o números de 4 dígitos.
- **RF-003:** El sistema deberá extraer e identificar de forma autónoma los códigos numéricos de 4 dígitos.
- **RF-004:** El sistema deberá permitir seleccionar cuáles extensiones de archivo procesar (RAWs: CR3, CR2, NEF, ARW, DNG, etc. y XMP).
- **RF-005:** El sistema deberá buscar únicamente las extensiones seleccionadas correspondientes a los códigos extraídos.
- **RF-006:** El sistema deberá presentar un informe de verificación detallando:
  - Total de códigos únicos recibidos.
  - Archivos encontrados por cada extensión seleccionada.
  - Archivos faltantes por cada extensión seleccionada.
- **RF-007:** El sistema deberá contar con una Vista Previa modal antes de ejecutar cualquier movimiento de archivos.
- **RF-008:** El sistema deberá permitir al usuario elegir entre el modo `Copiar` o `Mover` archivos a la subcarpeta `Seleccionadas/`.
- **RF-009:** El sistema deberá recordar la última carpeta de origen utilizada.
- **RF-010:** El sistema deberá recordar las extensiones seleccionadas por el usuario.

## Requisitos No Funcionales (RNF)

- **RNF-001:** La aplicación funcionará de manera 100% offline (sin dependencia de internet ni servidores externos).
- **RNF-002:** La interfaz será desarrollada con `CustomTkinter`, ofreciendo una estética moderna y soporte para temas.
- **RNF-003:** El sistema no sobreescribirá archivos de destino sin advertir previamente al usuario.
- **RNF-004:** El rendimiento del escaneo deberá ser eficiente incluso en carpetas con miles de fotografías.
