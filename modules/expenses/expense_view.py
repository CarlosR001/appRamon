import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date

# Intentamos importar el widget de calendario. Si no está, usamos un Entry normal.
try:
    from tkcalendar import DateEntry
    calendar_available = True
except ImportError:
    calendar_available = False

class ExpensesView(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=15)
        self.controller = None

        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1) # La tabla se expandirá

        # --- Widgets ---
        self.create_add_expense_form()
        self.create_expenses_treeview()

    def set_controller(self, controller):
        self.controller = controller
        self.add_button.config(command=self.controller.add_expense)
        self.delete_button.config(command=self.controller.delete_expense)

    def create_add_expense_form(self):
        """Crea el formulario para añadir un nuevo gasto."""
        form_frame = ttk.LabelFrame(self, text="Registrar Nuevo Gasto", padding=10)
        form_frame.grid(row=0, column=0, sticky="ew", pady=(0, 15))
        form_frame.columnconfigure(1, weight=1) # El campo de descripción se expande

        # Descripción
        ttk.Label(form_frame, text="Descripción:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.description_var = tk.StringVar()
        description_entry = ttk.Entry(form_frame, textvariable=self.description_var)
        description_entry.grid(row=0, column=1, columnspan=3, padx=5, pady=5, sticky="ew")

        # Monto
        ttk.Label(form_frame, text="Monto (S/):").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.amount_var = tk.DoubleVar()
        amount_entry = ttk.Entry(form_frame, textvariable=self.amount_var)
        amount_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        # Fecha
        ttk.Label(form_frame, text="Fecha:").grid(row=1, column=2, padx=5, pady=5, sticky="e")
        if calendar_available:
            self.date_entry = DateEntry(form_frame, date_pattern='dd/mm/yyyy', width=12, background='darkblue', foreground='white', borderwidth=2)
            self.date_entry.set_date(date.today())
        else:
            self.date_entry = ttk.Entry(form_frame)
            self.date_entry.insert(0, date.today().strftime('%Y-%m-%d'))
        self.date_entry.grid(row=1, column=3, padx=5, pady=5, sticky="w")

        # Botón de Añadir
        self.add_button = ttk.Button(form_frame, text="Añadir Gasto", style="Accent.TButton")
        self.add_button.grid(row=2, column=0, columnspan=4, pady=(10,0), ipady=4, sticky="ew")

    def create_expenses_treeview(self):
        """Crea la tabla (Treeview) para mostrar los gastos."""
        list_frame = ttk.Frame(self)
        list_frame.grid(row=1, column=0, sticky="nsew")
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)
        
        # Botón de Eliminar
        self.delete_button = ttk.Button(list_frame, text="Eliminar Gasto Seleccionado")
        self.delete_button.pack(anchor="e", pady=(0,5))
        
        # Treeview
        self.tree = ttk.Treeview(list_frame, columns=("id", "fecha", "descripcion", "monto"), show="headings")
        self.tree.heading("id", text="ID")
        self.tree.heading("fecha", text="Fecha")
        self.tree.heading("descripcion", text="Descripción")
        self.tree.heading("monto", text="Monto")

        self.tree.column("id", width=50, anchor=tk.CENTER)
        self.tree.column("fecha", width=100, anchor=tk.CENTER)
        self.tree.column("descripcion", width=400)
        self.tree.column("monto", width=120, anchor=tk.E)

        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def get_expense_data(self):
        """Recupera los datos del formulario de nuevo gasto."""
        try:
            description = self.description_var.get()
            amount = self.amount_var.get()
            
            if calendar_available:
                expense_date = self.date_entry.get_date()
            else:
                expense_date = datetime.strptime(self.date_entry.get(), '%Y-%m-%d').date()

            if not description or amount <= 0:
                messagebox.showwarning("Datos incompletos", "La descripción y un monto mayor a cero son requeridos.", parent=self)
                return None
            
            return {'description': description, 'amount': amount, 'expense_date': expense_date}
        except (ValueError, tk.TclError):
            messagebox.showerror("Dato inválido", "Por favor, ingrese un monto numérico válido.", parent=self)
            return None
        except Exception as e:
            messagebox.showerror("Error de Fecha", f"El formato de la fecha no es válido: {e}", parent=self)
            return None

    def get_selected_expense_id(self):
        selection = self.tree.selection()
        if selection:
            return self.tree.item(selection[0], "values")[0]
        return None

    def clear_form(self):
        """Limpia los campos del formulario después de añadir un gasto."""
        self.description_var.set("")
        self.amount_var.set(0.0)
        if calendar_available:
            self.date_entry.set_date(date.today())

    def clear_tree(self):
        self.tree.delete(*self.tree.get_children())

    def insert_expense(self, expense):
        fecha = expense.get('fecha')
        if isinstance(fecha, date):
            fecha = fecha.strftime('%d/%m/%Y')
        
        monto_formateado = f"S/ {expense.get('monto', 0.0):.2f}"
        
        self.tree.insert("", "end", iid=expense['id'], values=(
            expense['id'],
            fecha,
            expense.get('descripcion', ''),
            monto_formateado
        ))
