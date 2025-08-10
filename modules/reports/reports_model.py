from database import get_db_connection
from mysql.connector import Error
from datetime import date

def get_daily_sales_summary():
    """Recupera un resumen de las ventas totales agrupadas por fecha."""
    conn = get_db_connection()
    if not conn: return []
    cursor = conn.cursor(dictionary=True)
    query = """
        SELECT
            DATE(fecha) as venta_fecha,
            COUNT(id) as numero_ventas,
            SUM(total) as total_vendido
        FROM ventas
        GROUP BY DATE(fecha)
        ORDER BY venta_fecha DESC;
    """
    try:
        cursor.execute(query)
        return cursor.fetchall()
    except Error as e:
        print(f"Error al obtener el resumen diario de ventas: {e}")
        return []
    finally:
        cursor.close()
        conn.close()

def get_sales_details_for_date(sale_date_obj):
    """Recupera todas las ventas de una fecha específica con sus detalles."""
    conn = get_db_connection()
    if not conn: return []
    cursor = conn.cursor(dictionary=True)
    try:
        sale_date_str = sale_date_obj.strftime('%Y-%m-%d')
        query_sales = """
            SELECT v.id, v.fecha, v.total, c.nombre as cliente_nombre
            FROM ventas v
            LEFT JOIN clientes c ON v.id_cliente = c.id
            WHERE DATE(v.fecha) = %s
            ORDER BY v.fecha ASC;
        """
        cursor.execute(query_sales, (sale_date_str,))
        sales = cursor.fetchall()
        if not sales: return []
        query_items = """
            SELECT d.cantidad, d.precio_unitario, p.nombre as producto_nombre
            FROM detalle_ventas d
            JOIN productos p ON d.id_producto = p.id
            WHERE d.id_venta = %s;
        """
        for sale in sales:
            cursor.execute(query_items, (sale['id'],))
            sale['items'] = cursor.fetchall()
        return sales
    except Error as e:
        print(f"Error al obtener los detalles de ventas por fecha: {e}")
        return []
    finally:
        cursor.close()
        conn.close()

def get_sales_by_product():
    """
    Recupera un resumen de ventas agrupado por producto.
    """
    conn = get_db_connection()
    if not conn: return []
    cursor = conn.cursor(dictionary=True)
    query = """
        SELECT
            p.nombre,
            p.codigo,
            SUM(dv.cantidad) as total_unidades_vendidas,
            SUM(dv.cantidad * dv.precio_unitario) as total_ingresos
        FROM detalle_ventas dv
        JOIN productos p ON dv.id_producto = p.id
        GROUP BY p.id, p.nombre, p.codigo
        ORDER BY total_unidades_vendidas DESC;
    """
    try:
        cursor.execute(query)
        return cursor.fetchall()
    except Error as e:
        print(f"Error al obtener el resumen de ventas por producto: {e}")
        return []
    finally:
        cursor.close()
        conn.close()
