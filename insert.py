import psycopg2

def insert_inventario(categoria_producto,nombre_producto,codigo_producto,precio_costo,precio_venta,utilidad,stock):
    sql = """ INSERT INTO inventario (categoria_producto,nombre_producto,codigo_producto,precio_costo,precio_venta,utilidad,stock) VALUES (%s,%s,%s,%s,%s,%s,%s);"""
    
    conn = None
    
    try:
        conn = psycopg2.connect(
        host="localhost",
        port="5432",
        user="postgres",
        database="prueba1",
        password="123456789")
        
        cur = conn.cursor()
        
        cur.execute(sql, (categoria_producto,nombre_producto,codigo_producto,precio_costo,precio_venta,utilidad,stock))
        
        conn.commit()
        cur.close()

        if conn is not None:
            conn.close()
            
    except (Exception, psycopg2.DatabaseError) as e:
        print(e)
    
    finally:
        if conn is not None:
            conn.close()