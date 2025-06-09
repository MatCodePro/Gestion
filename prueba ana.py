#TODO:

#1 Una vez buscado el huesped, qué hacer con él
#Continuar por cambiar estado huesped

#Cargar productos al huesped
#Definir acciones al cambiar el estado del huesped
#Al cerrar un huesped modificar la habitación a 0

#producir_informes()
#Generar reporte de huéspedes en estado ABIERTO
#Generar reporte de huéspedes en estado A LA ESPERA cuya fecha de checkin sea el día siguiente

from datetime import datetime, date
import sqlite3
from unidecode import *


### VARIABLES GLOBALES ###

conexion = sqlite3.connect('BaseDeDatos')
cursor = conexion.cursor()


### FUNCIONES ###

def productos_existe():
    cursor.execute('''CREATE TABLE IF NOT EXISTS PRODUCTOS(CODIGO INTEGER PRIMARY KEY AUTOINCREMENT, NOMBRE TEXT, PRECIO REAL)''')

def huespedes_existe():
    cursor.execute('''CREATE TABLE IF NOT EXISTS HUESPEDES(NUMERO INTEGER PRIMARY KEY AUTOINCREMENT, APELLIDO TEXT, NOMBRE TEXT, TELEFONO INTEGER, EMAIL TEXT, BOOKING INTEGER, ESTADO INTEGER, CHECKIN TEXT, CHECKOUT TEXT, DOCUMENTO INTEGER, NACIMIENTO TEXT, HABITACION INTEGER, CONTINGENTE INTEGER, REGISTRO TEXT)''')

def inicio():
    respuesta_home = input("\n¿Qué desea hacer?:\n1. Gestionar de huéspedes\n2. Gestionar de consumos\n3. Gestionar de productos\n4. Gestionar de inventario\n5. Generar reportes\n")
    try:
        respuesta_home = int(respuesta_home)
    except ValueError:
        print("Elección inválida. Intente nuevamente: ")
        inicio()
    if respuesta_home == 1:
        gestionar_huespedes() 
    elif respuesta_home == 2:
        gestionar_consumos()
    elif respuesta_home == 3:
        gestionar_productos()
    elif respuesta_home == 4:
        gestionar_inventario()
    elif respuesta_home == 5:
        generar_reportes()
    else: inicio()

def gestionar_huespedes():
    respuesta_huespedes = input("\n1. Registrar nuevo huesped\n2. Buscar un huesped\n3. Cambiar el estado de un huesped\n4. Editar huesped\n5. Eliminar un huesped\n9. Volver al inicio\n")
    try:
        respuesta_huespedes = int(respuesta_huespedes)
    except ValueError:
        print("Elección inválida. Intente nuevamente: ")
        gestionar_huespedes()
    if respuesta_huespedes == 1:
        nuevo_huesped()
    elif respuesta_huespedes == 2:
        buscar_huesped()
    elif respuesta_huespedes == 3:
        cambiar_estado()
    elif respuesta_huespedes == 4:
        editar_huesped()
    elif respuesta_huespedes == 5:
        eliminar_huesped()
    elif respuesta_huespedes == 9:
        inicio()
    else: gestionar_huespedes()

def nuevo_huesped():
    while True:
        apellido = input("\nEscriba el apellido del huesped ó (0) para cancelar: ")
        if apellido.isdigit():
            try:
                apellido = int(apellido)
                if apellido == 0:
                    gestionar_huespedes()
                    return
            except ValueError:
                print("Selección inválida. Intente nuevamente. ")
                continue
        else:
            apellido = unidecode(apellido)
            break
    nombre = input("Escriba el nombre del huesped: ")
    while True:
        telefono = input("Ingrese un whatsapp de contacto: ")
        if telefono.isdigit():
            telefono = int(telefono)
            break
        else:
            print("Teléfono inválido. Intente nuevamente. ")
    email = input("Ingrese el e-mail de contacto: ")
    while True:
        respuesta_booking = input("Es una reserva de booking? si/no ")
        if respuesta_booking == "si" or respuesta_booking == "no":
            booking = respuesta_booking
            break
        else:
            print('Respuesta inválida. Intente nuevamente con "si" o "no" ')
    while True:
        estado = input("Es un huesped programado (0) ó es un checkin (1)? ")
        try:
            estado = int(estado)
            if estado == 0:
                checkin = input("Ingrese la fecha de checkin? (DD-MM-YYYY): ")
                checkout = input("Ingrese la fecha de checkout en formato DD-MM-YYYY: ")
                documento = 0
                nacimiento = "DD-MM-YYYY"
                habitacion = 0
                break
            elif estado == 1:
                checkin = str(date.today())
                checkout = input("Ingrese la fecha de checkout en formato DD-MM-YYYY: ")
                documento = input("Ingerse el documento: ")
                nacimiento = input("Ingrese la fecha de nacimiento en formato DD-MM-YYYY: ")
                habitacion = input("Ingresa el número de habitación: ")
                break
            else:
                print("Respuesta inválida. Intente nuevamente. ")
                continue
        except ValueError:
            print("Respuesta inválida. Intente nuevamente. ")
    while True:
        contingente = input("Ingrese la cantidad de huéspedes: ")
        if contingente.isdigit():
            try:
                contingente = int(contingente)
                break
            except ValueError:
                print("Respuesta inválida. Intente nuevamente. ")
    registro = str(datetime.now())[:-7]
    cursor.execute('''INSERT INTO HUESPEDES (APELLIDO, NOMBRE, TELEFONO, EMAIL, BOOKING, ESTADO, CHECKIN, CHECKOUT, DOCUMENTO, NACIMIENTO, HABITACION, CONTINGENTE, REGISTRO) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?) ''', (apellido,nombre,telefono,email,booking,estado,checkin,checkout,documento,nacimiento,habitacion,contingente,registro))
    conexion.commit()
    gestionar_huespedes()

