#TODO:

#Guardar LOG cuando se eliminan huéspedes, eliminan consumos o cierran huéspedes.


from datetime import datetime, date, timedelta
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

    def obtener_uno(self, query, params=()):
        self.cursor.execute(query, params)
        return self.cursor.fetchone()

    def obtener_todos(self, query, params=()):
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def cerrar(self):
        self.conn.close()


### VARIABLES GLOBALES ###

db = DBManager()


### FUNCIONES ###

def productos_existe():
    db.ejecutar('''CREATE TABLE IF NOT EXISTS PRODUCTOS(CODIGO INTEGER PRIMARY KEY AUTOINCREMENT, NOMBRE TEXT, PRECIO REAL, STOCK INTEGER)''')

def huespedes_existe():
    db.ejecutar('''CREATE TABLE IF NOT EXISTS HUESPEDES(NUMERO INTEGER PRIMARY KEY AUTOINCREMENT, APELLIDO TEXT, NOMBRE TEXT, TELEFONO INTEGER, EMAIL TEXT, BOOKING TEXT, ESTADO TEXT, CHECKIN TEXT, CHECKOUT TEXT, DOCUMENTO INTEGER, NACIMIENTO INTEGER, HABITACION INTEGER, CONTINGENTE INTEGER, REGISTRO TEXT)''')

def consumos_existe():
    db.ejecutar('''CREATE TABLE IF NOT EXISTS CONSUMOS(ID INTEGER PRIMARY KEY AUTOINCREMENT, HUESPED INTEGER, PRODUCTO INTEGER, CANTIDAD INTEGER, FECHA TEXT, FOREIGN KEY (HUESPED) REFERENCES HUESPEDES(NUMERO), FOREIGN KEY (PRODUCTO) REFERENCES PRODUCTOS(CODIGO))''')

def imprimir_huesped(huesped):
    print(f"\nHuésped seleccionado:")
    columnas = ["NUMERO", "APELLIDO", "NOMBRE", "TELEFONO", "EMAIL", "BOOKING", "ESTADO","CHECKIN", "CHECKOUT", "DOCUMENTO", "NACIMIENTO", "HABITACION", "CONTINGENTE", "REGISTRO"]
    for col, val in zip(columnas, huesped):
        if col in ("CHECKIN", "CHECKOUT"):
            val = formatear_fecha(val)
        print(f"{col:<15}: {val}")
    print("-" * 40)

def imprimir_huespedes(huespedes):
    columnas = ["NUMERO", "APELLIDO", "NOMBRE", "TELEFONO", "EMAIL", "BOOKING", "ESTADO", "CHECKIN", "CHECKOUT", "DOCUMENTO", "NACIMIENTO", "HABITACION", "CONTINGENTE", "REGISTRO"]
    for huesped in huespedes:
        for col, val in zip(columnas, huesped):
            if col in ("CHECKIN", "CHECKOUT"):
                val = formatear_fecha(val)
            print(f"{col:<15}: {val}")
        print("-" * 40)

def pedir_fecha_valida(mensaje, allow_past=False):
    while True:
        fecha_input = input(mensaje).strip()
        try:
            fecha = datetime.strptime(fecha_input, '%d-%m-%Y').date()
            if fecha < date.today():
                if allow_past:
                    respuesta = pedir_confirmacion("La fecha de check-in es anterior a hoy. ¿Desea registrarla de todas formas? (si/no): ")
                    if respuesta == "si":
                        return fecha.isoformat()
                    else:
                        print("Por favor, ingrese una fecha igual o posterior a hoy.")
                        continue
                else:
                    print("La fecha debe ser igual o posterior a hoy.")
            else:
                return fecha.isoformat()  # → 'YYYY-MM-DD'
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
        print(f"{col:<15}: {val}")
    print("-" * 40)

def imprimir_productos(productos):
    columnas = ["CODIGO", "NOMBRE", "PRECIO", "STOCK"]
    print("\nListado de productos:\n")
    for producto in productos:
        for col, val in zip(columnas, producto):
            print(f"{col:<15}: {val}")
        print("-" * 40)

