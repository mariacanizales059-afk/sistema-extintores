import streamlit as st

# Configuración para que se vea bien en celulares
st.set_page_config(page_title="Extincañisol S.A. - Contacto", page_icon="🧯", layout="centered")

# CSS para darle estilo de "Tarjeta"
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stButton>button {
        width: 100%;
        border-radius: 20px;
        height: 3em;
        background-color: #D32F2F;
        color: white;
        font-weight: bold;
        border: none;
    }
    .profile-pic { display: block; margin-left: auto; margin-right: auto; border-radius: 50%; }
    .name-text { text-align: center; font-size: 28px; font-weight: bold; color: #D32F2F; margin-top: 10px; }
    .info-text { text-align: center; font-size: 16px; color: #666; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_headers=True)

# --- CONTENIDO DE LA TARJETA ---
# Si tienes una foto del logo o de tu papá, cámbiala aquí
st.markdown('<div style="text-align: center;"><img src="https://cdn-icons-png.flaticon.com/512/782/782761.png" width="120"></div>', unsafe_allow_headers=True)

st.markdown('<p class="name-text">Extincañisol S.A.</p>', unsafe_allow_headers=True)
st.markdown('<p class="info-text">🛡️ 45 Años de Excelencia en Seguridad Humana</p>', unsafe_allow_headers=True)

st.write("---")

# Botones de Acción Rápida
st.subheader("📲 Contáctanos Ahora")

# Botón de WhatsApp (Reemplaza el número 506... con el de tu papá)
link_whatsapp = "https://wa.me/50688888888?text=Hola!%20Necesito%20información%20sobre%20extintores"
st.markdown(f'[@button] <a href="{link_whatsapp}" target="_blank"><button style="width:100%; background-color:#25D366; color:white; border:none; padding:12px; border-radius:10px; cursor:pointer; font-weight:bold;">💬 Escribir por WhatsApp</button></a>', unsafe_allow_headers=True)

st.write("") # Espacio

# Botón de Llamada directa
st.markdown(f'<a href="tel:50688888888"><button style="width:100%; background-color:#1976D2; color:white; border:none; padding:12px; border-radius:10px; cursor:pointer; font-weight:bold;">📞 Llamar por Teléfono</button></a>', unsafe_allow_headers=True)

st.write("") # Espacio

# Botón para ver el catálogo o servicios (Redirige a otra parte de la misma web)
if st.button("🔍 Ver Nuestros Servicios"):
    st.info("Especialistas en: PQS, CO2, Agua, K y Mantenimiento Industrial.")

st.write("---")
st.caption("📍 Cobertura en todo el país | San José, Costa Rica")
