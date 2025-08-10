import os
import webbrowser
from datetime import datetime
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.units import mm

if not os.path.exists('receipts'):
    os.makedirs('receipts')

def generate_receipt(receipt_data, print_format="ticket"):
    sale_id = receipt_data.get('id', 'N_A')
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = os.path.join('receipts', f'recibo_{sale_id}_{timestamp}.pdf')

    if print_format == "ticket":
        page_width, page_height = 80 * mm, 150 * mm
        c = canvas.Canvas(file_path, pagesize=(page_width, page_height))
        margin = 4 * mm
        font_size_normal, font_size_small, font_size_large = 9, 7, 12
    else: # A4
        page_width, page_height = A4
        c = canvas.Canvas(file_path, pagesize=A4)
        margin = 20 * mm
        font_size_normal, font_size_small, font_size_large = 12, 10, 16

    width, height = page_width, page_height
    y_position = height - margin

    try:
        def draw_text(text, font, size, y_offset, align="left"):
            nonlocal y_position
            c.setFont(font, size)
            if align == "center": c.drawCentredString(width / 2, y_position, text)
            elif align == "right": c.drawRightString(width - margin, y_position, text)
            else: c.drawString(margin, y_position, text)
            y_position -= y_offset

        draw_text("Centro electronico Ramon", "Helvetica-Bold", font_size_large, 8 * mm, align="center")
        draw_text("Recibo de Venta", "Helvetica", font_size_small, 8 * mm, align="center")

        fecha_venta = receipt_data.get('fecha', datetime.now()).strftime('%d/%m/%Y %H:%M')
        cliente = receipt_data.get('cliente_nombre', 'Público General')
        vendedor = receipt_data.get('vendedor_nombre', 'N/A')
        
        draw_text(f"ID Venta: #{sale_id}", "Helvetica", font_size_normal, 6 * mm)
        draw_text(f"Fecha: {fecha_venta}", "Helvetica", font_size_normal, 6 * mm)
        draw_text(f"Cliente: {cliente}", "Helvetica", font_size_normal, 6 * mm)
        draw_text(f"Vendido por: {vendedor}", "Helvetica", font_size_normal, 10 * mm)

        c.line(margin, y_position, width - margin, y_position)
        y_position -= 5 * mm

        c.setFont("Helvetica-Bold", font_size_normal)
        c.drawString(margin, y_position, "Cant.")
        c.drawString(margin + 15 * mm, y_position, "Producto")
        c.drawRightString(width - margin, y_position, "Subtotal")
        y_position -= 6 * mm

        for item in receipt_data.get('items', []):
            qty = str(item.get('cantidad', 0))
            name = item.get('producto_nombre', '')
            subtotal = f"S/ {item.get('cantidad', 0) * item.get('precio_unitario', 0):.2f}"
            if print_format == "ticket" and len(name) > 25:
                name = name[:22] + "..."
            c.setFont("Helvetica", font_size_normal)
            c.drawString(margin, y_position, qty)
            c.drawString(margin + 15 * mm, y_position, name)
            c.drawRightString(width - margin, y_position, subtotal)
            y_position -= 5 * mm

        y_position -= 5 * mm
        c.line(margin, y_position, width - margin, y_position)
        y_position -= 8 * mm

        total = f"S/ {receipt_data.get('total', 0.0):.2f}"
        c.setFont("Helvetica-Bold", font_size_large)
        c.drawString(margin, y_position, "TOTAL:")
        c.drawRightString(width - margin, y_position, total)

        c.save()
        webbrowser.open(os.path.realpath(file_path))
    except Exception as e:
        print(f"Error al generar el PDF: {e}")

def generate_cash_balance_report(report_data):
    balance_date = report_data.get('date', datetime.now().date())
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = os.path.join('receipts', f'cuadre_caja_{balance_date.strftime("%Y%m%d")}_{timestamp}.pdf')
    c = canvas.Canvas(file_path, pagesize=A4)
    width, height = A4
    margin = 20 * mm
    try:
        y_pos = height - margin
        def draw_line(y_offset=4 * mm):
            nonlocal y_pos
            y_pos -= y_offset; c.line(margin, y_pos, width - margin, y_pos); y_pos -= y_offset
        c.setFont("Helvetica-Bold", 18); c.drawCentredString(width / 2, y_pos, "Cuadre de Caja")
        y_pos -= 8 * mm
        c.setFont("Helvetica", 12); c.drawCentredString(width / 2, y_pos, f"Fecha: {balance_date.strftime('%d/%m/%Y')}"); y_pos -= 12 * mm
        c.setFont("Helvetica-Bold", 14); c.drawString(margin, y_pos, "Ingresos (Ventas)"); draw_line()
        c.setFont("Helvetica-Bold", 10); c.drawString(margin, y_pos, "ID Venta"); c.drawString(margin + 60*mm, y_pos, "Vendedor"); c.drawRightString(width - margin, y_pos, "Total"); y_pos -= 6 * mm
        c.setFont("Helvetica", 10)
        for sale in report_data.get('sales_list', []):
            c.drawString(margin, y_pos, str(sale['id'])); c.drawString(margin + 60*mm, y_pos, str(sale.get('nombre_usuario', 'N/A'))); c.drawRightString(width - margin, y_pos, f"S/ {sale['total']:.2f}")
            y_pos -= 5 * mm
        y_pos -= 8 * mm
        c.setFont("Helvetica-Bold", 14); c.drawString(margin, y_pos, "Egresos (Gastos)"); draw_line()
        c.setFont("Helvetica-Bold", 10); c.drawString(margin, y_pos, "Descripción"); c.drawRightString(width - margin, y_pos, "Monto"); y_pos -= 6 * mm
        c.setFont("Helvetica", 10)
        for expense in report_data.get('expenses_list', []):
            c.drawString(margin, y_pos, str(expense['descripcion'])); c.drawRightString(width - margin, y_pos, f"S/ {expense['monto']:.2f}")
            y_pos -= 5 * mm
        y_pos -= 15 * mm; draw_line(2*mm); y_pos -= 2*mm
        c.setFont("Helvetica-Bold", 12)
        c.drawRightString(width - margin - 40*mm, y_pos, "Total Ingresos:"); c.drawRightString(width - margin, y_pos, f"S/ {report_data.get('total_sales', 0.0):.2f}"); y_pos -= 7 * mm
        c.drawRightString(width - margin - 40*mm, y_pos, "Total Egresos:"); c.drawRightString(width - margin, y_pos, f"S/ {report_data.get('total_expenses', 0.0):.2f}"); y_pos -= 7 * mm
        c.setFont("Helvetica-Bold", 14)
        c.drawRightString(width - margin - 40*mm, y_pos, "BALANCE DE CAJA:"); c.drawRightString(width - margin, y_pos, f"S/ {report_data.get('balance', 0.0):.2f}")
        c.save()
        webbrowser.open(os.path.realpath(file_path))
    except Exception as e:
        print(f"Error al generar PDF de cuadre: {e}")
