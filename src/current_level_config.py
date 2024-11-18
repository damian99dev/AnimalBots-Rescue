# config.py
import json

# Ruta del archivo JSON donde se guardará el nivel actual
CONFIG_FILE = 'current_level_config.json'

# Cargar el nivel actual desde el archivo JSON
def load_current_level():
    try:
        with open(CONFIG_FILE, 'r') as file:
            data = json.load(file)
            return data.get("current_level")  # Valor predeterminado si no existe en JSON
    except (FileNotFoundError, json.JSONDecodeError):
        return "prueba.tmx"  # Nivel inicial si el archivo no existe o está vacío

# Guardar el nivel actual en el archivo JSON
def save_current_level(level):
    with open(CONFIG_FILE, 'w') as file:
        json.dump({"current_level": level}, file)

# Al iniciar, cargamos el nivel actual desde el archivo JSON
current_level = load_current_level()
