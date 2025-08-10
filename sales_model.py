from database import get_db_connection
from mysql.connector import Error

def record_sale(cart_data, total):
    """
    Registra una venta en la base de datos como una transacción.
    Esto incluye la tabla 'ventas', 'detalle_ventas' y la actualización de 'productos'.
    """
    conn = get_db_connection()
    if not conn:
        return False

    cursor = conn.cursor()

    try:
        # Iniciar transacción
        conn.start_transaction()

        # 1. Insertar en la tabla 'ventas'
        # Por ahora, no asignamos un cliente específico (id_cliente=NULL)
        query_venta = "INSERT INTO ventas (total) VALUES (%s)"
        cursor.execute(query_venta, (total,))
        id_venta = cursor.lastrowid

        # 2. Iterar sobre el carrito para insertar en 'detalle_ventas' y actualizar 'productos'
        query_detalle = """
            INSERT INTO detalle_ventas (id_venta, id_producto, cantidad, precio_unitario)
            VALUES (%s, %s, %s, %s)
        """
        query_update_stock = """
            UPDATE productos SET stock = stock - %s WHERE id = %s
        """
        
        for product_id, item in cart_data.items():
            product = item['data']
            quantity = item['qty']
            
            # Insertar detalle de venta
            cursor.execute(query_detalle, (id_venta, product['id'], quantity, product['precio_venta']))
            
            # Actualizar stock
            cursor.execute(query_update_stock, (quantity, product['id']))

        # Si todo fue bien, confirmar todos los cambios
        conn.commit()
        return True

    except Error as e:
        print(f"Error en la transacción de venta: {e}")
        # Si algo sale mal, deshacer todos los cambios desde el inicio de la transacción
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()
