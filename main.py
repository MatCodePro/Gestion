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

def solo_por_hoy():
    cursor.execute("ALTER TABLE HUESPEDES RENAME TO HUESPEDES_OLD")

    # Paso 2: Crear la nueva tabla con ESTADO como TEXT
    cursor.execute("""CREATE TABLE HUESPEDES (NUMERO INTEGER PRIMARY KEY AUTOINCREMENT, APELLIDO TEXT, NOMBRE TEXT, TELEFONO INTEGER, EMAIL TEXT, BOOKING TEXT, ESTADO TEXT, CHECKIN TEXT, CHECKOUT TEXT, DOCUMENTO INTEGER, NACIMIENTO INTEGER, HABITACION INTEGER, CONTINGENTE INTEGER, REGISTRO TEXT)""")

    # Paso 3: Copiar los datos, convirtiendo ESTADO a TEXT
    cursor.execute("""INSERT INTO HUESPEDES (NUMERO, APELLIDO, NOMBRE, TELEFONO, EMAIL, BOOKING, ESTADO, CHECKIN, CHECKOUT, DOCUMENTO, NACIMIENTO, HABITACION, CONTINGENTE, REGISTRO)
    SELECT NUMERO, APELLIDO, NOMBRE, TELEFONO, EMAIL, CAST(BOOKING AS TEXT), ESTADO, CHECKIN, CHECKOUT, DOCUMENTO, CAST(NACIMIENTO AS INTEGER), HABITACION, CONTINGENTE, REGISTRO
    FROM HUESPEDES_OLD
    """)

    # Paso 4: Eliminar la tabla antigua si todo está bien
    cursor.execute("DROP TABLE HUESPEDES_OLD")

    # Guardar cambios y cerrar
    conexion.commit()

def productos_existe():
    cursor.execute('''CREATE TABLE IF NOT EXISTS PRODUCTOS(CODIGO INTEGER PRIMARY KEY AUTOINCREMENT, NOMBRE TEXT, PRECIO REAL, STOCK INTEGER)''')

def huespedes_existe():
    cursor.execute('''CREATE TABLE IF NOT EXISTS HUESPEDES(NUMERO INTEGER PRIMARY KEY AUTOINCREMENT, APELLIDO TEXT, NOMBRE TEXT, TELEFONO INTEGER, EMAIL TEXT, BOOKING TEXT, ESTADO TEXT, CHECKIN TEXT, CHECKOUT TEXT, DOCUMENTO INTEGER, NACIMIENTO INTEGER, HABITACION INTEGER, CONTINGENTE INTEGER, REGISTRO TEXT)''')

def imprimir_huesped(huesped):
    print(f"\nHuesped seleccionado:")
    columnas = [desc[0] for desc in cursor.description]
    for col, val in zip(columnas, huesped):
        print(f"{col}: {val}")
    print("")
    print("-" * 40)

def imprimir_huespedes(huespedes):
    print("\nListado de huéspedes:\n")
    for huesped in huespedes:
        columnas = [column[0] for column in cursor.description]
        for col, val in zip(columnas, huesped):
            print(f"{col}: {val}")
        print("")
    print("-" * 40)

def pedir_fecha_valida(mensaje):
    while True:
        fecha_input = input(mensaje)
        try:
            fecha = datetime.strptime(fecha_input, '%d-%m-%Y').date()
            if fecha >= date.today():
                return fecha_input  # Devolvemos la cadena válida para guardar
            else:
                print("La fecha debe ser igual o posterior a hoy.")
        except ValueError:
            print("Formato inválido. Use DD-MM-YYYY.")

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
    respuesta_huespedes = input("\n1. Registrar nuevo huesped\n2. Buscar un huesped\n3. Cambiar el estado de un huesped\n4. Editar huesped\n5. Eliminar un huesped\n0. Volver al inicio\n")
    try:
        respuesta_huespedes = int(respuesta_huespedes)
    except ValueError:
        print("Elección inválida. Intente nuevamente: ")
        return gestionar_huespedes()
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
    elif respuesta_huespedes == 0:
        inicio()
    else: gestionar_huespedes()

