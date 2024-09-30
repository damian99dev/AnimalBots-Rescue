import pygame
import sys
from button import Button  # Asegúrate de tener la clase Button

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

# Inicializamos Pygame y la pantalla
pygame.init()
SCREEN = pygame.display.set_mode((1920, 1080))
pygame.display.set_caption("Hurra!")

# Cargar música de victoria
VICTORY_MUSIC = pygame.mixer.Sound("assets/sounds/music/End and Thanks!.flac")
WINBANJO = pygame.mixer.Sound("assets/sounds/fx/winbanjo.mp3")

# Cargar imágenes y fuentes
BG_IMAGE = pygame.image.load("graphics/Background/backgg.png")
BG_IMAGE = pygame.transform.scale(BG_IMAGE, (1920, 1080))

def set_volume(sound, volume):
                            # Establece el volumen para un sonido
    sound.set_volume(volume)

# Cargar volumen desde la configuración
config = load_config()  # Cargar el volumen guardado
set_volume(VICTORY_MUSIC, config["music_volume"])  # Establecer volumen de música de victoria
set_volume(WINBANJO, config["music_volume"])  # Establecer volumen de WINBANJO

def get_font(size):
    return pygame.font.Font("assets/fonts/gameovercre1.ttf", size)

class VictoryScreen:
    def __init__(self):
        # Comenzar con un fadeout de la música actual
        pygame.mixer.music.fadeout(8000)  # Fundido de salida de la música actual en 8 segundos
        pygame.mixer.music.pause()  # Pausar la música

        # Control de sonido
        self.sound_stage = 0  # Etapa inicial de la reproducción de sonidos
        self.sound_timer = pygame.time.get_ticks()  # Guardar el tiempo actual
        self.sound_duration = WINBANJO.get_length() * 1000  # Duración de WINBANJO en milisegundos

        # Crear botones
        self.menu_button = Button(image=pygame.image.load("assets/images/ui/tabla_menu_bt.png"), 
                                  pos=(1920 // 2, 1080 // 2), 
                                  text_input="MENU", font=get_font(50), 
                                  base_color="#361612", hovering_color="White")
        
        self.quit_button = Button(image=pygame.image.load("assets/images/ui/tabla_exit_bt.png"), 
                                  pos=(1920 // 2, 1080 // 2 + 150), 
                                  text_input="EXIT", font=get_font(50), 
                                  base_color="#361612", hovering_color="Red")

        # Empezar con el sonido WINBANJO
        WINBANJO.play()

    def run(self):
        while True:
            SCREEN.blit(BG_IMAGE, (0, 0))
            mouse_pos = pygame.mouse.get_pos()

            # Crear texto de victoria
            victory_text = get_font(120).render("You WON :D!", True, "White")
            victory_rect = victory_text.get_rect(center=(1920 // 2, 1080 // 4))
            SCREEN.blit(victory_text, victory_rect)

            # Actualizar botones
            for button in [self.menu_button, self.quit_button]:
                button.changeColor(mouse_pos)
                button.update(SCREEN)

            # Controlar la secuencia de los sonidos
            self.play_next_sound()

            # Eventos del mouse y teclado
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.menu_button.checkForInput(mouse_pos):
                        VICTORY_MUSIC.stop()
                        main_menu_status()  
                    if self.quit_button.checkForInput(mouse_pos):
                        pygame.quit()
                        sys.exit()

            pygame.display.update()

    def play_next_sound(self):
        current_time = pygame.time.get_ticks()

        # Si WINBANJO ha terminado, reproduce la música de victoria
        if self.sound_stage == 0 and current_time - self.sound_timer >= self.sound_duration:
            VICTORY_MUSIC.play(-1, fade_ms=3000)  # Reproduce la música de victoria en bucle
            self.sound_stage = 1  # Cambia el estado para evitar repetir la música

def main_menu_status():
    # Para volver al menú principal
    print("Volviendo al menú principal...") 
    from main import main_menu
    main_menu()

# Para probar la pantalla de victoria
if __name__ == "__main__":
    victory_screen = VictoryScreen()
    victory_screen.run()

