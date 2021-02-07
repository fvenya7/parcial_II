import psycopg2

def select_inventario(codigo_producto):
    sql = """ SELECT nombre_producto, precio_venta, stock, categoria_producto FROM inventario WHERE codigo_producto = %s;"""
    
    conn = None
    
    try:
        conn = psycopg2.connect(
        host="localhost",
        port="5432",
        user="postgres",
        database="prueba1",
        password="123456789")
        
        with conn:
            with conn.cursor() as cur:
                cur.execute(sql, (codigo_producto,))
                
                if cur is not None:
                    fila = cur.fetchone()
                    return fila
                    
        if conn is not None:
            conn.close()
            
    except (Exception, psycopg2.DatabaseError) as e:
        print(e)
    
    finally:
        if conn is not None:
            conn.close()

#if __name__ == "__main__":
#    a = select_inventario("AC20A")
#   print(a)