def buscar_huesped():
    while True:
        campo = input("\n¿Cómo desea buscar al huesped?\n1. Por apellido\n2. Por número de huesped\n3. Por número de habitación\n4. Por documento\n5. Imprimir todos\n0. Cancelar\n")
        if campo.isdigit():
            try:
                campo = int(campo)
                if campo == 0:
                    gestionar_huespedes()
                    return
                elif campo == 1:
                    criterio = input("Ingrese el apellido: ")
                    criterio = f"%{criterio}%"
                    cursor.execute('SELECT * FROM HUESPEDES WHERE APELLIDO LIKE ?', (criterio,))
                    huespedes = cursor.fetchall()
                    if huespedes:
                        print("\nListado de huéspedes:\n")
                        for huesped in huespedes:
                            imprimir_huesped(huesped)
                        break
                    else:
                        print(f"No se encontraron huéspedes con el apellido {criterio}")
                elif campo == 2:
                    while True:
                        criterio = input("Ingrese el número de huesped: ")
                        if criterio.isdigit():
                            try:
                                criterio = int(criterio)
                                cursor.execute('SELECT * FROM HUESPEDES WHERE NUMERO = ?', (criterio,))
                                huesped = cursor.fetchone()
                                if not huesped == None:
                                    print(huesped)
                                    break
                                else:
                                    print(f"No se encontraron huéspedes con el número {criterio}")
                                    buscar_huesped()
                                    return
                                break
                            except ValueError:
                                print("Numero inválido. Intente nuevamente.")
                elif campo == 3:
                    while True:
                        criterio = input("Ingrese el número de habitación: ")
                        if criterio.isdigit():
                            try:
                                criterio = int(criterio)
                                cursor.execute('SELECT * FROM HUESPEDES WHERE HABITACION = ?', (criterio,))
                                huesped = cursor.fetchone()
                                if not huesped == None:
                                    print(huesped)
                                    break
                                else:
                                    print(f"No se encontraron huéspedes en la habitación {criterio}")
                                    buscar_huesped()
                                    return
                                break
                            except ValueError:
                                print("Numero inválido. Intente nuevamente.")
                elif campo == 4:
                    criterio = input("Ingrese el número de documento: ")
                    cursor.execute('SELECT * FROM HUESPEDES WHERE DOCUMENTO LIKE ?', (criterio,))
                    huespedes = cursor.fetchall()
                    if huespedes:
                        print("Listado de huésspedes\n")
                        for huesped in huespedes:
                            imprimir_huesped(huesped)
                        break
                    else:
                        print(f"No se encontraron huéspedes con el documento {criterio}")
                        buscar_huesped()
                        return
                    break
                elif campo == 5:
                    cursor.execute('SELECT * FROM HUESPEDES')
                    huespedes = cursor.fetchall()
                    if huespedes:
                        for huesped in huespedes:
                            imprimir_huesped(huesped)
                    break
            except ValueError:
                print("Respuesta inválida. Intente nuevamente. ")
                continue
        else:
            print("Respuesta inválida. Intente nuevamente. ")
    #1 Preguntar que hacer con el huesped que buscamos
    gestionar_huespedes()

def imprimir_huesped(huesped):
    columnas = [desc[0] for desc in cursor.description]
    for col, val in zip(columnas, huesped):
        print(f"{col}: {val}")
    print("-" * 40)

def cambiar_estado():
    

def gestionar_consumos():
    respuesta_consumos = input("\n1. Agregar consumo\n2. Ver consumos\n9. Volver al inicio\n")
    try:
        respuesta_consumos = int(respuesta_consumos)
    except ValueError:
        print("Elección inválida. Intente nuevamente: ")
        gestionar_consumos()
    if respuesta_consumos == 1:
        agregar_consumo()
    elif respuesta_consumos == 2:
        ver_consumos()
    elif respuesta_consumos == 9:
        inicio()
    else: gestionar_consumos()

