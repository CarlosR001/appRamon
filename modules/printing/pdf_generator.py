import os
import webbrowser
from datetime import datetime
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.units import mm

# Asegurarse de que el directorio de recibos exista
if not os.path.exists('receipts'):
    os.makedirs('receipts')

def generate_receipt(receipt_data, print_format="ticket"):
    """
    Genera un archivo PDF para un recibo de venta en formato ticket o A4.
    """
    sale_id = receipt_data.get('id', 'N_A')
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = os.path.join('receipts', f'recibo_{sale_id}_{timestamp}.pdf')

    # --- Configuración de página y coordenadas ---
    if print_format == "ticket":
        # Ancho de ticket estándar (80mm), altura variable
        page_width = 80 * mm
        page_height = 150 * mm # Altura inicial, se puede ajustar
        c = canvas.Canvas(file_path, pagesize=(page_width, page_height))
        margin = 4 * mm
        font_size_normal = 9
        font_size_small = 7
        font_size_large = 12
    else: # A4
        page_width, page_height = A4
        c = canvas.Canvas(file_path, pagesize=A4)
        margin = 20 * mm
        font_size_normal = 12
        font_size_small = 10
        font_size_large = 16

    width, height = page_width, page_height
    y_position = height - margin

    try:
        # --- Función auxiliar para dibujar texto y bajar el cursor ---
        def draw_text(text, font, size, y_offset, align="left"):
            nonlocal y_position
            c.setFont(font, size)
            if align == "center":
                c.drawCentredString(width / 2, y_position, text)
            elif align == "right":
                c.drawRightString(width - margin, y_position, text)
            else: # left
                c.drawString(margin, y_position, text)
            y_position -= y_offset

        # --- Contenido del PDF ---
        # Encabezado
        draw_text("Electronica Ramon Planta", "Helvetica-Bold", font_size_large, 8 * mm, align="center")
        draw_text("Recibo de Venta", "Helvetica", font_size_small, 8 * mm, align="center")

        # Información de la venta
        fecha_venta = receipt_data.get('fecha', datetime.now()).strftime('%d/%m/%Y %H:%M')
        draw_text(f"ID Venta: #{sale_id}", "Helvetica", font_size_normal, 6 * mm)
        draw_text(f"Fecha: {fecha_venta}", "Helvetica", font_size_normal, 6 * mm)
        cliente = receipt_data.get('cliente_nombre', 'Público General')
        draw_text(f"Cliente: {cliente}", "Helvetica", font_size_normal, 10 * mm)

        # Línea separadora
        c.line(margin, y_position, width - margin, y_position)
        y_position -= 5 * mm

        # Cabecera de la tabla de items
        c.setFont("Helvetica-Bold", font_size_normal)
        c.drawString(margin, y_position, "Cant.")
        c.drawString(margin + 15 * mm, y_position, "Producto")
        c.drawRightString(width - margin, y_position, "Subtotal")
        y_position -= 6 * mm

        # Items de la venta
        for item in receipt_data.get('items', []):
            qty = str(item.get('cantidad', 0))
            name = item.get('producto_nombre', '')
            subtotal = f"S/ {item.get('cantidad', 0) * item.get('precio_unitario', 0):.2f}"
            
            # Limitar longitud del nombre para que no se desborde
            if print_format == "ticket" and len(name) > 25:
                name = name[:22] + "..."

            c.setFont("Helvetica", font_size_normal)
            c.drawString(margin, y_position, qty)
            c.drawString(margin + 15 * mm, y_position, name)
            c.drawRightString(width - margin, y_position, subtotal)
            y_position -= 5 * mm

        # Línea separadora
        y_position -= 5 * mm
        c.line(margin, y_position, width - margin, y_position)
        y_position -= 8 * mm

        # Total
        total = f"S/ {receipt_data.get('total', 0.0):.2f}"
        c.setFont("Helvetica-Bold", font_size_large)
        c.drawString(margin, y_position, "TOTAL:")
        c.drawRightString(width - margin, y_position, total)

        # --- Guardar y Abrir ---
        c.save()
        
        # Abrir el archivo PDF con el visor por defecto del sistema
        webbrowser.open(os.path.realpath(file_path))

    except Exception as e:
        print(f"Error al generar el PDF: {e}")