def inicio():
    while True:
        respuesta_home = input("\n¿Qué desea hacer?:\n1. Gestionar de huéspedes\n2. Gestionar de consumos\n3. Gestionar de productos\n4. Gestionar de inventario\n5. Generar reportes\n0. Cerrar\n").strip()
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
        elif respuesta_huespedes == "6":
            mostrar_registro()
        elif respuesta_huespedes == "0":
            return
        else:
            print("Opción inválida. Intente nuevamente: ")

def nuevo_huesped_db(db, data):
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
        respuesta_nombre = input("\nEscriba el nombre del huesped ó (0) para cancelar: ").strip()
        if respuesta_nombre == "0":
            return
        if not respuesta_nombre:
            print("El nombre no puede estar vacío")
        else:
            nombre = unidecode(respuesta_nombre)
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
            checkin = pedir_fecha_valida("Ingrese la fecha de checkin (DD-MM-YYYY): ", allow_past=True)
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

    nuevo_huesped_db(db, data)
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
                print("\nListado de huéspedes:\n")
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
        registro_anterior_data = db.obtener_uno("SELECT REGISTRO FROM HUESPEDES WHERE NUMERO = ?", (numero,))
        registro_anterior = registro_anterior_data[0] if registro_anterior_data and registro_anterior_data[0] else ""
        separador = "\n---\n"

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
            registro_nuevo = f"Estado modificado a {nuevo_estado} - {datetime.now().isoformat(timespec='seconds')}"
            registro = registro_anterior + separador + registro_nuevo
            updates = {"ESTADO": nuevo_estado, "CHECKIN": checkin, "CHECKOUT": checkout, "HABITACION": 0, "NACIMIENTO": nacimiento, "REGISTRO": registro}
            editar_huesped_db(db, numero, updates)

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
            registro_nuevo = f"Estado modificado a {nuevo_estado} - {datetime.now().isoformat(timespec='seconds')}"
            registro = registro_anterior + separador + registro_nuevo

            # Unificar todas las actualizaciones en un diccionario
            updates = {"ESTADO": nuevo_estado, "CHECKIN": checkin, "CHECKOUT": checkout, "DOCUMENTO": documento, "NACIMIENTO": nacimiento, "HABITACION": habitacion, "CONTINGENTE": contingente, "REGISTRO": registro}
            editar_huesped_db(db, numero, updates)

        elif nuevo_estado == "CERRADO":
            checkout = hoy
            registro_nuevo = f"Estado modificado a {nuevo_estado} - {datetime.now().isoformat(timespec='seconds')}"
            registro = registro_anterior + separador + registro_nuevo
            updates = {"ESTADO": nuevo_estado, "CHECKOUT": checkout, "HABITACION": 0, "REGISTRO": registro}
            editar_huesped_db(db, numero, updates) # Llamada única

        print(f"✔ Estado actualizado a {nuevo_estado}.")
        break

    return

def editar_huesped_db(db, numero, updates_dict):
    """
    Actualiza uno o varios campos del huésped dado su número de registro.
    updates_dict es un diccionario con {campo: valor}.
    """
    if not updates_dict:
        return # No hay nada que actualizar si el diccionario está vacío

    set_clauses = []
    valores = []
    for campo, valor in updates_dict.items():
        set_clauses.append(f"{campo} = ?")
        valores.append(valor)

    # Añadir el número del huésped al final de los valores para la cláusula WHERE
    valores.append(numero)

    sql = f"UPDATE HUESPEDES SET {', '.join(set_clauses)} WHERE NUMERO = ?"
    db.ejecutar(sql, tuple(valores))

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
"6": ("CHECKIN", lambda: pedir_fecha_valida("Ingrese la fecha de checkin (DD-MM-YYYY): ", allow_past=True)),
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
            registro_anterior_data = db.obtener_uno("SELECT REGISTRO FROM HUESPEDES WHERE NUMERO = ?", (numero,))
            registro_anterior = registro_anterior_data[0] if registro_anterior_data and registro_anterior_data[0] else ""
            separador = "\n---\n"
            registro_actual = f"Se modificó {campo_sql} a ´{nuevo_valor} - {datetime.now().isoformat(timespec='seconds')}"
            nuevo_registro = registro_anterior + separador + registro_actual
            updates = {campo_sql: nuevo_valor, "REGISTRO": nuevo_registro}
            editar_huesped_db(db, numero, updates)

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
            return
        else:
            print("Eliminación cancelada.")
            return

