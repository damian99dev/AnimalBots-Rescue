import pygame
import sys
from button import Button  # Asegúrate de tener la clase Button
from options_menu import get_text
import json
import current_level_config  # Importa el módulo de configuración

# Funciones para cargar y guardar la configuración
music_playing = False                                                   

# Inicializar Pygame y la pantalla
pygame.init()
SCREEN = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)
pygame.display.set_caption("Game Over!")


# Cargar música de Game Over
GAMEOVER_MUSIC = pygame.mixer.Sound("assets/sounds/music/Death is only the beginning.mp3")

# Cargar imágenes y fuentes
BG_IMAGE = pygame.image.load("assets/images/backgrounds/gameover_bgg.jpg")
BG_IMAGE = pygame.transform.scale(BG_IMAGE, (1550, 870))

# Cargar volumen desde la configuración

def get_font(size):                                                 # Función para obtener la fuente con un tamaño específico
    return pygame.font.Font("assets/fonts/font1.otf", size)

def load_languages():
    with open("languages.json", "r", encoding="utf-8") as f:
        return json.load(f)
    
# Clase para la pantalla de Game Over
music_playing = False

class NivelManager:
    niveles = ['prueba.tmx', 'prueba2.tmx', 'prueba3.tmx']
    nivel_actual = niveles[0]  # Nivel inicial

    @classmethod
    def siguiente_nivel(cls):
        # Encuentra el índice actual y establece el siguiente nivel si existe
        nivel_index = cls.niveles.index(cls.nivel_actual)
        if nivel_index < len(cls.niveles) - 1:
            cls.nivel_actual = cls.niveles[nivel_index + 1]
        else:
            cls.nivel_actual = None  # No hay más niveles


class GameOverScreen:
    def __init__(self, screen, font):
        self.screen = screen  # Guardar la pantalla
        self.font = font  # Guardar la fuente como un objeto ya creado

        # Comenzar con un fadeout de la música actual
        pygame.mixer.music.fadeout(5000)  # Fundido de salida de la música actual en 5 segundos
        pygame.mixer.music.pause()  # Pausar la música
    
        pygame.mixer.music.load("assets/sounds/music/Death is only the beginning.mp3")
        pygame.mixer.music.play(-1)


    def run(self):  
        while True: 
            
            LEVEL_MOUSE_POS = pygame.mouse.get_pos()  

            RETRY_BT = Button(image=pygame.image.load("assets/images/ui/GO_retry_bt.PNG"),
                                    pos=(1920 // 2.5, 1080 // 2), 
                                    text_input=get_text("retry"), font=get_font(60), 
                                    base_color="#231f1f", hovering_color="#38bc0f")
            MENU_BT = Button(image=pygame.image.load("assets/images/ui/GO_tabla_menu_bt_.PNG"), 
                                    pos=(1920 // 2.5, 1080 // 2 + 140), 
                                    text_input=get_text("menu"), font=get_font(50), 
                                    base_color="#231f1f", hovering_color="#ffef00")
            EXIT_BT = Button(image=pygame.image.load("assets/images/ui/GO_tabla_exit_bt.PNG"), 
                                    pos=(1920 // 2.5, 1080 // 2 + 250), 
                                    text_input=get_text("exit"), font=get_font(50), 
                                    base_color="#231f1f", hovering_color="#ff0031")


            self.screen.blit(BG_IMAGE, (0, 0))
            mouse_pos = pygame.mouse.get_pos()

        # Crear una nueva fuente solo para el texto "Game Over" con un tamaño más grande
            gameover_font = get_font(120)  # Cambia el tamaño a 120 o al valor que desees

        # Crear texto de Game Over con la nueva fuente
            gameover_text = gameover_font.render(get_text("game_over"), True, "#231f1f")
            gameover_rect = gameover_text.get_rect(center=(1920 // 2.5, 1080 // 4))
            self.screen.blit(gameover_text, gameover_rect)

            # Actualizar botones
            for button in [MENU_BT, RETRY_BT , EXIT_BT]:
                button.changeColor(LEVEL_MOUSE_POS)
                button.update(SCREEN)


            music_playing = False


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if RETRY_BT.checkForInput(LEVEL_MOUSE_POS):
                        from game_class import Game
                        game = Game(current_level_config.current_level)  # Cargar el nivel actual desde config
                        game.run()

                    elif EXIT_BT.checkForInput(LEVEL_MOUSE_POS):
                        pygame.quit()
                        sys.exit()
                    
                    elif MENU_BT.checkForInput(LEVEL_MOUSE_POS):    
                        GAMEOVER_MUSIC.stop()
                        if not music_playing:
                            pygame.mixer.music.load("assets/sounds/music/Main Menu.mp3")
                            pygame.mixer.music.play(-1, fade_ms=3000)
                            music_playing = True
                        from main_menu import main_menu
                        main_menu()



            pygame.display.update()