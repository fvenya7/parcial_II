import csv
lista_ingresos_stock=[]
def AGREGAR_STOCK_CSV(codigo,nombre,cantidad):
    
    lista_ingresos_stock.append([codigo,nombre,cantidad])

    with open("ingresos_stock.csv","w", newline="") as file:
        writer =csv.writer(file, delimiter=",")
        writer.writerows(lista_ingresos_stock)
