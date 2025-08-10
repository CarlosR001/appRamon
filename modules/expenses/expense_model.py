from database import get_db_connection
from mysql.connector import Error
from datetime import date

def get_all():
    """Recupera todos los gastos de la base de datos."""
    conn = get_db_connection()
    if not conn:
        return []
    
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT id, descripcion, monto, fecha FROM gastos ORDER BY fecha DESC")
        return cursor.fetchall()
    except Error as e:
        print(f"Error al obtener los gastos: {e}")
        return []
    finally:
        cursor.close()
        conn.close()

def add(description, amount, expense_date):
    """Añade un nuevo gasto."""
    conn = get_db_connection()
    if not conn: return False
    cursor = conn.cursor()
    query = "INSERT INTO gastos (descripcion, monto, fecha) VALUES (%s, %s, %s)"
    try:
        cursor.execute(query, (description, amount, expense_date))
        conn.commit()
        return True
    except Error as e:
        print(f"Error al añadir gasto: {e}")
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()

def delete(expense_id):
    """Elimina un gasto."""
    conn = get_db_connection()
    if not conn: return False
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM gastos WHERE id = %s", (expense_id,))
        conn.commit()
        return True
    except Error as e:
        print(f"Error al eliminar gasto: {e}")
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()
