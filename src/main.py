from settings import *                      # Importa todas las configuraciones desde el archivo settings
from level import Level                     # Importa la clase Level para manejar los niveles del juego
from pytmx.util_pygame import load_pygame   # Carga los mapas .tmx con soporte para Pygame
from pathlib import Path                    # Manejo de rutas de archivos de manera flexible
import pygame, sys                          # Importa Pygame para el motor del juego y sys para la gestión del sistema
from button import Button                   # Importa la clase Button para todos los botones del menú                 # Importa la función main_menu para el menú principal
from game_over import GameOverScreen


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
    return pygame.font.Font("assets/fonts/gameovercre1.ttf", size)

class Game:
    def __init__(self, level_number):
        self.display_surface = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)
        pygame.display.set_caption('AnimalBot Rescue')
        self.clock = pygame.time.Clock()

        # Carga el mapa .tmx correspondiente al nivel
        base_path = Path(__file__).parent
        tmx_path = base_path / '..' / 'data' / 'tmx' / 'prueba.tmx'
        self.tmx_maps = {0: load_pygame(str(tmx_path))}
    
        self.current_stage = Level(self.tmx_maps[level_number])

        self.paused = False  # Controla el estado de pausa
    
        # Temporizador de 600 segundos
        self.timer = 60
        self.font = get_font(50)  # Usa la misma fuente con un tamaño de 50
        self.start_time = pygame.time.get_ticks()  # Tiempo al que se inicia el juego

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
        
        SCREEN = pygame.display.set_mode((1920, 1080))
        game_over_screen = GameOverScreen(SCREEN, self.font)
    # Mostrar la pantalla de Game Over y manejar la lógica de reinicio/salida
        while True:
        # Ejecutar la pantalla de Game Over
            game_over_screen.run()  # Llama al método run() de GameOverScreen

        #

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

    


    def show_pause_menu(self):
        # Muestra el menú de pausa
        pause_font = get_font(75)
        pause_text = pause_font.render("", True, "White")
        pause_rect = pause_text.get_rect(center=(SCREEN.get_width() // 2, SCREEN.get_height() // 2 - 100))
        SCREEN.blit(pause_text, pause_rect)

        # Crear botones de reanudar, salir, volver al menú principal y abrir opciones
        puased_button = Button(image=pygame.image.load("assets/images/ui/paused_bt.png"), pos=(SCREEN.get_width() // 2.01, SCREEN.get_height() // 2 + -200),
                            text_input="", font=get_font(50), base_color="Green", hovering_color="Green")
        resume_button = Button(image=pygame.image.load("assets/images/ui/tabla_resume_bt.png"), pos=(SCREEN.get_width() // 2, SCREEN.get_height() // 2),
                            text_input="RESUME", font=get_font(50), base_color="#361612", hovering_color="Green")
        main_menu_button = Button(image=pygame.image.load("assets/images/ui/tabla_menu_bt.png"), pos=(SCREEN.get_width() // 2, SCREEN.get_height() // 2 + 100),
                                text_input="MENU", font=get_font(50), base_color="#361612", hovering_color="White")
        quit_button = Button(image=pygame.image.load("assets/images/ui/tabla_exit_bt.png") , pos=(SCREEN.get_width() // 2, SCREEN.get_height() // 2 + 200),
                            text_input="EXIT", font=get_font(50), base_color="#361612", hovering_color="Red")

        # Cambiar color de los botones al pasar el mouse
        mouse_pos = pygame.mouse.get_pos()
        for button in [puased_button,resume_button, main_menu_button, quit_button]:
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
                    main_menu()  # Vuelve al menú principa
                elif quit_button.checkForInput(mouse_pos):
                    pygame.quit()  # Cierra Pygame
                    sys.exit()  # Cierra el sistema


def play():
    # Pantalla de selección de niveles
    while True:
        
        # Obtener tamaño de la pantalla
        screen_width, screen_height = pygame.display.get_surface().get_size()
        SCREEN.blit(BG, (0, 0))  # Establecer fondo del menú de selección de niveles
        LEVEL_MOUSE_POS = pygame.mouse.get_pos()

        # Texto para la selección de nivel
        LEVEL_TEXT = get_font(135).render("Select Level", True, "White")
        LEVEL_RECT = LEVEL_TEXT.get_rect(center=(screen_width // 2, screen_height // 5))
        SCREEN.blit(LEVEL_TEXT, LEVEL_RECT)

        # Crea botones para los niveles y el botón de retroceso
        LEVEL_1_BUTTON = Button(image=pygame.image.load("assets/images/ui/tabla4_bt.png"), pos=(screen_width // 2, screen_height // 2), 
                                text_input="BEGINNER", font=get_font(75), base_color="#361612", hovering_color="#97ff00") 
        LEVEL_2_BUTTON = Button(image=pygame.image.load("assets/images/ui/tabla4_bt.png"), pos=(screen_width // 2, screen_height // 2 + 150), 
                                text_input="MEDIUM", font=get_font(75), base_color="#361612", hovering_color="#ffef00")
        LEVEL_3_BUTTON = Button(image=pygame.image.load("assets/images/ui/tabla4_bt.png"), pos=(screen_width // 2, screen_height // 2 + 300), 
                                text_input="ADVANCED", font=get_font(75), base_color="#361612", hovering_color="#ff0031")
        BACK_BUTTON = Button(image=None, pos=(screen_width // 7, screen_height // 7 + 650), 
                            text_input="BACK", font=get_font(55), base_color="White", hovering_color="Green",)
        

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
                    
                    pygame.mixer.music.stop() # Detener la música del menú principal
                    pygame.mixer.music.load("assets/sounds/music/Hypertext.mp3") # Reproduce la música del nivel 1 al darle al boton level 1
                    pygame.mixer.music.play(-1, fade_ms=3000)
    
                    game = Game(0)  # Cargar el nivel 1
                    game.run()
                elif LEVEL_2_BUTTON.checkForInput(LEVEL_MOUSE_POS):
                    print("Level 2 not yet implemented")  # Niveles aún no implementados
                elif LEVEL_3_BUTTON.checkForInput(LEVEL_MOUSE_POS):
                    print("Level 3 not yet implemented")
                elif BACK_BUTTON.checkForInput(LEVEL_MOUSE_POS):
                    main_menu()  # Volver al menú principal

        pygame.display.update()

import json
def load_config():    # Cargar la configuración
    try:
        with open('config.json', 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"music_volume": 0.5}  # Valores predeterminados

def save_config(music_volume):  # Elimina effects_volume
    with open('config.json', 'w') as f:
        json.dump({"music_volume": music_volume}, f)


class Slider:
    def __init__(self, position, width, initial_value=0.5):
        self.position = position
        self.width = width
        self.value = initial_value
        self.slider_rect = pygame.Rect(position[0], position[1], width, 10)  # Rectángulo del slider
        self.circle_rect = pygame.Rect(position[0] + initial_value * width - 10, position[1] - 10, 20, 30)  # Círculo del slider
        self.dragging = False  # Para controlar el arrastre

    def draw(self, screen):
        # Dibuja el fondo del slider
        pygame.draw.rect(screen, (100, 100, 100), self.slider_rect)  # Color del fondo
        # Dibuja el círculo que representa el valor
        pygame.draw.ellipse(screen, (255, 0, 0), self.circle_rect)  # Color del círculo
        # Opcional: Dibuja el valor del slider sin decimales
        value_text = get_font(20).render(f"{int(self.value * 100)}%", True, "White")  # Convertir a entero y mostrar en porcentaje
        screen.blit(value_text, (self.position[0] + self.width + 20, self.position[1] - 10))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.circle_rect.collidepoint(event.pos):
                self.dragging = True
                
        if event.type == pygame.MOUSEBUTTONUP: 
            self.dragging = False
            
        if event.type == pygame.MOUSEMOTION and self.dragging:
            mouse_x = event.pos[0]
            # Limita el movimiento del slider dentro del rango
            if mouse_x < self.position[0]:
                mouse_x = self.position[0]
            elif mouse_x > self.position[0] + self.width:
                mouse_x = self.position[0] + self.width
            # Actualiza la posición del círculo
            self.circle_rect.x = mouse_x - 10  # Centra el círculo
            # Calcula el nuevo valor
            self.value = (self.circle_rect.x - self.position[0] + 10) / self.width  # Normaliza el valor entre 0 y 1

    def get_value(self):
        return self.value  # Devuelve el valor actual del slider

    def set_volume(self, volume):
        # Establece el volumen del sonido (entre 0 y 1)
        self.value = volume
        self.circle_rect.x = self.position[0] + volume * self.width - 10  # Actualiza la posición del círculo

def options():
    screen_width, screen_height = pygame.display.get_surface().get_size()

    # Cargar los volúmenes de configuración
    config = load_config()

    # Centrar los sliders horizontalmente y ubicarlos más arriba
    slider_x_position = screen_width // 2 - 150  # Centrar los sliders en la pantalla
    music_slider_y_position = screen_height // 3

    music_slider = Slider((slider_x_position, music_slider_y_position + 60), 300, initial_value=config["music_volume"])

    while True:
        SCREEN.blit(BG, (0, 0))  # Establecer fondo del menú de opciones
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        # Títulos para las opciones
        OPTIONS_TITLE = get_font(55).render("OPTIONS", True, "Yellow")
        OPTIONS_TITLE_RECT = OPTIONS_TITLE.get_rect(center=(screen_width // 2, screen_height // 5))
        SCREEN.blit(OPTIONS_TITLE, OPTIONS_TITLE_RECT)

        # Dibuja el slider de música
        music_slider.draw(SCREEN)
        pygame.mixer.music.set_volume(music_slider.get_value())  # Establecer el volumen de música

        # Texto para los sliders, centrado y más arriba
        music_label = get_font(40).render("Music volume", True, "White")
        music_label_rect = music_label.get_rect(center=(screen_width // 2, music_slider_y_position + 30))
        SCREEN.blit(music_label, music_label_rect)

        

        # Botón para regresar al menú principal
        OPTIONS_BACK = Button(image=None, pos=(screen_width // 2, screen_height // 2 + 200), 
                            text_input="BACK", font=get_font(55), base_color="White", hovering_color="Green")
        
        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        #OPTIONS_BACK.set_click_volume(0.3)

        OPTIONS_BACK.update(SCREEN)

        # Detectar eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Maneja los eventos del slider
            music_slider.handle_event(event)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    # Guardar los volúmenes en la configuración antes de regresar
                    save_config(music_slider.get_value())
                    main_menu()

        pygame.display.update()

def main_menu():
    global music_playing
    
    # Reproducir la música del menú principal solo una vez al inicio
    if not music_playing:
        pygame.mixer.music.load("assets/sounds/music/Main Menu.mp3")
        pygame.mixer.music.play(-1, fade_ms=3000) 
        music_playing = True

    # Obtener tamaño de la pantalla
    screen_width, screen_height = pygame.display.get_surface().get_size()

    # Cargar la imagen "AMF CORP"
    amf_corp_image = pygame.image.load("assets/images/ui/AMF CORP.png").convert_alpha()
    amf_corp_width, amf_corp_height = amf_corp_image.get_size()

    # Crea una fuente
    beta_font = get_font(30) 
    beta_text = beta_font.render("BETA 1.1.38", True, (255, 255, 255)) 
    beta_text_rect = beta_text.get_rect(topleft=(10, screen_height - 30))
    # Menú principal
    while True:
        SCREEN.blit(BG, (0, 0))  # Establecer fondo del menú
        MENU_MOUSE_POS = pygame.mouse.get_pos()

        # Texto del título del menú
        MENU_TITLE_BT = Button(image=pygame.image.load("assets/images/ui/menu_title_bt.png"), pos=(screen_width // 2, screen_height // 4), 
                            text_input="", font=get_font(105), base_color="#d7fcd4", hovering_color="Cyan")

        # Crear botones del menú principal
        PLAY_BUTTON = Button(image=pygame.image.load("assets/images/ui/play_bt.png"), pos=(screen_width // 2, screen_height // 1.7), 
                            text_input="PLAY", font=get_font(99), base_color="#361612", hovering_color="Green")
        OPTIONS_BUTTON = Button(image=pygame.image.load("assets/images/ui/tabla_options_bt.png"), pos=(screen_width // 2 - 10, screen_height // 2 + 230), 
                                text_input="OPTIONS", font=get_font(60), base_color="#361612", hovering_color="white")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/images/ui/tabla_exit_bt.png"), pos=(screen_width // 2, screen_height // 2 + 350), 
                            text_input="EXIT", font=get_font(60), base_color="#361612", hovering_color="Red")

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
                    play()  # Inicia la pantalla de selección de niveles
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()  # Inicia la pantalla de opciones
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

# Llama al menú principal cuando el juego se ejecuta
main_menu()

