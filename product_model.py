from database import get_db_connection
from mysql.connector import Error

def get_all_products():
    """Recupera todos los productos de la base de datos con sus categorías."""
    # Esta función ahora puede ser un caso especial de search_products
    return search_products("")

def search_products(search_term):
    """Busca productos por nombre o código."""
    conn = get_db_connection()
    if not conn:
        return []
    
    products = []
    cursor = conn.cursor(dictionary=True)
    # El término de búsqueda se formatea con '%' para buscar coincidencias parciales
    like_term = f"%{search_term}%"
    
    query = """
        SELECT p.id, p.codigo, p.nombre, p.descripcion, p.precio_compra, p.precio_venta, p.stock, c.nombre as categoria
        FROM productos p
        LEFT JOIN categorias c ON p.id_categoria = c.id
        WHERE p.nombre LIKE %s OR p.codigo LIKE %s
        ORDER BY p.nombre
    """
    try:
        cursor.execute(query, (like_term, like_term))
        products = cursor.fetchall()
    except Error as e:
        print(f"Error al buscar productos: {e}")
    finally:
        cursor.close()
        conn.close()
    return products


def add_product(data):
    """Añade un nuevo producto a la base de datos."""
    conn = get_db_connection()
    if not conn:
        return None

    cursor = conn.cursor()
    query = """
        INSERT INTO productos (codigo, nombre, descripcion, precio_compra, precio_venta, stock, id_categoria)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    try:
        cursor.execute(query, (data['codigo'], data['nombre'], data['descripcion'], data['precio_compra'], data['precio_venta'], data['stock'], data['id_categoria']))
        conn.commit()
        return cursor.lastrowid
    except Error as e:
        print(f"Error al añadir producto: {e}")
        conn.rollback()
        return None
    finally:
        cursor.close()
        conn.close()

def update_product(product_id, data):
    """Actualiza un producto existente."""
    conn = get_db_connection()
    if not conn:
        return False
        
    cursor = conn.cursor()
    query = """
        UPDATE productos SET
        codigo = %s, nombre = %s, descripcion = %s, precio_compra = %s, precio_venta = %s, stock = %s, id_categoria = %s
        WHERE id = %s
    """
    try:
        cursor.execute(query, (data['codigo'], data['nombre'], data['descripcion'], data['precio_compra'], data['precio_venta'], data['stock'], data['id_categoria'], product_id))
        conn.commit()
        return True
    except Error as e:
        print(f"Error al actualizar producto: {e}")
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()

def delete_product(product_id):
    """Elimina un producto de la base de datos."""
    conn = get_db_connection()
    if not conn:
        return False

    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM productos WHERE id = %s", (product_id,))
        conn.commit()
        return True
    except Error as e:
        print(f"Error al eliminar producto: {e}")
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()

def get_all_categories():
    """Recupera todas las categorías."""
    conn = get_db_connection()
    if not conn:
        return []
    
    categories = []
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT id, nombre FROM categorias ORDER BY nombre")
        categories = cursor.fetchall()
    except Error as e:
        print(f"Error al obtener categorías: {e}")
    finally:
        cursor.close()
        conn.close()
    return categories