def mostrar_registro():
    while True:
        numero = input("Ingrese el número de huésped para ver su historial, (*) para buscar ó (0) para cancelar: ").strip()
        if numero == "0":
            return gestionar_huespedes()
        if numero == "*":
            buscar_huesped()
            continue
        if not numero.isdigit():
            print("Número inválido.")
            continue

        numero = int(numero)
        huesped = db.obtener_uno("SELECT NOMBRE, APELLIDO, REGISTRO FROM HUESPEDES WHERE NUMERO = ?", (numero,))
        if huesped is None:
            print("❌ Huésped no encontrado.")
            continue

        nombre, apellido, registro = huesped
        print(f"\nHistorial del huésped {nombre} {apellido}:\n")

        if not registro:
            print("Este huésped no tiene historial registrado.")
        else:
            entradas = registro.split("\n---\n")
            for i, linea in enumerate(entradas, start=1):
                print(f"{i}. {linea.strip()}\n")

        return gestionar_huespedes()

def gestionar_consumos():
    while True:
        respuesta_consumos = input("\n1. Agregar consumo\n2. Ver consumos\n3. Eliminar consumos\n0. Volver al inicio\n").strip()
        if respuesta_consumos == "1":
            agregar_consumo()
        elif respuesta_consumos == "2":
            ver_consumos()
        elif respuesta_consumos == "3":
            eliminar_consumos()
        elif respuesta_consumos == "0":
            return
        else: 
            print("Opción inválida. Intente nuevamente: ")

def agregar_consumo():
    while True:
        habitacion = input("Ingrese el número de habitación ó (0) para cancelar: ").strip()
        if habitacion == "0":
            return
        if not habitacion.isdigit():
            print("Número inválido.")
            continue

        habitacion = int(habitacion)
        huesped = db.obtener_uno("SELECT * FROM HUESPEDES WHERE HABITACION = ? AND ESTADO = 'ABIERTO'", (habitacion,))
        if huesped is None:
            print("❌ No se encontró un huésped ABIERTO en esa habitación.")
            continue

        imprimir_huesped(huesped)
        break

    numero_huesped = huesped[0]
    consumos_agregados = []

    while True:
        codigo = input("Ingrese el CÓDIGO del producto consumido, (*) para buscar ó (0) para finalizar: ").strip()
        if codigo == "0":
            break
        elif codigo == "*":
            productos = db.obtener_todos("SELECT * FROM PRODUCTOS WHERE STOCK > 0")
            if not productos:
                print("No hay productos en stock.")
                return
            else:
                imprimir_productos(productos)
                continue
        elif not codigo.isdigit():
            print("Código inválido")
            continue

        codigo = int(codigo)
        producto = db.obtener_uno("SELECT * FROM PRODUCTOS WHERE CODIGO = ?", (codigo,))
        if not producto:
            print("❌ Producto no encontrado.")
            continue

        _, nombre, precio, stock = producto
        print(f"Producto seleccionado: {nombre} (Stock: {stock})")

        while True:
            cantidad = pedir_entero("Ingrese la cantidad consumida ó (0) para cancelar: ", minimo=0)
            if cantidad == 0:
                print("❌ Producto cancelado.")
                break  # vuelve a pedir otro producto
            elif cantidad > stock:
                print(f"❌ No hay suficiente stock. Disponibles: {stock}")
                continue
            else:
                fecha = datetime.now().isoformat(sep=" ", timespec="seconds")
                db.ejecutar("INSERT INTO CONSUMOS (HUESPED, PRODUCTO, CANTIDAD, FECHA) VALUES (?, ?, ?, ?)",
                            (huesped[0], codigo, cantidad, fecha))

                consumo_id = db.cursor.lastrowid
                consumos_agregados.append((consumo_id, fecha, codigo, nombre, cantidad))

                nuevo_stock = stock - cantidad
                db.ejecutar("UPDATE PRODUCTOS SET STOCK = ? WHERE CODIGO = ?", (nuevo_stock, codigo))
                registro_anterior_data = db.obtener_uno("SELECT REGISTRO FROM HUESPEDES WHERE NUMERO = ?", (numero_huesped,))
                registro_anterior = registro_anterior_data[0] if registro_anterior_data and registro_anterior_data[0] else ""
                separador = "\n---\n"
                registro_consumo = f"Consumo agregado: {nombre} (x{cantidad}) - {fecha}"
                nuevo_registro = registro_anterior + separador + registro_consumo if registro_anterior else registro_consumo
                editar_huesped_db(db, numero_huesped, {"REGISTRO": nuevo_registro})

                print(f"✔ Se registró el consumo de {cantidad} unidad(es) de '{nombre}' para {huesped[2]} {huesped[1]}, habitación {habitacion}.")
                break
    
    if consumos_agregados:
        respuesta = pedir_confirmacion("\n¿Desea eliminar alguno de los consumos recién agregados? (si/no): ")
        if respuesta in ("si", "s"):
            eliminar_consumos_db(consumos_agregados)

    return

