import psycopg2
from editar_excel import list1

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

if __name__ == "__main__":
    for i in range(len(list1)):
        insert_inventario(list1[i][0],list1[i][1],list1[i][2],list1[i][3],list1[i][4],list1[i][5],list1[i][6])