def nuevo_huesped():
    while True:
        apellido = input("\nEscriba el apellido del huesped ó (0) para cancelar: ")
        if apellido.isdigit():
            try:
                apellido = int(apellido)
                if apellido == 0:
                    return gestionar_huespedes()
            except ValueError:
                print("Selección inválida. Intente nuevamente. ")
                continue
        else:
            apellido = unidecode(apellido)
            break
    while True:
        nombre = input("\nEscriba el nombre del huesped ó (0) para cancelar: ")
        if nombre.isdigit():
            try:
                nombre = int(nombre)
                if nombre == 0:
                    return gestionar_huespedes()
            except ValueError:
                print("Selección inválida. Intente nuevamente. ")
                continue
        else:
            nombre = unidecode(nombre)
            break
    while True:
        telefono = input("Ingrese un whatsapp de contacto: ")
        if telefono.isdigit():
            try:
                telefono = int(telefono)
                break
            except ValueError:
                print("Teléfono inválido. Intente nuevamente.")
        else:
            print("Teléfono inválido. Intente nuevamente.")
    email = input("Ingrese el e-mail de contacto: ")
    while True:
        respuesta_booking = input("Es una reserva de booking? si/no ")
        if respuesta_booking == "si" or respuesta_booking == "no":
            booking = respuesta_booking
            break
        else:
            print('Respuesta inválida. Intente nuevamente con "si" o "no" ')
    while True:
        pregunta_estado = input("Es un huesped programado (1) ó es un checkin (2)? ")
        try:
            pregunta_estado = int(pregunta_estado)
            if pregunta_estado == 1:
                estado = "PROGRAMADO"
                checkin = pedir_fecha_valida("Ingrese la fecha de checkin (DD-MM-YYYY): ")
                while True:
                    checkout = input("Ingrese la fecha de checkout en formato DD-MM-YYYY: ")
                    numeros_checkout = checkout.split("-")
                    fecha_checkout = date(numeros_checkout[2],numeros_checkout[1],numeros_checkout[0])
                    numeros = checkin.split("-")
                    fecha_checkin = date(numeros[2],numeros[1],numeros[0])
                    if fecha_checkout >= fecha_checkin:
                        break
                    else:
                        print("La fecha de checkout es anterior a la fecha de checkin.")
                documento = 0
                nacimiento = 0
                habitacion = 0
                break
            elif pregunta_estado == 2:
                estado = "ABIERTO"
                checkin = str(date.today())
                checkout = pedir_fecha_valida("Ingrese la fecha de checkout en formato DD-MM-YYYY: ")
                while datetime.strptime(checkout, '%d-%m-%Y').date() < datetime.strptime(checkin, '%d-%m-%Y').date():
                    print("La fecha de checkout no puede ser anterior al checkin.")
                    checkout = pedir_fecha_valida("Ingrese la fecha de checkout nuevamente (DD-MM-YYYY): ")
                documento = input("Ingerse el documento: ")
                while True:
                    nacimiento = input("Ingrese el año de nacimiento: ")
                    try:
                        nacimiento = int(nacimiento)
                        if nacimiento > 1900:
                            break
                        else:
                            print("Año inválido. Intente nuevamente")
                            continue
                    except ValueError:
                        print("Año inválido. Intente nuevamente")
                habitacion = input("Ingresa el número de habitación: ")
                break
            elif pregunta_estado == 0:
                return gestionar_huespedes()
            else:
                print("Respuesta inválida. Intente nuevamente. ")
                continue
        except ValueError:
            print("Respuesta inválida. Intente nuevamente. ")
    while True:
        contingente = input("Ingrese la cantidad de huéspedes: ")
        try:
            contingente = int(contingente)
            break
        except ValueError:
            print("Respuesta inválida. Intente nuevamente. ")
    registro = f"CREADO {estado} - {str(datetime.now())[:-7]}"
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
                    return gestionar_huespedes()
                elif campo == 1:
                    criterio = input("Ingrese el apellido: ")
                    criterio = f"%{criterio}%"
                    cursor.execute('SELECT * FROM HUESPEDES WHERE APELLIDO LIKE ?', (criterio,))
                    huespedes = cursor.fetchall()
                    if huespedes:
                        imprimir_huespedes(huespedes)
                        break
                    else:
                        criterio = criterio.replace("%","")
                        print(f"No se encontraron huéspedes con el apellido {criterio}")
                        return buscar_huesped()
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
                                    return buscar_huesped()
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
                                    return buscar_huesped()
                            except ValueError:
                                print("Numero inválido. Intente nuevamente.")
                elif campo == 4:
                    criterio = input("Ingrese el número de documento: ")
                    cursor.execute('SELECT * FROM HUESPEDES WHERE DOCUMENTO LIKE ?', (criterio,))
                    huespedes = cursor.fetchall()
                    if huespedes:
                        imprimir_huespedes(huespedes)
                        break
                    else:
                        print(f"No se encontraron huéspedes con el documento {criterio}")
                        return buscar_huesped()
                elif campo == 5:
                    cursor.execute('SELECT * FROM HUESPEDES')
                    huespedes = cursor.fetchall()
                    if huespedes:
                        imprimir_huespedes(huespedes)
                        break
                    else:
                        print("No se encontraron huespedes")
                        return gestionar_huespedes()
                else:
                    print("Respuesta inválida. Intente nuevamente. ")
                editar_huesped()
            except ValueError:
                print("Respuesta inválida. Intente nuevamente. ")
                continue
        else:
            print("Respuesta inválida. Intente nuevamente. ")
    #1 Preguntar que hacer con el huesped que buscamos
    gestionar_huespedes()