def ver_consumos():
    while True:
        habitacion = input("Ingrese el número de habitación para ver sus consumos, (*) para buscar ó (0) para cancelar: ").strip()
        if habitacion == "0":
            return
        if habitacion == "*":
            buscar_huesped()
            continue
        if not habitacion.isdigit():
            print("Número inválido.")
            continue

        habitacion = int(habitacion)
        huesped = db.obtener_uno("SELECT * FROM HUESPEDES WHERE HABITACION = ?", (habitacion,))
        if huesped is None:
            print("❌ Habitación no encontrada.")
            continue

        imprimir_huesped(huesped)

        query = """SELECT C.ID, C.FECHA, C.PRODUCTO, P.NOMBRE, C.CANTIDAD FROM CONSUMOS C JOIN PRODUCTOS P ON C.PRODUCTO = P.CODIGO WHERE C.HUESPED = ? ORDER BY C.FECHA DESC"""
        consumos = db.obtener_todos(query, (huesped[0],))

        if consumos:
            print(f"\nHistorial de consumos de la habitación {huesped[11]}, huésped {huesped[2]} {huesped[1]}:\n")
            print(f"{'#':<3} {'FECHA':<12} {'PRODUCTO':<30} {'CANTIDAD':<10}")
            print("-" * 60)
            for idx, (consumo_id, fecha, producto_id, producto_nombre, cantidad) in enumerate(consumos, start=1):
                print(f"{idx:<3} {fecha:<12} {producto_nombre:<30} {cantidad:<10}")
        else:
            print("Esta habitación no tiene consumos registrados.")
        return

def eliminar_consumos():
    while True:
        habitacion = input("Ingrese el número de habitación para eliminar consumos, (*) para buscar ó (0) para cancelar: ").strip()
        if habitacion == "0":
            return
        if habitacion == "*":
            buscar_huesped()
            continue
        if not habitacion.isdigit():
            print("Número inválido.")
            continue

        habitacion = int(habitacion)
        huesped = db.obtener_uno("SELECT * FROM HUESPEDES WHERE HABITACION = ?", (habitacion,))
        if huesped is None:
            print("❌ Habitación no encontrada.")
            continue

        imprimir_huesped(huesped)

        query = """ SELECT C.ID, C.FECHA, C.PRODUCTO, P.NOMBRE, C.CANTIDAD FROM CONSUMOS C JOIN PRODUCTOS P ON C.PRODUCTO = P.CODIGO WHERE C.HUESPED = ? ORDER BY C.FECHA DESC"""
        consumos = db.obtener_todos(query, (huesped[0],))

        if not consumos:
            print("Esta habitación no tiene consumos registrados.")
            return

        print(f"\nConsumos de la habitación {huesped[11]}, huésped {huesped[2]} {huesped[1]}:\n")
        print(f"{'#':<3} {'FECHA':<12} {'PRODUCTO':<30} {'CANTIDAD':<10}")
        print("-" * 60)
        for idx, (consumo_id, fecha, producto_id, producto_nombre, cantidad) in enumerate(consumos, start=1):
            print(f"{idx:<3} {fecha:<12} {producto_nombre:<30} {cantidad:<10}")

        eliminar_consumos_db(consumos)
        return

