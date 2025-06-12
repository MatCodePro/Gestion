#TODO:

#Cargar productos al huesped

#Inventario

#producir_informes()
#Generar reporte de huéspedes en estado ABIERTO
#Generar reporte de huéspedes en estado A LA ESPERA cuya fecha de checkin sea el día siguiente

from datetime import datetime, date
import sqlite3
from unidecode import unidecode
import re


### CLASES ###

class DBManager:
    def __init__(self, db_path="BaseDeDatos"):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

    def ejecutar(self, query, params=()):
        self.cursor.execute(query, params)
        self.conn.commit()

    def obtener_uno(self, query, params=()): # Renamed from 'uno'
        self.cursor.execute(query, params)
        return self.cursor.fetchone()

    def obtener_todos(self, query, params=()): # Renamed from 'todos'
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def cerrar(self):
        self.conn.close()


### VARIABLES GLOBALES ###

db = DBManager()


### FUNCIONES ###

def productos_existe():
    db.ejecutar('''CREATE TABLE IF NOT EXISTS PRODUCTOS(CODIGO INTEGER PRIMARY KEY AUTOINCREMENT, NOMBRE TEXT, PRECIO REAL, STOCK INTEGER)''')
    #cursor.execute('''CREATE TABLE IF NOT EXISTS PRODUCTOS(CODIGO INTEGER PRIMARY KEY AUTOINCREMENT, NOMBRE TEXT, PRECIO REAL, STOCK INTEGER)''')

def huespedes_existe():
    db.ejecutar('''CREATE TABLE IF NOT EXISTS HUESPEDES(NUMERO INTEGER PRIMARY KEY AUTOINCREMENT, APELLIDO TEXT, NOMBRE TEXT, TELEFONO INTEGER, EMAIL TEXT, BOOKING TEXT, ESTADO TEXT, CHECKIN TEXT, CHECKOUT TEXT, DOCUMENTO INTEGER, NACIMIENTO INTEGER, HABITACION INTEGER, CONTINGENTE INTEGER, REGISTRO TEXT)''')
    #cursor.execute('''CREATE TABLE IF NOT EXISTS HUESPEDES(NUMERO INTEGER PRIMARY KEY AUTOINCREMENT, APELLIDO TEXT, NOMBRE TEXT, TELEFONO INTEGER, EMAIL TEXT, BOOKING TEXT, ESTADO TEXT, CHECKIN TEXT, CHECKOUT TEXT, DOCUMENTO INTEGER, NACIMIENTO INTEGER, HABITACION INTEGER, CONTINGENTE INTEGER, REGISTRO TEXT)''')

def imprimir_huesped(huesped):
    print(f"\nHuésped seleccionado:")
    columnas = ["NUMERO", "APELLIDO", "NOMBRE", "TELEFONO", "EMAIL", "BOOKING", "ESTADO","CHECKIN", "CHECKOUT", "DOCUMENTO", "NACIMIENTO", "HABITACION", "CONTINGENTE", "REGISTRO"]
    for col, val in zip(columnas, huesped):
        if col in ("CHECKIN", "CHECKOUT"):
            val = formatear_fecha(val)
        print(f"{col}: {val}")
    print("-" * 40)

def imprimir_huespedes(huespedes):
    columnas = ["NUMERO", "APELLIDO", "NOMBRE", "TELEFONO", "EMAIL", "BOOKING", "ESTADO", "CHECKIN", "CHECKOUT", "DOCUMENTO", "NACIMIENTO", "HABITACION", "CONTINGENTE", "REGISTRO"]
    print("\nListado de huéspedes:\n")
    for huesped in huespedes:
        for col, val in zip(columnas, huesped):
            if col in ("CHECKIN", "CHECKOUT"):
                val = formatear_fecha(val)
            print(f"{col}: {val}")
        print("-" * 40)

def pedir_fecha_valida(mensaje):
    while True:
        fecha_input = input(mensaje).strip()
        try:
            fecha = datetime.strptime(fecha_input, '%d-%m-%Y').date()
            if fecha >= date.today():
                return fecha.isoformat()  # → 'YYYY-MM-DD'
            else:
                print("La fecha debe ser igual o posterior a hoy.")
        except ValueError:
            print("Formato inválido. Use DD-MM-YYYY.")

