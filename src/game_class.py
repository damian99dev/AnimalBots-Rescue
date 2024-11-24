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


TUT_BUTTON_IMAGE = pygame.image.load("assets/images/ui/tutorial_btt.png")
TUT_BUTTON_IMAGE = pygame.transform.scale(TUT_BUTTON_IMAGE, (int(TUT_BUTTON_IMAGE.get_width() * 1.3),  # Ajusta el tamaño del botón de pausa
                                                                 int(TUT_BUTTON_IMAGE.get_height() * 1.3)))
TUT_BUTTON_RECT = TUT_BUTTON_IMAGE.get_rect(topleft=(1350, 10))       # Coloca en la esquina superior izquierda



PAUSE_BUTTON_IMAGE = pygame.image.load("assets/images/ui/pause_bt.png")
PAUSE_BUTTON_IMAGE = pygame.transform.scale(PAUSE_BUTTON_IMAGE, (int(PAUSE_BUTTON_IMAGE.get_width() * 1.9),  # Ajusta el tamaño del botón de pausa
                                                                 int(PAUSE_BUTTON_IMAGE.get_height() * 1.9)))
PAUSE_BUTTON_RECT = PAUSE_BUTTON_IMAGE.get_rect(topleft=(1440, 10))       # Coloca en la esquina superior izquierda

HEALTH_BAR_IMAGE = pygame.image.load("graphics/ui/game_elements/corazonV1.png")
HEALTH_BAR_IMAGE = pygame.transform.scale(HEALTH_BAR_IMAGE, (int(HEALTH_BAR_IMAGE.get_width() * 0.15),  # Ajusta el tamaño de la barra de salud
                                                               int(HEALTH_BAR_IMAGE.get_height() * 0.15)))
