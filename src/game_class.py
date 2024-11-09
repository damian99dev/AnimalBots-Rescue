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

class Game:
    def __init__(self, tmx_file):
        pygame.init()
        self.display_surface = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)
        pygame.display.set_caption("AnimalBot Rescue")
        self.clock = pygame.time.Clock()

        # Carga el mapa .tmx correspondiente al nivel
        base_path = Path(__file__).parent
        tmx_path = base_path / '..' / 'data' / 'tmx' / tmx_file
        self.tmx_maps = {0: load_pygame(str(tmx_path))}
    
        self.current_stage = Level(self.tmx_maps[0])

        self.paused = False  # Controla el estado de pausa
    
        # Temporizador de 600 segundos
        self.timer = 300
        self.font = get_font(50)  # Usa la misma fuente con un tamaño de 50
        self.start_time = pygame.time.get_ticks()  # Tiempo al que se inicia el juego

        # Reproducir música del nivel
        pygame.mixer.music.load("assets\sounds\music\Hypertext.mp3")
        pygame.mixer.music.play(-1)

    def run(self):
        while True:
            dt = self.clock.tick(60) / 1000  # Limita el framerate a 60 FPS
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_p:  # Presiona 'P' o 'ESCAPE' para pausar
                        self.paused = not self.paused  # Alterna el estado de pausa
                        if self.paused:
                            pygame.mixer.music.pause()  # Pausar la música
                            PAUSE_SOUND.play()  # Reproducir sonido de pausa
                        else:
                            pygame.mixer.music.unpause()  # Reanudar la música

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if PAUSE_BUTTON_RECT.collidepoint(event.pos):
                        self.paused = not self.paused
                        if self.paused:
                            pygame.mixer.music.pause()  # Pausar la música
                            PAUSE_SOUND.play()  # Reproducir sonido de pausa
                        else:
                            pygame.mixer.music.unpause()  # Reanudar la música

            if self.paused:
                self.show_pause_menu()  # Muestra el menú de pausa
            else:
                # Actualiza el nivel actual y temporizador
                self.current_stage.run(dt)

                # Calcula el tiempo restante
                self.update_timer()

            # Mostrar la barra de salud y el botón de pausa en pantalla
            SCREEN.blit(HEALTH_BAR_IMAGE, HEALTH_BAR_POS)
            SCREEN.blit(PAUSE_BUTTON_IMAGE, PAUSE_BUTTON_RECT)

            pygame.display.update()

    def update_timer(self):
        # Calcula el tiempo transcurrido
        elapsed_time = (pygame.time.get_ticks() - self.start_time) / 1000  # Convertir a segundos
        remaining_time = max(0, self.timer - elapsed_time)  # Asegurarse que no sea negativo

        # Muestra el temporizador en pantalla solo con los números
        timer_text = self.font.render(f'{int(remaining_time)}', True, "White")
        timer_rect = timer_text.get_rect(center=(SCREEN.get_width() // 2, 50))  # Centrado horizontalmente

        SCREEN.blit(timer_text, timer_rect)

        # Si el tiempo llega a 0, activa la pantalla de Game Over
        if remaining_time <= 0:
            self.game_over()

    def game_over(self):
        # Crear instancia de la pantalla de Game Over
        SCREEN = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)
        game_over_screen = GameOverScreen(SCREEN, self.font)
        # Mostrar la pantalla de Game Over y manejar la lógica de reinicio/salida
        while True:
            # Ejecutar la pantalla de Game Over
            game_over_screen.run()  # Llama al método run() de GameOverScreen

    def show_pause_menu(self):
        # Muestra el menú de pausa
        pause_font = get_font(75)
        pause_text = pause_font.render("", True, "White")
        pause_rect = pause_text.get_rect(center=(SCREEN.get_width() // 2, SCREEN.get_height() // 2 - 100))
        SCREEN.blit(pause_text, pause_rect)

        # Crear botones de reanudar, salir, volver al menú principal y abrir opciones
        paused_button = Button(image=pygame.image.load("assets/images/ui/paused_bt.png"), pos=(SCREEN.get_width() // 2.01, SCREEN.get_height() // 2 - 200),
                            text_input="", font=get_font(50), base_color="Green", hovering_color="Green")
        resume_button = Button(image=pygame.image.load("assets/images/ui/tabla_resume_bt.png"), pos=(SCREEN.get_width() // 2, SCREEN.get_height() // 2),
                            text_input=get_text("resume"), font=get_font(50), base_color="#361612", hovering_color="#97ff00")
        main_menu_button = Button(image=pygame.image.load("assets/images/ui/tabla_menu_bt.png"), pos=(SCREEN.get_width() // 2, SCREEN.get_height() // 2 + 100),
                                text_input=get_text("menu"), font=get_font(50), base_color="#361612", hovering_color="#ffef00")
        quit_button = Button(image=pygame.image.load("assets/images/ui/tabla_exit_bt.png") , pos=(SCREEN.get_width() // 2, SCREEN.get_height() // 2 + 200),
                            text_input=get_text("exit"), font=get_font(50), base_color="#361612", hovering_color="#ff0031")

        # Cambiar color de los botones al pasar el mouse
        mouse_pos = pygame.mouse.get_pos()
        for button in [paused_button, resume_button, main_menu_button, quit_button]:
            button.changeColor(mouse_pos)
            button.update(SCREEN)

        # Detectar eventos para los botones
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if resume_button.checkForInput(mouse_pos):
                    self.paused = False  # Reanuda el juego
                    pygame.mixer.music.unpause()  # Reanudar la música
                elif main_menu_button.checkForInput(mouse_pos):
                    pygame.mixer.music.load("assets/sounds/music/Main Menu.mp3")
                    pygame.mixer.music.play(-1, fade_ms=3000)
                    from main_menu import main_menu
                    main_menu()  # Vuelve al menú principal
                elif quit_button.checkForInput(mouse_pos):
                    pygame.quit()  # Cierra Pygame
                    sys.exit()  # Cierra el sistema
