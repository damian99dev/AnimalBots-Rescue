import pygame
import sys
from button import Button  # Asegúrate de tener la clase Button
from options_menu import get_text
import json
from game_class import Game
import current_level_config
import cv2
video_path = "assets/images/backgrounds/play_menu.mp4"   # Carga el video con OpenCV
cap = cv2.VideoCapture(video_path)
from moviepy import VideoFileClip

def load_config():    # Cargar la configuración
    try:
        with open('config_music.json', 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"music_volume": 0.5}  # Valores predeterminados

def save_config(music_volume):  # Elimina effects_volume
    with open('config.json', 'w') as f:
        json.dump({"music_volume": music_volume}, f)

# Inicializamos Pygame y la pantalla
pygame.init()

VICTORY_MUSIC = pygame.mixer.Sound("assets/sounds/music/End and Thanks!.flac")
SCREEN = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN) 
pygame.display.set_caption("Hurra!")

# Cargar música de victoria
WINBANJO = pygame.mixer.Sound("assets/sounds/music/Dating Start!.mp3")

# Cargar imágenes y fuentes
BG_IMAGE = pygame.image.load("assets/images/backgrounds/win_bgg.jpg")
BG_IMAGE = pygame.transform.scale(BG_IMAGE, (1550, 870))

def set_volume(sound, volume):                            # Establece el volumen para un sonido
    sound.set_volume(volume)

# Cargar volumen desde la configuración
config = load_config()  # Cargar el volumen guardado
set_volume(WINBANJO, config["music_volume"])  # Establecer volumen de WINBANJO
set_volume(VICTORY_MUSIC, config["music_volume"])  # Establecer volumen de música 

def get_font(size):                                                 # Función para obtener la fuente con un tamaño específico
    return pygame.font.Font("assets/fonts/font1.otf", size)

def load_languages():
    with open("languages.json", "r", encoding="utf-8") as f:
        return json.load(f)
    
class NivelManager:
    niveles = ['None', 'prueba.tmx', 'prueba1-2.tmx', 'prueba2.tmx', 'prueba2-2.tmx', 'prueba3.tmx', 'prueba3-2.tmx' ]
    nivel_actual = current_level_config.load_current_level()  # Nivel inicial

    @classmethod
    def siguiente_nivel(cls):
        # Encuentra el índice actual y establece el siguiente nivel si existe
        nivel_index = cls.niveles.index(cls.nivel_actual)
        if nivel_index < len(cls.niveles) - 1:
            cls.nivel_actual = cls.niveles[nivel_index + 1]
        else:
            cls.nivel_actual = None  # No hay más niveles



