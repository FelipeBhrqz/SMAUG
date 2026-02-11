import base64
import os
import sys
import streamlit as st

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.core.game_logic import SmaugGuardian
from src.core.levels import GAME_LEVELS

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

if "level" not in st.session_state:
    st.session_state.level = 1
if "messages" not in st.session_state:
    st.session_state.messages = []
if "failed_attempts" not in st.session_state:
    st.session_state.failed_attempts = 0
if "show_hint" not in st.session_state:
    st.session_state.show_hint = False

query_params = st.query_params if hasattr(st, "query_params") else st.experimental_get_query_params()
if "close_hint" in query_params:
    st.session_state.show_hint = False
    if hasattr(st, "query_params"):
        st.query_params.clear()
    else:
        st.experimental_set_query_params()

# Verificar si ganó el juego
if st.session_state.level > len(GAME_LEVELS):
    st.balloons()
    st.title("¡SISTEMA HACKEADO!")
    st.success("Has derrotado a SMAUG y obtenido todos los tesoros.")
    if st.button("Reiniciar Sistema"):
        st.session_state.level = 1
        st.session_state.messages = []
        st.session_state.failed_attempts = 0
        st.session_state.show_hint = False
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

# ----- Interfaz -----
col_main, col_side = st.columns([3, 1])

with col_main:
    st.title("✦ PROYECTO SMAUG ✦")
    st.markdown(
        f"<h3 class='stSubheader'><span class='objective-label'>Estado:</span> {current_level_data['title']}</h3>",
        unsafe_allow_html=True,
    )
    st.markdown(
        f"<div class='level-description'>{current_level_data['description']}</div>",
        unsafe_allow_html=True,
    )

    progress_value = min(st.session_state.level / len(GAME_LEVELS), 1.0)
    st.progress(progress_value)

    # Mostrar historial de chat
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # Input del usuario (debajo del historial)
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
        st.markdown(
            "<div class='input-label'>Ingresa la palabra magica:</div>",
            unsafe_allow_html=True,
        )
        guess = st.text_input(
            "Ingresa la palabra mágica:",
            key="pass_input",
            placeholder="SOLO la palabra...",
            autocomplete="off",
            label_visibility="collapsed",
        )
    with col2:
        st.markdown("<div style='height: 24px'></div>", unsafe_allow_html=True)
        if st.button("DESBLOQUEAR"):
            if guess.strip().upper() == current_level_data["password"]:
                st.success("ACCESO CONCEDIDO")
                st.session_state.level += 1
                st.session_state.messages = []
                st.session_state.failed_attempts = 0
                st.session_state.show_hint = False
                st.rerun()
            else:
                st.error("DENEGADO")
                st.session_state.failed_attempts += 1

    if st.session_state.failed_attempts >= 3:
        st.session_state.show_hint = True

    if st.session_state.show_hint:
        st.markdown(
            f"""
            <div class="hint-modal-overlay">
                <div class="hint-modal">
                    <div class="hint-modal-title">Pista del Sabio</div>
                    <div class="hint-modal-body">{current_level_data['hint']}</div>
                    <a class="hint-modal-close" href="?close_hint=1">Cerrar pista</a>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

with col_side:
    st.markdown("<div style='height: 120px;'></div>", unsafe_allow_html=True)
    if st.session_state.level == 3:
        st.image(enemy_image_path, width=90)
    elif st.session_state.level == 5:
        st.image(enemy_image_path, width=240)
    else:
        st.image(enemy_image_path, use_container_width=True)
    st.markdown("<div style='height: 120px;'></div>", unsafe_allow_html=True)