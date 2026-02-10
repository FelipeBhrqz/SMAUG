# src/ui/app.py
import streamlit as st
import sys
import os

# --- 1. CONFIGURACIÓN DE RUTAS (Importante para que funcione) ---
# Esto permite que Python encuentre la carpeta 'src'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.core.game_logic import SmaugGuardian
from src.core.levels import GAME_LEVELS

# --- 2. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="SMAUG | Prompt Injection", page_icon="🐉", layout="centered")

# CSS Estilo Hacker
st.markdown("""
<style>
    .stApp {background-color: #0e1117; color: #00ff41;}
    .stTextInput > div > div > input {background-color: #111; color: #00ff41; border: 1px solid #00ff41;}
    h1 {color: #00ff41; text-shadow: 0 0 10px #00ff41;}
    .stButton>button {background-color: #00ff41; color: black; font-weight: bold;}
</style>
""", unsafe_allow_html=True)

# --- 3. LÓGICA DE ESTADO (Memoria) ---
if "level" not in st.session_state:
    st.session_state.level = 1
if "messages" not in st.session_state:
    st.session_state.messages = []

# Verificar si ganó el juego
if st.session_state.level > len(GAME_LEVELS):
    st.balloons()
    st.title("🏆 ¡SISTEMA HACKEADO!")
    st.success("Has derrotado a SMAUG y obtenido todos los tesoros.")
    if st.button("Reiniciar Sistema"):
        st.session_state.level = 1
        st.session_state.messages = []
        st.rerun()
    st.stop()

# Cargar nivel actual
current_level_data = GAME_LEVELS[st.session_state.level]
bot = SmaugGuardian(use_local=True)

# --- 4. INTERFAZ ---
st.title("🐉 PROYECTO SMAUG")
st.subheader(f"Objetivo: {current_level_data['title']}")
st.progress(st.session_state.level * 33)

# Mostrar historial de chat
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Input del usuario
if prompt := st.chat_input("Intenta engañar a la IA..."):
    # 1. Mostrar mensaje usuario
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # 2. Obtener respuesta IA
    response = bot.get_response(prompt, current_level_data["system_prompt"])
    
    # 3. Mostrar respuesta IA
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.write(response)

# Zona de Validación (Password)
st.divider()
col1, col2 = st.columns([3, 1])
with col1:
    guess = st.text_input("Ingresa la contraseña:", key="pass_input", placeholder="SOLO la contraseña...")
with col2:
    if st.button("HACKEAR"):
        if guess.strip().upper() == current_level_data["password"]:
            st.success("✅ ¡ACCESO CONCEDIDO! Pasando al siguiente nivel...")
            st.session_state.level += 1
            st.session_state.messages = [] # Limpiar chat
            st.rerun()
        else:
            st.error("❌ DENEGADO. Esa no es la contraseña.")