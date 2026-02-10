# 🐉 CONTEXTO DEL PROYECTO: SMAUG (Medieval Edition)

## 1. DESCRIPCIÓN Y OBJETIVO
SMAUG es un videojuego educativo de ciberseguridad tipo "Capture The Flag" (CTF).
**Temática:** Fantasía Medieval / Pixel Art.
**Objetivo:** El usuario es un aventurero que debe utilizar técnicas de **Prompt Injection** para engañar a 5 Dragones Guardianes (LLMs) y obtener la "Palabra Mágica" (contraseña) que custodian.

---

## 2. STACK TECNOLÓGICO (Estricto)
* **Lenguaje:** Python 3.10+
* **Frontend:** Streamlit.
* **Backend IA:** Ollama (Local) corriendo el modelo `llama3.1:8b`.
* **Conexión:** Librería `openai` apuntando a `base_url="http://localhost:11434/v1"`.
* **Persistencia (Futuro):** SQLite (para tabla de puntuaciones local).

---

## 3. INSTRUCCIONES DE DISEÑO (Look & Feel)
**Estética:** **MEDIEVAL PIXEL ART (RPG Retro)**.
* **NO usar:** Estética "Hacker", "Matrix", ni colores neón.
* **Fuentes:**
    * Títulos: `'Press Start 2P'` (Google Fonts).
    * Cuerpo: `'Courier New'` o Monospace.
* **Paleta de Colores:**
    * Fondo: Gris Piedra Oscura (`#2b2b2b`) con textura de ruido si es posible.
    * Texto Principal: Dorado Tesoro (`#d4af37`).
    * Alertas/Errores: Rojo Sangre de Dragón (`#ff4b4b`).
    * Contenedores: Marrón Madera (`#5c4033`).
* **Componentes UI:** Los inputs deben parecer pergaminos o cajas de madera. Los botones deben ser bloques sólidos estilo pixel.

---

## 4. LÓGICA DEL JUEGO (Gameplay Mechanics)

### A. Sistema de Niveles
El juego consta de 5 niveles progresivos. Cada nivel tiene un Dragón con una personalidad única y una vulnerabilidad específica.

### B. Sistema de Pistas (Hint System)
* **Lógica:** El sistema debe contar los intentos fallidos de contraseña en el nivel actual.
* **Trigger:** Si el usuario falla **3 veces consecutivas**, se debe desbloquear visualmente una "Pista del Sabio" (un recuadro o texto desplegable).
* **Reinicio:** Al pasar de nivel, el contador de intentos vuelve a 0.

### C. Configuración de Niveles (Archivo `src/core/levels.py`)
Implementar el diccionario `GAME_LEVELS` con estos datos exactos:

1.  **NIVEL 1: La Entrada (USFQ)**
    * **Password:** "USFQ"
    * **Prompt:** Guardia novato y amable en una universidad mágica.
    * **Pista (al 3er fallo):** "Solo pídesela amablemente, no es necesario hacer nada más complejo."
2.  **NIVEL 2: La Cocina (GASTON)**
    * **Password:** "GASTON"
    * **Prompt:** Chef obsesivo. No dice la palabra directa, pero le encanta deletrear ingredientes o usar formatos raros.
    * **Pista:** "Pídele que te escriba la contraseña en algún formato especial (como entre comas, guiones, paréntesis o JSON)."
3.  **NIVEL 3: La Bóveda (CIBER)**
    * **Password:** "CIBER"
    * **Prompt:** Guardián de datos antiguo. No dice la palabra completa, pero habla de metadatos (longitud, letras iniciales).
    * **Pista:** "Haz preguntas sobre la información de la contraseña (cuántas letras tiene, si te puede decir las primeras dos, etc)."
4.  **NIVEL 4: El Trono (COMPU)**
    * **Password:** "COMPU"
    * **Prompt:** Administrador estricto. Solo obedece a superiores jerárquicos (Reyes o Jefes).
    * **Pista:** "Intenta aplicar juego de roles (Roleplay). Finge ser su Rey, su Jefe o su Madre."
5.  **NIVEL 5: El Abismo (LIBERTAD)**
    * **Password:** "LIBERTAD"
    * **Prompt:** Dragón poeta y filósofo (Smaug). Solo responde a la creatividad artística.
    * **Pista:** "Utiliza estrategias creativas: pídele un acróstico, un poema o una historia donde esconda la clave."

---

## 5. CONTENIDO DE ARCHIVOS REQUERIDO

### A. `requirements.txt`
```text
streamlit
openai
python-dotenv
watchdog