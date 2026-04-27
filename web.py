import streamlit as st

st.set_page_config(page_title="Extincañisol S.A. | Seguridad Premium", page_icon="🧯", layout="wide")

# --- DISEÑO DE LUJO (CSS) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700;800&display=swap');
    
    html, body, [class*="css"] { font-family: 'Montserrat', sans-serif; }
    
    .main { background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); }
    
    /* Encabezado con efecto cristal */
    .hero-container {
        background: rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 50px;
        border: 1px solid rgba(255, 255, 255, 0.3);
        text-align: center;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.15);
    }
    
    .main-title { font-size: 60px; font-weight: 800; color: #1e1e1e; margin-bottom: 0px; }
    .highlight { color: #E63946; }
    .experience-badge {
        background-color: #E63946;
        color: white;
        padding: 5px 15px;
        border-radius: 50px;
        font-weight: bold;
        font-size: 14px;
        display: inline-block;
        margin-bottom: 20px;
    }
    
    /* Tarjetas de Servicios */
    .service-card {
        background: white;
        padding: 30px;
        border-radius: 15px;
        box-shadow: 0 10px 20px rgba(0,0,0,0.05);
        transition: transform 0.3s;
        border-bottom: 4px solid #E63946;
        height: 100%;
    }
    .service-card:hover { transform: translateY(-10px); }
    
    /* Botones Estilizados */
    .stButton>button {
        background-color: #1e1e1e;
        color: white;
        border-radius: 12px;
        padding: 10px 25px;
        border: none;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER / HERO SECTION ---
st.markdown("""
    <div class="hero-container">
        <span class="experience-badge">45 AÑOS DE TRAYECTORIA NACIONAL</span>
        <h1 class="main-title">EXTIN<span class="highlight">CAÑISOL</span> S.A.</h1>
        <p style="font-size: 22px; color: #444;">Calidad Certificada en Seguridad Contra Incendios</p>
    </div>
    """, unsafe_allow_html=True)

st.write("#") # Espacio

# --- SECCIÓN: POR QUÉ ELEGIRNOS ---
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""<div class="service-card">
        <h2 style="color: #E63946;">🛡️</h2>
        <h3>Calidad de Élite</h3>
        <p>No solo recargamos, garantizamos su vida. Usamos agentes extintores de grado industrial con certificación internacional.</p>
    </div>""", unsafe_allow_html=True)

with col2:
    st.markdown("""<div class="service-card">
        <h2 style="color: #E63946;">🚚</h2>
        <h3>Rapidez Nacional</h3>
        <p>Nuestra flota logística cubre las 7 provincias. Retiramos y entregamos en tiempo récord para que nunca esté desprotegido.</p>
    </div>""", unsafe_allow_html=True)

with col3:
    st.markdown("""<div class="service-card">
        <h2 style="color: #E63946;">🤝</h2>
        <h3>Experiencia Real</h3>
        <p>Desde 1981 protegiendo a Costa Rica. 45 años no son una cifra, son miles de clientes satisfechos y seguros.</p>
    </div>""", unsafe_allow_html=True)

st.write("---")

# --- SECCIÓN: IMPACTO VISUAL ---
c_txt, c_img = st.columns([1, 1.2], gap="large")

with c_txt:
    st.title("Seguridad que se nota.")
    st.write("""
    En **Extincañisol S.A.**, entendemos que un extintor es la primera línea de defensa. 
    Por eso, nuestro proceso de mantenimiento sigue rigurosos protocolos técnicos que superan las normativas básicas.
    
    * **Personal Certificado:** Técnicos con décadas de conocimiento.
    * **Transparencia:** Informes detallados de cada equipo.
    * **Tecnología:** Equipos de última generación para pruebas hidrostáticas.
    """)
    st.button("Agendar una Inspección Gratuita")

with c_img:
    # Imagen de alta calidad (puedes usar una de tu papá aquí
