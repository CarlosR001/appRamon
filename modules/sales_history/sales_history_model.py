from database import get_db_connection
from mysql.connector import Error

def search_sales(start_date=None, end_date=None):
    """
    Busca ventas dentro de un rango de fechas. Si no hay fechas, busca todas.
    """
    conn = get_db_connection()
    if not conn: return []
    cursor = conn.cursor(dictionary=True)
    
    query = """
        SELECT v.id, v.fecha, v.total, v.estado,
               c.nombre as cliente_nombre, u.nombre_usuario
        FROM ventas v
        LEFT JOIN clientes c ON v.id_cliente = c.id
        LEFT JOIN usuarios u ON v.id_usuario = u.id
    """
    params = []
    if start_date and end_date:
        query += " WHERE DATE(v.fecha) BETWEEN %s AND %s"
        params.extend([start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')])
    
    query += " ORDER BY v.fecha DESC;"
    
    try:
        cursor.execute(query, params)
        return cursor.fetchall()
    except Error as e:
        print(f"Error al buscar ventas: {e}")
        return []
    finally:
        cursor.close(); conn.close()

def void_sale(sale_id):
    """
    Anula una venta: cambia su estado a 'Anulada' y restaura el stock.
    Esto se ejecuta como una transacción.
    """
    conn = get_db_connection()
    if not conn: return False
    cursor = conn.cursor(dictionary=True)
    try:
        conn.start_transaction()

        # 1. Obtener los detalles de la venta (qué productos y cantidades se vendieron)
        query_items = "SELECT id_producto, cantidad FROM detalle_ventas WHERE id_venta = %s"
        cursor.execute(query_items, (sale_id,))
        items_sold = cursor.fetchall()

        # 2. Restaurar el stock de cada producto
        query_update_stock = "UPDATE productos SET stock = stock + %s WHERE id = %s"
        for item in items_sold:
            cursor.execute(query_update_stock, (item['cantidad'], item['id_producto']))

        # 3. Cambiar el estado de la venta a 'Anulada'
        query_void = "UPDATE ventas SET estado = 'Anulada' WHERE id = %s"
        cursor.execute(query_void, (sale_id,))

        conn.commit()
        return True
    except Error as e:
        print(f"Error en la transacción de anulación: {e}")
        conn.rollback()
        return False
    finally:
        cursor.close(); conn.close()
