import tkinter as tk
from tkinter import ttk, simpledialog, messagebox

class CategoriesView(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Gestión de Categorías")
        self.geometry("400x500")
        self.resizable(False, False)
        self.grab_set()

        self.controller = None # El controlador se asignará más tarde

        # --- Layout ---
        main_frame = ttk.Frame(self, padding=10)
        main_frame.pack(expand=True, fill="both")
        main_frame.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)

        # --- Treeview para mostrar categorías ---
        tree_frame = ttk.Frame(main_frame)
        tree_frame.grid(row=0, column=0, columnspan=3, sticky="nsew", pady=(0, 10))
        tree_frame.columnconfigure(0, weight=1)
        tree_frame.rowconfigure(0, weight=1)

        self.tree = ttk.Treeview(tree_frame, columns=("id", "nombre"), show="headings")
        self.tree.heading("id", text="ID")
        self.tree.heading("nombre", text="Nombre de la Categoría")
        self.tree.column("id", width=50, anchor=tk.CENTER)
        self.tree.grid(row=0, column=0, sticky="nsew")

        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky="ns")

        # --- Botones de Acción ---
        self.add_button = ttk.Button(main_frame, text="Añadir", style="Accent.TButton")
        self.add_button.grid(row=1, column=0, sticky="ew", padx=(0, 5))

        self.edit_button = ttk.Button(main_frame, text="Editar")
        self.edit_button.grid(row=1, column=1, sticky="ew", padx=5)
        
        self.delete_button = ttk.Button(main_frame, text="Eliminar")
        self.delete_button.grid(row=1, column=2, sticky="ew", padx=(5, 0))

    def set_controller(self, controller):
        self.controller = controller
        self.add_button.config(command=self.controller.add_category)
        self.edit_button.config(command=self.controller.edit_category)
        self.delete_button.config(command=self.controller.delete_category)

    def clear_tree(self):
        self.tree.delete(*self.tree.get_children())

    def insert_category(self, category):
        self.tree.insert("", tk.END, iid=category['id'], values=(category['id'], category['nombre']))

    def get_selected_category_id(self):
        selection = self.tree.selection()
        if selection:
            return self.tree.item(selection[0], "values")[0]
        return None
    
    def get_selected_category_name(self):
        selection = self.tree.selection()
        if selection:
            return self.tree.item(selection[0], "values")[1]
        return None

    def ask_category_name(self, title, prompt, initial_value=""):
        return simpledialog.askstring(title, prompt, initialvalue=initial_value, parent=self)

    def show_info(self, message):
        messagebox.showinfo("Información", message, parent=self)

    def show_error(self, message):
        messagebox.showerror("Error", message, parent=self)
        
    def confirm(self, title, message):
        return messagebox.askyesno(title, message, parent=self)