def formatear_fecha(fecha_iso):
    """
    Convierte una fecha 'YYYY-MM-DD' a 'DD-MM-YYYY'.
    Si ya está vacía o mal formateada, la devuelve igual.
    """
    try:
        return datetime.strptime(fecha_iso, "%Y-%m-%d").strftime("%d-%m-%Y")
    except Exception:
        return fecha_iso

def pedir_entero(mensaje, minimo=None, maximo=None):
    while True:
        valor = input(mensaje).strip()
        if not valor.isdigit():
            print("Debe ingresar un número válido.")
            continue
        valor = int(valor)
        if minimo is not None and valor < minimo:
            print(f"Debe ser mayor o igual a {minimo}.")
            continue
        if maximo is not None and valor > maximo:
            print(f"Debe ser menor o igual a {maximo}.")
            continue
        return valor

def pedir_confirmacion(mensaje="¿Confirma la acción? (si/no): "):
    while True:
        respuesta = input(mensaje).strip().lower()
        if respuesta in ("si", "s"):
            return "si"
        elif respuesta in ("no", "n"):
            return "no"
        else:
            print("Respuesta inválida. Escriba 'si' o 'no'.")

def pedir_mail():
    while True:
        email = input("Ingrese el e-mail de contacto: ").strip()
        if re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return email
        print("Correo electrónico inválido.")

def pedir_precio(mensaje):
    while True:
        entrada = input(mensaje).replace(",", ".").strip()
        try:
            return float(entrada)
        except ValueError:
            print("Precio no válido. Intente nuevamente.")

def imprimir_producto(producto):
    columnas = ["CODIGO", "NOMBRE", "PRECIO", "STOCK"]
    print("\nProducto seleccionado:")
    for col, val in zip(columnas, producto):
        print(f"{col}: {val}")
    print("-" * 40)

def imprimir_productos(productos):
    columnas = ["CODIGO", "NOMBRE", "PRECIO", "STOCK"]
    print("\nListado de productos:\n")
    for producto in productos:
        for col, val in zip(columnas, producto):
            print(f"{col}: {val}")
        print("-" * 40)

def inicio():
    while True:
        respuesta_home = input("\n¿Qué desea hacer?:\n1. Gestionar de huéspedes\n2. Gestionar de consumos\n3. Gestionar de productos\n4. Gestionar de inventario\n5. Generar reportes\n0. Cerrar").strip()
        if respuesta_home == "0":
            return
        if respuesta_home == "1":
            gestionar_huespedes()
        elif respuesta_home == "2":
            gestionar_consumos()
        elif respuesta_home == "3":
            gestionar_productos()
        elif respuesta_home == "4":
            gestionar_inventario()
        elif respuesta_home == "5":
            generar_reportes()
        else:
            print("Opción inválida. Intente nuevamente: ")

def gestionar_huespedes():
    while True:
        respuesta_huespedes = input("\n1. Registrar nuevo huesped\n2. Buscar un huesped\n3. Cambiar el estado de un huesped\n4. Editar huesped\n5. Eliminar un huesped\n0. Volver al inicio\n").strip()
        if respuesta_huespedes == "1":
            nuevo_huesped()
        elif respuesta_huespedes == "2":
            buscar_huesped()
        elif respuesta_huespedes == "3":
            cambiar_estado()
        elif respuesta_huespedes == "4":
            editar_huesped()
        elif respuesta_huespedes == "5":
            eliminar_huesped()
        elif respuesta_huespedes == "0":
            return
        else:
            print("Opción inválida. Intente nuevamente: ")

