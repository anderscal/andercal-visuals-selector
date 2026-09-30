"""
src/gui/main_window.py
Ventana principal de la aplicación andercal.visuals — Selector desarrollada con CustomTkinter.
"""

import customtkinter as ctk
from tkinter import filedialog, messagebox
from pathlib import Path
from typing import Dict, List, Any

from src.config.settings_manager import (
    load_settings,
    save_settings,
    load_formats,
    add_custom_format
)
from src.core.validator import validate_photo_selection
from src.core.mover import process_files
from src.gui.preview_dialog import PreviewDialog

# Configuración visual de CustomTkinter
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class MainWindow(ctk.CTk):
    """
    Ventana principal de escritorio para la selección y traslado de fotografías.
    """

    def __init__(self):
        super().__init__()

        self.title("andercal.visuals — Selector")
        
        # Centrar ventana dinámicamente en la pantalla del usuario
        width = 850
        height = 640
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        
        x = (screen_width - width) // 2
        y = max(20, (screen_height - height) // 2 - 30) # Ligeramente desplazado hacia arriba
        
        self.geometry(f"{width}x{height}+{x}+{y}")
        self.minsize(750, 500)

        # Estado interno
        self.settings = load_settings()
        self.available_formats = load_formats()
        self.checkbox_vars: Dict[str, ctk.BooleanVar] = {}
        self.last_validation_report: Dict[str, Any] = {}

        self._build_ui()
        self._load_initial_state()


    def _build_ui(self):
        # 1. ENCABEZADO
        header_frame = ctk.CTkFrame(self, fg_color="#1e1e1e", corner_radius=0)
        header_frame.pack(fill="x", padx=0, pady=0)

        title_label = ctk.CTkLabel(
            header_frame,
            text="andercal.visuals",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color="#4fc3f7"
        )
        title_label.pack(side="left", padx=20, pady=12)

        subtitle_label = ctk.CTkLabel(
            header_frame,
            text="SELECTOR DE FOTOGRAFÍAS v1.0.0",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#aaaaaa"
        )
        subtitle_label.pack(side="right", padx=20, pady=12)

        # SCROLLABLE CONTAINER PRINCIPAL
        main_scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        main_scroll.pack(fill="both", expand=True, padx=15, pady=10)

        # 2. SECCIÓN: CARPETA DE TRABAJO
        folder_frame = ctk.CTkFrame(main_scroll, corner_radius=10)
        folder_frame.pack(fill="x", padx=5, pady=8)

        folder_title = ctk.CTkLabel(
            folder_frame,
            text="📁 1. CARPETA DE TRABAJO (ORIGEN)",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        folder_title.pack(anchor="w", padx=15, pady=(10, 5))

        folder_input_frame = ctk.CTkFrame(folder_frame, fg_color="transparent")
        folder_input_frame.pack(fill="x", padx=15, pady=(0, 10))

        self.folder_entry = ctk.CTkEntry(
            folder_input_frame,
            placeholder_text="Selecciona la carpeta donde están tus fotografías...",
            font=ctk.CTkFont(size=12)
        )
        self.folder_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))

        btn_browse = ctk.CTkButton(
            folder_input_frame,
            text="Buscar carpeta...",
            width=140,
            command=self._on_browse_folder
        )
        btn_browse.pack(side="right")

        # 3. SECCIÓN: ENTRADA DE LISTA / NOMBRES
        list_frame = ctk.CTkFrame(main_scroll, corner_radius=10)
        list_frame.pack(fill="x", padx=5, pady=8)

        list_title = ctk.CTkLabel(
            list_frame,
            text="📋 2. PEGA AQUÍ LA LISTA O NOMBRES DE FOTOGRAFÍAS",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        list_title.pack(anchor="w", padx=15, pady=(10, 5))

        self.textbox_input = ctk.CTkTextbox(
            list_frame,
            height=130,
            font=ctk.CTkFont(family="Consolas", size=12)
        )
        self.textbox_input.pack(fill="x", padx=15, pady=(0, 10))

        # 4. SECCIÓN: FORMATOS A PROCESAR (CON ADICIÓN PERSONALIZADA)
        formats_frame = ctk.CTkFrame(main_scroll, corner_radius=10)
        formats_frame.pack(fill="x", padx=5, pady=8)

        formats_header = ctk.CTkFrame(formats_frame, fg_color="transparent")
        formats_header.pack(fill="x", padx=15, pady=(10, 5))

        formats_title = ctk.CTkLabel(
            formats_header,
            text="⚙️ 3. FORMATOS A PROCESAR",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        formats_title.pack(side="left")

        # Fila para añadir formato personalizado
        custom_fmt_frame = ctk.CTkFrame(formats_header, fg_color="transparent")
        custom_fmt_frame.pack(side="right")

        self.entry_custom_fmt = ctk.CTkEntry(
            custom_fmt_frame,
            placeholder_text="Ej: PSD, TIFF, PNG...",
            width=150,
            font=ctk.CTkFont(size=11)
        )
        self.entry_custom_fmt.pack(side="left", padx=(0, 5))

        btn_add_fmt = ctk.CTkButton(
            custom_fmt_frame,
            text="➕ Agregar extensión",
            width=130,
            fg_color="#37474f",
            hover_color="#455a64",
            command=self._on_add_custom_format
        )
        btn_add_fmt.pack(side="right")

        # Contenedor de Checkboxes
        self.checkboxes_container = ctk.CTkFrame(formats_frame, fg_color="transparent")
        self.checkboxes_container.pack(fill="x", padx=15, pady=(5, 10))

        self._render_format_checkboxes()

        # 5. SECCIÓN: ACCIÓN Y VERIFICACIÓN
        action_frame = ctk.CTkFrame(main_scroll, corner_radius=10)
        action_frame.pack(fill="x", padx=5, pady=8)

        action_title = ctk.CTkLabel(
            action_frame,
            text="🔄 4. ACCIÓN A REALIZAR",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        action_title.pack(anchor="w", padx=15, pady=(10, 5))

        self.action_var = ctk.StringVar(value=self.settings.get("default_action", "copy"))

        radio_copy = ctk.CTkRadioButton(
            action_frame,
            text="Copiar (Recomendado: mantiene originales en la raíz)",
            variable=self.action_var,
            value="copy"
        )
        radio_copy.pack(anchor="w", padx=25, pady=4)

        radio_move = ctk.CTkRadioButton(
            action_frame,
            text="Mover (Traslada físicamente a /Seleccionadas)",
            variable=self.action_var,
            value="move"
        )
        radio_move.pack(anchor="w", padx=25, pady=(4, 10))

        # 6. SECCIÓN: BOTÓN VERIFICAR Y RESULTADOS
        verify_frame = ctk.CTkFrame(main_scroll, corner_radius=10)
        verify_frame.pack(fill="x", padx=5, pady=8)

        btn_verify = ctk.CTkButton(
            verify_frame,
            text="🔍 VERIFICAR ARCHIVOS",
            font=ctk.CTkFont(size=15, weight="bold"),
            height=40,
            fg_color="#1976d2",
            hover_color="#1565c0",
            command=self._on_verify
        )
        btn_verify.pack(fill="x", padx=15, pady=12)

        # Panel de diagnóstico
        self.diag_textbox = ctk.CTkTextbox(
            verify_frame,
            height=130,
            font=ctk.CTkFont(family="Consolas", size=12),
            state="disabled"
        )
        self.diag_textbox.pack(fill="x", padx=15, pady=(0, 10))

        # BOTÓN FINAL: VISTA PREVIA Y EJECUTAR
        self.btn_execute = ctk.CTkButton(
            verify_frame,
            text="🚀 VISTA PREVIA Y PROCESAR",
            font=ctk.CTkFont(size=16, weight="bold"),
            height=45,
            fg_color="#2e7d32",
            hover_color="#1b5e20",
            state="disabled",
            command=self._on_show_preview
        )
        self.btn_execute.pack(fill="x", padx=15, pady=(0, 15))

    def _render_format_checkboxes(self):
        """Renderiza la cuadrícula de checkboxes de formatos disponibles."""
        for widget in self.checkboxes_container.winfo_children():
            widget.destroy()

        selected_saved = set(self.settings.get("selected_extensions", ["CR3", "XMP"]))

        col_max = 6
        for i, fmt in enumerate(self.available_formats):
            row = i // col_max
            col = i % col_max

            if fmt not in self.checkbox_vars:
                # Si el formato estaba guardado previamente, lo marcamos
                is_checked = fmt in selected_saved
                self.checkbox_vars[fmt] = ctk.BooleanVar(value=is_checked)

            chk = ctk.CTkCheckBox(
                self.checkboxes_container,
                text=fmt,
                variable=self.checkbox_vars[fmt],
                font=ctk.CTkFont(size=12, weight="bold"),
                command=self._save_current_settings
            )
            chk.grid(row=row, column=col, padx=10, pady=6, sticky="w")

    def _load_initial_state(self):
        """Carga la ruta guardada previamente."""
        last_dir = self.settings.get("last_directory", "")
        if last_dir:
            self.folder_entry.insert(0, last_dir)

    def _save_current_settings(self):
        """Guarda el estado actual en settings.json."""
        current_dir = self.folder_entry.get().strip()
        active_exts = [
            fmt for fmt, var in self.checkbox_vars.items() if var.get()
        ]

        self.settings["last_directory"] = current_dir
        self.settings["selected_extensions"] = active_exts
        self.settings["default_action"] = self.action_var.get()

        save_settings(self.settings)

    def _on_browse_folder(self):
        """Abre el explorador de archivos de Windows."""
        initial = self.folder_entry.get().strip() or str(Path.home())
        selected = filedialog.askdirectory(initialdir=initial, title="Seleccionar carpeta de fotografías")
        if selected:
            self.folder_entry.delete(0, "end")
            self.folder_entry.insert(0, selected)
            self._save_current_settings()

    def _on_add_custom_format(self):
        """Añade un nuevo formato personalizado ingresado por el usuario."""
        new_ext = self.entry_custom_fmt.get().strip().lstrip(".").upper()
        if not new_ext:
            return

        self.available_formats = add_custom_format(new_ext)

        # Marcar la nueva extensión por defecto
        self.checkbox_vars[new_ext] = ctk.BooleanVar(value=True)

        self._render_format_checkboxes()
        self._save_current_settings()
        self.entry_custom_fmt.delete(0, "end")

        messagebox.showinfo(
            "Formato Añadido",
            f"La extensión '{new_ext}' ha sido agregada correctamente al catálogo."
        )

    def _get_active_extensions(self) -> List[str]:
        return [fmt for fmt, var in self.checkbox_vars.items() if var.get()]

    def _update_diag_textbox(self, text: str):
        self.diag_textbox.configure(state="normal")
        self.diag_textbox.delete("1.0", "end")
        self.diag_textbox.insert("1.0", text)
        self.diag_textbox.configure(state="disabled")

    def _on_verify(self):
        """Ejecuta el análisis de diagnóstico."""
        folder_path = self.folder_entry.get().strip()
        raw_input = self.textbox_input.get("1.0", "end-1c").strip()
        active_exts = self._get_active_extensions()

        if not folder_path or not Path(folder_path).is_dir():
            messagebox.showerror("Error de Carpeta", "Por favor selecciona una carpeta de origen válida.")
            return

        if not raw_input:
            messagebox.showwarning("Entrada Vacía", "Por favor pega la lista o nombres de fotografías a procesar.")
            return

        if not active_exts:
            messagebox.showwarning("Formatos no seleccionados", "Selecciona al menos una extensión a procesar.")
            return

        self._save_current_settings()

        # Ejecutar validación
        report = validate_photo_selection(folder_path, raw_input, active_exts)
        self.last_validation_report = report

        # Construir informe de diagnóstico
        diag_lines = []
        diag_lines.append(f"📊 DIAGNÓSTICO DE LA SELECCIÓN")
        diag_lines.append(f"--------------------------------------------------")
        diag_lines.append(f"• Códigos únicos identificados : {report['total_codes']}")

        diag_lines.append(f"• Archivos encontrados por extensión:")
        for ext, count in report['found_counts'].items():
            diag_lines.append(f"    - {ext}: {count} encontrados")

        if report['missing_details']:
            diag_lines.append(f"\n⚠️ ARCHIVOS FALTANTES REGISTRADOS ({len(report['missing_details'])} códigos):")
            for code, missing_exts in report['missing_details'].items():
                diag_lines.append(f"    - Código {code}: Falta [{', '.join(missing_exts)}]")
        else:
            diag_lines.append(f"\n✔ NINGÚN ARCHIVO FALTANTE. Todos los códigos están completos.")

        if report['ambiguous_details']:
            diag_lines.append(f"\n⚠️ AMBIGÜEDADES / COLISIONES DETECTADAS:")
            for code in report['ambiguous_details']:
                diag_lines.append(f"    - Código {code}: Múltiples archivos encontrados para el mismo número.")

        self._update_diag_textbox("\n".join(diag_lines))

        # Habilitar botón si es válido
        if report['is_valid_for_operation']:
            self.btn_execute.configure(state="normal", fg_color="#2e7d32")
        else:
            self.btn_execute.configure(state="disabled", fg_color="#555555")

    def _on_show_preview(self):
        """Abre la ventana modal de vista previa."""
        if not self.last_validation_report or not self.last_validation_report.get("is_valid_for_operation"):
            return

        folder_path = self.folder_entry.get().strip()
        dest_dir = str(Path(folder_path) / "Seleccionadas")
        action = self.action_var.get()
        files = self.last_validation_report.get("files_to_process", [])

        PreviewDialog(
            parent=self,
            source_dir=folder_path,
            dest_dir=dest_dir,
            action=action,
            files_to_process=files,
            on_confirm_callback=self._execute_process
        )

    def _execute_process(self):
        """Ejecuta la copia o movimiento final tras la confirmación en el modal."""
        folder_path = self.folder_entry.get().strip()
        action = self.action_var.get()
        files = self.last_validation_report.get("files_to_process", [])

        result = process_files(folder_path, files, action=action)

        if result["success"]:
            messagebox.showinfo(
                "¡Operación Exitosa!",
                f"Se han procesado correctamente {result['processed_count']} archivos hacia:\n{result['destination_directory']}"
            )
            # Re-verificar para actualizar estado
            self._on_verify()
        else:
            messagebox.showerror(
                "Error en Operación",
                f"Ocurrieron errores durante el proceso:\n{result.get('error_message', 'Revisa los permisos de archivo.')}"
            )
