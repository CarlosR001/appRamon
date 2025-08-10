import tkinter as tk
from tkinter import ttk, messagebox

class EditProductView(tk.Toplevel):
    def __init__(self, parent, product_data, categories):
        super().__init__(parent)
        self.parent = parent
        self.product_data = product_data
        self.categories = categories

        self.title("Editar Producto")
        self.geometry("400x450")
        self.resizable(False, False)
        self.grab_set()

        self.create_widgets()
        self.load_product_data()

    def create_widgets(self):
        frame = ttk.Frame(self, padding="10")
        frame.pack(expand=True, fill="both")

        # --- Campos del formulario ---
        self.entries = {}
        fields = ["Código:", "Nombre:", "Descripción:", "Precio Compra:", "Precio Venta:", "Stock:", "Categoría:"]
        
        for i, text in enumerate(fields):
            label = ttk.Label(frame, text=text)
            label.grid(row=i, column=0, padx=5, pady=8, sticky="w")

            if text == "Descripción:":
                self.entries[text] = tk.Text(frame, height=4, width=30)
            elif text == "Categoría:":
                self.entries[text] = ttk.Combobox(frame, state="readonly")
                self.entries[text]['values'] = [cat['nombre'] for cat in self.categories]
            else:
                self.entries[text] = ttk.Entry(frame)
            
            self.entries[text].grid(row=i, column=1, padx=5, pady=8, sticky="ew")

        # --- Botones ---
        button_frame = ttk.Frame(frame)
        button_frame.grid(row=len(fields), column=0, columnspan=2, pady=20)
        
        save_button = ttk.Button(button_frame, text="Guardar Cambios", command=self.save, style="Accent.TButton")
        save_button.pack(side="left", padx=10)

        cancel_button = ttk.Button(button_frame, text="Cancelar", command=self.destroy)
        cancel_button.pack(side="left", padx=10)
    
    def load_product_data(self):
        """Carga los datos del producto en los campos del formulario."""
        self.entries["Código:"].insert(0, self.product_data.get('codigo', ''))
        self.entries["Nombre:"].insert(0, self.product_data.get('nombre', ''))
        self.entries["Descripción:"].insert("1.0", self.product_data.get('descripcion', ''))
        self.entries["Precio Compra:"].insert(0, self.product_data.get('precio_compra', 0.0))
        self.entries["Precio Venta:"].insert(0, self.product_data.get('precio_venta', 0.0))
        self.entries["Stock:"].insert(0, self.product_data.get('stock', 0))
        
        # Seleccionar la categoría actual en el Combobox
        current_category_name = self.product_data.get('categoria', '')
        self.entries["Categoría:"].set(current_category_name)

    def save(self):
        """Recopila los datos y los pasa al controlador para guardarlos."""
        try:
            updated_data = {
                'codigo': self.entries['Código:'].get(),
                'nombre': self.entries['Nombre:'].get(),
                'descripcion': self.entries['Descripción:'].get("1.0", tk.END).strip(),
                'precio_compra': float(self.entries['Precio Compra:'].get()),
                'precio_venta': float(self.entries['Precio Venta:'].get()),
                'stock': int(self.entries['Stock:'].get()),
                'categoria_nombre': self.entries['Categoría:'].get()
            }

            if not all([updated_data['codigo'], updated_data['nombre'], updated_data['precio_venta'], updated_data['categoria_nombre']]):
                messagebox.showerror("Error de Validación", "Código, Nombre, Precio Venta y Categoría son campos obligatorios.", parent=self)
                return

            cat_id = next((cat['id'] for cat in self.categories if cat['nombre'] == updated_data['categoria_nombre']), None)
            if cat_id is None:
                messagebox.showerror("Error de Categoría", "La categoría seleccionada no es válida.", parent=self)
                return
            
            updated_data['id_categoria'] = cat_id
            
            # Llamada al controlador corregida
            self.parent.controllers['products'].update_existing_product(self.product_data['id'], updated_data)
            self.destroy()

        except (ValueError, tk.TclError):
            messagebox.showerror("Error de Tipo de Dato", "Por favor, ingrese un número válido en los campos de precio y stock.", parent=self)
        except Exception as e:
            messagebox.showerror("Error Inesperado", f"Ocurrió un error: {e}", parent=self)