def registrar_huesped(db, data):
    """ Registra un nuevo huésped en la base de datos.
    `data` es un diccionario con todos los campos necesarios."""
    sql = """ INSERT INTO HUESPEDES (APELLIDO, NOMBRE, TELEFONO, EMAIL, BOOKING, ESTADO, CHECKIN, CHECKOUT, DOCUMENTO, NACIMIENTO, HABITACION, CONTINGENTE, REGISTRO) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
    valores = (data["apellido"],data["nombre"], data["telefono"], data["email"], data["booking"], data["estado"], data["checkin"], data["checkout"], data["documento"], data["nacimiento"], data["habitacion"], data["contingente"], data["registro"])
    db.ejecutar(sql, valores)

def nuevo_huesped():
    while True:
        respuesta_apellido = input("\nEscriba el apellido del huesped ó (0) para cancelar: ").strip()
        if respuesta_apellido == "0":
            print("Registro de huésped cancelado.")
            return
        if not respuesta_apellido:
            print("El apellido no puede estar vacío.")
            continue
        apellido = unidecode(respuesta_apellido)
        break
    while True:
        nombre = input("\nEscriba el nombre del huesped ó (0) para cancelar: ").strip()
        if nombre.isdigit():
            try:
                nombre = int(nombre)
                if nombre == 0:
                    return
            except ValueError:
                print("Selección inválida. Intente nuevamente. ")
                continue
        else:
            nombre = unidecode(nombre)
            break
    while True:
        telefono = pedir_entero("Ingrese un whatsapp de contacto: ", minimo=10000000000)
        break
    email = pedir_mail()
    booking = pedir_confirmacion("¿Es una reserva de booking? si/no ")
    while True:
        pregunta_estado = input("¿Es un huesped programado (1) ó es un checkin (2)? ").strip()
        if pregunta_estado == "1":
            estado = "PROGRAMADO"
            checkin = pedir_fecha_valida("Ingrese la fecha de checkin (DD-MM-YYYY): ")
            checkout = pedir_fecha_valida("Ingrese la fecha de checkout en formato DD-MM-YYYY: ")
            while checkout < checkin:
                print("La fecha de checkout no puede ser anterior al checkin.")
                checkout = pedir_fecha_valida("Ingrese la fecha de checkout nuevamente (DD-MM-YYYY): ")
            documento = 0
            nacimiento = 0
            habitacion = 0
            break
        elif pregunta_estado == "2":
            estado = "ABIERTO"
            checkin = date.today().isoformat()
            checkout = pedir_fecha_valida("Ingrese la fecha de checkout en formato DD-MM-YYYY: ")
            while checkout < checkin:
                print("La fecha de checkout no puede ser anterior al checkin.")
                checkout = pedir_fecha_valida("Ingrese la fecha de checkout nuevamente (DD-MM-YYYY): ")
            documento = input("Ingerse el documento: ").strip()
            nacimiento = pedir_entero("Ingrese el año de nacimiento: ", minimo=1900)
            habitacion = pedir_entero("Ingrese el número de habitación: ", minimo=1 , maximo=7)
            break
        elif pregunta_estado == "0":
            return
        else:
            print("Respuesta inválida. Intente nuevamente. ")
            continue
    contingente = pedir_entero("Ingrese la cantidad de huéspedes: ",minimo=1)
    registro = f"CREADO {estado} - {datetime.now().isoformat(timespec='seconds')}"

    data = {"apellido": apellido, "nombre": nombre, "telefono": telefono, "email": email, "booking": booking, "estado": estado, "checkin": checkin, "checkout": checkout, "documento": documento, "nacimiento": nacimiento, "habitacion": habitacion, "contingente": contingente, "registro": registro}

    registrar_huesped(db, data)
    print("✔ Huésped registrado correctamente.")
    return

def buscar_huesped():
    opciones = {
        "1": ("APELLIDO", lambda: f"%{input("Ingrese el apellido: ").strip()}%"),
        "2": ("NUMERO", lambda: input("Ingrese el número de huesped: ").strip()),
        "3": ("HABITACION", lambda: input("Ingrese el número de habitación: ").strip()),
        "4": ("DOCUMENTO", lambda: input("Ingrese el número de documento: ").strip()),
        "5": ("*", None)  # Ver todos
    }

    while True:
        opcion = input("\n¿Cómo desea buscar al huesped?\n1. Por apellido\n2. Por número de huesped\n3. Por número de habitación\n4. Por documento\n5. Imprimir todos\n0. Cancelar\n").strip()

        if opcion == "0":
            return

        if opcion in opciones:
            campo, get_valor = opciones[opcion]
            if campo == "*":
                huespedes = db.obtener_todos("SELECT * FROM HUESPEDES")
            else:
                valor = get_valor()
                query = f"SELECT * FROM HUESPEDES WHERE {campo} LIKE ?" if campo == "APELLIDO" else f"SELECT * FROM HUESPEDES WHERE {campo} = ?"
                huespedes = db.obtener_todos(query, (valor,))

            if huespedes:
                imprimir_huespedes(huespedes)
            else:
                print("No se encontraron coincidencias.")
            break
        else:
            print("Opción inválida. Intente nuevamente.")
    
    return

def cambiar_estado():
    while True:
        numero = input("Ingrese el número de huésped que desea cambiar de estado, (*) para buscar ó (0) para cancelar: ").strip()
        if numero == "*":
            return buscar_huesped()
        if numero == "0":
            print("Cambio cancelado.")
            return gestionar_huespedes()
        if not numero.isdigit():
            print("Número inválido. Intente nuevamente.")
            continue

        numero = int(numero)
        huesped = db.obtener_uno("SELECT * FROM HUESPEDES WHERE NUMERO = ?", (numero,))
        if huesped is None:
            print("Huésped no encontrado. Intente nuevamente.")
            continue

        imprimir_huesped(huesped)
        break

    opciones = {"1": "PROGRAMADO","2": "ABIERTO","3": "CERRADO"}

    while True:
        seleccion = input('\n¿A qué estado quiere cambiar\nIngrese (1) "PROGRAMADO", (2) "ABIERTO", (3) "CERRADO", ó (0) para cancelar: ').strip()

        if seleccion == "0":
            print("Cambio cancelado.")
            return cambiar_estado()

        if seleccion not in opciones:
            print("Opción inválida. Intente nuevamente.")
            continue

        nuevo_estado = opciones[seleccion]
        hoy = date.today().isoformat()

        if nuevo_estado == "PROGRAMADO":
            checkin = pedir_fecha_valida("Ingrese la nueva fecha de checkin (DD-MM-YYYY): ")
            checkout = pedir_fecha_valida("Ingrese la nueva fecha de checkout (DD-MM-YYYY): ")
            while checkout < checkin:
                print("La fecha de checkout no puede ser anterior al checkin.")
                checkout = pedir_fecha_valida("Ingrese la fecha de checkout nuevamente (DD-MM-YYYY): ")
            nacimiento_data = db.obtener_uno("SELECT NACIMIENTO FROM HUESPEDES WHERE NUMERO = ?", (numero,))
            nacimiento = nacimiento_data[0] if nacimiento_data and nacimiento_data[0] else ""
            if nacimiento < 1900:
                nacimiento = pedir_entero("Ingrese el año de nacimiento: ", minimo=1900)

            actualizar_huesped(db, numero, "ESTADO", nuevo_estado)
            actualizar_huesped(db, numero, "CHECKIN", checkin)
            actualizar_huesped(db, numero, "CHECKOUT", checkout)
            actualizar_huesped(db, numero, "HABITACION", 0)
            actualizar_huesped(db, numero, "NACIMIENTO", nacimiento)

        elif nuevo_estado == "ABIERTO":
            checkin = hoy
            checkout = pedir_fecha_valida("Ingrese la nueva fecha de checkout (DD-MM-YYYY): ")
            while checkout < checkin:
                print("La fecha de checkout no puede ser anterior al checkin.")
                checkout = pedir_fecha_valida("Ingrese la fecha de checkout nuevamente (DD-MM-YYYY): ")
            documento = input("Ingrese el documento: ").strip()
            nacimiento = db.obtener_uno("SELECT NACIMIENTO FROM HUESPEDES WHERE NUMERO = ?", (numero,))[0]
            if nacimiento < 1900:
                nacimiento = pedir_entero("Ingrese el año de nacimiento: ", minimo=1900)

            habitacion = pedir_entero("Ingrese el número de habitación: ", minimo=1, maximo=7)
            contingente = pedir_entero("Ingrese la cantidad de huéspedes: ", minimo=1)

            actualizar_huesped(db, numero, "ESTADO", nuevo_estado)
            actualizar_huesped(db, numero, "CHECKIN", checkin)
            actualizar_huesped(db, numero, "CHECKOUT", checkout)
            actualizar_huesped(db, numero, "DOCUMENTO", documento)
            actualizar_huesped(db, numero, "NACIMIENTO", nacimiento)
            actualizar_huesped(db, numero, "HABITACION", habitacion)
            actualizar_huesped(db, numero, "CONTINGENTE", contingente)

        elif nuevo_estado == "CERRADO":
            checkout = hoy
            actualizar_huesped(db, numero, "ESTADO", nuevo_estado)
            actualizar_huesped(db, numero, "CHECKOUT", checkout)
            actualizar_huesped(db, numero, "HABITACION", 0)

        # Actualizar el registro de historial
        registro_anterior_data = db.obtener_uno("SELECT REGISTRO FROM HUESPEDES WHERE NUMERO = ?", (numero,))
        registro_anterior = registro_anterior_data[0] if registro_anterior_data and registro_anterior_data[0] else ""
        registro_actual = f"Estado modificado a {nuevo_estado} - {datetime.now().isoformat(timespec='seconds')}"
        nuevo_registro = registro_anterior + registro_actual
        actualizar_huesped(db, numero, "REGISTRO", nuevo_registro)

        print(f"✔ Estado actualizado a {nuevo_estado}.")
        break

    return

def actualizar_huesped(db, numero, campo, valor):
    """Actualiza un único campo del huésped dado su número de registro."""
    sql = f"UPDATE HUESPEDES SET {campo} = ? WHERE NUMERO = ?"
    db.ejecutar(sql, (valor, numero))

def editar_huesped():
    while True:
        numero = input("Ingrese el número de huésped que desea editar, (*) para buscar ó (0) para cancelar: ").strip()
        if numero == "*":
            return buscar_huesped()
        if numero == "0":
            print("Edición cancelada.")
            return
        if not numero.isdigit():
            print("Número inválido. Intente nuevamente.")
            continue

        numero = int(numero)
        huesped = db.obtener_uno("SELECT * FROM HUESPEDES WHERE NUMERO = ?", (numero,))
        if huesped is None:
            print("Huésped no encontrado. Intente nuevamente.")
            continue

        imprimir_huesped(huesped)
        break

    campos = {
"1": ("APELLIDO", lambda: unidecode(input("Ingrese el nuevo apellido: ").strip())),
"2": ("NOMBRE", lambda: unidecode(input("Ingrese el nuevo nombre: ").strip())),
"3": ("TELEFONO", lambda: pedir_entero("Ingrese el nuevo whatsapp de contacto: ", minimo=10000000000)),
"4": ("EMAIL", lambda: pedir_mail()),
"5": ("BOOKING", lambda: pedir_confirmacion("¿Es una reserva de Booking? si/no ")),
"6": ("CHECKIN", lambda: pedir_fecha_valida("Ingrese la nueva fecha de checkin (DD-MM-YYYY): ")),
"7": ("CHECKOUT", lambda: pedir_fecha_valida("Ingrese la nueva fecha de checkout (DD-MM-YYYY): ")),
"8": ("DOCUMENTO", lambda: input("Ingrese el nuevo documento: ").strip()),
"9": ("NACIMIENTO", lambda: pedir_entero("Ingrese el año de nacimiento: ", minimo=1900)),
"10": ("HABITACION", lambda: pedir_entero("Ingrese la nueva habitación: ", minimo=1, maximo=7)),
"11": ("CONTINGENTE", lambda: pedir_entero("Ingrese la cantidad de huéspedes: ", minimo=1)),
}

    while True:
        opcion = input("\n¿Qué desea editar?\nIngrese (1) Apellido, (2) Nombre,\n(3) Teléfono, (4) Email, (5) Booking\n(6) Checkin, (7) Checkout, (8) Documento\n(9) Nacimiento, (10) Habitación, (11) Contingente\nó ingrese (0) para cancelar\n").strip()
        if opcion == "0":
            print("Edición cancelada.")
            break

        if opcion in campos:
            campo_sql, funcion_valor = campos[opcion]
            nuevo_valor = funcion_valor()
            actualizar_huesped(db, numero, campo_sql, nuevo_valor)
            print(f"✔ {campo_sql} actualizado correctamente.")
            break
        else:
            print("Opción inválida. Intente nuevamente.")

    return

def eliminar_huesped_db(db, numero):
    db.ejecutar("DELETE FROM HUESPEDES WHERE NUMERO = ?", (numero,))

def eliminar_huesped():
    while True:
        numero = input("Ingrese el número del huésped a eliminar, (*) para buscar ó (0) para cancelar: ").strip()
        if numero == "*":
            return buscar_huesped()
        if numero == "0":
            print("Eliminación cancelada.")
            return
        if not numero.isdigit():
            print("Número inválido. Intente nuevamente.")
            continue

        numero = int(numero)
        huesped = db.obtener_uno("SELECT * FROM HUESPEDES WHERE NUMERO = ?", (numero,))
        if huesped is None:
            print("Huésped no encontrado.")
            continue

        imprimir_huesped(huesped)

        confirmacion = pedir_confirmacion("¿Está seguro que desea eliminar este huésped? (si/no): ")
        if confirmacion == "si":
            eliminar_huesped_db(db, numero)
            print("✔ Huésped eliminado.")
            return gestionar_huespedes()
        else:
            print("Eliminación cancelada.")
            return

def gestionar_consumos():
    while True:
        respuesta_consumos = input("\n1. Agregar consumo\n2. Ver consumos\n0. Volver al inicio\n").strip()
        if respuesta_consumos == "1":
            agregar_consumo()
        elif respuesta_consumos == "2":
            ver_consumos()
        elif respuesta_consumos == "0":
            return
        else: 
            print("Opción inválida. Intente nuevamente: ")

def gestionar_productos():
    while True:
        respuesta_productos = input("\n1. Agregar producto\n2. Ver productos\n3. Buscar productos\n4. Editar producto\n5. Eliminar producto\n0. Volver al inicio\n").strip()
        if respuesta_productos == "1":
            agregar_producto()
        elif respuesta_productos == "2":
            ver_productos()
        elif respuesta_productos == "3":
            buscar_producto()
        elif respuesta_productos == "4":
            editar_producto()
        elif respuesta_productos == "5":
            eliminar_producto()
        elif respuesta_productos == "0":
            return
        else: 
            print("Opción inválida. Intente nuevamente: ")

def registrar_producto(db, data):
    sql = "INSERT INTO PRODUCTOS (NOMBRE, PRECIO, STOCK) VALUES (?, ?, ?)"
    db.ejecutar(sql, (data["nombre"], data["precio"], data["stock"]))

def agregar_producto():
    nombre = input("\nEscriba el nombre del producto ó (0) para cancelar: ").strip()
    if nombre == "0":
        return

    precio = pedir_precio("Ingrese el precio del producto: ")
    stock = pedir_entero("Ingrese el stock inicial: ", minimo=0)

    data = {"nombre": nombre, "precio": precio, "stock": stock}
    registrar_producto(db, data)
    print("✔ Producto registrado correctamente.")
    return

def ver_productos():
    print("")
    productos = db.obtener_todos(''' SELECT * FROM PRODUCTOS ''')
    imprimir_productos(productos)
    return

def buscar_producto():
    criterio = input("Ingrese el producto a buscar ó (0) para cancelar: ").strip()
    if criterio == "0":
        return
    
    criterios = criterio.lower().split()
    if not criterios:
        print("Debe ingresar al menos una palabra clave.")
        return buscar_producto()

    where_clauses = ["LOWER(NOMBRE) LIKE ?"] * len(criterios)
    params = [f"%{p}%" for p in criterios]
    query = f"SELECT * FROM PRODUCTOS WHERE {' OR '.join(where_clauses)}"
    productos = db.obtener_todos(query, params)

    resultados = [
        (prod, sum(1 for palabra in criterios if palabra in prod[1].lower()))
        for prod in productos
    ]
    resultados.sort(key=lambda x: x[1], reverse=True)

    if resultados:
        print(f"\nResultados para: '{criterio}'")
        productos_ordenados = [p for p, _ in resultados]
        imprimir_productos(productos_ordenados)
    else:
        print("No se encontraron productos.")

    return

def actualizar_producto(db, codigo, campo, valor):
    db.ejecutar(f"UPDATE PRODUCTOS SET {campo} = ? WHERE CODIGO = ?", (valor, codigo))

def editar_producto():
    while True:
        codigo = input("\nIngrese el código del producto que desea editar, ingrese (*) para ver el listado ó ingrese (0) para cancelar: ").strip()
        if codigo == "*":
            ver_productos()
            continue
        if codigo == "0":
            return
        if not codigo.isdigit():
            print("Código inválido.")
            continue

        codigo = int(codigo)
        producto = db.obtener_uno("SELECT * FROM PRODUCTOS WHERE CODIGO = ?", (codigo,))
        if not producto:
            print("Producto no encontrado.")
            continue

        imprimir_producto(producto)
        break

    campos = {
        "1": ("NOMBRE", lambda: input("Ingrese el nuevo nombre: ").strip()),
        "2": ("PRECIO", lambda: pedir_precio("Ingrese el nuevo precio: "))}

    while True:
        opcion = input("\n¿Desea editar el nombre (1), el precio (2) ó cancelar (0)? ").strip()
        if opcion == "0":
            return
        if opcion in campos:
            campo, get_valor = campos[opcion]
            valor = get_valor()
            actualizar_producto(db, codigo, campo, valor)
            print(f"✔ {campo} actualizado.")
            break
        else:
            print("Opción inválida.")

    return

def eliminar_producto_db(db, codigo):
    db.ejecutar("DELETE FROM PRODUCTOS WHERE CODIGO = ?", (codigo,))

def eliminar_producto():
    while True:
        codigo = input("\nIngrese el código del producto que desea eliminar, ingrese (*) para ver el listado ó ingrese (0) para cancelar: ").strip()
        if codigo == "*":
            ver_productos()
            continue
        if codigo == "0":
            print("Eliminación cancelada.")
            return gestionar_productos()
        if not codigo.isdigit():
            print("Código inválido.")
            continue

        codigo = int(codigo)
        producto = db.obtener_uno("SELECT * FROM PRODUCTOS WHERE CODIGO = ?", (codigo,))
        if not producto:
            print("Producto no encontrado.")
            continue

        print(f"Producto seleccionado: ")
        imprimir_producto(producto)

        confirmacion = pedir_confirmacion("¿Está seguro que desea eliminar este producto? (si/no): ")
        if confirmacion == "si":
            eliminar_producto_db(db, codigo)
            print("✔ Producto eliminado.")
            return
        else:
            print("Eliminación cancelada.")
        return

def gestionar_inventario():
    while True:
        respuesta_inventario = input("\n1. Abrir inventario\n2. Ingresar compra\n3. Editar inventario\n0. Volver al inicio\n").strip()
        if respuesta_inventario == "1":
            abrir_inventario()
        elif respuesta_inventario == "2":
            ingresar_compra()
        elif respuesta_inventario == "3":
            editar_inventario()
        elif respuesta_inventario == "0":
            return
        else:
             print("Opción inválida. Intente nuevamente: ")

def abrir_inventario():
    #Esta función debe imprimir el nombre de cada producto y su respectivo stock.
    return

def ingresar_compra():
    #Esta función se encargará de aumentar en una cantidad específica, los productos que sean seleccionados.
    return

def editar_inventario():
    #Esta función debe permitir modificar el stock de un producto particular que será escogido por el usuario.
    return

def generar_reportes():
    while True:
        respuesta_reportes = input("\n1. Generar reporte de consumos diarios\n2. Generar reporte de consumos pendientes\n3. Generar reporte de consumos cerrados\n4. Generar reporte de pronto checkin\n0. Volver al inicio\n").strip()
        if respuesta_reportes == "1":
            reporte_diario()
        elif respuesta_reportes == "2":
            reporte_pendientes()
        elif respuesta_reportes == "3":
            reporte_cerrados()
        elif respuesta_reportes == "4":
            reporte_pronto_checkin()
        elif respuesta_reportes == "0":
            return
        else:
            print("Opción inválida. Intente nuevamente: ")

###INTERFAZ GRAFICA###


### PROGRAMA ###

try:
    print("Bienvenido al sistema de gestión de la posada Onda de mar 1.1 (Demo)")
    productos_existe()
    huespedes_existe()
    inicio()
finally:
    db.cerrar()
    print("Conexión a la base de datos cerrada.")