def eliminar_consumos_db(lista_consumos):
    """
    Recibe una lista de tuplas (ID, FECHA, PRODUCTO, NOMBRE, CANTIDAD) y permite eliminar por índice.
    Restaura el stock al producto correspondiente.
    """
    indices_validos = list(range(1, len(lista_consumos)+1))
    seleccion = input("Ingrese el/los número(s) de consumo a eliminar separados por coma (ej: 1,3): ").strip()
    seleccion = seleccion.split(",")

    a_eliminar = []
    for item in seleccion:
        item = item.strip()
        if item.isdigit():
            idx = int(item)
            if idx in indices_validos:
                a_eliminar.append(idx - 1)
            else:
                print(f"Índice fuera de rango: {idx}")
        else:
            print(f"Entrada inválida: {item}")

    for i in a_eliminar:
        consumo_id, _, producto_id, producto_nombre, cantidad = lista_consumos[i]

        # Obtener código del producto
        producto = db.obtener_uno("SELECT STOCK FROM PRODUCTOS WHERE CODIGO = ?", (producto_id,))
        if producto:
            stock_actual = producto[0]
            stock_nuevo = stock_actual + cantidad
            db.ejecutar("UPDATE PRODUCTOS SET STOCK = ? WHERE CODIGO = ?", (stock_nuevo, producto_id))
            print(f"✔ Stock de '{producto_nombre}' restaurado.")
        else:
            print(f"⚠ Producto '{producto_nombre}' (ID: {producto_id}) no encontrado. No se restauró el stock.")

        # Eliminar consumo
        db.ejecutar("DELETE FROM CONSUMOS WHERE ID = ?", (consumo_id,))
        print(f"✔ Consumo #{i+1} eliminado y stock de '{producto_nombre}' restaurado.")

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

def agregar_producto_db(db, data):
    sql = "INSERT INTO PRODUCTOS (NOMBRE, PRECIO, STOCK) VALUES (?, ?, ?)"
    db.ejecutar(sql, (data["nombre"], data["precio"], data["stock"]))

def agregar_producto():
    nombre = input("\nEscriba el nombre del producto ó (0) para cancelar: ").strip()
    if nombre == "0":
        return

    precio = pedir_precio("Ingrese el precio del producto: ")
    stock = pedir_entero("Ingrese el stock inicial: ", minimo=0)

    data = {"nombre": nombre, "precio": precio, "stock": stock}
    agregar_producto_db(db, data)
    print("✔ Producto registrado correctamente.")
    return

def ver_productos():
    print("")
    productos = db.obtener_todos(''' SELECT * FROM PRODUCTOS ''')
    imprimir_productos(productos)
    return

def buscar_producto():
    while True:
        criterio = input("Ingrese el nombre o código del producto, ó (0) para cancelar: ").strip()
        if criterio == "0":
            return
        criterios = criterio.lower().split()
        if not criterios:
            print("Debe ingresar al menos una palabra para buscar.")
            continue
        else:
            break

    where_clauses = ["LOWER(NOMBRE) LIKE ?"] * len(criterios)
    params = [f"%{palabra}%" for palabra in criterios]

    query = f"SELECT * FROM PRODUCTOS WHERE {' OR '.join(where_clauses)}"
    productos = db.obtener_todos(query, params)

    # Ordenar por relevancia (cantidad de palabras que coinciden en el nombre)
    resultados = [(prod, sum(1 for palabra in criterios if palabra in prod[1].lower())) for prod in productos]
    resultados.sort(key=lambda x: x[1], reverse=True)

    if resultados:
        print(f"\nResultados para: '{criterio}'\n")
        productos_ordenados = [p for p, _ in resultados]
        imprimir_productos(productos_ordenados)
    else:
        print("No se encontraron productos que coincidan con la búsqueda.")

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
    productos = db.obtener_todos("SELECT * FROM PRODUCTOS ORDER BY NOMBRE")
    if not productos:
        print("No hay productos cargados.")
        return gestionar_inventario()

    print("\n📦 Inventario actual:")
    print(f"{'CÓDIGO':<7} {'NOMBRE':<30} {'STOCK':<10}")
    print("-" * 50)
    for codigo, nombre, precio, stock in productos:
        print(f"{codigo:<7} {nombre:<30} {stock:<10}")
    
    return gestionar_inventario()

