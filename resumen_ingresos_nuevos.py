import csv
lista_ingresos_nuevos=[]
def AGREGAR_NUEVO_PRODUCTO_CSV(categoria,nombre,codigo,
                                precio_costo,precio_venta,
                                utilidad,stock):
    
    lista_ingresos_nuevos.append([categoria,nombre,codigo,
                                precio_costo,precio_venta,
                                utilidad,stock])

    with open("ingresos_nuevos.csv","w", newline="") as file:
        writer =csv.writer(file, delimiter=",")
        writer.writerows(lista_ingresos_nuevos)
#AGREGAR_NUEVO_PRODUCTO_CSV('categoria','nombre','codigo', 5 , 10 , 5,444)