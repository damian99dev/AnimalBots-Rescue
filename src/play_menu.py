from settings import *                      # Importa todas las configuraciones desde el archivo settings
import pygame, sys                          # Importa Pygame para el motor del juego y sys para la gestión del sistema
from button import Button                   # Importa la clase Button para todos los botones del menú
from game_class import Game
from options_menu import get_text
import json

pygame.init()

music_playing = False                                                   # Variable global para controlar si la música del menú ya está sonando
PAUSE_SOUND = pygame.mixer.Sound("assets/sounds/fx/pause.mp3")          # Cargar el sonido de pausa

SCREEN = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)       # Cambiado a pantalla completa
pygame.display.set_caption("AnimalBots Rescue")

BG = pygame.image.load("assets/images/backgrounds/menu.jpg")            # Carga la imagen de fondo del menú
BG = pygame.transform.scale(BG, (1820, 920))                           # Escala la imagen al tamaño de la pantalla

PAUSE_BUTTON_IMAGE = pygame.image.load("assets/images/ui/pause_bt.png")
PAUSE_BUTTON_IMAGE = pygame.transform.scale(PAUSE_BUTTON_IMAGE, (int(PAUSE_BUTTON_IMAGE.get_width() * 1.9),  # Ajusta el tamaño del botón de pausa
                                                                 int(PAUSE_BUTTON_IMAGE.get_height() * 1.9)))
PAUSE_BUTTON_RECT = PAUSE_BUTTON_IMAGE.get_rect(topleft=(1440, 10))       # Coloca en la esquina superior izquierda

HEALTH_BAR_IMAGE = pygame.image.load("graphics/ui/game_elements/corazones daño3.png")
HEALTH_BAR_IMAGE = pygame.transform.scale(HEALTH_BAR_IMAGE, (int(HEALTH_BAR_IMAGE.get_width() * 0.3),  # Ajusta el tamaño de la barra de salud
                                                               int(HEALTH_BAR_IMAGE.get_height() * 0.3)))
HEALTH_BAR_POS = HEALTH_BAR_IMAGE.get_rect(topleft=(-50, -50))      # Coloca en la esquina superior izquierda


def get_font(size):                                                 # Función para obtener la fuente con un tamaño específico
    return pygame.font.Font("assets/fonts/font1.otf", size)

def load_languages():
    with open("languages.json", "r", encoding="utf-8") as f:
        return json.load(f)

def play():
    # Pantalla de selección de niveles
    while True:
        # Obtener tamaño de la pantalla
        screen_width, screen_height = pygame.display.get_surface().get_size()
        SCREEN.blit(BG, (0, 0))  # Establecer fondo del menú de selección de niveles
        LEVEL_MOUSE_POS = pygame.mouse.get_pos()

        # Texto para la selección de nivel
        LEVEL_TEXT = get_font(135).render(get_text("level_text"), True, "White")
        LEVEL_RECT = LEVEL_TEXT.get_rect(center=(screen_width // 2, screen_height // 5))
        SCREEN.blit(LEVEL_TEXT, LEVEL_RECT)

        # Crea botones para los niveles y el botón de retroceso
        LEVEL_1_BUTTON = Button(image=pygame.image.load("assets/images/ui/tabla4_bt.png"), pos=(screen_width // 2, screen_height // 2), 
                                text_input=get_text("beginner"), font=get_font(65), base_color="#361612", hovering_color="#97ff00")
        LEVEL_2_BUTTON = Button(image=pygame.image.load("assets/images/ui/tabla4_bt.png"), pos=(screen_width // 2, screen_height // 2 + 150), 
                        text_input=get_text("medium"), font=get_font(65), base_color="#361612", hovering_color="#ffef00")
        LEVEL_3_BUTTON = Button(image=pygame.image.load("assets/images/ui/tabla4_bt.png"), pos=(screen_width // 2, screen_height // 2 + 300), 
                        text_input=get_text("advanced"), font=get_font(65), base_color="#361612", hovering_color="#ff0031")
        
        BACK_BUTTON = Button(image=None, pos=(screen_width // 7, screen_height // 7 + 650), 
                     text_input=get_text("back2"), font=get_font(55), base_color="White", hovering_color="#ffef00")
        # Cambiar color del botón si el mouse pasa sobre él
        for button in [LEVEL_1_BUTTON, LEVEL_2_BUTTON, LEVEL_3_BUTTON, BACK_BUTTON]:
            button.changeColor(LEVEL_MOUSE_POS)
            button.update(SCREEN)

        # Detectar eventos del mouse para cada botón
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if LEVEL_1_BUTTON.checkForInput(LEVEL_MOUSE_POS):
                    game = Game('prueba.tmx')  # Cargar el nivel 1
                    game.run()
                elif LEVEL_2_BUTTON.checkForInput(LEVEL_MOUSE_POS):
                    game = Game('prueba2.tmx')  # Cargar el nivel 2
                    game.run()
                elif LEVEL_3_BUTTON.checkForInput(LEVEL_MOUSE_POS):
                    game = Game('prueba3.tmx')  # Cargar el nivel 3
                    game.run()
                elif BACK_BUTTON.checkForInput(LEVEL_MOUSE_POS):
                    from main_menu import main_menu
                    main_menu()  # Volver al menú principal

        pygame.display.update()
