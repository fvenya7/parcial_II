import psycopg2

def update_stock(codigo_producto,stock):
    sql = """ UPDATE inventario SET stock=%s WHERE codigo_producto=%s;"""
    
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
                cur.execute(sql, (stock,codigo_producto))
        
        if conn is not None:
            conn.close()
            
    except (Exception, psycopg2.DatabaseError) as e:
        print(e)
    
    finally:
        if conn is not None:
            conn.close()
#if __name__ == "__main__":
    #update_stock('PH20A','56')