def cambiar_estado():
    while True:
        numero = input("Ingrese el número de huesped que desea cambiar el estado, ingrese (*) para buscar ó ingrese (0) para cancelar: ")
        if numero == "*":
            return buscar_huesped()
        try:
            numero = int(numero)
            if numero == 0:
                print("Cambio cancelado.")
                return gestionar_huespedes()
            else:
                cursor.execute('SELECT * FROM HUESPEDES WHERE NUMERO = ?', (numero,))
                huesped = cursor.fetchone()
                if huesped is None:
                    print("\nHuesped no encontrado. Intente nuevamente.")
                    continue
                print(f"\nHuesped seleccionado:\n{huesped}")
                break
        except ValueError:
            print("Selección inválida. Intente nuevamente.")
            continue
    
    while True:
        opcion = input('\n¿A qué estado quiere cambiar? Ingrese (1) "PROGRAMADO", (2) "ABIERTO", (3) "CERRADO", ó (0) para cancelar: ')
        if opcion == "0":
            print("Cambio cancelado.")
            return cambiar_estado()
        elif opcion == "1":
            estado = "PROGRAMADO"
            checkin = pedir_fecha_valida("Ingrese la nueva fecha de checkin (DD-MM-YYYY): ")
            checkout = pedir_fecha_valida("Ingrese la nueva fecha de checkout (DD-MM-YYYY): ")
            while datetime.strptime(checkout, '%d-%m-%Y').date() < datetime.strptime(checkin, '%d-%m-%Y').date():
                print("La fecha de checkout no puede ser anterior al checkin.")
                checkout = pedir_fecha_valida("Ingrese la fecha de checkout nuevamente (DD-MM-YYYY): ")
            cursor.execute('SELECT NACIMIENTO FROM HUESPEDES WHERE NUMERO = ?',(numero,))
            nacimiento = cursor.fetchone()[0]
            if nacimiento < 1900:
                while True:
                    nacimiento = input("Ingrese el año de nacimiento: ")
                    try:
                        nacimiento = int(nacimiento)
                        if nacimiento > 1900:
                            break
                        else:
                            print("Año inválido. Intente nuevamente")
                            continue
                    except ValueError:
                        print("Año inválido. Intente nuevamente")
            habitacion = 0
            registro = f"Estado modificado a {estado} - {str(datetime.now())[:-7]}"
            cursor.execute('''UPDATE HUESPEDES SET ESTADO = ?, CHECKIN = ?, CHECKOUT = ?, NACIMIENTO = ?, HABITACION = ?, REGISTRO = ? WHERE NUMERO = ?''', (estado,checkin,checkout,nacimiento,habitacion,registro,numero))
            conexion.commit()
        elif opcion == "2":
            estado = "ABIERTO"
            checkin = str(date.today())
            checkout = pedir_fecha_valida("Ingrese la nueva fecha de checkout (DD-MM-YYYY): ")
            while datetime.strptime(checkout, '%d-%m-%Y').date() < datetime.strptime(checkin, '%d-%m-%Y').date():
                print("La fecha de checkout no puede ser anterior al checkin.")
                checkout = pedir_fecha_valida("Ingrese la fecha de checkout nuevamente (DD-MM-YYYY): ")
            cursor.execute('SELECT NACIMIENTO FROM HUESPEDES WHERE NUMERO = ?',(numero,))
            documento = input("Ingerse el documento: ")
            cursor.execute('SELECT NACIMIENTO FROM HUESPEDES WHERE NUMERO = ?',(numero,))
            nacimiento = cursor.fetchone()[0]
            if nacimiento < 1900:
                while True:
                    nacimiento = input("Ingrese el año de nacimiento: ")
                    try:
                        nacimiento = int(nacimiento)
                        if nacimiento > 1900:
                            break
                        else:
                            print("Año inválido. Intente nuevamente")
                            continue
                    except ValueError:
                        print("Año inválido. Intente nuevamente")
            habitacion = input("Ingresa el número de habitación: ")
            while True:
                contingente = input("Ingrese la cantidad de huéspedes: ")
                try:
                    contingente = int(contingente)
                    break
                except ValueError:
                    print("Respuesta inválida. Intente nuevamente. ")
            cursor.execute('''UPDATE HUESPEDES ESTADO = ?, CHECKIN = ?, CHECKOUT = ?, DOCUMENTO = ?, NACIMIENTO = ?, HABITACION = ?, CONTINGENTE = ? WHERE NUMERO = ?''', (estado,checkin,checkout,documento,nacimiento,habitacion,contingente,numero))
            conexion.commit()
        elif opcion == "3":
            estado = "CERRADO"
            checkout = str(date.today())
            cursor.execute('''UPDATE HUESPEDES ESTADO = ?, CHECKOUT = ?, HABITACION = ? WHERE NUMERO = ?''', (estado,checkout,0,numero))
            conexion.commit()
        else:
            print("Elección inválida. Intente nuevamente")
        cursor.execute("SELECT REGISTRO FROM HUESPEDES WHERE NUMERO = ?", (numero,))
        registro_anterior = f"{cursor.fetchone()[0]}\n"
        registro_actual = f"Estado modificado a {estado} - {str(datetime.now())[:-7]}"
        nuevo_registro = registro_anterior + registro_actual
        cursor.execute("UPDATE HUESPEDES SET REGISTRO = ? WHERE NUMERO = ?", (nuevo_registro, numero))
        conexion.commit()
        print("Estado actualizado exitosamente: ")
        break
    gestionar_huespedes()

