import psycopg2

def crear_tupla_codigos():
    sql = """ SELECT codigo_producto FROM inventario;"""
    
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
                    
        if conn is not None:
            conn.close()
            
    except (Exception, psycopg2.DatabaseError) as e:
        print(e)
    
    finally:
        if conn is not None:
            conn.close()
"""if __name__ == "__main__":
    tupla_cod=crear_tupla_codigos()
    lista_cod=[]
    for i in range(0,len(tupla_cod)):
        lista_cod.append(tupla_cod[i][0])
    print(tupla_cod)"""