import psycopg2

def crear_tablas():
    comandos = (
        """CREATE TABLE INVENTARIO(
            categoria_producto VARCHAR(20) NOT NULL,
            nombre_producto VARCHAR(30) NOT NULL,
            codigo_producto VARCHAR(5) PRIMARY KEY,
            precio_costo FLOAT NOT NULL,
            precio_venta FLOAT NOT NULL,
            utilidad FLOAT NOT NULL,
            stock INTEGER NOT NULL)
        """,
    )
    
    conn = None
    
    try:
        conn = psycopg2.connect(
        host="localhost",
        port="5432",
        user="postgres",
        database="prueba1",
        password="123456789")
        
        cur = conn.cursor()
        
        for comando in comandos:
            cur.execute(comando)
        
        cur.close()
        conn.commit()

        if conn is not None:
            conn.close()
            
    except (Exception, psycopg2.DatabaseError) as e:
        print(e)
    
    finally:
        if conn is not None:
            conn.close()

if __name__ == "__main__":
    crear_tablas()