def editar_huesped():
    while True:
        numero = input("Ingrese el número de huesped que desea editar, ingrese (*) para buscar ó ingrese (0) para cancelar: ")
        if numero == "*":
            return buscar_huesped()
        try:
            numero = int(numero)
            if numero == 0:
                print("Edición cancelada.")
                return gestionar_huespedes()
            else:
                cursor.execute('SELECT * FROM HUESPEDES WHERE NUMERO = ?', (numero,))
                huesped = cursor.fetchone()
                if huesped is None:
                    print("\nHuesped no encontrado. Intente nuevamente.")
                    continue
                imprimir_huesped(huesped)
                break
        except ValueError:
            print("Selección inválida. Intente nuevamente.")
            continue
    while True:
        opcion = input("\n¿Desea editar el apellido (1), nombre (2), teléfono (3), e-mail (4), booking (5), checkin (6), checkout (7), documento (8), nacimiento (9), habitación (10), contingente (11) ó cancelar (0)? ")
        if opcion == "0":
            print("Edición cancelada.")
            break
        elif opcion == "1":            
            nuevo_apellido = input("Ingrese el nuevo apellido: ")
            if nuevo_apellido:
                cursor.execute('UPDATE HUESPEDES SET APELLIDO = ? WHERE NUMERO = ?', (nuevo_apellido, numero))
                conexion.commit()
                print("Apellido actualizado exitosamente.")
                break
            else:
                print("El apellido no puede estar vacío.")
        elif opcion == "2":            
            nuevo_nombre = input("Ingrese el nuevo nombre: ")
            if nuevo_nombre:
                cursor.execute('UPDATE HUESPEDES SET NOMBRE = ? WHERE NUMERO = ?', (nuevo_nombre, numero))
                conexion.commit()
                print("Nombre actualizado exitosamente.")
                break
            else:
                print("El nombre no puede estar vacío.")
        elif opcion == "3":            
            while True:
                nuevo_telefono = input("Ingrese el nuevo whatsapp de contacto: ")
                if nuevo_telefono:
                    try:
                        nuevo_telefono = int(nuevo_telefono)
                        cursor.execute('UPDATE HUESPEDES SET TELEFONO = ? WHERE NUMERO = ?', (nuevo_telefono, numero))
                        conexion.commit()
                        print("Teléfono actualizado exitosamente.")
                        break
                    except ValueError:
                        print("Teléfono inválido. Intente nuevamente.")
                else:
                    print("El teléfono no puede estar vacío.")
        elif opcion == "4":
            while True:
                nuevo_email = input("Ingrese el e-mail de contacto: ")
                if nuevo_email:
                    cursor.execute('UPDATE HUESPEDES SET EMAIL = ? WHERE NUMERO = ?', (nuevo_email, numero))
                    conexion.commit()
                    print("E-mail actualizado exitosamente.")
                    break
                else:
                    print("El e-mail no puede estar vacío.")
        elif opcion == "5":
            while True:
                nuevo_booking = input("Es una reserva de booking? si/no ")
                if nuevo_booking:
                    if nuevo_booking == "si" or nuevo_booking == "no":
                        cursor.execute('UPDATE HUESPEDES SET BOOKING = ? WHERE NUMERO = ?', (nuevo_booking, numero))
                        conexion.commit()
                        print("Booking actualizado exitosamente.")
                        break
                    else:
                        print('Respuesta inválida. Intente nuevamente con "si" o "no" ')
                else:
                    print("Booking no puede estar vacío.")
        elif opcion == "6":
            while True:
                nuevo_checkin = pedir_fecha_valida("Ingrese la nueva fecha de checkin (DD-MM-YYYY): ")
                cursor.execute('UPDATE HUESPEDES SET CHECKIN = ? WHERE NUMERO = ?', (nuevo_checkin, numero))
                conexion.commit()
                print("Checkin actualizado exitosamente.")
        elif opcion == "7":
            while True:
                    nuevo_checkout = input("Ingrese la fecha de checkout en formato DD-MM-YYYY: ")
                    try:
                        datetime.datetime.strptime(nuevo_checkout, '%d-%m-%Y')
                        numeros_checkout = nuevo_checkout.split("-")
                        fecha_checkout = date(numeros_checkout[2],numeros_checkout[1],numeros_checkout[0])
                        cursor.execute("SELECT CHECKIN FROM HUESPEDES WHERE NUMERO = ?", (numero,))
                        checkin = f"{cursor.fetchone()[0]}\n"
                        numeros = checkin.split("-")
                        fecha_checkin = date(numeros[2],numeros[1],numeros[0])
                        if fecha_checkout >= fecha_checkin:
                            cursor.execute("UPDATE HUESPEDES SET CHECKOUT = ? WHERE NUMERO = ?", (nuevo_checkout, numero))
                            conexion.commit()
                            print("Checkout actualizado exitosamente: ")
                            break
                        else:
                            print("La fecha de checkout es anterior a la fecha de checkin.")
                    except ValueError:
                        print("Formato de fecha no válido. Intente nuevamente.")
        elif opcion == "8":
            nuevo_documento = input("Ingrese el nuevo documento: ")
            cursor.execute("UPDATE HUESPEDES SET DOCUMENTO = ? WHERE NUMERO = ?", (nuevo_documento, numero))
            conexion.commit()
            print("Documento actualizado exitosamente: ")
        elif opcion == "9":
            while True:
                nuevo_nacimiento = input("Ingrese el año de nacimiento: ")
                try:
                    nuevo_nacimiento = int(nuevo_nacimiento)
                    if nuevo_nacimiento > 1900:
                        cursor.execute("UPDATE HUESPEDES SET NACIMIENTO = ? WHERE NUMERO = ?", (nuevo_nacimiento, numero))
                        conexion.commit()
                        print("Nacimiento actualizado exitosamente: ")
                        break
                    else:
                        print("Año inválido. Intente nuevamente")
                        continue
                except ValueError:
                    print("Año inválido. Intente nuevamente")
        elif opcion == "10":
            while True:
                nueva_habitacion = input("Ingrese la nueva habitación: ")
                try:
                    nueva_habitacion = int(nueva_habitacion)
                    if nueva_habitacion < 8:
                        cursor.execute("UPDATE HUESPEDES SET HABITACION = ? WHERE NUMERO = ?", (nueva_habitacion, numero))
                        conexion.commit()
                        print("Habitación actualizada exitosamente: ")
                        break
                    else:
                        print("Habitación inválida. Intente nuevamente")
                except ValueError:
                    print("Habitación inválida. Intente nuevamente")
        elif opcion == "11":
            while True:
                nuevo_contingente = input("Ingrese la cantidad de huéspedes: ")
                try:
                    nuevo_contingente = int(nuevo_contingente)
                    cursor.execute("UPDATE HUESPEDES SET CONTINGENTE = ? WHERE NUMERO = ?", (nuevo_contingente, numero))
                    conexion.commit()
                    print("Contingente actualizado exitosamente: ")
                    break
                except ValueError:
                    print("Cantidad inválida. Intente nuevamente")
    gestionar_huespedes()

