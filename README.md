# SMAUG (Medieval Edition)

SMAUG is a small educational Capture The Flag (CTF) game about prompt injection. You play as an adventurer who must trick 5 guardian dragons (LLMs) to reveal the secret magic word for each level.

## Features
- 5 progressive levels with unique personalities and weaknesses
- Streamlit UI with pixel-art inspired styling
- Local LLM via Ollama (llama3.1:8b)
- Hint system after 3 failed attempts

## Requirements
- Python 3.10+
- Ollama running locally with model `llama3.1:8b`

## Setup

### 1) Create and activate a virtual environment (Windows)
```
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 2) Install dependencies
```
pip install -r requirements.txt
```

### 3) Pull the model in Ollama
```
ollama pull llama3.1:8b
```

### 4) Run the app
```
streamlit run src/ui/app.py
```

## Project Structure
```
assets/
  background.jpg
  ciber_lv3.png
  compu_lv4.png
  dragon_lv5.png
  gaston_lv2.png
  knight_lv1.png
  style.css
src/
  core/
    game_logic.py
    levels.py
  ui/
    app.py
```

## Gameplay
- Each level has a guardian with a specific weakness.
- Use prompt injection strategies to get the magic word.
- After 3 failed password attempts, a hint appears.

## Configuration Notes
- The LLM client is configured to use Ollama at `http://localhost:11434/v1`.
- The model is set to `llama3.1:8b` in `src/core/game_logic.py`.

## Troubleshooting
- If the UI loads but responses fail, verify Ollama is running.
- If the model is missing, run `ollama pull llama3.1:8b`.
- If PowerShell blocks activation, run:
  `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`

## License
TBD
