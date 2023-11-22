import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime

# Conectar a la base de datos SQLite
conn = sqlite3.connect('registro_app.db')

# Crear una tabla para almacenar los datos de los usuarios y la asistencia
conn.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT,
        ap_paterno TEXT,
        ap_materno TEXT,
        edad INTEGER,
        rut TEXT,
        correo TEXT,
        telefono TEXT
    )
''')

conn.execute('''
    CREATE TABLE IF NOT EXISTS asistencia (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        rut TEXT,
        fecha TEXT,
        hora TEXT
    )
''')

# Función para agregar usuarios
def agregar_usuario(nombre, ap_paterno, ap_materno, edad, rut, correo, telefono):
    conn.execute('''
        INSERT INTO usuarios (nombre, ap_paterno, ap_materno, edad, rut, correo, telefono)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (nombre, ap_paterno, ap_materno, edad, rut, correo, telefono))
    conn.commit()

# Función para registrar la asistencia
def registrar_asistencia(rut):
    now = datetime.now()
    fecha_hora = now.strftime("%Y-%m-%d %H:%M:%S")
    conn.execute('''
        INSERT INTO asistencia (rut, fecha, hora)
        VALUES (?, ?, ?)
    ''', (rut, now.date(), now.time()))
    conn.commit()

# Interfaz de la aplicación
st.title("Registro de Usuarios y Asistencia")

# Sección para agregar usuarios
st.header("Agregar Usuarios")
nombre = st.text_input("Nombre:")
ap_paterno = st.text_input("Apellido Paterno:")
ap_materno = st.text_input("Apellido Materno:")
edad = st.number_input("Edad:", min_value=0, max_value=150)
rut = st.text_input("RUT:")
correo = st.text_input("Correo Electrónico:")
telefono = st.text_input("Teléfono:")

if st.button("Agregar Usuario"):
    agregar_usuario(nombre, ap_paterno, ap_materno, edad, rut, correo, telefono)
    st.success("Usuario agregado con éxito!")

# Sección para registrar asistencia
st.header("Registrar Asistencia")
rut_asistencia = st.text_input("RUT para registrar asistencia:")

if st.button("Registrar Asistencia"):
    if rut_asistencia:
        registrar_asistencia(rut_asistencia)
        st.success("Asistencia registrada con éxito!")

# Mostrar datos de usuarios y asistencia
st.header("Datos de Usuarios")
usuarios_data = pd.read_sql('SELECT * FROM usuarios', conn)
st.write(usuarios_data)

st.header("Registro de Asistencia")
asistencia_data = pd.read_sql('SELECT * FROM asistencia', conn)
st.write(asistencia_data)

# Cerrar la conexión a la base de datos al finalizar
conn.close()