def ingresar_compra():
    productos = db.obtener_todos("SELECT * FROM PRODUCTOS ORDER BY NOMBRE")
    if not productos:
        print("No hay productos cargados.")
        return gestionar_inventario()

    imprimir_productos(productos)

    while True:
        codigo = input("Ingrese el CÓDIGO del producto comprado ó (0) para cancelar: ").strip()
        if codigo == "0":
            return gestionar_inventario()
        if not codigo.isdigit():
            print("Código inválido.")
            continue

        codigo = int(codigo)
        producto = db.obtener_uno("SELECT * FROM PRODUCTOS WHERE CODIGO = ?", (codigo,))
        if not producto:
            print("Producto no encontrado.")
            continue

        _, nombre, _, stock = producto
        cantidad = pedir_entero(f"Ingrese la cantidad comprada de '{nombre}': ", minimo=1)
        nuevo_stock = stock + cantidad
        db.ejecutar("UPDATE PRODUCTOS SET STOCK = ? WHERE CODIGO = ?", (nuevo_stock, codigo))
        if cantidad == 1:
            print(f"✔ Se aumentó {cantidad} unidad el stock de '{nombre}' (Nuevo stock: {nuevo_stock}).")
        else:
            print(f"✔ Se aumentó {cantidad} unidades el stock de '{nombre}' (Nuevo stock: {nuevo_stock}).")
        return gestionar_inventario()

def editar_inventario():
    productos = db.obtener_todos("SELECT * FROM PRODUCTOS ORDER BY NOMBRE")
    if not productos:
        print("No hay productos cargados.")
        return gestionar_inventario()

    imprimir_productos(productos)

    while True:
        codigo = input("Ingrese el CÓDIGO del producto a modificar ó (0) para cancelar: ").strip()
        if codigo == "0":
            return gestionar_inventario()
        if not codigo.isdigit():
            print("Código inválido.")
            continue

        codigo = int(codigo)
        producto = db.obtener_uno("SELECT * FROM PRODUCTOS WHERE CODIGO = ?", (codigo,))
        if not producto:
            print("Producto no encontrado.")
            continue

        _, nombre, _, stock = producto
        nuevo_stock = pedir_entero(f"Ingrese el nuevo stock de '{nombre}': ", minimo=0)
        db.ejecutar("UPDATE PRODUCTOS SET STOCK = ? WHERE CODIGO = ?", (nuevo_stock, codigo))

        print(f"✔ Stock actualizado para '{nombre}'. Nuevo stock: {nuevo_stock}.")
        return gestionar_inventario()

def generar_reportes():
    while True:
        respuesta_reportes = input("\n1. Generar reporte de consumos diarios\n2. Generar reporte de pasajeros abiertos\n3. Generar reporte de pasajeros cerrados\n4. Generar reporte de pronto checkin\n0. Volver al inicio\n").strip()
        if respuesta_reportes == "1":
            reporte_diario()
        elif respuesta_reportes == "2":
            reporte_abiertos()
        elif respuesta_reportes == "3":
            reporte_cerrados()
        elif respuesta_reportes == "4":
            reporte_pronto_checkin()
        elif respuesta_reportes == "0":
            return
        else:
            print("Opción inválida. Intente nuevamente: ")

