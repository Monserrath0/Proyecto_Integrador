import tkinter as tk
from tkinter import messagebox
from tkinter import PhotoImage  # Importa PhotoImage para manejar imágenes
import mysql.connector
import qrcode
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
import smtplib
import os


# Configuración de la base de datos
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="123456789",
    database="Empresa_Acierto"
)
cursor = db.cursor()

# Configuración del servidor de correo
smtp_server = "smtp.gmail.com"
smtp_port = 587
email_address = "luisdiegoduque49@gmail.com"
email_password = "xyur kczx nqni cesc"


def enviar_correo(destinatario, asunto, cuerpo, qr_path):
    msg = MIMEMultipart()
    msg['From'] = email_address
    msg['To'] = destinatario
    msg['Subject'] = asunto

    # Adjunta el cuerpo del correo
    msg.attach(MIMEText(cuerpo, 'plain'))

    # Adjunta la imagen del código QR
    with open(qr_path, 'rb') as img:
        qr_image = MIMEImage(img.read())
    msg.attach(qr_image)

    # Establece la conexión y envía el correo
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(email_address, email_password)
        server.sendmail(email_address, destinatario, msg.as_string())


def guardar_datos(tabla, datos):
    # Asegúrate de que el nombre de la tabla sea en minúsculas
    tabla = tabla.lower()

    columns = ', '.join(datos.keys())
    values = ', '.join(['%s'] * len(datos))
    query = f"INSERT INTO {tabla} ({columns}) VALUES ({values})"
    cursor.execute(query, list(datos.values()))
    db.commit()


def generar_qr(data, filename):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(filename)


def guardar_residente():
    residente_data = {
        'Area': entry_area.get(),
        'Matricula': entry_matricula.get(),
        'Nombre': entry_nombre.get(),
        'Apellido_Paterno': entry_apellido_paterno.get(),
        'Apellido_Materno': entry_apellido_materno.get(),
        'CURP': entry_curp.get()
    }

    guardar_datos('residentes', residente_data)

    # Genera el código QR y envía el correo
    qr_filename = f"qr_residente_{entry_matricula.get()}.png"
    generar_qr(str(residente_data), qr_filename)
    enviar_correo(entry_correo.get(), "Código QR Residente",
                  "Adjunto se encuentra su código QR", qr_filename)
    messagebox.showinfo("Éxito", "Residente registrado correctamente")


def guardar_visitante():
    visitante_data = {
        'Id_visitante': None,  # Autoincremental, no es necesario proporcionar un valor
        'Nombre': entry_nombre_visitante.get(),
        'Apellido_Paterno': entry_apellido_paterno_visitante.get(),
        'Apellido_Materno': entry_apellido_materno_visitante.get(),
        'Edad': entry_edad_visitante.get(),
        'CURP': entry_curp_visitante.get(),
        'Direccion': entry_direccion_visitante.get(),
        'Motivo_visita': entry_motivo_visita.get(),
        'Area_departamento': entry_area_departamento_visitante.get(),
        'Correo': entry_correo_visitante.get(),
        'Telefono': entry_telefono_visitante.get()
    }

    guardar_datos('visitantes', visitante_data)

    # Obtén el id_visitante recién insertado
    cursor.execute("SELECT LAST_INSERT_ID()")
    id_visitante = cursor.fetchone()[0]

    # Genera el código QR y envía el correo
    qr_filename = f"qr_visitante_{id_visitante}.png"
    generar_qr(str(visitante_data), qr_filename)
    enviar_correo(entry_correo_visitante.get(), "Código QR Visitante",
                  "Adjunto se encuentra su código QR", qr_filename)
    messagebox.showinfo("Éxito", "Visitante registrado correctamente")

# Función para comunicar el área 1


def comunicar_area_1():
    # Aquí puedes implementar la lógica para comunicar el área 1
    messagebox.showinfo("Comunicar Área 1",
                        "Se ha comunicado el Área 1 exitosamente")

# Función para detener la comunicación del área 1


def detener_comunicacion_area_1():
    # Aquí puedes implementar la lógica para detener la comunicación del área 1
    messagebox.showinfo("Detener Comunicación Área 1",
                        "Se ha detenido la comunicación del Área 1")

# Función para comunicar el área 2


def comunicar_area_2():
    # Aquí puedes implementar la lógica para comunicar el área 2
    messagebox.showinfo("Comunicar Área 2",
                        "Se ha comunicado el Área 2 exitosamente")

# Función para detener la comunicación del área 2


def detener_comunicacion_area_2():
    # Aquí puedes implementar la lógica para detener la comunicación del área 2
    messagebox.showinfo("Detener Comunicación Área 2",
                        "Se ha detenido la comunicación del Área 2")


# Configuración de la interfaz gráfica
root = tk.Tk()
root.title("Registro Residente/Visitante")

# Agrega una imagen de la empresa al formulario
# Reemplaza con la ruta de tu logo
logo_path = "C:/Users/HP/Documents/Tecnologias/Interfon/Acierto.png"
if os.path.exists(logo_path):
    logo_image = PhotoImage(file=logo_path)
    logo_label = tk.Label(root, image=logo_image)
    logo_label.pack()

