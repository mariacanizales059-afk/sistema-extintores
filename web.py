import streamlit as st

# Configuración de página
st.set_page_config(page_title="Extincañisol S.A.", page_icon="🧯", layout="centered")

# CSS Corregido
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .name-text { text-align: center; font-size: 28px; font-weight: bold; color: #D32F2F; }
    .info-text { text-align: center; font-size: 16px; color: #666; }
    </style>
    """, unsafe_allow_html=True) # USAR HTML AQUÍ

# --- CONTENIDO ---
st.markdown('<div style="text-align: center;"><img src="https://cdn-icons-png.flaticon.com/512/782/782761.png" width="120"></div>', unsafe_allow_html=True)

st.markdown('<p class="name-text">Extincañisol S.A.</p>', unsafe_allow_html=True)
st.markdown('<p class="info-text">🛡️ 45 Años Protegiendo a Costa Rica</p>', unsafe_allow_html=True)

st.write("---")

st.subheader("📲 Contacto Directo")

# Botón de WhatsApp
link_wa = "https://wa.me/50688888888" # CAMBIA EL NÚMERO
st.markdown(f'<a href="{link_wa}" target="_blank"><button style="width:100%; background-color:#25D366; color:white; border:none; padding:15px; border-radius:10px; font-weight:bold; cursor:pointer;">💬 Escribir por WhatsApp</button></a>', unsafe_allow_html=True)

st.write("")

# Botón de Llamada
st.markdown(f'<a href="tel:50688888888"><button style="width:100%; background-color:#1976D2; color:white; border:none; padding:15px; border-radius:10px; font-weight:bold; cursor:pointer;">📞 Llamar ahora</button></a>', unsafe_allow_html=True)

st.write("---")
st.caption("📍 Servicio en todo el país")
