from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup

from consulta_con_codigo import select_inventario
from update_stock import update_stock
from insert import insert_inventario

from resumen_ingresos_stock import AGREGAR_STOCK_CSV
from resumen_ingresos_nuevos import AGREGAR_NUEVO_PRODUCTO_CSV

from listas_categorias import crear_tupla_categorias
from listas_codigos import crear_tupla_codigos


class MenuScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class CatalogoScreen(Screen):
    pass

class InventarioScreen(Screen):
    pass

class Actualizar_Stock(Screen):

    def consultar_nombre(self):
        try:
            a = self.ids.entradacodigo.text
            self.b=(str(a)).upper()
            tupladatos = select_inventario(self.b)
            self.nombre = str(tupladatos[0])
            self.stock = str(tupladatos[2])
            self.ids.salidanombre.text = self.nombre
            self.ids.salidastock.text = self.stock
        except:
            self.nombre=''
            #self.ids.entradacodigo.text =''
            self.ids.salidanombre.text = 'NO ENCONTRADO'
            self.ids.salidastock.text = 'NO ENCONTRADO'

    def Sumar_Stock(self):
        a = self.ids.salidastock.text
        b = self.ids.ingresostock.text
        d = self.ids.entradacodigo.text
        aa = int(a)
        self.bb = int(b)
        self.dd = d.upper()
        self.c = aa + self.bb
        cc = str(self.c)
        update_stock(self.dd, self.c)

    def Limpiar(self):
        self.ids.ingresostock.text = ''
        self.ids.entradacodigo.text=''
        self.ids.salidanombre.text='NOMBRE DEL PRODUCTO'
        self.ids.salidastock.text='STOCK ACTUAL'
        
    def Abrir_Pop(self):
        Pop(self).Llenar()
        Pop(self).open()

class Pop(Popup):
    def __init__(self,As):
        super().__init__()
        self.As = As
        self.Llenar()
    def Llamar_Limpiar(self):
        self.As.nombre
        if type(self.As) == Actualizar_Stock:
            self.As.Limpiar()
        #nombre producto(self.As.nombre)
        #cant. ingresada entero(self.As.bb)
        #codigo en mayusculas (self.As.dd)
        AGREGAR_STOCK_CSV(self.As.dd,self.As.nombre,self.As.bb)

    def Llenar(self):
        total=int(self.As.ids.ingresostock.text)+int(self.As.ids.salidastock.text)
        self.ids.vpnombre.text = self.As.nombre
        self.ids.vpstock.text = str(total)
        
