from database import get_db_connection
from mysql.connector import Error
from datetime import date

def get_dashboard_data():
    """
    Recupera todos los datos necesarios para el dashboard en una sola pasada.
    """
    conn = get_db_connection()
    if not conn:
        return {
            'today_revenue': 0.0,
            'pending_services': 0,
            'low_stock_items': 0
        }

    cursor = conn.cursor(dictionary=True)
    dashboard_data = {}

    try:
        # 1. Obtener ingresos totales del día de hoy
        today = date.today().strftime('%Y-%m-%d')
        query_today_sales = "SELECT SUM(total) as total_today FROM ventas WHERE DATE(fecha) = %s"
        cursor.execute(query_today_sales, (today,))
        result = cursor.fetchone()
        dashboard_data['today_revenue'] = float(result['total_today']) if result and result['total_today'] else 0.0

        # 2. Obtener el conteo de servicios pendientes (no entregados)
        query_pending_services = "SELECT COUNT(id) as pending_count FROM servicios WHERE estado != 'Entregado'"
        cursor.execute(query_pending_services)
        result = cursor.fetchone()
        dashboard_data['pending_services'] = result['pending_count'] if result else 0

        # 3. Obtener el conteo de productos con bajo stock (ej. <= 5 unidades)
        low_stock_threshold = 5
        query_low_stock = "SELECT COUNT(id) as low_stock_count FROM productos WHERE stock <= %s"
        cursor.execute(query_low_stock, (low_stock_threshold,))
        result = cursor.fetchone()
        dashboard_data['low_stock_items'] = result['low_stock_count'] if result else 0
        
        return dashboard_data

    except Error as e:
        print(f"Error al obtener los datos del dashboard: {e}")
        return {} # Devolver un diccionario vacío en caso de error
    finally:
        cursor.close()
        conn.close()
