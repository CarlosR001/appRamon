import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

class UpdateServiceView(tk.Toplevel):
    def __init__(self, parent, controller, service_data):
        super().__init__(parent)
        self.controller = controller
        self.service_data = service_data

        # --- Window Setup ---
        self.title(f"Actualizar Servicio #{service_data.get('id')}")
        self.geometry("450x500")
        self.resizable(False, False)
        self.grab_set()

        # --- Main Frame ---
        main_frame = ttk.Frame(self, padding=15)
        main_frame.pack(expand=True, fill="both")

        # --- Service Info (Read-only) ---
        info_frame = ttk.LabelFrame(main_frame, text="Detalles de la Orden", padding=10)
        info_frame.pack(fill="x", pady=(0, 15))
        info_frame.columnconfigure(1, weight=1)

        # Labels and data
        fecha_recepcion = service_data.get('fecha_recepcion', '')
        if isinstance(fecha_recepcion, datetime):
            fecha_recepcion = fecha_recepcion.strftime('%d/%m/%Y %H:%M')

        info_labels = {
            "Cliente:": service_data.get('nombre_cliente', 'N/A'),
            "Teléfono:": service_data.get('telefono_cliente', 'N/A'),
            "Equipo:": service_data.get('descripcion_equipo', ''),
            "Fecha Recepción:": fecha_recepcion
        }

        for i, (label_text, value_text) in enumerate(info_labels.items()):
            ttk.Label(info_frame, text=label_text, font=("Segoe UI", 10, "bold")).grid(row=i, column=0, sticky="nw", padx=5, pady=2)
            ttk.Label(info_frame, text=value_text, wraplength=300).grid(row=i, column=1, sticky="w", padx=5, pady=2)

        # --- Problem Description (Read-only) ---
        problem_frame = ttk.LabelFrame(main_frame, text="Problema Reportado", padding=10)
        problem_frame.pack(fill="x", pady=(0, 15))
        problem_text = tk.Text(problem_frame, height=5, state="disabled", background="gray20")
        problem_text.pack(fill="x", expand=True)
        problem_text.config(state="normal")
        problem_text.insert("1.0", service_data.get('problema_reportado', ''))
        problem_text.config(state="disabled")
        
        # --- Update Form ---
        update_frame = ttk.LabelFrame(main_frame, text="Actualizar Orden", padding=10)
        update_frame.pack(fill="x")
        update_frame.columnconfigure(1, weight=1)

        # Status
        ttk.Label(update_frame, text="Nuevo Estado:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.status_var = tk.StringVar()
        status_options = ['Recibido', 'En Diagnostico', 'Esperando Piezas', 'En Reparacion', 'Listo', 'Entregado']
        status_combobox = ttk.Combobox(update_frame, textvariable=self.status_var, values=status_options, state="readonly")
        status_combobox.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
        status_combobox.set(service_data.get('estado', 'Recibido'))

        # Final Cost
        ttk.Label(update_frame, text="Costo Final (S/):").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.cost_var = tk.DoubleVar(value=service_data.get('costo_servicio', 0.0))
        cost_entry = ttk.Entry(update_frame, textvariable=self.cost_var)
        cost_entry.grid(row=1, column=1, sticky="w", padx=5, pady=5)

        # --- Action Buttons ---
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(side="bottom", fill="x", pady=(15, 0))
        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)

        save_button = ttk.Button(button_frame, text="Guardar Cambios", style="Accent.TButton", command=self.save)
        save_button.grid(row=0, column=1, sticky="e")

        cancel_button = ttk.Button(button_frame, text="Cancelar", command=self.destroy)
        cancel_button.grid(row=0, column=0, sticky="w")

    def save(self):
        """Recopila los datos de actualización y los envía al controlador."""
        try:
            new_status = self.status_var.get()
            final_cost = self.cost_var.get()

            if not new_status:
                messagebox.showwarning("Estado no seleccionado", "Por favor, seleccione un nuevo estado para el servicio.", parent=self)
                return

            if final_cost < 0:
                messagebox.showwarning("Costo Inválido", "El costo del servicio no puede ser negativo.", parent=self)
                return

            update_data = {
                'id': self.service_data['id'],
                'status': new_status,
                'cost': final_cost
            }
            
            self.controller.update_service(update_data)
            self.destroy()

        except tk.TclError:
            messagebox.showerror("Dato Inválido", "Por favor, ingrese un costo numérico válido.", parent=self)
