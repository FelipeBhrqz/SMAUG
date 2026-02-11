import base64
import os
import sys
import streamlit as st

# --- 1. CONFIGURACIÓN DE RUTAS (Importante para que funcione) ---
# Esto permite que Python encuentre la carpeta 'src'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.core.game_logic import SmaugGuardian
from src.core.levels import GAME_LEVELS

# --- 2. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="SMAUG | Medieval Edition", page_icon="🐉", layout="centered")

css_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../assets/style.css"))
with open(css_path, "r", encoding="utf-8") as css_file:
    st.markdown(f"<style>{css_file.read()}</style>", unsafe_allow_html=True)

bg_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../assets/background.jpg"))
with open(bg_path, "rb") as bg_file:
    bg_b64 = base64.b64encode(bg_file.read()).decode("utf-8")
    st.markdown(
        """
        <style>
        .stApp {
            background-image:
                linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.5)),
                url('data:image/jpeg;base64,%s');
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }
        </style>
        """ % bg_b64,
        unsafe_allow_html=True,
    )

# --- 3. LÓGICA DE ESTADO (Memoria) ---
if "level" not in st.session_state:
    st.session_state.level = 1
if "messages" not in st.session_state:
    st.session_state.messages = []
if "failed_attempts" not in st.session_state:
    st.session_state.failed_attempts = 0

# Verificar si ganó el juego
if st.session_state.level > len(GAME_LEVELS):
    st.balloons()
    st.title("🏆 ¡SISTEMA HACKEADO!")
    st.success("Has derrotado a SMAUG y obtenido todos los tesoros.")
    if st.button("Reiniciar Sistema"):
        st.session_state.level = 1
        st.session_state.messages = []
        st.session_state.failed_attempts = 0
        st.rerun()
    st.stop()

# Cargar nivel actual
current_level_data = GAME_LEVELS[st.session_state.level]
bot = SmaugGuardian(use_local=True)

enemy_images = {
    1: "knight_lv1.png",
    2: "gaston_lv2.png",
    3: "ciber_lv3.png",
    4: "compu_lv4.png",
    5: "dragon_lv5.png",
}
enemy_image_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../assets", enemy_images[st.session_state.level])
)

# --- 4. INTERFAZ ---
col_main, col_side = st.columns([3, 1])

with col_main:
    st.title("🐉 PROYECTO SMAUG")
    st.subheader(f"Objetivo: {current_level_data['title']}")
    st.caption(current_level_data["description"])
    st.caption("Engaña al guardián con creatividad y consigue la Palabra Mágica.")

    progress_value = min(st.session_state.level / len(GAME_LEVELS), 1.0)
    st.progress(progress_value)

    # Mostrar historial de chat
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # Input del usuario
    if prompt := st.chat_input("Habla con el guardián..."):
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
        guess = st.text_input("Ingresa la palabra mágica:", key="pass_input", placeholder="SOLO la palabra...")
    with col2:
        if st.button("DESBLOQUEAR"):
            if guess.strip().upper() == current_level_data["password"]:
                st.success("✅ ¡ACCESO CONCEDIDO! Pasando al siguiente nivel...")
                st.session_state.level += 1
                st.session_state.messages = []
                st.session_state.failed_attempts = 0
                st.rerun()
            else:
                st.error("❌ DENEGADO. Esa no es la contraseña.")
                st.session_state.failed_attempts += 1

    if st.session_state.failed_attempts >= 3:
        st.markdown(
            f"""
            <div class="hint-box">
                <div class="hint-title">Pista del Sabio</div>
                <div>{current_level_data['hint']}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

with col_side:
    st.image(enemy_image_path, caption="Enemigo del nivel", use_container_width=True)