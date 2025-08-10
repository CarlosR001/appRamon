import tkinter as tk
from tkinter import ttk
from datetime import datetime

class ReceiptView(tk.Toplevel):
    def __init__(self, parent, controller, receipt_data):
        super().__init__(parent)
        self.controller = controller
        self.receipt_data = receipt_data

        self.title(f"Recibo de Venta #{receipt_data.get('id', '')}")
        self.geometry("380x550")
        self.resizable(False, False)
        self.grab_set()

        main_frame = ttk.Frame(self, padding=15)
        main_frame.pack(expand=True, fill="both")
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(4, weight=1)

        ttk.Label(main_frame, text="Centro electronico Ramon", font=("Segoe UI", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=(0,5))
        ttk.Label(main_frame, text="Recibo de Venta", font=("Segoe UI", 10, "italic")).grid(row=1, column=0, columnspan=2, pady=(0, 10))

        info_frame = ttk.Frame(main_frame)
        info_frame.grid(row=2, column=0, columnspan=2, sticky="ew", pady=5)
        fecha_venta = receipt_data.get('fecha', datetime.now()).strftime('%d/%m/%Y %H:%M:%S')
        cliente = receipt_data.get('cliente_nombre', 'Público General')
        vendedor = receipt_data.get('vendedor_nombre', 'N/A')
        
        ttk.Label(info_frame, text=f"Fecha: {fecha_venta}").pack(anchor="w")
        ttk.Label(info_frame, text=f"Cliente: {cliente}").pack(anchor="w")
        ttk.Label(info_frame, text=f"Vendido por: {vendedor}").pack(anchor="w")

        ttk.Separator(main_frame, orient="horizontal").grid(row=3, column=0, columnspan=2, sticky="ew", pady=10)

        items_frame = ttk.Frame(main_frame)
        items_frame.grid(row=4, column=0, columnspan=2, sticky="nsew")
        items_frame.columnconfigure(0, weight=1); items_frame.rowconfigure(0, weight=1)
        
        tree = ttk.Treeview(items_frame, columns=("qty", "desc", "subtotal"), show="headings")
        tree.heading("qty", text="Cant."); tree.heading("desc", text="Producto"); tree.heading("subtotal", text="Subtotal")
        tree.column("qty", width=40, anchor="c"); tree.column("desc", width=200, anchor="w"); tree.column("subtotal", width=80, anchor="e")
        for item in receipt_data.get('items', []):
            subtotal = item['cantidad'] * item['precio_unitario']
            tree.insert("", "end", values=(item['cantidad'], item['producto_nombre'], f"S/ {subtotal:.2f}"))
        tree.grid(row=0, column=0, sticky="nsew")
        scrollbar = ttk.Scrollbar(items_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky="ns")

        total_frame = ttk.Frame(main_frame)
        total_frame.grid(row=5, column=0, columnspan=2, sticky="ew", pady=(10, 0))
        total_frame.columnconfigure(1, weight=1)
        total_amount = receipt_data.get('total', 0.0)
        ttk.Label(total_frame, text="TOTAL:", font=("Segoe UI", 14, "bold")).grid(row=0, column=0, sticky="w")
        ttk.Label(total_frame, text=f"S/ {total_amount:.2f}", font=("Segoe UI", 14, "bold")).grid(row=0, column=1, sticky="e")

        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=6, column=0, columnspan=2, sticky="ew", pady=(15, 0))
        button_frame.columnconfigure(0, weight=1); button_frame.columnconfigure(1, weight=1)
        
        print_ticket_button = ttk.Button(button_frame, text="Imprimir Ticket", command=self.print_ticket)
        print_ticket_button.grid(row=0, column=0, sticky="ew", padx=(0, 5))
        print_a4_button = ttk.Button(button_frame, text="Imprimir A4", command=self.print_a4)
        print_a4_button.grid(row=0, column=1, sticky="ew", padx=(5, 0))
        close_button = ttk.Button(button_frame, text="Cerrar", command=self.destroy, style="Accent.TButton")
        close_button.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(5,0))

    def print_ticket(self):
        self.controller.print_receipt(self.receipt_data, "ticket")

    def print_a4(self):
        self.controller.print_receipt(self.receipt_data, "a4")
