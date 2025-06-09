import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import sqlite3
from datetime import datetime, date


### VARIABLES GLOBALES ###

conexion = sqlite3.connect('base_datos')
cursor = conexion.cursor()


### FUNCIONES ###

def tabla_existe(producto):
                      #Cúantas veces DESDE SQLiteMaster DONDE el tipo sea tabla y su nomrbe {}
    cursor.execute(''' SELECT COUNT(name) FROM SQLITE_MASTER WHERE TYPE = 'table' AND name = '{}' '''.format(producto))
    #Si hay 1 significa que existe, y sino no.
    if cursor.fetchone()[0] == 1:
        return True
    else:
        cursor.execute(''' CREATE TABLE PRODUCTOS (CODIGO INTEGER PRIMARY KEY AUTOINCREMENT, NOMBRE TEXT, PRECIO REAL) ''')
        return False

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
    respuesta_huespedes = input("\n1. Registrar nuevo huesped\n2. Buscar un huesped\n3. Cambiar el estado de un huesped\n4. Eliminar un huesped\n9. Volver al inicio\n")
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
        eliminar_huesped()
    elif respuesta_huespedes == 9:
        inicio()
    else: gestionar_huespedes()

def nuevo_huesped():
    apellido = input("\nEscriba el apellido del huesped: ")
    nombre = input("Escriba el nombre del huesped: ")
    telefono = input("Ingrese un whatsapp de contacto: ")
    email = input("Ingrese el e-mail de contacto: ")
    respuesta_booking = input("Es una reserva de booking? si/no ")
    if (respuesta_booking == "si" or respuesta_booking == "s"):
        booking = True
    else:
        booking = False
    estado = input("Es un huesped programado (0) ó es un checkin (1)? ")
    if estado == 0:
        checkin = input("Ingrese la fecha de checkin? (DD-MM-YYYY): ")
        documento = 0
        nacimiento = ""
        habitacion = 0
    elif estado == 1:
        checkin = str(date.today())
        documento = input("Ingerse el documento: ")
        nacimiento = input("Ingrese la fecha de nacimiento en formato DD-MM-YYYY: ")
        habitacion = input("Ingresa el número de habitación: ")
    contingente = input("Ingrese la cantidad de huéspedes? ")
    registro = {"Registro":str(datetime.now())}
    my_huesped = {"Nombre":nombre, "Apellido":apellido, "Teléfono":telefono, "E-mail":email, "Contingente":contingente, "Fecha de nacimiento":nacimiento, "Documento":documento, "Checkin":checkin, "Booking":booking, "Habitación":habitacion, "Estado":estado, "Registro":registro}
    registro_de_huespedes.append(my_huesped)
    print (registro_de_huespedes)

def buscar_huesped(tipo, dato):
    return True

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
    lanzar_interfaz_productos()

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

def cargar_productos(tree):
    for row in tree.get_children():
        tree.delete(row)
    cursor.execute('SELECT * FROM PRODUCTOS')
    for producto in cursor.fetchall():
        tree.insert('', 'end', values=producto)

def agregar_producto(tree):
    nombre = simpledialog.askstring("Agregar producto", "Ingrese el nombre del producto:")
    if not nombre:
        return
    precio_str = simpledialog.askstring("Agregar producto", "Ingrese el precio del producto:")
    try:
        precio = float(precio_str.replace(",", "."))
    except:
        messagebox.showerror("Error", "Precio inválido.")
        return
    cursor.execute('INSERT INTO PRODUCTOS (NOMBRE, PRECIO) VALUES (?, ?)', (nombre, precio))
    conexion.commit()
    cargar_productos(tree)

def editar_producto(tree):
    seleccionado = tree.selection()
    if not seleccionado:
        messagebox.showwarning("Atención", "Seleccione un producto.")
        return
    item = tree.item(seleccionado)
    codigo, nombre_actual, precio_actual = item['values']

    nuevo_nombre = simpledialog.askstring("Editar producto", "Nuevo nombre:", initialvalue=nombre_actual)
    if not nuevo_nombre:
        return
    nuevo_precio_str = simpledialog.askstring("Editar producto", "Nuevo precio:", initialvalue=str(precio_actual))
    try:
        nuevo_precio = float(nuevo_precio_str.replace(",", "."))
    except:
        messagebox.showerror("Error", "Precio inválido.")
        return
    cursor.execute('UPDATE PRODUCTOS SET NOMBRE = ?, PRECIO = ? WHERE CODIGO = ?', (nuevo_nombre, nuevo_precio, codigo))
    conexion.commit()
    cargar_productos(tree)

def eliminar_producto(tree):
    seleccionado = tree.selection()
    if not seleccionado:
        messagebox.showwarning("Atención", "Seleccione un producto.")
        return
    item = tree.item(seleccionado)
    codigo = item['values'][0]
    confirmar = messagebox.askyesno("Eliminar", f"¿Está seguro que desea eliminar el producto con código {codigo}?")
    if confirmar:
        cursor.execute('DELETE FROM PRODUCTOS WHERE CODIGO = ?', (codigo,))
        conexion.commit()
        cargar_productos(tree)

def lanzar_interfaz_productos():
    ventana = tk.Toplevel()
    ventana.title("Gestión de Productos")
    ventana.geometry("600x400")

    tree = ttk.Treeview(ventana, columns=('CODIGO', 'NOMBRE', 'PRECIO'), show='headings')
    tree.heading('CODIGO', text='Código')
    tree.heading('NOMBRE', text='Nombre')
    tree.heading('PRECIO', text='Precio')
    tree.pack(expand=True, fill='both', padx=10, pady=10)

    boton_frame = tk.Frame(ventana)
    boton_frame.pack(pady=10)

    tk.Button(boton_frame, text="Agregar", command=lambda: agregar_producto(tree)).pack(side='left', padx=10)
    tk.Button(boton_frame, text="Editar", command=lambda: editar_producto(tree)).pack(side='left', padx=10)
    tk.Button(boton_frame, text="Eliminar", command=lambda: eliminar_producto(tree)).pack(side='left', padx=10)
    tk.Button(boton_frame, text="Cerrar", command=ventana.destroy).pack(side='left', padx=10)

    cargar_productos(tree)


### PROGRAMA ###

print("Bienvenido al sistema de gestión de la posada Onda de mar 1.0 (Demo)")
tabla_existe('PRODUCTOS')

root = tk.Tk()
root.withdraw()  # Opcional si no usas root directamente

inicio()

root.mainloop()  # Este mantiene vivas las ventanas de tkinter