def eliminar_huesped():
    while True:
        numero = input("Ingrese el número del huésped que desea eliminar, (*) para buscar o (0) para cancelar: ").strip()
        if numero == "*":
            buscar_huesped()
            return
        if not numero.isdigit():
            print("Número inválido. Intente nuevamente.")
            continue
        numero = int(numero)
        if numero == 0:
            print("Eliminación cancelada.")
            gestionar_huespedes()
            return

        # Buscar el huésped por número
        cursor.execute('SELECT * FROM HUESPEDES WHERE NUMERO = ?', (numero,))
        huesped = cursor.fetchone()
        if huesped is None:
            print("Huésped no encontrado. Intente nuevamente.")
            continue

        # Mostrar los datos del huésped
        imprimir_huesped(huesped)

        # Confirmación
        confirmacion = input("¿Está seguro que desea eliminar este huésped? (si/no): ").lower()
        if confirmacion == "si":
            cursor.execute('DELETE FROM HUESPEDES WHERE NUMERO = ?', (numero,))
            conexion.commit()
            print("Huésped eliminado correctamente.\n")
            gestionar_huespedes()
            return
        elif confirmacion == "no":
            print("Eliminación cancelada.\n")
            gestionar_huespedes()
            return
        else:
            print("Respuesta inválida. Se canceló la eliminación por seguridad.\n")
            gestionar_huespedes()
            return

