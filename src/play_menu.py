from settings import *                      # Importa todas las configuraciones desde el archivo settings
import pygame, sys                          # Importa Pygame para el motor del juego y sys para la gestión del sistema
from button import Button                   # Importa la clase Button para todos los botones del menú
from game_class import Game
from options_menu import get_text
import json
import cv2 
import current_level_config
from victory import NivelManager
from moviepy import VideoFileClip

pygame.init()

video_path = "assets/images/backgrounds/play_menu.mp4"   # Carga el video con OpenCV
cap = cv2.VideoCapture(video_path)

music_playing = False  

current_level = 'prueba.tmx'


SCREEN = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)       # Cambiado a pantalla completa
pygame.display.set_caption("AnimalBots Rescue")

def get_font(size):                                                 # Función para obtener la fuente con un tamaño específico
    return pygame.font.Font("assets/fonts/font1.otf", size)

def load_languages():
    with open("languages.json", "r", encoding="utf-8") as f:
        return json.load(f)



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
            pygame.mixer.music.load("assets/sounds/music/Spider Dance.mp3")
            pygame.mixer.music.play(-1)
            break

        frame = cv2.flip(frame, 1)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (1820, 920))
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



def play():
    while True:  # Pantalla de selección de niveles

        screen_width, screen_height = pygame.display.get_surface().get_size()  # Obtener tamaño de la pantalla 
        ret, frame = cap.read()
        if not ret:  # Si el video ha terminado, reinícialo
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            ret, frame = cap.read()

        frame = cv2.flip(frame, 1)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (1700, 870))
        frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
        frame_surface = pygame.surfarray.make_surface(frame)

        # Dibuja el frame en la pantalla
        SCREEN.blit(frame_surface, (-100, 0))

        LEVEL_MOUSE_POS = pygame.mouse.get_pos()

        LEVEL_TEXT = get_font(135).render(get_text("level_text"), True, "White")  # Texto para la selección de nivel
        LEVEL_RECT = LEVEL_TEXT.get_rect(center=(screen_width // 2, screen_height // 5 - 100))
        SCREEN.blit(LEVEL_TEXT, LEVEL_RECT)

        # Textos de etiquetas para las columnas

        BEGINNER_TEXT = get_font(70).render(get_text("beginner"), True, "#38bc0f")
        BEGINNER_RECT = BEGINNER_TEXT.get_rect(center=(screen_width // 6, screen_height // 2.8))
        SCREEN.blit(BEGINNER_TEXT, BEGINNER_RECT)

        INTERMEDIATE_TEXT = get_font(70).render(get_text("medium"), True, "#ffef00")
        INTERMEDIATE_RECT = INTERMEDIATE_TEXT.get_rect(center=(screen_width // 1.9, screen_height // 2.8))
        SCREEN.blit(INTERMEDIATE_TEXT, INTERMEDIATE_RECT)

        ADVANCED_TEXT = get_font(70).render(get_text("advanced"), True, "#ff0031")
        ADVANCED_RECT = ADVANCED_TEXT.get_rect(center=(3 * screen_width // 3.5, screen_height // 2.8))
        SCREEN.blit(ADVANCED_TEXT, ADVANCED_RECT)

        # Crea botones para los niveles y el botón de retroceso en forma de zigzag
        # Crea botones para los niveles y el botón de retroceso en forma de zigzag
        LEVEL_1_BUTTON = Button(image=pygame.image.load("assets/images/ui/tabla4_bt.png"), pos=(screen_width // 6, screen_height // 1.55 - 100), 
                                text_input=get_text("1-1"), font=get_font(55), base_color="#361612", hovering_color="#38bc0f")
        LEVEL_2_BUTTON = Button(image=pygame.image.load("assets/images/ui/tabla4_bt.png"), pos=(screen_width // 6 , screen_height // 1.68 + 100), 
                                text_input=get_text("1-2"), font=get_font(55), base_color="#361612", hovering_color="#38bc0f")
        LEVEL_3_BUTTON = Button(image=pygame.image.load("assets/images/ui/tabla4_bt.png"), pos=(screen_width // 1.9, screen_height // 1.55 - 100), 
                                text_input=get_text("2-1"), font=get_font(55), base_color="#361612", hovering_color="#ffef00")
        LEVEL_4_BUTTON = Button(image=pygame.image.load("assets/images/ui/tabla4_bt.png"), pos=(screen_width // 1.9, screen_height // 1.68 + 100), 
                                text_input=get_text("2-2"), font=get_font(55), base_color="#361612", hovering_color="#ffef00")
        LEVEL_5_BUTTON = Button(image=pygame.image.load("assets/images/ui/tabla4_bt.png"), pos=(3 * screen_width // 3.5, screen_height // 1.55 - 100), 
                                text_input=get_text("3-1"), font=get_font(55), base_color="#361612", hovering_color="#ff0031")
        LEVEL_6_BUTTON = Button(image=pygame.image.load("assets/images/ui/tabla4_bt.png"), pos=(3 * screen_width // 3.5, screen_height // 1.68+ 100), 
                                text_input=get_text("3-2"), font=get_font(55), base_color="#361612", hovering_color="#ff0031")

        BACK_BUTTON = Button(image=pygame.image.load("assets/images/ui/tabla_back_bt.png"), pos=(screen_width // 7, screen_height // 7 + 650), 
                                text_input=get_text("back2"), font=get_font(50), base_color="#361612", hovering_color="#ffef00")


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
                            play_video("assets/images/backgrounds/historia_parte1.mp4")  # Reproduce el video
                            pygame.mixer.music.load("assets/sounds/music/Hypertext.mp3")
                            pygame.mixer.music.play(-1)
                            NivelManager.nivel_actual = 'prueba.tmx'
                            current_level_config.current_level = NivelManager.nivel_actual
                            current_level_config.save_current_level(current_level_config.current_level)
                            game = Game(current_level_config.current_level)
                            game.run()
                        elif LEVEL_2_BUTTON.checkForInput(LEVEL_MOUSE_POS):
                            pygame.mixer.music.load("assets/sounds/music/Deal 'Em Out.mp3")
                            pygame.mixer.music.play(-1)
                            NivelManager.nivel_actual = 'prueba1-2.tmx'
                            current_level_config.current_level = NivelManager.nivel_actual
                            current_level_config.save_current_level(current_level_config.current_level)  # Guardar el nivel actual
                            game = Game(current_level_config.current_level)  # Cargar el nivel 2
                            game.run()
                        elif LEVEL_3_BUTTON.checkForInput(LEVEL_MOUSE_POS):
                            pygame.mixer.music.load("assets/sounds/music/Waterfall.mp3")
                            pygame.mixer.music.play(-1)
                            NivelManager.nivel_actual = 'prueba2.tmx'
                            current_level_config.current_level = NivelManager.nivel_actual
                            current_level_config.save_current_level(current_level_config.current_level)  # Guardar el nivel actual
                            game = Game(current_level_config.current_level)  # Cargar el nivel 3
                            game.run()
                        elif LEVEL_4_BUTTON.checkForInput(LEVEL_MOUSE_POS):
                            pygame.mixer.music.load("assets/sounds/music/Ruins.mp3")
                            pygame.mixer.music.play(-1)
                            NivelManager.nivel_actual = 'prueba2-2.tmx'
                            current_level_config.current_level = NivelManager.nivel_actual
                            current_level_config.save_current_level(current_level_config.current_level)  # Guardar el nivel actual
                            game = Game(current_level_config.current_level)  # Cargar el nivel 4
                            game.run()
                        elif LEVEL_5_BUTTON.checkForInput(LEVEL_MOUSE_POS):
                            pygame.mixer.music.load("assets/sounds/music/Another Medium.mp3")
                            pygame.mixer.music.play(-1)
                            NivelManager.nivel_actual = 'prueba3.tmx'
                            current_level_config.current_level = NivelManager.nivel_actual
                            current_level_config.save_current_level(current_level_config.current_level)  # Guardar el nivel actual
                            game = Game(current_level_config.current_level)  # Cargar el nivel 5
                            game.run()
                        elif LEVEL_6_BUTTON.checkForInput(LEVEL_MOUSE_POS):
                            pygame.mixer.music.load("assets/sounds/music/CORE.mp3")
                            pygame.mixer.music.play(-1)
                            NivelManager.nivel_actual = 'prueba3-2.tmx'
                            current_level_config.current_level = NivelManager.nivel_actual
                            current_level_config.save_current_level(current_level_config.current_level)  # Guardar el nivel actual
                            game = Game(current_level_config.current_level)  # Cargar el nivel 6
                            game.run()
                        elif BACK_BUTTON.checkForInput(LEVEL_MOUSE_POS):
                            from main_menu import main_menu
                            main_menu()  # Volver al menú principal

        pygame.display.update()