def gestionar_productos():
    respuesta_productos = input("\n1. Agregar producto\n2. Ver productos\n3. Editar producto\n4. Eliminar producto\n9. Volver al inicio\n")
    try:
        respuesta_productos = int(respuesta_productos)
    except ValueError:
        print("Elección inválida. Intente nuevamente: ")
        gestionar_productos()
    if respuesta_productos == 1:
        agregar_producto()
    elif respuesta_productos == 2:
        ver_productos()
    elif respuesta_productos == 3:
        editar_producto()
    elif respuesta_productos == 4:
        eliminar_producto()
    elif respuesta_productos == 9:
        inicio()
    else: gestionar_productos()

def agregar_producto():
    nombre = input("\nEscriba el nombre del producto: ")
    precio = 0.01
    while True:
        respuesta_precio = str(input("Ingrese el precio del producto: "))
        try:
            precio = float(respuesta_precio.replace("," , "."))
            break
        except ValueError:
            print("El precio ingresado es un valor no valido")

    cursor.execute('''INSERT INTO PRODUCTOS (NOMBRE, PRECIO) VALUES (?,?) ''', (nombre,precio))
    conexion.commit()
    gestionar_productos()

def ver_productos():
    cursor.execute(''' SELECT * FROM PRODUCTOS ''')
    print("")
    for producto in cursor.fetchall():
        print(producto)
    gestionar_productos()

""" def editar_producto(repre = 0):
    if repre == 0:
        codigo = input("\nIngrese el código del producto que desea editar, ó ingrese * para ver el listado: ")
    elif repre == 1:
        codigo = input("\nIngrese el código del producto que desea editar: ")
    elif repre == 2:
        codigo = input("\nEl código ingresado es inválido. Intente nuevamente: ")
    if codigo == "*":
        cursor.execute(''' SELECT * FROM PRODUCTOS ''')
        print("")
        for producto in cursor.fetchall():
            print(producto)
        editar_producto(1)
    elif codigo.isdigit():
        try:
            codigo = int(codigo)
            if codigo == 0:
                editar_producto(2)
        except ValueError:
            editar_producto(2)
    else:
        editar_producto(2)
    #Acá ya tenemos "codigo"
    editando = cursor.execute(''' SELECT * FROM PRODUCTOS WHERE CODIGO = {}'''.format(codigo))
    editado = editando.fetchone()
    if editado == None:
        print("editado es None")
        editar_producto(2)
    else:
        print("editado es:")
        print(editado)
    def pregunta_edicion(repre = 0):
        if repre == 0:
            respuesta_edicion = input("\n¿Quiere editar el nombre(1) ó el precio(2) ó cancelar(0)? ")
        else:
            respuesta_edicion = input("\nElección invalida. ¿Quiere editar el nombre(1) ó el precio(2) ó cencelar (0)? ")
        if respuesta_edicion.isdigit():
            respuesta_edicion = int(respuesta_edicion)
            if respuesta_edicion == 0:
                gestionar_productos()
            elif respuesta_edicion == 1:
                respuesta_edicion = "NOMBRE"
                return respuesta_edicion
            elif respuesta_edicion == 2:
                respuesta_edicion = "PRECIO"
                return respuesta_edicion
            else:
                print("Respuesta identificada ni 0, ni 1, ni 2")
                pregunta_edicion(1)
        else:
            return pregunta_edicion(1)
    edicion = pregunta_edicion()
    #Acá ya tenemos "edición"
    def pregunta_nombre(repre=0):
        if repre == 0:
            respuesta_nombre = input(f"Ingrese el nuevo nombre ó cancelar(0): ")
        else:
            respuesta_nombre = input(f"Inválido. Ingrese el nuevo nombre ó cancelar(0): ")
        try:
            respuesta_nombre = int(respuesta_nombre)
            if respuesta_nombre == 0:
                gestionar_productos()
            else:
                pregunta_nombre(1)
        except ValueError:
            return respuesta_nombre
    def pregunta_precio(repre=0):
        if repre == 0:
            respuesta_precio = str(input(f"Ingrese el nuevo precio: "))
        else:
            respuesta_precio = str(input(f"Valor inválido. Ingrese el nuevo precio: "))
        try:
            if "," in respuesta_precio:
                respuesta_precio = float(respuesta_precio.replace("," , "."))
                return respuesta_precio
            else:
                respuesta_precio = float(respuesta_precio)
                return respuesta_precio
        except ValueError:
            pregunta_precio(1)
    if edicion == "NOMBRE":
        valor = pregunta_nombre()
    elif edicion == "PRECIO":
        valor = pregunta_precio()
    else:
        print("no se por que termina acá")
    update = ''' UPDATE PRODUCTOS SET {} = '{}' WHERE CODIGO = {} '''.format(edicion, valor, codigo)
    cursor.execute(update)
    conexion.commit()
    gestionar_productos() """

