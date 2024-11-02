from settings import *                      # Importa todas las configuraciones desde el archivo settings
from level import Level                     # Importa la clase Level para manejar los niveles del juego
from pytmx.util_pygame import load_pygame   # Carga los mapas .tmx con soporte para Pygame
from pathlib import Path                    # Manejo de rutas de archivos de manera flexible
import pygame, sys                          # Importa Pygame para el motor del juego y sys para la gestión del sistema
from button import Button                   # Importa la clase Button para todos los botones del menú
from game_over import GameOverScreen
from options_menu import get_text
import json


pygame.init()

music_playing = False                                                   # Variable global para controlar si la música del menú ya está sonando
PAUSE_SOUND = pygame.mixer.Sound("assets/sounds/fx/pause.mp3")          # Cargar el sonido de pausa

SCREEN = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)       # Cambiado a pantalla completa
pygame.display.set_caption("AnimalBots Rescue")

BG = pygame.image.load("assets/images/backgrounds/menu.jpg")            # Carga la imagen de fondo del menú
BG = pygame.transform.scale(BG, (1820, 920))                            # Escala la imagen al tamaño de la pantalla

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
    amf_corp_image = pygame.image.load("assets/images/ui/AMF CORP.png").convert_alpha()
    amf_corp_width, amf_corp_height = amf_corp_image.get_size()

    # Crea una fuente
    beta_font = get_font(30) 
    beta_text = beta_font.render("VERSION 2.1.0", True, (255, 255, 255)) 
    beta_text_rect = beta_text.get_rect(topleft=(10, screen_height - 40))
    # Menú principal
    while True:
        SCREEN.blit(BG, (0, 0))  # Establecer fondo del menú
        MENU_MOUSE_POS = pygame.mouse.get_pos()

        # Texto del título del menú
        MENU_TITLE_BT = Button(image=pygame.image.load("assets/images/ui/menu_title_bt.png"), pos=(screen_width // 2 , screen_height // 4), 
                            text_input="", font=get_font(105), base_color="#d7fcd4", hovering_color="Cyan")

        # Crear botones del menú principal
        PLAY_BUTTON = Button(image=pygame.image.load("assets/images/ui/play_bt.png"), pos=(screen_width // 2 + 25, screen_height // 1.7), 
                         text_input=get_text("play"), font=get_font(80), base_color="#361612", hovering_color="#97ff00")
        OPTIONS_BUTTON = Button(image=pygame.image.load("assets/images/ui/tabla_options_bt.png"), pos=(screen_width // 2 + 22, screen_height // 2 + 230), 
                            text_input=get_text("options"), font=get_font(57), base_color="#361612", hovering_color="white")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/images/ui/tabla_exit_bt.png"), pos=(screen_width // 2 + 20, screen_height // 2 + 350), 
                         text_input=get_text("exit"), font=get_font(57), base_color="#361612", hovering_color="#ff0031")

        # Dibujar la imagen "AMF CORP" en la esquina inferior derecha
        SCREEN.blit(amf_corp_image, (screen_width - amf_corp_width, screen_height - amf_corp_height))  # Ajustar para esquina inferior derecha

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

# Llama al menú principal cuando el juego se ejecuta
