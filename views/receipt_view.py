import tkinter as tk
from tkinter import ttk
from datetime import datetime

class ReceiptView(tk.Toplevel):
    def __init__(self, parent, receipt_data):
        super().__init__(parent)
        self.title(f"Recibo de Venta #{receipt_data.get('id', '')}")
        self.geometry("350x450")
        self.resizable(False, False)
        self.grab_set()

        # --- Main Frame ---
        main_frame = ttk.Frame(self, padding=15)
        main_frame.pack(expand=True, fill="both")

        # --- Header ---
        ttk.Label(main_frame, text="ELECTRO-PRO", font=("Segoe UI", 16, "bold")).pack()
        ttk.Label(main_frame, text="Recibo de Venta", font=("Segoe UI", 10, "italic")).pack(pady=(0, 10))

        # --- Sale Info ---
        info_frame = ttk.Frame(main_frame)
        info_frame.pack(fill="x", pady=5)
        
        fecha_venta = receipt_data.get('fecha')
        if isinstance(fecha_venta, datetime):
            fecha_venta = fecha_venta.strftime('%d/%m/%Y %H:%M:%S')

        ttk.Label(info_frame, text=f"Fecha: {fecha_venta}").pack(anchor="w")
        
        cliente = receipt_data.get('cliente_nombre', 'Público General')
        ttk.Label(info_frame, text=f"Cliente: {cliente}").pack(anchor="w")

        ttk.Separator(main_frame, orient="horizontal").pack(fill="x", pady=10)

        # --- Items Treeview ---
        items_frame = ttk.Frame(main_frame)
        items_frame.pack(expand=True, fill="both")
        items_frame.columnconfigure(0, weight=1)
        items_frame.rowconfigure(0, weight=1)

        tree = ttk.Treeview(items_frame, columns=("qty", "desc", "subtotal"), show="headings")
        tree.heading("qty", text="Cant.")
        tree.heading("desc", text="Producto")
        tree.heading("subtotal", text="Subtotal")
        tree.column("qty", width=40, anchor="c")
        tree.column("desc", width=180, anchor="w")
        tree.column("subtotal", width=80, anchor="e")
        
        for item in receipt_data.get('items', []):
            subtotal = item['cantidad'] * item['precio_unitario']
            tree.insert("", "end", values=(
                item['cantidad'],
                item['producto_nombre'],
                f"S/ {subtotal:.2f}"
            ))

        tree.grid(row=0, column=0, sticky="nsew")

        # --- Total ---
        total_frame = ttk.Frame(main_frame)
        total_frame.pack(fill="x", pady=(10, 0))
        total_frame.columnconfigure(0, weight=1)
        
        total_amount = receipt_data.get('total', 0.0)
        ttk.Label(total_frame, text="TOTAL:", font=("Segoe UI", 14, "bold")).grid(row=0, column=0, sticky="w")
        ttk.Label(total_frame, text=f"S/ {total_amount:.2f}", font=("Segoe UI", 14, "bold")).grid(row=0, column=1, sticky="e")

        # --- Close Button ---
        close_button = ttk.Button(main_frame, text="Cerrar", command=self.destroy, style="Accent.TButton")
        close_button.pack(side="bottom", pady=(15, 0))
