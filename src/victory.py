import pygame
import sys
from button import Button  # Asegúrate de tener la clase Button
from options_menu import get_text
import json
from game_class import Game
import current_level_config


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
SCREEN = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN) 
pygame.display.set_caption("Hurra!")

# Cargar música de victoria
VICTORY_MUSIC = pygame.mixer.Sound("assets/sounds/music/End and Thanks!.flac")
WINBANJO = pygame.mixer.Sound("assets/sounds/fx/winbanjo.mp3")

# Cargar imágenes y fuentes
BG_IMAGE = pygame.image.load("assets/images/backgrounds/win_bgg.jpg")
BG_IMAGE = pygame.transform.scale(BG_IMAGE, (1550, 870))

def set_volume(sound, volume):                            # Establece el volumen para un sonido
    sound.set_volume(volume)

# Cargar volumen desde la configuración
config = load_config()  # Cargar el volumen guardado
set_volume(VICTORY_MUSIC, config["music_volume"])  # Establecer volumen de música de victoria
set_volume(WINBANJO, config["music_volume"])  # Establecer volumen de WINBANJO

def get_font(size):                                                 # Función para obtener la fuente con un tamaño específico
    return pygame.font.Font("assets/fonts/font1.otf", size)

def load_languages():
    with open("languages.json", "r", encoding="utf-8") as f:
        return json.load(f)
    
class NivelManager:
    niveles = ['prueba.tmx', 'prueba2.tmx', 'prueba3.tmx']
    nivel_actual = current_level_config.load_current_level()  # Nivel inicial

    @classmethod
    def siguiente_nivel(cls):
        # Encuentra el índice actual y establece el siguiente nivel si existe
        nivel_index = cls.niveles.index(cls.nivel_actual)
        if nivel_index < len(cls.niveles) - 1:
            cls.nivel_actual = cls.niveles[nivel_index + 1]
        else:
            cls.nivel_actual = None  # No hay más niveles

class VictoryScreen:
    def __init__(self):
        # Comenzar con un fadeout de la música actual
        
        pygame.mixer.music.fadeout(1000)  # Fundido de salida de la música actual en 8 segundos
        pygame.mixer.music.pause()  # Pausar la música
        # Control de sonido
        self.sound_stage = 0  # Etapa inicial de la reproducción de sonidos
        self.sound_timer = pygame.time.get_ticks()  # Guardar el tiempo actual
        self.sound_duration = WINBANJO.get_length() * 1000  # Duración de WINBANJO en milisegundos

        # Empezar con el sonido WINBANJO
        pygame.mixer.music.load("assets/sounds/fx/winbanjo.mp3")
        pygame.mixer.music.play()
        

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

            # Controlar la secuencia de los sonidos
            self.play_next_sound()
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
                        # Llama a la clase de gestión de niveles
                        NivelManager.siguiente_nivel()
                        if NivelManager.nivel_actual:
                            VICTORY_MUSIC.stop()
                            current_level_config.current_level = NivelManager.nivel_actual
                            current_level_config.save_current_level(current_level_config.current_level)
                            game = Game(NivelManager.nivel_actual)
                            game.run()

                        else:
                            # No hay más niveles, regresa al menú
                            VICTORY_MUSIC.stop()
                            if not music_playing:
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
                        if not music_playing:
                            pygame.mixer.music.load("assets/sounds/music/Main Menu.mp3")
                            pygame.mixer.music.play(-1, fade_ms=3000)
                            music_playing = True
                        from main_menu import main_menu
                        main_menu()

            pygame.display.update()


    def play_next_sound(self):
        current_time = pygame.time.get_ticks()

        # Si WINBANJO ha terminado, reproduce la música de victoria
        if self.sound_stage == 0 and current_time - self.sound_timer >= self.sound_duration:
            VICTORY_MUSIC.play(-1, fade_ms=3000)  # Reproduce la música de victoria en bucle
            self.sound_stage = 1  # Cambia el estado para evitar repetir la música



# Para probar la pantalla de victoria
if __name__ == "__main__":
    victory_screen = VictoryScreen()
    victory_screen.run()