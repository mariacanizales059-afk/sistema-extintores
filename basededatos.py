import os
import subprocess
import sys

# --- 1. CONFIGURACIÓN E INSTALACIÓN ---
NOMBRE_ARCHIVO = "basededatos.py"

def configurar_entorno():
    librerias = ["streamlit", "pandas", "xlsxwriter"]
    for lib in librerias:
        try:
            __import__(lib)
        except ImportError:
            subprocess.check_call([sys.executable, "-m", "pip", "install", lib])
    if not os.path.exists("Abrir_Programa.bat"):
        with open("Abrir_Programa.bat", "w") as f:
            f.write(f"@echo off\npython -m streamlit run {NOMBRE_ARCHIVO} --server.address 0.0.0.0\npause")

configurar_entorno()

import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime, timedelta
import io

# --- 2. BASE DE DATOS (NUEVA TABLA DE PAGOS) ---
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
    # Tabla de Pagos
    cursor.execute('''CREATE TABLE IF NOT EXISTS pagos 
                      (id_pago INTEGER PRIMARY KEY AUTOINCREMENT, id_cli INTEGER, monto REAL, 
                       estado TEXT, metodo TEXT, fecha_pago DATE)''')
    conn.commit()
    conn.close()

inicializar_bd()

# --- 3. SEGURIDAD ---
def check_password():
    if "password_correct" not in st.session_state:
        st.session_state["password_correct"] = False
    if st.session_state["password_correct"]: return True
    st.title("🔐 Acceso al Sistema de Extintores")
    pwd = st.text_input("Contraseña:", type="password")
    if st.button("Entrar"):
        if pwd == "extintores2026":
            st.session_state["password_correct"] = True
            st.rerun()
        else: st.error("❌ Incorrecta")
    return False

# --- 4. PROGRAMA PRINCIPAL ---
if check_password():
    st.sidebar.title("Menú Principal")
    menu = ["➕ Registrar Cliente", "💰 Gestión de Pagos", "🔍 Buscar/Inventario", "🚨 Vencimientos", "📊 Reportes Excel", "🗑️ Eliminar"]
    opcion = st.sidebar.selectbox("Ir a:", menu)

    # --- REGISTRAR CLIENTE ---
    if opcion == "➕ Registrar Cliente":
        st.header("Nuevo Cliente y Equipo")
        with st.form("reg"):
            c1, c2 = st.columns(2)
            nombre = c1.text_input("Nombre")
            tel = c1.text_input("Teléfono")
            tipo = c2.selectbox("Extintor", ["PQS", "CO2", "Agua", "Espuma"])
            fecha = c2.date_input("Fecha Carga", datetime.now())
            if st.form_submit_button("Guardar"):
                conn = conectar(); curr = conn.cursor()
                curr.execute("INSERT INTO clientes (nombre, tel) VALUES (?,?)", (nombre, tel))
                id_c = curr.lastrowid
                vence = fecha + timedelta(days=365)
                curr.execute("INSERT INTO extintores (id_cli, tipo, fecha_carga, vencimiento) VALUES (?,?,?,?)", (id_c, tipo, fecha, vence))
                conn.commit(); conn.close()
                st.success("Registrado correctamente")

    # --- GESTIÓN DE PAGOS (NUEVO) ---
    elif opcion == "💰 Gestión de Pagos":
        st.header("Control de Cobros")
        tab_reg, tab_ver = st.tabs(["Registrar Pago", "Ver Estado de Cuentas"])
        
        with tab_reg:
            conn = conectar()
            clientes = pd.read_sql_query("SELECT id, nombre FROM clientes", conn)
            conn.close()
            if not clientes.empty:
                with st.form("pagos_form"):
                    dict_c = dict(zip(clientes['nombre'], clientes['id']))
                    selec = st.selectbox("Seleccionar Cliente", list(dict_c.keys()))
                    monto = st.number_input("Monto a Pagar", min_value=0.0)
                    estado = st.radio("Estado", ["Pagado", "Pendiente"])
                    metodo = st.selectbox("Método de Pago", ["Efectivo", "Cheque", "Depósito", "SINPE", "N/A"])
                    f_pago = st.date_input("Fecha de Pago", datetime.now())
                    if st.form_submit_button("Registrar Movimiento"):
                        conn = conectar(); curr = conn.cursor()
                        curr.execute("INSERT INTO pagos (id_cli, monto, estado, metodo, fecha_pago) VALUES (?,?,?,?,?)",
                                     (dict_c[selec], monto, estado, metodo, f_pago))
                        conn.commit(); conn.close()
                        st.success(f"Pago de {selec} registrado")
            else: st.info("Primero registra un cliente")

        with tab_ver:
            conn = conectar()
            query = '''SELECT c.nombre as Cliente, p.monto as Monto, p.estado as Estado, 
                              p.metodo as Metodo, p.fecha_pago as Fecha 
                       FROM clientes c JOIN pagos p ON c.id = p.id_cli ORDER BY p.fecha_pago DESC'''
            df_pagos = pd.read_sql_query(query, conn)
            conn.close()
            st.dataframe(df_pagos, use_container_width=True)

    # --- BUSCAR ---
    elif opcion == "🔍 Buscar/Inventario":
        st.header("Buscador")
        conn = conectar()
        df = pd.read_sql_query("SELECT c.nombre, c.tel, e.tipo, e.vencimiento FROM clientes c JOIN extintores e ON c.id = e.id_cli", conn)
        conn.close()
        bus = st.text_input("Buscar nombre:")
        if bus: df = df[df['nombre'].str.contains(bus, case=False)]
        st.table(df)

    # --- VENCIMIENTOS ---
    elif opcion == "🚨 Vencimientos":
        st.header("Vencen este mes")
        hoy = datetime.now().date()
        lim = hoy + timedelta(days=30)
        conn = conectar()
        res = conn.execute("SELECT c.nombre, e.vencimiento FROM clientes c JOIN extintores e ON c.id = e.id_cli WHERE e.vencimiento BETWEEN ? AND ?", (hoy, lim)).fetchall()
        conn.close()
        for r in res: st.error(f"⚠️ {r[0]} - Vence: {r[1]}")

    # --- EXCEL ---
    elif opcion == "📊 Reportes Excel":
        st.header("Descargar Datos")
        conn = conectar()
        df1 = pd.read_sql_query("SELECT * FROM clientes", conn)
        df2 = pd.read_sql_query("SELECT * FROM pagos", conn)
        conn.close()
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df1.to_excel(writer, sheet_name='Clientes', index=False)
            df2.to_excel(writer, sheet_name='Pagos', index=False)
        st.download_button("📥 Bajar Excel", output.getvalue(), "Negocio.xlsx")

    # --- ELIMINAR ---
    elif opcion == "🗑️ Eliminar":
        st.header("Eliminar Cliente")
        conn = conectar()
        cl = pd.read_sql_query("SELECT id, nombre FROM clientes", conn)
        conn.close()
        if not cl.empty:
            d_c = dict(zip(cl['nombre'], cl['id']))
            borrar = st.selectbox("Cliente a eliminar", list(d_c.keys()))
            if st.button("BORRAR PERMANENTEMENTE"):
                id_b = d_c[borrar]
                conn = conectar(); cur = conn.cursor()
                cur.execute("DELETE FROM extintores WHERE id_cli=?", (id_b,))
                cur.execute("DELETE FROM pagos WHERE id_cli=?", (id_b,))
                cur.execute("DELETE FROM clientes WHERE id=?", (id_b,))
                conn.commit(); conn.close()
                st.rerun()
