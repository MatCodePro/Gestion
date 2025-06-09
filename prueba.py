import tkinter as tk
from tkinter import ttk
from datetime import datetime, date

# Lista global para almacenar los registros de huéspedes
registro_de_huespedes = []

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gestión - Onda de Mar 1.0")
        self.geometry("800x600")

        self.frames = {}

        # Crear el menú lateral
        self.menu = tk.Frame(self, width=200, bg='#dddddd')
        self.menu.pack(side="left", fill="y")

        # Contenedor para las secciones
        self.container = tk.Frame(self)
        self.container.pack(side="right", fill="both", expand=True)

        # Botones del menú
        botones = [
            ("Gestión de Huéspedes", self.mostrar_gestion_huespedes),
            ("Gestión de Consumos", self.mostrar_gestion_consumos),
            ("Gestión de Productos", self.mostrar_gestion_productos),
            ("Gestión de Inventario", self.mostrar_gestion_inventario),
            ("Reportes", self.mostrar_reportes)
        ]

        for texto, comando in botones:
            b = tk.Button(self.menu, text=texto, command=comando, height=2, width=25)
            b.pack(pady=5)

        # Crear y guardar los frames para cada sección
        self.frames['huespedes'] = self.crear_frame_huespedes()
        self.frames['consumos'] = self.crear_frame_generico("Gestión de Consumos")
        self.frames['productos'] = self.crear_frame_generico("Gestión de Productos")
        self.frames['inventario'] = self.crear_frame_generico("Gestión de Inventario")
        self.frames['reportes'] = self.crear_frame_generico("Reportes")

        self.mostrar_frame('huespedes')

    def crear_frame_generico(self, texto):
        frame = tk.Frame(self.container)
        label = tk.Label(frame, text=texto, font=("Arial", 16))
        label.pack(pady=20)
        return frame

    def crear_frame_huespedes(self):
        frame = tk.Frame(self.container)

        tk.Label(frame, text="Nombre:").grid(row=0, column=0, sticky="e")
        nombre_entry = tk.Entry(frame)
        nombre_entry.grid(row=0, column=1)

        tk.Label(frame, text="Apellido:").grid(row=1, column=0, sticky="e")
        apellido_entry = tk.Entry(frame)
        apellido_entry.grid(row=1, column=1)

        tk.Label(frame, text="Teléfono:").grid(row=2, column=0, sticky="e")
        telefono_entry = tk.Entry(frame)
        telefono_entry.grid(row=2, column=1)

        tk.Label(frame, text="Email:").grid(row=3, column=0, sticky="e")
        email_entry = tk.Entry(frame)
        email_entry.grid(row=3, column=1)

        tk.Label(frame, text="¿Es reserva de Booking? (si/no):").grid(row=4, column=0, sticky="e")
        booking_entry = tk.Entry(frame)
        booking_entry.grid(row=4, column=1)

        tk.Label(frame, text="Estado (0: programado, 1: check-in):").grid(row=5, column=0, sticky="e")
        estado_entry = tk.Entry(frame)
        estado_entry.grid(row=5, column=1)

        tk.Label(frame, text="Check-in (DD-MM-YYYY):").grid(row=6, column=0, sticky="e")
        checkin_entry = tk.Entry(frame)
        checkin_entry.grid(row=6, column=1)

        tk.Label(frame, text="Documento:").grid(row=7, column=0, sticky="e")
        documento_entry = tk.Entry(frame)
        documento_entry.grid(row=7, column=1)

        tk.Label(frame, text="Fecha de nacimiento:").grid(row=8, column=0, sticky="e")
        nacimiento_entry = tk.Entry(frame)
        nacimiento_entry.grid(row=8, column=1)

        tk.Label(frame, text="Habitación:").grid(row=9, column=0, sticky="e")
        habitacion_entry = tk.Entry(frame)
        habitacion_entry.grid(row=9, column=1)

        tk.Label(frame, text="Contingente:").grid(row=10, column=0, sticky="e")
        contingente_entry = tk.Entry(frame)
        contingente_entry.grid(row=10, column=1)

        def guardar_huesped():
            nombre = nombre_entry.get()
            apellido = apellido_entry.get()
            telefono = telefono_entry.get()
            email = email_entry.get()
            booking = booking_entry.get().lower() in ["si", "s"]
            estado = int(estado_entry.get())
            if estado == 0:
                checkin = checkin_entry.get()
                documento = ""
                nacimiento = ""
                habitacion = 0
            else:
                checkin = str(date.today())
                documento = documento_entry.get()
                nacimiento = nacimiento_entry.get()
                habitacion = habitacion_entry.get()
            contingente = int(contingente_entry.get())
            registro = str(datetime.now())

            huesped = [nombre, apellido, telefono, email, contingente, nacimiento, documento, checkin, booking, habitacion, estado, registro]
            registro_de_huespedes.append(huesped)
            print(registro_de_huespedes)

        guardar_btn = tk.Button(frame, text="Guardar Huésped", command=guardar_huesped)
        guardar_btn.grid(row=11, column=0, columnspan=2, pady=10)

        return frame

    def mostrar_frame(self, nombre):
        for f in self.frames.values():
            f.pack_forget()
        self.frames[nombre].pack(fill="both", expand=True)

    def mostrar_gestion_huespedes(self):
        self.mostrar_frame('huespedes')

    def mostrar_gestion_consumos(self):
        self.mostrar_frame('consumos')

    def mostrar_gestion_productos(self):
        self.mostrar_frame('productos')

    def mostrar_gestion_inventario(self):
        self.mostrar_frame('inventario')

    def mostrar_reportes(self):
        self.mostrar_frame('reportes')

if __name__ == "__main__":
    app = App()
    app.mainloop()
