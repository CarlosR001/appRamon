import tkinter as tk
from tkinter import ttk, messagebox

class AddEditClientView(tk.Toplevel):
    def __init__(self, parent, controller, client_data=None):
        super().__init__(parent)
        self.controller = controller
        self.client_data = client_data
        self.is_edit_mode = client_data is not None

        # --- Window Setup ---
        self.title("Editar Cliente" if self.is_edit_mode else "Añadir Nuevo Cliente")
        self.geometry("400x250")
        self.resizable(False, False)
        self.grab_set()

        # --- Widgets ---
        frame = ttk.Frame(self, padding="15")
        frame.pack(expand=True, fill="both")

        fields = ["Nombre:", "Teléfono:", "Email:", "Dirección:"]
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

        cancel_button = ttk.Button(button_frame, text="Cancelar", command=self.destroy)
        cancel_button.pack(side="left", padx=10)

        # Si estamos en modo edición, cargamos los datos
        if self.is_edit_mode:
            self.load_data()

    def load_data(self):
        self.entries["Nombre:"].insert(0, self.client_data.get('nombre', ''))
        self.entries["Teléfono:"].insert(0, self.client_data.get('telefono', ''))
        self.entries["Email:"].insert(0, self.client_data.get('email', ''))
        self.entries["Dirección:"].insert(0, self.client_data.get('direccion', ''))

    def save(self):
        """Recopila los datos y los envía al controlador."""
        data = {
            'nombre': self.entries["Nombre:"].get(),
            'telefono': self.entries["Teléfono:"].get(),
            'email': self.entries["Email:"].get(),
            'direccion': self.entries["Dirección:"].get()
        }

        if not data['nombre']:
            messagebox.showerror("Campo Requerido", "El nombre del cliente es obligatorio.", parent=self)
            return

        if self.is_edit_mode:
            self.controller.update_client(self.client_data['id'], data)
        else:
            self.controller.add_client(data)
        
        self.destroy()