# Frame para el formulario de Residente
frame_residente = tk.Frame(root)
frame_residente.pack(padx=10, pady=10)

tk.Label(frame_residente, text="Área:").grid(row=0, column=0)
entry_area = tk.Entry(frame_residente)
entry_area.grid(row=0, column=1)

tk.Label(frame_residente, text="Matrícula:").grid(row=1, column=0)
entry_matricula = tk.Entry(frame_residente)
entry_matricula.grid(row=1, column=1)

tk.Label(frame_residente, text="Nombre:").grid(row=2, column=0)
entry_nombre = tk.Entry(frame_residente)
entry_nombre.grid(row=2, column=1)

tk.Label(frame_residente, text="Apellido Paterno:").grid(row=3, column=0)
entry_apellido_paterno = tk.Entry(frame_residente)
entry_apellido_paterno.grid(row=3, column=1)

tk.Label(frame_residente, text="Apellido Materno:").grid(row=4, column=0)
entry_apellido_materno = tk.Entry(frame_residente)
entry_apellido_materno.grid(row=4, column=1)

tk.Label(frame_residente, text="CURP:").grid(row=5, column=0)
entry_curp = tk.Entry(frame_residente)
entry_curp.grid(row=5, column=1)

tk.Label(frame_residente, text="Correo:").grid(row=6, column=0)
entry_correo = tk.Entry(frame_residente)
entry_correo.grid(row=6, column=1)
tk.Button(frame_residente, text="Registrar Residente",
          command=guardar_residente).grid(row=7, columnspan=2, pady=10)


# Frame para el formulario de Visitante
frame_visitante = tk.Frame(root)
frame_visitante.pack(padx=10, pady=10)

tk.Label(frame_visitante, text="Nombre:").grid(row=0, column=0)
entry_nombre_visitante = tk.Entry(frame_visitante)
entry_nombre_visitante.grid(row=0, column=1)

tk.Label(frame_visitante, text="Apellido Paterno:").grid(row=1, column=0)
entry_apellido_paterno_visitante = tk.Entry(frame_visitante)
entry_apellido_paterno_visitante.grid(row=1, column=1)

tk.Label(frame_visitante, text="Apellido Materno:").grid(row=2, column=0)
entry_apellido_materno_visitante = tk.Entry(frame_visitante)
entry_apellido_materno_visitante.grid(row=2, column=1)

tk.Label(frame_visitante, text="Edad:").grid(row=3, column=0)
entry_edad_visitante = tk.Entry(frame_visitante)
entry_edad_visitante.grid(row=3, column=1)

tk.Label(frame_visitante, text="CURP:").grid(row=4, column=0)
entry_curp_visitante = tk.Entry(frame_visitante)
entry_curp_visitante.grid(row=4, column=1)

tk.Label(frame_visitante, text="Dirección:").grid(row=5, column=0)
entry_direccion_visitante = tk.Entry(frame_visitante)
entry_direccion_visitante.grid(row=5, column=1)

tk.Label(frame_visitante, text="Motivo Visita:").grid(row=6, column=0)
entry_motivo_visita = tk.Entry(frame_visitante)
entry_motivo_visita.grid(row=6, column=1)

tk.Label(frame_visitante, text="Área/Departamento:").grid(row=7, column=0)
entry_area_departamento_visitante = tk.Entry(frame_visitante)
entry_area_departamento_visitante.grid(row=7, column=1)

tk.Label(frame_visitante, text="Correo:").grid(row=8, column=0)
entry_correo_visitante = tk.Entry(frame_visitante)
entry_correo_visitante.grid(row=8, column=1)

tk.Label(frame_visitante, text="Teléfono:").grid(row=9, column=0)
entry_telefono_visitante = tk.Entry(frame_visitante)
entry_telefono_visitante.grid(row=9, column=1)
tk.Button(frame_visitante, text="Registrar Visitante",
          command=guardar_visitante).grid(row=10, columnspan=2, pady=10)

# Botones para comunicar y detener la comunicación del área 1
frame_area_1 = tk.Frame(root)
frame_area_1.pack(pady=5)
tk.Button(frame_area_1, text="Comunicar Área 1",
          command=comunicar_area_1).pack(side=tk.LEFT, padx=5)
tk.Button(frame_area_1, text="Detener Comunicación Área 1",
          command=detener_comunicacion_area_1).pack(side=tk.LEFT, padx=5)

# Botones para comunicar y detener la comunicación del área 2
frame_area_2 = tk.Frame(root)
frame_area_2.pack(pady=5)
tk.Button(frame_area_2, text="Comunicar Área 2",
          command=comunicar_area_2).pack(side=tk.LEFT, padx=5)
tk.Button(frame_area_2, text="Detener Comunicación Área 2",
          command=detener_comunicacion_area_2).pack(side=tk.LEFT, padx=5)

root.mainloop()