class Agregar_Producto(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        #crear la tupla de categorias(para spinner)
        tupla_cat = crear_tupla_categorias()
        lista_cat=[]
        for i in range(0,len(tupla_cat)):
            lista_cat.append(tupla_cat[i][0])
        lista_cat.append('Otro')
        self.lista_categorias=(list(set(lista_cat)))
        self.ids.spin.values = self.lista_categorias
        #crear la tupla de codigos(evitar repeticiones)
        tupla_cod = crear_tupla_codigos()
        self.lista_cod=[]
        for i in range(0,len(tupla_cod)):
            self.lista_cod.append(tupla_cod[i][0])

        
    def Comprobar_Categoria(self):
        self.categoria = self.ids.spin.text
        if self.categoria == 'Otro':
            self.ids.entrada_nueva_cat.text =  ''
            self.ids.entrada_nueva_cat.hint_text = 'Ingrese Nueva Categoria'
            self.ids.entrada_nueva_cat.readonly = False

        else:
            self.ids.entrada_nueva_cat.text =  self.categoria
            

    def Comprobar_Codigo(self):
        cod_entrada = str(self.ids.APCodigo.text)
        if (cod_entrada).upper() in self.lista_cod:
            self.ids.APCodigo.text = ''
            self.ids.APCodigo.hint_text = 'INGRESE CODIGO DIFERENTE'


    def Calcular_Utilidad(self):
        try:
            if float(self.ids.APPV.text)-float(self.ids.APPC.text) < 0:
                self.ids.APU.text = 'NO RENTABLE'
            else:
                self.ids.APU.text=str(float(self.ids.APPV.text)-float(self.ids.APPC.text))
        except:
            self.ids.APU.text = 'NO RENTABLE'
    def Guardar_Nuevo(self):
        #print(self.ids.entrada_nueva_cat.text)
        #funcion 
        #dar formato srt y poner en mayusculas
        a = str(self.ids.entrada_nueva_cat.text).upper()
        b = str(self.ids.APNombre.text).upper()
        c = str(self.ids.APCodigo.text).upper()
        d = self.ids.APPC.text
        e = self.ids.APPV.text
        f = self.ids.APU.text
        g = self.ids.APStock.text
        #subir a la base de daos
        insert_inventario(a,b,c,d,e,f,g)
        #limpiar entradas
        self.ids.entrada_nueva_cat.text = ''
        self.ids.APNombre.text = ''
        self.ids.APCodigo.text = ''
        self.ids.APPC.text = ''
        self.ids.APPV.text = ''
        self.ids.APU.text = ''
        self.ids.APStock.text = ''
        #guardar en la lista temporal
        AGREGAR_NUEVO_PRODUCTO_CSV(a,b,c,d,e,f,g)
    #abrir el pop de confirmacion
    def Abrir_Pop_Confirmacion_Nuevo(self):
        Pop_Confirmacion().open()

class Pop_Confirmacion(Popup):
    pass

class BoletaScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.numero_de_boleta = 0
        self.sub1 = '00.00'
        self.sub2 = '00.00'
        self.sub3 = '00.00'
        self.sub4 = '00.00'
        self.sub5 = '00.00'
        self.listaindices = ['CODIGO','NOMBRE','CATEGORIA','PRECIO',
                            'DISPONIBLE', 'CANTIDAD', 'SUBTOTAL']
        for i in range(len(self.listaindices)):
            self.ids.GRIDBOLETA.add_widget(Label(text=self.listaindices[i],color= (0,0,0,1)))

        self.lista_codigo = [self.ids.VBCodigo1,self.ids.VBCodigo2,self.ids.VBCodigo3,self.ids.VBCodigo4,self.ids.VBCodigo5]
        self.lista_nombre = [self.ids.VBNombre1,self.ids.VBNombre2,self.ids.VBNombre3,self.ids.VBNombre4,self.ids.VBNombre5]
        self.lista_categoria = [self.ids.VBCategoria1,self.ids.VBCategoria2,self.ids.VBCategoria3,self.ids.VBCategoria4,self.ids.VBCategoria5]
        self.lista_precio = [self.ids.VBPrecio1,self.ids.VBPrecio2,self.ids.VBPrecio3,self.ids.VBPrecio4,self.ids.VBPrecio5]
        self.lista_stock = [self.ids.VBStockdis1,self.ids.VBStockdis2,self.ids.VBStockdis3,self.ids.VBStockdis4,self.ids.VBStockdis5]
        self.lista_cantidad = [self.ids.VBCantidad1,self.ids.VBCantidad2,self.ids.VBCantidad3,self.ids.VBCantidad4,self.ids.VBCantidad5]
        self.lista_sub = [self.ids.VBSub1,self.ids.VBSub2,self.ids.VBSub3,self.ids.VBSub4,self.ids.VBSub5]
        self.lista_s = [self.sub1,self.sub2,self.sub3,self.sub4,self.sub4,self.sub5]
        #LISTA DE LISTAS
        self.lista_de_listas = [self.lista_codigo,self.lista_nombre,self.lista_categoria,
                                self.lista_precio,self.lista_stock,
                                self.lista_cantidad,self.lista_sub,self.lista_s]

    def Llenar_Boletas(self,i):
        try:
            li1 = list(select_inventario((self.lista_codigo[i].text)))
            
            self.lista_nombre[i].text = li1[0]
            self.lista_categoria[i].text = li1[3]
            self.lista_precio[i].text = str(f'S/. {li1[1]}')
            self.lista_stock[i].text = str(li1[2])
            self.lista_sub[i].text = f'S/. {self.lista_s[i]}'
            if int(self.lista_cantidad[i].text)<= int(li1[2]):
                self.lista_s[i] = str(round(float(self.lista_cantidad[i].text)*float(li1[1]),2))
                self.lista_sub[i].text = str(f'S/. {self.lista_s[i]}')
            else:
                self.lista_cantidad[i].text =''
                self.lista_sub[i].text ='S/. 00.00'
                self.lista_s[i] = '00.00'
                Pop_Advertencia().open()
        except:
            pass

    def Calcular_Total(self):
        total = 0
        #self.ids.total.text = f'S/. {str(round(float(self.sub1)+float(self.sub2)+float(self.sub3)+float(self.sub4)+float(self.sub5),2))}'
        for i in range(5):
            total += round(float(self.lista_s[i]),2)
        self.ids.total.text = f'S/. {total}'   

    def Restar_Ventas_Base(self,x2):
        #SE ACTUALIZA LA BASE DE DATOS RETANDO LA CANT VENDIDA AL STOCK
        try:
            
            for i in range (0,len(self.lista_s)):
                
                cod = self.lista_codigo[i].text
                stock = int(self.lista_stock[i].text)
                cant_vendida = int(self.lista_cantidad[i].text)
                update_stock(cod,(stock-cant_vendida))
            
        except:
            pass

    def Limpiar_Boleta(self):
        #SE LIMPIAN LOS CAMPOS TRAS LA VENTA
        for i in range(7):
            for j in range(5):
                if i == 6:
                    self.lista_de_listas[i][j].text = "S/. 00.00"
                elif i in [0,5]:
                    self.lista_de_listas[i][j].text = ""
                else:
                    self.lista_de_listas[i][j].text = "---"
            
    def pop_confirmacion(self):
        #Pop de confirmacion venta

        titulo =Label(text='TOTAL DE PRODUCTOS',size_hint=(1, .2))
        boxcontenedor = BoxLayout(orientation = 'vertical')
        contenedor = GridLayout(cols = 5)

        botones_y_total = GridLayout(cols=4, size_hint=(1, .2))

        bot_volver = Button(text = 'VOLVER')
        bot_volver.bind(on_release=self.cerrar_vent)

        bot_generar_bol = Button(text = 'GENERAR BOLETA')
        bot_generar_bol.bind(on_release = self.Restar_Ventas_Base)
        bot_generar_bol.bind(on_release = self.cerrar_vent)
        bot_generar_bol.bind(on_release = self.Confirmar_Pop_Venta)
        bot_generar_bol.bind(on_release = self.Crear_Escribir_Boleta)

        lbtotal1 = Label(text = 'TOTAL: ')
        lbtotal2 = Label(text = self.ids.total.text)

        botones_y_total.add_widget(bot_volver)
        botones_y_total.add_widget(bot_generar_bol)
        botones_y_total.add_widget(lbtotal1)
        botones_y_total.add_widget(lbtotal2)

        boxcontenedor.add_widget(titulo)
        boxcontenedor.add_widget(contenedor)
        boxcontenedor.add_widget(botones_y_total)
        self.ventana = Popup(content=boxcontenedor, 
                    auto_dismiss=False,
                    size_hint= (.8,.8),
                    title='CONFIRMACION DE VENTA')
        for i in range (5):
            contenedor.add_widget(Label(text = self.lista_codigo[i].text))
            contenedor.add_widget(Label(text = self.lista_nombre[i].text))
            contenedor.add_widget(Label(text = self.lista_cantidad[i].text))
            contenedor.add_widget(Label(text = self.lista_precio[i].text))
            contenedor.add_widget(Label(text = self.lista_sub[i].text))

        # bind the on_press event of the button to the dismiss function
        #self.ventana.bind(on_dismiss = self.Limpiar_Boleta)
        # open the popup
        self.ventana.open()
    

    def Confirmar_Pop_Venta(self,Y):
        box2 = BoxLayout(orientation = 'vertical')
        box2.add_widget(Label(text = 'VENTA EXITOSA'))
        baceptar = Button(text = 'ACEPTAR')
        baceptar.bind(on_release = self.abrir_limpiar)
        baceptar.bind(on_release = self.cerrar_ventita)
        box2.add_widget(baceptar)
        self.ventanita = Popup(content = box2,size_hint= (.5,.3))
        self.ventanita.open()

    def Abrir_Pop_Advertencia(self):
        #abrir el pop de advertencia
        Pop_Advertencia().open()
    def abrir_limpiar(self,s):
        self.Limpiar_Boleta()  
    def cerrar_vent(self,x1):
        self.ventana.dismiss()
    def cerrar_ventita(self,a):
        self.ventanita.dismiss()

    def Crear_Escribir_Boleta(self,f):
        self.numero_de_boleta += 1
        try:
            text_boleta=open(f"BOLETA N° {self.numero_de_boleta}.txt","w") 
            for i in range(6):
                for j in range(7):
                    if i == 0 and j in [0,1,3,5]:
                        text_boleta.write(f"{self.listaindices[j]}   -   ") 
                    elif i == 0 and  j == 6:
                        text_boleta.write(f"{self.listaindices[j]}      \n") 
                    elif i > 0 and j in [0,1,3,5]:
                        text_boleta.write(f"{self.lista_de_listas[j][i-1].text}   -   ") 
                    elif i > 0 and j == 6:
                        text_boleta.write(f"{self.lista_de_listas[j][i-1].text}     \n")
            text_boleta.write(f" TOTAL A PAGAR:{self.ids.total.text}")
            text_boleta.close() 
        except:
            pass

class Pop_Confirmar_Venta(Popup):
    pass
class Pop_Advertencia(Popup):
    pass

class VENTANA_PRINCIPALApp(App):
    title = 'VENTANA PRINCIPAL'

    def build(self):
        sm = ScreenManager()
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(BoletaScreen(name='boleta'))
        sm.add_widget(CatalogoScreen(name='catalogo'))
        sm.add_widget(InventarioScreen(name='inventario'))
        sm.add_widget(Actualizar_Stock(name='actstock'))
        sm.add_widget(Agregar_Producto(name='aproducto'))
        
        return sm

if __name__ == '__main__':
    VENTANA_PRINCIPALApp().run()