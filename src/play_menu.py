from settings import *                      # Importa todas las configuraciones desde el archivo settings
import pygame, sys                          # Importa Pygame para el motor del juego y sys para la gestión del sistema
from button import Button                   # Importa la clase Button para todos los botones del menú
from game_class import Game
from options_menu import get_text
import json
import cv2 
import current_level_config
from victory import NivelManager
                                 # Importar OpenCV  # Importar el módulo de configuración

pygame.init()

video_path = "assets/images/backgrounds/menu.mp4"   # Carga el video con OpenCV
cap = cv2.VideoCapture(video_path)

music_playing = False  

current_level = 'prueba.tmx'

                                      # Variable global para controlar si la música del menú ya está sonando

SCREEN = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)       # Cambiado a pantalla completa
pygame.display.set_caption("AnimalBots Rescue")

def get_font(size):                                                 # Función para obtener la fuente con un tamaño específico
    return pygame.font.Font("assets/fonts/font1.otf", size)

def load_languages():
    with open("languages.json", "r", encoding="utf-8") as f:
        return json.load(f)

def play():
    while True:  # Pantalla de selección de niveles

        screen_width, screen_height = pygame.display.get_surface().get_size()  # Obtener tamaño de la pantalla 
        ret, frame = cap.read()
        if not ret:  # Si el video ha terminado, reinícialo
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            ret, frame = cap.read()

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convierte el frame de BGR (formato de OpenCV) a RGB (formato de Pygame)
        frame = cv2.resize(frame, (1820, 920))  # Ajusta el tamaño del frame a la resolución de la pantalla completa
        frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)  # Rota el video 90 grados.
        frame_surface = pygame.surfarray.make_surface(frame)  # Convierte el frame en una superficie de Pygame y dibújalo en la pantalla
        SCREEN.blit(frame_surface, (0, 0))

        LEVEL_MOUSE_POS = pygame.mouse.get_pos()

        LEVEL_TEXT = get_font(135).render(get_text("level_text"), True, "White")  # Texto para la selección de nivel
        LEVEL_RECT = LEVEL_TEXT.get_rect(center=(screen_width // 2, screen_height // 5))
        SCREEN.blit(LEVEL_TEXT, LEVEL_RECT)

        # Crea botones para los niveles y el botón de retroceso en forma de zigzag
        LEVEL_1_BUTTON = Button(image=pygame.image.load("assets/images/ui/tabla4_bt.png"), pos=(screen_width // 4 - 170, screen_height // 2 - 100 + 100), 
                                text_input=get_text("1-1"), font=get_font(40), base_color="#361612", hovering_color="#38bc0f")
        LEVEL_2_BUTTON = Button(image=pygame.image.load("assets/images/ui/tabla4_bt.png"), pos=(screen_width // 4 + 50, screen_height // 2 + 100 + 100), 
                                text_input=get_text("1-2"), font=get_font(40), base_color="#361612", hovering_color="#ffef00")
        LEVEL_3_BUTTON = Button(image=pygame.image.load("assets/images/ui/tabla4_bt.png"), pos=(screen_width // 2 - 120, screen_height // 2 - 100 + 100), 
                                text_input=get_text("2-1"), font=get_font(40), base_color="#361612", hovering_color="#ff0031")
        LEVEL_4_BUTTON = Button(image=pygame.image.load("assets/images/ui/tabla4_bt.png"), pos=(screen_width // 2 + 70, screen_height // 2 + 100 + 100), 
                                text_input=get_text("2-2"), font=get_font(40), base_color="#361612", hovering_color="#38bc0f")
        LEVEL_5_BUTTON = Button(image=pygame.image.load("assets/images/ui/tabla4_bt.png"), pos=(3 * screen_width // 4 - 90, screen_height // 2 - 100 + 100), 
                                text_input=get_text("3-1"), font=get_font(40), base_color="#361612", hovering_color="#ffef00")
        LEVEL_6_BUTTON = Button(image=pygame.image.load("assets/images/ui/tabla4_bt.png"), pos=(3 * screen_width // 4 + 150, screen_height // 2 + 100 + 100), 
                                text_input=get_text("3-2"), font=get_font(40), base_color="#361612", hovering_color="#ff0031")

        BACK_BUTTON = Button(image=None, pos=(screen_width // 7, screen_height // 7 + 650), 
                             text_input=get_text("back2"), font=get_font(55), base_color="White", hovering_color="#ffef00")

        for button in [LEVEL_1_BUTTON, LEVEL_2_BUTTON, LEVEL_3_BUTTON, LEVEL_4_BUTTON, LEVEL_5_BUTTON, LEVEL_6_BUTTON, BACK_BUTTON]:
            button.changeColor(LEVEL_MOUSE_POS)
            button.update(SCREEN)

        # Detectar eventos del mouse para cada botón
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if LEVEL_1_BUTTON.checkForInput(LEVEL_MOUSE_POS):
                    NivelManager.nivel_actual = 'prueba.tmx'
                    current_level_config.current_level = NivelManager.nivel_actual
                    current_level_config.save_current_level(current_level_config.current_level)  # Guardar el nivel actual
                    game = Game(current_level_config.current_level)  # Cargar el nivel 1
                    game.run()
                elif LEVEL_2_BUTTON.checkForInput(LEVEL_MOUSE_POS):
                    NivelManager.nivel_actual = 'prueba1-2.tmx'
                    current_level_config.current_level = NivelManager.nivel_actual
                    current_level_config.save_current_level(current_level_config.current_level)  # Guardar el nivel actual
                    game = Game(current_level_config.current_level)  # Cargar el nivel 2
                    game.run()
                elif LEVEL_3_BUTTON.checkForInput(LEVEL_MOUSE_POS):
                    NivelManager.nivel_actual = 'prueba2.tmx'
                    current_level_config.current_level = NivelManager.nivel_actual
                    current_level_config.save_current_level(current_level_config.current_level)  # Guardar el nivel actual
                    game = Game(current_level_config.current_level)  # Cargar el nivel 3
                    game.run()
                elif LEVEL_4_BUTTON.checkForInput(LEVEL_MOUSE_POS):
                    NivelManager.nivel_actual = 'prueba2-2.tmx'
                    current_level_config.current_level = NivelManager.nivel_actual
                    current_level_config.save_current_level(current_level_config.current_level)  # Guardar el nivel actual
                    game = Game(current_level_config.current_level)  # Cargar el nivel 4
                    game.run()
                elif LEVEL_5_BUTTON.checkForInput(LEVEL_MOUSE_POS):
                    NivelManager.nivel_actual = 'prueba3.tmx'
                    current_level_config.current_level = NivelManager.nivel_actual
                    current_level_config.save_current_level(current_level_config.current_level)  # Guardar el nivel actual
                    game = Game(current_level_config.current_level)  # Cargar el nivel 5
                    game.run()
                elif LEVEL_6_BUTTON.checkForInput(LEVEL_MOUSE_POS):
                    NivelManager.nivel_actual = 'prueba3-2.tmx'
                    current_level_config.current_level = NivelManager.nivel_actual
                    current_level_config.save_current_level(current_level_config.current_level)  # Guardar el nivel actual
                    game = Game(current_level_config.current_level)  # Cargar el nivel 6
                    game.run()
                elif BACK_BUTTON.checkForInput(LEVEL_MOUSE_POS):
                    from main_menu import main_menu
                    main_menu()  # Volver al menú principal

        pygame.display.update()