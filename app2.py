import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime

# Conectar a la base de datos SQLite
conn = sqlite3.connect('registro_usuarios.db')

# Crear un DataFrame para almacenar los datos de los usuarios y la asistencia
usuarios_df = pd.DataFrame(columns=["Nombre", "Apellido Paterno", "Apellido Materno", "Edad", "RUT", "Correo Electrónico", "Teléfono"])
asistencia_df = pd.DataFrame(columns=["RUT", "Fecha", "Hora"])

# Verificar si las tablas existen, de lo contrario, crearlas
usuarios_df.to_sql('usuarios', conn, if_exists='replace', index=False)
asistencia_df.to_sql('asistencia', conn, if_exists='replace', index=False)

# Función para agregar usuarios
def agregar_usuario(nombre, ap_paterno, ap_materno, edad, rut, correo, telefono):
    global usuarios_df
    nuevo_usuario = pd.DataFrame([[nombre, ap_paterno, ap_materno, edad, rut, correo, telefono]],
                                 columns=["Nombre", "Apellido Paterno", "Apellido Materno", "Edad", "RUT", "Correo Electrónico", "Teléfono"])
    usuarios_df = pd.concat([usuarios_df, nuevo_usuario], ignore_index=True)
    usuarios_df.to_sql('usuarios', conn, if_exists='replace', index=False)

# Función para registrar la asistencia
def registrar_asistencia(rut):
    global asistencia_df
    now = datetime.now()
    fecha_hora = now.strftime("%Y-%m-%d %H:%M:%S")
    nuevo_registro = pd.DataFrame([[rut, now.date(), now.time()]],
                                  columns=["RUT", "Fecha", "Hora"])
    asistencia_df = pd.concat([asistencia_df, nuevo_registro], ignore_index=True)
    asistencia_df.to_sql('asistencia', conn, if_exists='replace', index=False)

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
    if rut_asistencia in usuarios_df["RUT"].values:
        registrar_asistencia(rut_asistencia)
        st.success("Asistencia registrada con éxito!")
    else:
        st.error("El RUT ingresado no corresponde a un usuario registrado.")

# Mostrar datos de usuarios y asistencia
st.header("Datos de Usuarios")
st.write(usuarios_df)

st.header("Registro de Asistencia")
st.write(asistencia_df)

# Cerrar la conexión a la base de datos al finalizar
conn.close()