HEALTH_BAR_POS = HEALTH_BAR_IMAGE.get_rect(topleft=(50, 15))      # Coloca en la esquina superior izquierda

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

        base_path = Path(__file__).parent
        tmx_path = base_path / '..' / 'data' / 'tmx' / tmx_file
        self.tmx_maps = {0: load_pygame(str(tmx_path))}
    
        self.current_stage = Level(self.tmx_maps[0])

        self.paused = False
        self.showing_tutorial = False  # Nuevo estado para mostrar el tutorial
        self.timer = 300
        self.start_time = pygame.time.get_ticks()
        self.pause_start_time = None
        self.total_pause_time = 0
        self.font = get_font(50)

        # Imagen del tutorial
        self.tutorial_image = pygame.image.load("assets/images/ui/tutorial_bgg.png")  # Ruta de la imagen del tutorial
        self.tutorial_image = pygame.transform.scale(self.tutorial_image, (1920, 1080))  # Ajusta al tamaño de la pantalla
           # Imagen del fondo del timer



    def run(self):
        while True:
            dt = self.clock.tick(60) / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_p:
                        self.paused = not self.paused
                        if self.paused:
                            pygame.mixer.music.pause()
                            PAUSE_SOUND.play()
                            self.pause_start_time = pygame.time.get_ticks()
                        else:
                            pygame.mixer.music.unpause()
                            if self.pause_start_time:
                                self.total_pause_time += pygame.time.get_ticks() - self.pause_start_time
                                self.pause_start_time = None

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if TUT_BUTTON_RECT.collidepoint(event.pos):
                        pygame.mixer.music.pause()
                        PAUSE_SOUND.play()
                        self.paused = True # Pausa el juego antes de mostrar el tutorial
                        self.show_tutorial_menu()  # Muestra el menú de tutorial
                        self.paused = not self.paused
                        if self.paused:
                            pygame.mixer.music.pause()
                            
                            self.pause_start_time = pygame.time.get_ticks()
                        else:
                            pygame.mixer.music.unpause()
                            if self.pause_start_time:
                                self.total_pause_time += pygame.time.get_ticks() - self.pause_start_time
                                self.pause_start_time = None
                    elif PAUSE_BUTTON_RECT.collidepoint(event.pos):
                        self.paused = not self.paused
                        if self.paused:
                            pygame.mixer.music.pause()
                            PAUSE_SOUND.play()
                            self.pause_start_time = pygame.time.get_ticks()
                        else:
                            pygame.mixer.music.unpause()
                            if self.pause_start_time:
                                self.total_pause_time += pygame.time.get_ticks() - self.pause_start_time
                                self.pause_start_time = None

            if self.showing_tutorial:
                self.show_tutorial_menu()  # Muestra el tutorial
            elif self.paused:
                self.show_pause_menu()  # Muestra el menú de pausa
            else:
                self.current_stage.run(dt)
                self.update_timer()  # Solo actualiza el temporizador si no está pausado
                
            SCREEN.blit(HEALTH_BAR_IMAGE, HEALTH_BAR_POS)
            SCREEN.blit(TUT_BUTTON_IMAGE, TUT_BUTTON_RECT)
            SCREEN.blit(PAUSE_BUTTON_IMAGE, PAUSE_BUTTON_RECT)
            pygame.display.update()



    def update_timer(self):
        if not self.paused:  # Asegúrate de que el temporizador no se actualice si está pausado
            self.timer_button_image = pygame.image.load("assets/images/ui/timer_btt.png").convert_alpha()
            self.timer_button_rect = self.timer_button_image.get_rect(center=(765, 55))  
            self.display_surface.blit(self.timer_button_image, self.timer_button_rect)
            elapsed_time = (pygame.time.get_ticks() - self.start_time - self.total_pause_time) / 1000
            remaining_time = max(0, self.timer - elapsed_time)
            timer_text = self.font.render(f'{int(remaining_time)}', True, "#361612")
            timer_rect = timer_text.get_rect(center=(SCREEN.get_width() // 1.92, 50))
            SCREEN.blit(timer_text, timer_rect)

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
                            text_input=get_text("resume"), font=get_font(50), base_color="#361612", hovering_color="#38bc0f")
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
                    self.paused = not self.paused
                    if self.paused:
                        pygame.mixer.music.pause()
                        PAUSE_SOUND.play()
                        self.pause_start_time = pygame.time.get_ticks()
                    else:
                        pygame.mixer.music.unpause()
                        if self.pause_start_time:
                            self.total_pause_time += pygame.time.get_ticks() - self.pause_start_time
                            self.pause_start_time = None


                elif main_menu_button.checkForInput(mouse_pos):
                    pygame.mixer.music.load("assets/sounds/music/Main Menu.mp3")
                    pygame.mixer.music.play(-1, fade_ms=3000)
                    from main_menu import main_menu
                    main_menu()  # Vuelve al menú principal

                elif quit_button.checkForInput(mouse_pos):
                    pygame.quit()  # Cierra Pygame
                    sys.exit()  # Cierra el sistema

    def show_tutorial_menu(self):
        screen_width, screen_height = pygame.display.get_surface().get_size()
        self.paused = True  # Asegura que el juego esté pausado al mostrar el tutorial
        tutorial_image = pygame.image.load("assets/images/ui/tutorial_bgg.png")  # Carga la imagen del tutorial
        tutorial_image = pygame.transform.scale(tutorial_image, (1550, 870))  # Escalar al tamaño de la pantalla
        back_and_play = Button(image=None, pos=(screen_width // 7, screen_height // 7 + 650), 
                                            text_input=get_text("back"), font=get_font(55), base_color="White", hovering_color="#ffef00")

        # Crear botones independientes
        title_button = Button(
            image=None,
            pos=(screen_width - 450, screen_height // 7 - 85),  # Ajustado al papel
            text_input=get_text("title"),
            font=get_font(55),  # Tamaño reducido
            base_color="#0b0925",
            hovering_color="#0b0925"
        )

        instruction_1_button = Button(
            image=None,
            pos=(screen_width - 360, screen_height // 7 + 120),  # Ajustado al papel
            text_input=get_text("instruction_1"),
            font=get_font(35),  # Tamaño reducido
            base_color="#53af70",
            hovering_color="#53af70"
        )

        instruction_2_button = Button(
            image=None,
            pos=(screen_width - 350, screen_height // 7 + 220),  # Ajustado al papel
            text_input=get_text("instruction_2"),
            font=get_font(35),  # Tamaño reducido
            base_color="#e974ff",
            hovering_color="#e974ff"
        )

        instruction_3_button = Button(
            image=None,
            pos=(screen_width - 430, screen_height // 7 + 320),  # Ajustado al papel
            text_input=get_text("instruction_3"), 
            font=get_font(35),  # Tamaño reducido
            base_color="#74afff",
            hovering_color="#74afff"
        )

        instruction_4_button = Button(
            image=None,
            pos=(screen_width - 400, screen_height // 7 + 420),  # Ajustado al papel
            text_input=get_text("instruction_4"), 
            font=get_font(35),  # Tamaño reducido
            base_color="#ffbd74",
            hovering_color="#ffbd74"
        )

        # Detener el temporizador mientras se ve el tutorial
        tutorial_start_time = pygame.time.get_ticks()

        while True:
            SCREEN.blit(tutorial_image, (0, 0))  # Mostrar la imagen del tutorial
            mouse_pos = pygame.mouse.get_pos()

            
                    # Actualizar y mostrar cada botón
            title_button.changeColor(mouse_pos)
            title_button.update(SCREEN)

            instruction_1_button.changeColor(mouse_pos)
            instruction_1_button.update(SCREEN)
            instruction_2_button.changeColor(mouse_pos)
            instruction_2_button.update(SCREEN)

            instruction_3_button.changeColor(mouse_pos)
            instruction_3_button.update(SCREEN)

            instruction_4_button.changeColor(mouse_pos)
            instruction_4_button.update(SCREEN)

            back_and_play.changeColor(mouse_pos)
            back_and_play.update(SCREEN)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if back_and_play.checkForInput(mouse_pos):
                        self.paused = False  # Despausar el juego al regresar del tutorial
                        # Asegúrate de que el temporizador se reanude desde el punto correcto
                        self.total_pause_time += pygame.time.get_ticks() - tutorial_start_time
                        return  # Salir del tutorial y volver al juego

            pygame.display.update()

