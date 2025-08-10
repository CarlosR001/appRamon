from database import get_db_connection
from mysql.connector import Error

def get_daily_sales_summary():
    """
    Recupera un resumen de las ventas totales agrupadas por fecha.
    """
    conn = get_db_connection()
    if not conn:
        return []

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
