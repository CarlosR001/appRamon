from database import get_db_connection
from mysql.connector import Error

def get_all():
    """Recupera todas las categorías de la base de datos."""
    conn = get_db_connection()
    if not conn:
        return []
    
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT id, nombre FROM categorias ORDER BY nombre")
        return cursor.fetchall()
    except Error as e:
        print(f"Error al obtener categorías: {e}")
        return []
    finally:
        cursor.close()
        conn.close()

def add(name):
    """Añade una nueva categoría."""
    conn = get_db_connection()
    if not conn: return False
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO categorias (nombre) VALUES (%s)", (name,))
        conn.commit()
        return True
    except Error as e:
        print(f"Error al añadir categoría: {e}")
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()

def update(category_id, name):
    """Actualiza el nombre de una categoría."""
    conn = get_db_connection()
    if not conn: return False
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE categorias SET nombre = %s WHERE id = %s", (name, category_id))
        conn.commit()
        return True
    except Error as e:
        print(f"Error al actualizar categoría: {e}")
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()

def delete(category_id):
    """Elimina una categoría."""
    # Consideración: ¿Qué pasa si un producto está usando esta categoría?
    # La BD podría fallar si hay una 'foreign key constraint'.
    # Una mejora futura sería comprobar esto antes de borrar.
    conn = get_db_connection()
    if not conn: return False
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM categorias WHERE id = %s", (category_id,))
        conn.commit()
        return True
    except Error as e:
        print(f"Error al eliminar categoría: {e}")
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()
