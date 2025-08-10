from database import get_db_connection
from mysql.connector import Error

def record_purchase(cart_data, total, supplier_id):
    """
    Registra una compra en la base de datos como una transacción.
    Esto incluye 'compras', 'detalle_compras' y la actualización de 'productos'.
    Devuelve True si tiene éxito, False si falla.
    """
    conn = get_db_connection()
    if not conn:
        return False

    cursor = conn.cursor()
    id_compra = None

    try:
        conn.start_transaction()

        # 1. Insertar en la tabla 'compras'
        query_compra = "INSERT INTO compras (id_proveedor, total_compra) VALUES (%s, %s)"
        cursor.execute(query_compra, (supplier_id, total))
        id_compra = cursor.lastrowid

        # 2. Iterar sobre el carrito para insertar en 'detalle_compras' y actualizar 'productos'
        query_detalle = """
            INSERT INTO detalle_compras (id_compra, id_producto, cantidad, costo_unitario)
            VALUES (%s, %s, %s, %s)
        """
        query_update_stock = """
            UPDATE productos SET stock = stock + %s WHERE id = %s
        """
        
        for product_id, item in cart_data.items():
            product = item['data']
            quantity = item['qty']
            cost = item['cost']
            
            # Insertar detalle de compra
            cursor.execute(query_detalle, (id_compra, product['id'], quantity, cost))
            
            # Actualizar (sumar) stock
            cursor.execute(query_update_stock, (quantity, product['id']))

        conn.commit()
        return True

    except Error as e:
        print(f"Error en la transacción de compra: {e}")
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()
