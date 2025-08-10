import tkinter as tk
from tkinter import ttk, messagebox

class AddProductView(tk.Toplevel):
    def __init__(self, parent, categories):
        super().__init__(parent)
        self.parent = parent
        self.categories = categories

        self.title("Añadir Nuevo Producto")
        self.geometry("400x450")
        self.resizable(False, False)
        self.grab_set() # Hace que la ventana sea modal

        self.create_widgets()

    def create_widgets(self):
        frame = ttk.Frame(self, padding="10")
        frame.pack(expand=True, fill="both")

        # Campos del formulario
        fields = {
            "Código:": tk.StringVar(),
            "Nombre:": tk.StringVar(),
            "Descripción:": None, # Usaremos un Text widget
            "Precio Compra:": tk.DoubleVar(),
            "Precio Venta:": tk.DoubleVar(),
            "Stock Inicial:": tk.IntVar(),
            "Categoría:": tk.StringVar()
        }
        self.entries = {}

        # Crear labels y entries
        for i, (text, var) in enumerate(fields.items()):
            label = ttk.Label(frame, text=text)
            label.grid(row=i, column=0, padx=5, pady=8, sticky="w")

            if text == "Descripción:":
                self.entries[text] = tk.Text(frame, height=4, width=30)
                self.entries[text].grid(row=i, column=1, padx=5, pady=8, sticky="ew")
            elif text == "Categoría:":
                # Combobox para las categorías
                self.entries[text] = ttk.Combobox(frame, textvariable=var, state="readonly")
                self.entries[text]['values'] = [cat['nombre'] for cat in self.categories]
                self.entries[text].grid(row=i, column=1, padx=5, pady=8, sticky="ew")
            else:
                self.entries[text] = ttk.Entry(frame, textvariable=var)
                self.entries[text].grid(row=i, column=1, padx=5, pady=8, sticky="ew")

        # Botones
        button_frame = ttk.Frame(frame)
        button_frame.grid(row=len(fields), column=0, columnspan=2, pady=20)
        
        save_button = ttk.Button(button_frame, text="Guardar", command=self.save)
        save_button.pack(side="left", padx=10)

        cancel_button = ttk.Button(button_frame, text="Cancelar", command=self.destroy)
        cancel_button.pack(side="left", padx=10)
    
    def save(self):
        # La lógica de guardado la manejará el controlador
        try:
            # Recopilar datos de los widgets
            data = {
                'codigo': self.entries['Código:'].get(),
                'nombre': self.entries['Nombre:'].get(),
                'descripcion': self.entries['Descripción:'].get("1.0", tk.END).strip(),
                'precio_compra': self.entries['Precio Compra:'].get(),
                'precio_venta': self.entries['Precio Venta:'].get(),
                'stock': self.entries['Stock Inicial:'].get(),
                'categoria_nombre': self.entries['Categoría:'].get()
            }

            # Validar que los campos no estén vacíos
            if not all([data['codigo'], data['nombre'], data['precio_venta'], data['categoria_nombre']]):
                messagebox.showerror("Error de Validación", "Código, Nombre, Precio Venta y Categoría son campos obligatorios.", parent=self)
                return

            # Buscar el ID de la categoría seleccionada
            cat_id = next((cat['id'] for cat in self.categories if cat['nombre'] == data['categoria_nombre']), None)
            if cat_id is None:
                messagebox.showerror("Error de Categoría", "La categoría seleccionada no es válida.", parent=self)
                return
            
            data['id_categoria'] = cat_id
            
            # Pasar los datos al controlador a través del método de la ventana principal
            self.parent.controller.save_new_product(data)
            self.destroy()

        except tk.TclError as e:
            messagebox.showerror("Error de Tipo de Dato", f"Por favor, ingrese un número válido en los campos de precio y stock.\n({e})", parent=self)
        except Exception as e:
            messagebox.showerror("Error Inesperado", f"Ocurrió un error: {e}", parent=self)
