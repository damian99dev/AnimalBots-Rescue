from settings import *                      # Importa todas las configuraciones desde el archivo settings
import pygame, sys                          # Importa Pygame para el motor del juego y sys para la gestión del sistema
from button import Button                   # Importa la clase Button para todos los botones del menú
from game_class import Game
from options_menu import get_text
import json
import cv2  # Importar OpenCV

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

def play():
    # Pantalla de selección de niveles
    while True:
        # Obtener tamaño de la pantalla
        screen_width, screen_height = pygame.display.get_surface().get_size()
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

   
        
        
          # Establecer fondo del menú de selección de niveles
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
