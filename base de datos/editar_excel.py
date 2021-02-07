import openpyxl
import csv


book = openpyxl.load_workbook("INVENTARIO.xlsx", data_only = True)

hoja = book.active
celdas = hoja["A2":"G51"]

list1=[]
for fila in celdas:
    list1.append([celda.value for celda in fila])

with open("a1.csv","w", newline="") as file:
    writer =csv.writer(file, delimiter=",")
    writer.writerows(list1)