def reporte_diario():
    hoy = date.today().isoformat()

    query = """SELECT H.HABITACION, H.NOMBRE, H.APELLIDO, C.FECHA, P.NOMBRE, C.CANTIDAD FROM CONSUMOS C JOIN HUESPEDES H ON C.HUESPED = H.NUMERO JOIN PRODUCTOS P ON C.PRODUCTO = P.CODIGO WHERE C.FECHA LIKE ? ORDER BY H.HABITACION, C.FECHA"""

    consumos = db.obtener_todos(query, (f"{hoy}%",)) 

    if not consumos:
        print(f"No se registraron consumos en la fecha de hoy ({date.today().strftime('%d-%m-%Y')}).")
        return

    print(f"\nConsumos registrados hoy ({date.today().strftime('%d-%m-%Y')}):\n")

    habitacion_actual = None
    for habitacion, nombre, apellido, fecha, producto, cantidad in consumos:
        if habitacion != habitacion_actual:
            habitacion_actual = habitacion
            print(f"\nHabitación {habitacion} - Huésped: {nombre} {apellido}")

        hora = datetime.strptime(fecha, "%Y-%m-%d %H:%M:%S").strftime("%H:%M") 
        print(f"  - {hora} {producto} (x{cantidad})")

    print()

def reporte_abiertos():
    query = "SELECT * FROM HUESPEDES WHERE ESTADO = ?"
    huespedes = db.obtener_todos(query, ("ABIERTO",))
    if huespedes:
        print(f"\nHuéspedes abiertos:\n")
        imprimir_huespedes(huespedes)
        return
    else:
        print("No se hallaron huéspedes abiertos\n")
        return

def reporte_cerrados():
    while True:
        fecha_str = input("Ingrese una fecha para generar el reporte, o deje vacío para el día de la fecha: ")
        if fecha_str:
            try:
                fecha = datetime.strptime(fecha_str, "%d-%m-%Y").date()
                break
            except ValueError:
                print("❌ Fecha inválida. Use el formato DD-MM-YYYY.")
                continue
        else:
            fecha = date.today()
            break
    fecha_iso = fecha.isoformat()
    query = "SELECT * FROM HUESPEDES WHERE ESTADO = 'CERRADO' AND CHECKOUT = ?"
    huespedes = db.obtener_todos(query, (fecha_iso,))

    if huespedes:
        print(f"\nHuéspedes cerrados el {fecha.strftime('%d-%m-%Y')}:\n")
        imprimir_huespedes(huespedes)
        return
    else:
        query_abiertos = "SELECT * FROM HUESPEDES WHERE ESTADO = 'ABIERTO' AND CHECKOUT <= ?"
        abiertos = db.obtener_todos(query_abiertos, (fecha_iso,))

        if abiertos:
            respuesta = pedir_confirmacion("¡¡¡ Atención !!!\nNo se encontraron huéspedes cerrados pero HAY HUÉSPEDES CON CHECKOUT VENCIDO\n¿Desea verlos? (si/no): ")
            if respuesta in ("si", "s"):
                print("\nHuéspedes con checkout vencido:\n")
                imprimir_huespedes(abiertos)
        else:
            print("No se hallaron huéspedes cerrados el día de hoy")

def reporte_pronto_checkin():
    manana = date.today() + timedelta(days=1)
    manana_iso = manana.isoformat()

    query = "SELECT * FROM HUESPEDES WHERE ESTADO = 'PROGRAMADO' AND CHECKIN = ?"
    huespedes = db.obtener_todos(query, (manana_iso,))

    if huespedes:
        print(f"\nHuéspedes con check-in programado para mañana ({manana.strftime('%d-%m-%Y')}):\n")
        imprimir_huespedes(huespedes)
        return
    else:
        print(f"No hay huéspedes con check-in programado para mañana ({manana.strftime('%d-%m-%Y')}).")
        return

###INTERFAZ GRAFICA###


### PROGRAMA ###

try:
    print("Bienvenido al sistema de gestión de la posada Onda de mar 1.0 (Demo)")
    productos_existe()
    huespedes_existe()
    consumos_existe()
    inicio()
finally:
    db.cerrar()
    print("Conexión a la base de datos cerrada.")