def gestionar_consumos():
    respuesta_consumos = input("\n1. Agregar consumo\n2. Ver consumos\n9. Volver al inicio\n")
    try:
        respuesta_consumos = int(respuesta_consumos)
    except ValueError:
        print("Elección inválida. Intente nuevamente: ")
        return gestionar_consumos()
    if respuesta_consumos == 1:
        agregar_consumo()
    elif respuesta_consumos == 2:
        ver_consumos()
    elif respuesta_consumos == 9:
        inicio()
    else: gestionar_consumos()

def gestionar_productos():
    respuesta_productos = input("\n1. Agregar producto\n2. Ver productos\n3. Buscar productos\n4. Editar producto\n5. Eliminar producto\n0. Volver al inicio\n")
    try:
        respuesta_productos = int(respuesta_productos)
    except ValueError:
        print("Elección inválida. Intente nuevamente: ")
        return gestionar_productos()
    if respuesta_productos == 1:
        agregar_producto()
    elif respuesta_productos == 2:
        ver_productos()
    elif respuesta_productos == 3:
        buscar_producto()
    elif respuesta_productos == 4:
        editar_producto()
    elif respuesta_productos == 5:
        eliminar_producto()
    elif respuesta_productos == 0:
        inicio()
    else: gestionar_productos()

