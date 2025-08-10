import tkinter as tk
from tkinter import ttk, messagebox

class AddEditSupplierView(tk.Toplevel):
    def __init__(self, parent, controller, supplier_data=None):
        super().__init__(parent)
        self.controller = controller
        self.supplier_data = supplier_data
        self.is_edit_mode = supplier_data is not None

        # --- Window Setup ---
        self.title("Editar Proveedor" if self.is_edit_mode else "Añadir Nuevo Proveedor")
        self.geometry("400x220")
        self.resizable(False, False)
        self.grab_set()

        # --- Widgets ---
        frame = ttk.Frame(self, padding="15")
        frame.pack(expand=True, fill="both")

        fields = ["Nombre:", "Teléfono:", "Email:"]
        self.entries = {}

        for i, text in enumerate(fields):
            label = ttk.Label(frame, text=text)
            label.grid(row=i, column=0, padx=5, pady=8, sticky="w")
            
            entry = ttk.Entry(frame)
            entry.grid(row=i, column=1, padx=5, pady=8, sticky="ew")
            self.entries[text] = entry
        
        frame.columnconfigure(1, weight=1)

        # --- Buttons ---
        button_frame = ttk.Frame(frame)
        button_frame.grid(row=len(fields), column=0, columnspan=2, pady=(20, 0))

        save_text = "Guardar Cambios" if self.is_edit_mode else "Guardar"
        save_button = ttk.Button(button_frame, text=save_text, command=self.save, style="Accent.TButton")
        save_button.pack(side="left", padx=10)

        cancel_button = ttk.Button(button_frame, text="Cancelar", command=self.controller.close_add_edit_window)
        cancel_button.pack(side="left", padx=10)

        if self.is_edit_mode:
            self.load_data()

    def load_data(self):
        self.entries["Nombre:"].insert(0, self.supplier_data.get('nombre', ''))
        self.entries["Teléfono:"].insert(0, self.supplier_data.get('telefono', ''))
        self.entries["Email:"].insert(0, self.supplier_data.get('email', ''))

    def save(self):
        """Recopila los datos y los envía al controlador."""
        data = {
            'nombre': self.entries["Nombre:"].get(),
            'telefono': self.entries["Teléfono:"].get(),
            'email': self.entries["Email:"].get()
        }

        if not data['nombre']:
            messagebox.showerror("Campo Requerido", "El nombre del proveedor es obligatorio.", parent=self)
            return

        if self.is_edit_mode:
            self.controller.update_supplier(self.supplier_data['id'], data)
        else:
            self.controller.add_supplier(data)
