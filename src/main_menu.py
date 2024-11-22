import pygame, sys                  # Importa Pygame para el motor del juego y sys para la gestión del sistema
from button import Button           # Importa la clase Button para todos los botones del menú
from options_menu import get_text
import json                         # 
import cv2                          # Importar OpenCV

pygame.init() 

video_path = "assets/images/backgrounds/menu.mp4"   # Carga el video con OpenCV
cap = cv2.VideoCapture(video_path)

music_playing = False                                                   # Variable global para controlar si la música del menú ya está sonando

SCREEN = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)       # Cambiado a pantalla completa
pygame.display.set_caption("AnimalBots Rescue")

def get_font(size):                                                 # Función para obtener la fuente con un tamaño específico
    return pygame.font.Font("assets/fonts/font1.otf", size)

def load_languages():
    with open("languages.json", "r", encoding="utf-8") as f:
        return json.load(f)
def load_config():
    try:
        with open('config.json', 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"music_volume": 0.5}  # Valores predeterminados

def save_config(music_volume):
    with open('config.json', 'w') as f:
        json.dump({"music_volume": music_volume}, f)

MAIN_MUSIC = pygame.mixer.Sound("assets/sounds/music/Main Menu.mp3")
def set_volume(sound, volume):
    sound.set_volume(volume)

# Cargar volumen desde la configuración
config = load_config()  # Cargar el volumen guardado
set_volume(MAIN_MUSIC, config["music_volume"])  # Establecer volumen de música de Game Over

def main_menu():
    global music_playing
    
    # Reproducir la música del menú principal solo una vez al inicio
    if not music_playing:
        pygame.mixer.music.load("assets/sounds/music/Main Menu.mp3")
        pygame.mixer.music.play(-1, fade_ms=3000) 
        music_playing = True

    # Obtener tamaño de la pantalla
    screen_width, screen_height = pygame.display.get_surface().get_size()

    # Cargar la imagen "AMF CORP"!!  
    amf_corp_image = pygame.image.load("assets/images/ui/logo1.png").convert_alpha()
    amf_corp_image = pygame.transform.scale(amf_corp_image, (220, 220))

    amf_corp_width, amf_corp_height = amf_corp_image.get_size()

    # Crea una fuente
    beta_font = get_font(30) 
    beta_text = beta_font.render("VERSION 3.1.0", True, (255, 255, 255)) 
    beta_text_rect = beta_text.get_rect(topleft=(10, screen_height - 40))

    # Menú principal
    
    while True:
        ret, frame = cap.read()
        if not ret:  # Si el video ha terminado, reinícialo
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            ret, frame = cap.read()

        # Convierte el frame de BGR (formato de OpenCV) a RGB (formato de Pygame)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Ajusta el tamaño del frame a la resolución de la pantalla completa
        frame = cv2.resize(frame, (1820, 920))  # resolución de pantalla 
        frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)

        # Convierte el frame en una superficie de Pygame y dibújalo en la pantalla
        frame_surface = pygame.surfarray.make_surface(frame)
        SCREEN.blit(frame_surface, (0, 0))


        MENU_MOUSE_POS = pygame.mouse.get_pos()

        # Texto del título del menú
        MENU_TITLE_BT = Button(image=pygame.image.load("assets/images/ui/menu_title_bt.png"), pos=(screen_width // 2 , screen_height // 4), 
                            text_input="", font=get_font(105), base_color="#d7fcd4", hovering_color="Cyan")

        # Crear botones del menú principal
        PLAY_BUTTON = Button(image=pygame.image.load("assets/images/ui/play_bt.png"), pos=(screen_width // 2 + 25, screen_height // 1.7), 
                        text_input=get_text("play"), font=get_font(80), base_color="#361612", hovering_color="#38bc0f")

        OPTIONS_BUTTON = Button(image=pygame.image.load("assets/images/ui/tabla_options_bt.png"), pos=(screen_width // 2 + 22, screen_height // 2 + 230), 
                            text_input=get_text("options"), font=get_font(57), base_color="#361612", hovering_color="white")
    
        QUIT_BUTTON = Button(image=pygame.image.load("assets/images/ui/tabla_exit_bt.png"), pos=(screen_width // 2 + 20, screen_height // 2 + 350), 
                         text_input=get_text("exit"), font=get_font(57), base_color="#361612", hovering_color="#ff0031")

        # Dibujar la imagen "AMF CORP" en la esquina inferior derecha
        SCREEN.blit(amf_corp_image, (screen_width - amf_corp_width, screen_height - 188))  # Ajustar para esquina inferior derecha

        # Dibujar el texto "Beta 1.1.6" en la esquina inferior izquierda
        SCREEN.blit(beta_text, beta_text_rect)

        MENU_TITLE_BT.update(SCREEN)

        # Cambiar color de los botones al pasar el mouse
        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        # Detectar eventos para cada botón
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    from play_menu import play
                    play()  # Inicia la pantalla de selección de niveles
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    from options_menu import options
                    options()  # Inicia la pantalla de opciones
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()