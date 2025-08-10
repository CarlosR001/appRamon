from database import get_db_connection
from mysql.connector import Error
from datetime import date

def get_daily_sales_summary(start_date=None, end_date=None):
    """Recupera un resumen de ventas agrupadas por fecha, con filtro opcional."""
    conn = get_db_connection()
    if not conn: return []
    cursor = conn.cursor(dictionary=True)
    
    query = "SELECT DATE(fecha) as venta_fecha, COUNT(id) as numero_ventas, SUM(total) as total_vendido FROM ventas"
    params = []
    if start_date and end_date:
        query += " WHERE DATE(fecha) BETWEEN %s AND %s"
        params.extend([start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')])
    
    query += " GROUP BY DATE(fecha) ORDER BY venta_fecha DESC;"
    
    try:
        cursor.execute(query, params)
        return cursor.fetchall()
    except Error as e:
        print(f"Error al obtener resumen diario de ventas: {e}")
        return []
    finally:
        cursor.close(); conn.close()

def get_sales_details_for_date(sale_date_obj):
    """Recupera todas las ventas de una fecha específica con sus detalles."""
    conn = get_db_connection()
    if not conn: return []
    cursor = conn.cursor(dictionary=True)
    try:
        sale_date_str = sale_date_obj.strftime('%Y-%m-%d')
        query_sales = """
            SELECT v.id, v.fecha, v.total, c.nombre as cliente_nombre FROM ventas v
            LEFT JOIN clientes c ON v.id_cliente = c.id
            WHERE DATE(v.fecha) = %s ORDER BY v.fecha ASC;
        """
        cursor.execute(query_sales, (sale_date_str,))
        sales = cursor.fetchall()
        if not sales: return []
        query_items = """
            SELECT d.cantidad, d.precio_unitario, p.nombre as producto_nombre FROM detalle_ventas d
            JOIN productos p ON d.id_producto = p.id WHERE d.id_venta = %s;
        """
        for sale in sales:
            cursor.execute(query_items, (sale['id'],))
            sale['items'] = cursor.fetchall()
        return sales
    except Error as e:
        print(f"Error al obtener detalles de ventas por fecha: {e}")
        return []
    finally:
        cursor.close(); conn.close()

def get_sales_by_product():
    """Recupera un resumen de ventas agrupado por producto (INTACTO)."""
    conn = get_db_connection()
    if not conn: return []
    cursor = conn.cursor(dictionary=True)
    query = """
        SELECT p.nombre, p.codigo, SUM(dv.cantidad) as total_unidades_vendidas,
               SUM(dv.cantidad * dv.precio_unitario) as total_ingresos
        FROM detalle_ventas dv JOIN productos p ON dv.id_producto = p.id
        GROUP BY p.id, p.nombre, p.codigo ORDER BY total_unidades_vendidas DESC;
    """
    try:
        cursor.execute(query)
        return cursor.fetchall()
    except Error as e:
        print(f"Error al obtener resumen de ventas por producto: {e}")
        return []
    finally:
        cursor.close(); conn.close()

def get_profit_summary(start_date=None, end_date=None):
    """Calcula un resumen financiero completo, con filtro opcional."""
    conn = get_db_connection()
    if not conn: return {}
    cursor = conn.cursor(dictionary=True)
    summary = {'total_revenue': 0.0, 'total_cogs': 0.0, 'total_expenses': 0.0}
    
    sales_where_clause = ""
    expenses_where_clause = ""
    params = []

    if start_date and end_date:
        start_str, end_str = start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')
        sales_where_clause = " WHERE DATE(v.fecha) BETWEEN %s AND %s"
        expenses_where_clause = " WHERE g.fecha BETWEEN %s AND %s"
        params.extend([start_str, end_str])

    try:
        query_sales_profit = f"""
            SELECT SUM(dv.cantidad * dv.precio_unitario) as total_revenue, SUM(dv.cantidad * p.precio_compra) as total_cogs
            FROM detalle_ventas dv
            JOIN productos p ON dv.id_producto = p.id
            JOIN ventas v ON dv.id_venta = v.id
            {sales_where_clause};
        """
        cursor.execute(query_sales_profit, params)
        sales_data = cursor.fetchone()
        if sales_data and sales_data['total_revenue']:
            summary['total_revenue'] = float(sales_data['total_revenue'])
            summary['total_cogs'] = float(sales_data['total_cogs'])

        query_expenses = f"SELECT SUM(g.monto) as total_expenses FROM gastos g{expenses_where_clause};"
        cursor.execute(query_expenses, params)
        expenses_data = cursor.fetchone()
        if expenses_data and expenses_data['total_expenses']:
            summary['total_expenses'] = float(expenses_data['total_expenses'])
            
        return summary
    except Error as e:
        print(f"Error al calcular resumen de ganancias: {e}")
        return {}
    finally:
        cursor.close(); conn.close()