def play_video(video_path):
    video_clip = VideoFileClip(video_path)
    audio = video_clip.audio
    audio.write_audiofile("temp_audio.mp3")
    fps = video_clip.fps

    pygame.mixer.init()
    pygame.mixer.music.load("temp_audio.mp3")
    pygame.mixer.music.play()

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: No se pudo cargar el video.")
        return

    clock = pygame.time.Clock()

    while True:
        ret, frame = cap.read()
        if not ret:  # Si el video ha terminado, salir del bucle
            break

        frame = cv2.flip(frame, 1)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (1540, 870))
        frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
        frame_surface = pygame.surfarray.make_surface(frame)

        # Dibuja el frame en la pantalla
        SCREEN.blit(frame_surface, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                cap.release()
                pygame.mixer.music.stop()
                pygame.quit()
                sys.exit()

        pygame.display.update()
        clock.tick(fps)

    cap.release()
    pygame.mixer.music.stop()




class VictoryScreen:
    def __init__(self):
        # Comenzar con un fadeout de la música actual
        
        pygame.mixer.music.fadeout(1000)  # Fundido de salida de la música actual en 8 segundos
        pygame.mixer.music.pause()  # Pausar la música
        pygame.mixer.music.load("assets/sounds/music/Dating Start!.mp3")
        pygame.mixer.music.play(-1)
        # Control de sonido
        self.sound_stage = 0  # Etapa inicial de la reproducción de sonidos
        self.sound_timer = pygame.time.get_ticks()  # Guardar el tiempo actual
        self.sound_duration = WINBANJO.get_length() * 1000  # Duración de WINBANJO en milisegundos

        

    def run(self):
        while True:
    

            LEVEL_MOUSE_POS = pygame.mouse.get_pos()  

            NEXT_BT = Button(image=pygame.image.load("assets/images/ui/next_bt.png"),
                                    pos=(1920 // 2.5, 1080 // 2), 
                                    text_input=get_text("next"), font=get_font(60), 
                                    base_color="#361612", hovering_color="#38bc0f")
            MENU_BT = Button(image=pygame.image.load("assets/images/ui/tabla_menu_bt.png"), 
                                    pos=(1920 // 2.5, 1080 // 2 + 140), 
                                    text_input=get_text("menu"), font=get_font(50), 
                                    base_color="#361612", hovering_color="#ffef00")
            EXIT_BT = Button(image=pygame.image.load("assets/images/ui/tabla_exit_bt.png"), 
                                    pos=(1920 // 2.5, 1080 // 2 + 250), 
                                    text_input=get_text("exit"), font=get_font(50), 
                                    base_color="#361612", hovering_color="#ff0031")


            SCREEN.blit(BG_IMAGE, (0, 0))
            mouse_pos = pygame.mouse.get_pos()

            # Crear texto de victoria
            victory_text = get_font(120).render(get_text("victory"), True, "White")
            victory_rect = victory_text.get_rect(center=(1920 // 2.5, 1080 // 4))
            SCREEN.blit(victory_text, victory_rect)

            # Actualizar botones
            for button in [MENU_BT, NEXT_BT , EXIT_BT]:
                button.changeColor(LEVEL_MOUSE_POS)
                button.update(SCREEN)

            # Lista de niveles en orden
            
            # Variables
            music_playing = False

# Ahora, en tu código principal
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if NEXT_BT.checkForInput(LEVEL_MOUSE_POS):
                        VICTORY_MUSIC.stop()
                        NivelManager.siguiente_nivel()
                        if NivelManager.nivel_actual:
                            # Detener música de victoria
                            pygame.mixer.music.stop()

                            # Determinar la canción del siguiente nivel
                            if NivelManager.nivel_actual == 'prueba.tmx':
                                pygame.mixer.music.load("assets/sounds/music/Hypertext.mp3")
                            elif NivelManager.nivel_actual == 'prueba1-2.tmx':
                                pygame.mixer.music.load("assets/sounds/music/Deal 'Em Out.mp3")
                            elif NivelManager.nivel_actual == 'prueba2.tmx':
                                pygame.mixer.music.load("assets/sounds/music/Waterfall.mp3")
                            elif NivelManager.nivel_actual == 'prueba2-2.tmx':
                                pygame.mixer.music.load("assets/sounds/music/Ruins.mp3")
                            elif NivelManager.nivel_actual == 'prueba3.tmx':
                                pygame.mixer.music.load("assets/sounds/music/Another Medium.mp3")
                            elif NivelManager.nivel_actual == 'prueba3-2.tmx':
                                pygame.mixer.music.load("assets/sounds/music/CORE.mp3")

                            # Reproducir la canción del nivel
                            pygame.mixer.music.play(-1)

                            # Actualizar nivel actual y guardar configuración
                            current_level_config.current_level = NivelManager.nivel_actual
                            current_level_config.save_current_level(current_level_config.current_level)

                            # Iniciar el juego con el nuevo nivel
                            game = Game(NivelManager.nivel_actual)
                            game.run()
                        else:
                            # No hay más niveles, regresa al menú
                            if not music_playing:
                                
                                play_video("assets/images/backgrounds/end.mp4")
                                pygame.mixer.music.load("assets/sounds/music/Main Menu.mp3")
                                pygame.mixer.music.play(-1, fade_ms=3000)
                                music_playing = True
                            from main_menu import main_menu
                            main_menu()

                    elif EXIT_BT.checkForInput(LEVEL_MOUSE_POS):
                        pygame.quit()
                        sys.exit()
                    
                    elif MENU_BT.checkForInput(LEVEL_MOUSE_POS):
                        VICTORY_MUSIC.stop()
                        
                        # Regresar al menú principal
                        if not music_playing:
                            pygame.mixer.music.load("assets/sounds/music/Main Menu.mp3")
                            pygame.mixer.music.play(-1, fade_ms=3000)
                            music_playing = True
                        from main_menu import main_menu
                        main_menu()

            pygame.display.update()





# Para probar la pantalla de victoria
if __name__ == "__main__":
    victory_screen = VictoryScreen()
    victory_screen.run()