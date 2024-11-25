from settings import *                      # Importa todas las configuraciones desde el archivo settings
import pygame, sys                          # Importa Pygame para el motor del juego y sys para la gestión del sistema
from button import Button                   # Importa la clase Button para todos los botones del menú
import json
import cv2  # Importar OpenCV

pygame.init()

video_path = "assets/images/backgrounds/menu.mp4"   # Carga el video con OpenCV
cap = cv2.VideoCapture(video_path)

SCREEN = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)       # Cambiado a pantalla completa
pygame.display.set_caption("AnimalBots Rescue")
def get_font(size):                                                     # Función para obtener la fuente con un tamaño específico
    return pygame.font.Font("assets/fonts/font1.otf", size)

# Cargar idiomas
def load_languages():
    with open("languages.json", "r", encoding="utf-8") as f:
        return json.load(f)

# Guardar idioma en config.json
def save_language(language):
    with open("config.json", "w") as f:
        json.dump({"language": language, "music_volume": slider.get_value()}, f)

# Cargar idioma seleccionado y volumen
def load_config():
    try:
        with open("config.json", "r") as f:
            config = json.load(f)
            return config.get("language", "es"), config.get("music_volume", 0.5)
    except (FileNotFoundError, json.JSONDecodeError):
        return "es", 0.5  # Valores predeterminados

# Inicializar idioma y volumen
language_data = load_languages()
current_language, initial_volume = load_config()

def get_text(key):
    return language_data[current_language].get(key, key)

class Slider:
    def __init__(self, position, width, initial_value=0.5):
        self.position = position
        self.width = width
        self.value = initial_value
        self.slider_rect = pygame.Rect(position[0], position[1], width, 10)  # Rectángulo del slider
        self.circle_rect = pygame.Rect(position[0] + initial_value * width - 10, position[1] - 15, 25, 35)  # Círculo del slider
        self.dragging = False  # Para controlar el arrastre

    def draw(self, screen):
        pygame.draw.rect(screen, (170, 170, 170), self.slider_rect)  # Fondo del slider
        pygame.draw.ellipse(screen, (255, 0, 0), self.circle_rect)    # Círculo del slider
        value_text = get_font(45).render(f"{int(self.value * 100)}%", True, "White")  # Valor en porcentaje
        screen.blit(value_text, (self.position[0] + self.width + 35, self.position[1] - 25))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.circle_rect.collidepoint(event.pos):
                self.dragging = True
                
        if event.type == pygame.MOUSEBUTTONUP: 
            self.dragging = False
            
        if event.type == pygame.MOUSEMOTION and self.dragging:
            mouse_x = event.pos[0]
            if mouse_x < self.position[0]:
                mouse_x = self.position[0]
            elif mouse_x > self.position[0] + self.width:
                mouse_x = self.position[0] + self.width
            self.circle_rect.x = mouse_x - 10
            self.value = (self.circle_rect.x - self.position[0] + 10) / self.width  # Normaliza el valor entre 0 y 1

    def get_value(self):
        return self.value

# Inicializar slider con el volumen inicial
screen_width, screen_height = pygame.display.get_surface().get_size()
slider = Slider(position=(screen_width // 2 - 150, screen_height // 2 - 50), width=300, initial_value=initial_volume)
world_image = pygame.image.load("assets/images/ui/world.png").convert_alpha()
world_width, world_height = world_image.get_size()

def options():
    global current_language
    screen_width, screen_height = pygame.display.get_surface().get_size()

    # Generar los textos iniciales en el idioma seleccionado
    OPTIONS_TITLE = get_font(145).render(get_text("options_title"), True, "Yellow")
    MUSIC_VOLUME_LABEL = get_font(60).render(get_text("music_volume"), True, "White")
    OPTIONS_BACK = Button(image=pygame.image.load("assets/images/ui/tabla_back_bt.png"), pos=(screen_width // 7, screen_height // 7 + 650), 
                        text_input=get_text("back"), font=get_font(50), base_color="#361612", hovering_color="#ffef00")
    
    # Establecer el texto completo de idioma inicial
    language_text = "Español" if current_language == "es" else "English"
    LANGUAGE_BUTTON = Button(image=None, pos=(screen_width // 2, screen_height // 2 + 200),
                            text_input=language_text, font=get_font(55), base_color="White", hovering_color="#b00035")

    while True:
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

        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        # Renderizar título, botones, etiqueta de volumen y slider
        SCREEN.blit(OPTIONS_TITLE, OPTIONS_TITLE.get_rect(center=(screen_width // 2, screen_height // 2 - 350)))
        SCREEN.blit(MUSIC_VOLUME_LABEL, MUSIC_VOLUME_LABEL.get_rect(center=(screen_width // 2, screen_height // 2 - 110)))
        SCREEN.blit(world_image, (screen_width - world_width // 2 - 770, screen_height - world_height // 2 - 350))
        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        LANGUAGE_BUTTON.changeColor(OPTIONS_MOUSE_POS)

        OPTIONS_BACK.update(SCREEN)
        LANGUAGE_BUTTON.update(SCREEN)
        slider.draw(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    save_language(current_language)
                    from main_menu import main_menu
                    main_menu()
                if LANGUAGE_BUTTON.checkForInput(OPTIONS_MOUSE_POS):
                    # Cambiar el idioma y actualizar el texto completo del botón
                    current_language = "en" if current_language == "es" else "es"
                    language_text = "Español" if current_language == "es" else "English"
                    LANGUAGE_BUTTON = Button(image=None, pos=(screen_width // 2, screen_height // 2 + 200),
                                            text_input=language_text, font=get_font(55), 
                                            base_color="White", hovering_color="#b00035")
                    
                    # Actualizar textos en el nuevo idioma seleccionado
                    OPTIONS_TITLE = get_font(145).render(get_text("options_title"), True, "Yellow")
                    MUSIC_VOLUME_LABEL = get_font(60).render(get_text("music_volume"), True, "White")
                    OPTIONS_BACK = Button(image=pygame.image.load("assets/images/ui/tabla_back_bt.png"), 
                                          pos=(screen_width // 7, screen_height // 7 + 650), 
                                          text_input=get_text("back"), font=get_font(50), 
                                          base_color="#361612", hovering_color="#ffef00")
            
            # Manejar eventos del slider
            slider.handle_event(event)

        # Actualizar volumen de la música
        pygame.mixer.music.set_volume(slider.get_value())

        pygame.display.update()
