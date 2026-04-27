import os
import subprocess
import sys

# --- CONFIGURACIÓN INICIAL ---
NOMBRE_ARCHIVO = "basededatos.py" # Asegúrate de que coincida con tu nombre de archivo

def configurar_entorno():
    # 1. Instalar librerías si faltan
    librerias = ["streamlit", "pandas", "xlsxwriter"]
    for lib in librerias:
        try:
            __import__(lib)
        except ImportError:
            print(f"Instalando {lib}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", lib])

    # 2. Crear el archivo de doble clic para la secretaria (.bat)
    if not os.path.exists("Abrir_Programa.bat"):
        with open("Abrir_Programa.bat", "w") as f:
            f.write(f"@echo off\n")
            f.write(f"streamlit run {NOMBRE_ARCHIVO}\n")
            f.write(f"pause")
        print("✅ Se ha creado el archivo 'Abrir_Programa.bat'. Úsalo para entrar siempre.")

configurar_entorno()

import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime, timedelta
import io

# --- BASE DE DATOS ---
def conectar():
    return sqlite3.connect("empresa_extintores.db", check_same_thread=False)

def inicializar_bd():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS clientes 
                      (id INTEGER PRIMARY KEY AUTOINCREMENT, nombre TEXT, tel TEXT, dir TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS extintores 
                      (id_ext INTEGER PRIMARY KEY AUTOINCREMENT, id_cli INTEGER, tipo TEXT, 
                       capacidad TEXT, fecha_carga DATE, vencimiento DATE)''')
    conn.commit()
    conn.close()

inicializar_bd()

# --- INTERFAZ STREAMLIT ---
st.set_page_config(page_title="Sistema Extintores Pro", layout="wide")
st.title("🧯 Control de Extintores")

menu = ["➕ Registrar Cliente", "🔍 Buscar Cliente", "🚨 Vencimientos", "📊 Reportes y Excel"]
opcion = st.sidebar.selectbox("Menú Principal", menu)

# --- 1. REGISTRAR ---
if opcion == "➕ Registrar Cliente":
    st.header("Nuevo Registro")
    with st.form("form_registro", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            nombre = st.text_input("Nombre del Cliente")
            tel = st.text_input("Teléfono")
            direccion = st.text_area("Dirección")
        with col2:
            tipo = st.selectbox("Tipo de Extintor", ["PQS", "CO2", "Agua", "Espuma"])
            cap = st.text_input("Capacidad (Ej: 10lb)")
            fecha = st.date_input("Fecha de Carga", datetime.now())
        
        if st.form_submit_button("Guardar en Base de Datos"):
            if nombre and tel:
                conn = conectar()
                curr = conn.cursor()
                curr.execute("INSERT INTO clientes (nombre, tel, dir) VALUES (?,?,?)", (nombre, tel, direccion))
                id_c = curr.lastrowid
                vence = fecha + timedelta(days=365) # Vence en 1 año
                curr.execute("INSERT INTO extintores (id_cli, tipo, capacidad, fecha_carga, vencimiento) VALUES (?,?,?,?,?)",
                             (id_c, tipo, cap, fecha, vence))
                conn.commit()
                conn.close()
                st.success(f"✅ ¡Guardado! Próxima recarga: {vence}")
            else:
                st.error("⚠️ Nombre y teléfono son necesarios.")

# --- 2. BUSCAR ---
elif opcion == "🔍 Buscar Cliente":
    st.header("Buscador de Clientes")
    conn = conectar()
    df = pd.read_sql_query('''SELECT c.nombre as Cliente, c.tel as Telefono, c.dir as Direccion, 
                              e.tipo as Equipo, e.vencimiento as Vencimiento 
                              FROM clientes c JOIN extintores e ON c.id = e.id_cli''', conn)
    conn.close()
    busqueda = st.text_input("Buscar por nombre:")
    if busqueda:
        df = df[df['Cliente'].str.contains(busqueda, case=False)]
    st.dataframe(df, use_container_width=True)

# --- 3. VENCIMIENTOS ---
elif opcion == "🚨 Vencimientos":
    st.header("Mantenimientos para este mes")
    hoy = datetime.now().date()
    limite = hoy + timedelta(days=30)
    conn = conectar()
    res = conn.execute('''SELECT c.nombre, c.tel, e.vencimiento FROM clientes c 
                          JOIN extintores e ON c.id = e.id_cli 
                          WHERE e.vencimiento BETWEEN ? AND ?''', (hoy, limite)).fetchall()
    conn.close()
    if res:
        for r in res:
            st.warning(f"⚠️ **{r[0]}** (Tel: {r[1]}) - Vence el {r[2]}")
    else:
        st.info("No hay vencimientos próximos.")

# --- 4. EXCEL ---
elif opcion == "📊 Reportes y Excel":
    st.header("Exportar a Excel")
    conn = conectar()
    df_total = pd.read_sql_query("SELECT * FROM clientes JOIN extintores ON clientes.id = extintores.id_cli", conn)
    conn.close()

    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df_total.to_excel(writer, index=False)
    
    st.download_button(label="📥 Descargar para Papá", data=output.getvalue(), 
                       file_name="Reporte_Extintores.xlsx", mime="application/vnd.ms-excel")