def editar_producto():
    while True:
        codigo = input("\nIngrese el código del producto que desea editar, ingrese (*) para ver el listado ó ingrese (0) para cancelar: ").strip()
        if codigo == "*":
            cursor.execute('SELECT * FROM PRODUCTOS')
            productos = cursor.fetchall()
            if productos:
                print("\nListado de productos:")
                for producto in productos:
                    print(producto)
            else:
                print("No hay productos disponibles.")
            continue
        if not codigo.isdigit():
            print("Código inválido. Intente nuevamente.")
            continue
        if int(codigo) == 0:
            print("Edición cancelada.")
            gestionar_productos()
            return
        codigo = int(codigo)
        cursor.execute('SELECT * FROM PRODUCTOS WHERE CODIGO = ?', (codigo,))
        producto = cursor.fetchone()
        if producto is None:
            print("\nProducto no encontrado. Intente nuevamente.")
            continue
        print(f"\nProducto seleccionado:\n{producto}")
        break

    while True:
        opcion = input("\n¿Desea editar el nombre (1), el precio (2) o cancelar (0)? ").strip()
        if opcion == "0":
            print("Edición cancelada.")
            break
        elif opcion == "1":            
            nuevo_nombre = input("Ingrese el nuevo nombre: ").strip()
            if nuevo_nombre:
                cursor.execute('UPDATE PRODUCTOS SET NOMBRE = ? WHERE CODIGO = ?', (nuevo_nombre, codigo))
                conexion.commit()
                print("Nombre actualizado exitosamente.")
                break
            else:
                print("El nombre no puede estar vacío.")
        elif opcion == "2":
            nuevo_precio = input("Ingrese el nuevo precio: ").strip().replace(",", ".")
            try:
                nuevo_precio = float(nuevo_precio)
                cursor.execute('UPDATE PRODUCTOS SET PRECIO = ? WHERE CODIGO = ?', (nuevo_precio, codigo))
                conexion.commit()
                print("Precio actualizado exitosamente.")
                break
            except ValueError:
                print("Precio inválido. Intente nuevamente.")
        else:
            print("Opción inválida. Intente nuevamente.")
    gestionar_productos()

def eliminar_producto(repre = 0):
    while True:
        codigo = input("\nIngrese el código del producto que desea eliminar, ingrese * para ver el listado ó ingrese 0 para cancelar: ")
        if codigo == "*":
            cursor.execute('SELECT * FROM PRODUCTOS')
            productos = cursor.fetchall()
            if productos:
                print("\nListado de productos:")
                for producto in productos:
                    print(producto)
            else:
                print("No hay productos disponibles.")
            continue
        if not codigo.isdigit():
            print("Código inválido. Intente nuevamente.")
            continue
        if int(codigo) == 0:
            print("Eliminación cancelada.")
            break
        codigo = int(codigo)
        cursor.execute(''' DELETE FROM PRODUCTOS WHERE CODIGO = {}'''.format(codigo))
        conexion.commit()
        break
    gestionar_productos()

def gestionar_inventario():
    respuesta_inventario = input("\n1. Abrir inventario\n2. Ingresar compra\n9. Volver al inicio\n")
    try:
        respuesta_inventario = int(respuesta_inventario)
    except ValueError:
        print("Elección inválida. Intente nuevamente: ")
        gestionar_inventario()
    if respuesta_inventario == 1:
        abrir_inventario()
    elif respuesta_inventario == 2:
        ingresar_compra()
    elif respuesta_inventario == 9:
        inicio()
    else: gestionar_inventario()

def generar_reportes():
    respuesta_reportes = input("\n1. Generar reporte de consumos diarios\n2. Generar reporte de consumos pendientes\n3. Generar reporte de consumos cerrados\n4. Generar reporte de pronto checkin\n9. Volver al inicio\n")
    try:
        respuesta_reportes = int(respuesta_reportes)
    except ValueError:
        print("Elección inválida. Intente nuevamente: ")
        generar_reportes()
    if respuesta_reportes == 1:
        reporte_diario()
    elif respuesta_reportes == 2:
        reporte_pendientes()
    elif respuesta_reportes == 3:
        reporte_cerrados()
    elif respuesta_reportes == 4:
        reporte_pronto_checkin()
    elif respuesta_reportes == 9:
        inicio()
    else: generar_reportes()


###INTERFAZ GRAFICA###


### PROGRAMA ###

print("Bienvenido al sistema de gestión de la posada Onda de mar 1.0 (Demo)")
productos_existe()
huespedes_existe()
inicio()