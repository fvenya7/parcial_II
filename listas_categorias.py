import psycopg2

def crear_tupla_categorias():
    sql = """ SELECT categoria_producto FROM inventario;"""
    
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
                cur.execute(sql, ())
                
                if cur is not None:
                    fila = cur.fetchall()
                    return fila
                    print(fila)
                    
        if conn is not None:
            conn.close()
            
    except (Exception, psycopg2.DatabaseError) as e:
        print(e)
    
    finally:
        if conn is not None:
            conn.close()