def agregar_producto():
    nombre = input("\nEscriba el nombre del producto ó (0) para cancelar: ")
    precio = 0.01
    stock = 0
    if nombre == 0:
        return gestionar_productos()
    else: 
        while True:
            respuesta_precio = str(input("Ingrese el precio del producto: "))
            try:
                precio = float(respuesta_precio.replace("," , "."))
                break
            except ValueError:
                print("El precio ingresado es un valor no valido")
        cursor.execute('''INSERT INTO PRODUCTOS (NOMBRE, PRECIO, STOCK) VALUES (?,?,?) ''', (nombre,precio,stock))
        conexion.commit()
        gestionar_productos()

def ver_productos():
    cursor.execute(''' SELECT * FROM PRODUCTOS ''')
    print("")
    for producto in cursor.fetchall():
        print(producto)
    gestionar_productos()

def buscar_producto():
    criterio = input("Ingrese el producto que desea buscar ó (0) para cancelar: ")
    if criterio == 0:
        return gestionar_productos()
    else:
        def buscar_criterio(criterio):
            # Separar palabras clave
            criterios = criterio.strip().lower().split()
            if not criterios:
                print("No se ingresaron criterios de búsqueda.")
                buscar_producto()
                
            # Crear la cláusula WHERE dinámica
            where_clauses = []
            params = []
            for palabra in criterios:
                where_clauses.append("LOWER(NOMBRE) LIKE ?")
                params.append(f"%{palabra}%")
            
            where_query = " OR ".join(where_clauses)
            
            query = f"SELECT * FROM PRODUCTOS WHERE {where_query}"
            cursor.execute(query, params)
            productos = cursor.fetchall()

            # Calcular la relevancia (cantidad de coincidencias de palabras clave)
            resultados = []
            for producto in productos:
                nombre = producto[1].lower()
                coincidencias = sum(1 for palabra in criterios if palabra in nombre)
                resultados.append((producto, coincidencias))

            # Ordenar por coincidencias (mayor a menor)
            resultados.sort(key=lambda x: x[1], reverse=True)

            # Mostrar con formato
            if resultados:
                print(f"\nResultados para: '{criterio}'\n")
                print(f"{'ID':<5} {'Nombre':<30} {'Precio':<10} {'Stock':<10}")
                print("-" * 60)
                for producto, relevancia in resultados:
                    id_prod = producto[0]
                    nombre = producto[1]
                    precio = producto[2]
                    stock = producto[3]
                    print(f"{id_prod:<5} {nombre:<30} {precio:<10.2f} {stock:<10}")
            else:
                print(f"\nNo se encontraron productos que coincidan con: '{criterio}'")
        buscar_criterio(criterio)

def editar_producto():
    while True:
        codigo = input("\nIngrese el código del producto que desea editar, ingrese (*) para ver el listado ó ingrese (0) para cancelar: ")
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
        try:
            codigo = int(codigo)
            if codigo == 0:
                print("Edición cancelada.")
                return gestionar_productos()
            else:
                cursor.execute('SELECT * FROM PRODUCTOS WHERE CODIGO = ?', (codigo,))
                producto = cursor.fetchone()
                if producto is None:
                    print("\nProducto no encontrado. Intente nuevamente.")
                    continue
                print(f"\nProducto seleccionado:\n{producto}")
                break
        except ValueError:
            print("Código inválido. Intente nuevamente.")
            continue

    while True:
        opcion = input("\n¿Desea editar el nombre (1), el precio (2) o cancelar (0)? ")
        if opcion == "0":
            print("Edición cancelada.")
            break
        elif opcion == "1":            
            nuevo_nombre = input("Ingrese el nuevo nombre: ")
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
        codigo = input("\nIngrese el código del producto que desea eliminar, ingrese (*) para ver el listado ó ingrese (0) para cancelar: ")
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