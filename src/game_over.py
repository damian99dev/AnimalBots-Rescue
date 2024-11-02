import pygame
import sys
from button import Button  # Asegúrate de tener la clase Button
from options_menu import get_text
import json

# Funciones para cargar y guardar la configuración
def load_config():
    try:
        with open('config_music.json', 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"music_volume": 0.5}  # Valores predeterminados

def save_config(music_volume):
    with open('config_music.json', 'w') as f:
        json.dump({"music_volume": music_volume}, f)

# Inicializar Pygame y la pantalla
pygame.init()
SCREEN = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)
pygame.display.set_caption("Game Over!")


# Cargar música de Game Over
GAMEOVER_MUSIC = pygame.mixer.Sound("assets/sounds/music/Death is only the beginning.mp3")

# Cargar imágenes y fuentes
BG_IMAGE = pygame.image.load("graphics/Background/backgg.png")
BG_IMAGE = pygame.transform.scale(BG_IMAGE, (1920, 1080))

def set_volume(sound, volume):
    sound.set_volume(volume)

# Cargar volumen desde la configuración
config = load_config()  # Cargar el volumen guardado
set_volume(GAMEOVER_MUSIC, config["music_volume"])  # Establecer volumen de música de Game Over

def get_font(size):                                                 # Función para obtener la fuente con un tamaño específico
    return pygame.font.Font("assets/fonts/font1.otf", size)

def load_languages():
    with open("languages.json", "r", encoding="utf-8") as f:
        return json.load(f)
# Clase para la pantalla de Game Over
class GameOverScreen:
    def __init__(self, screen, font):
        self.screen = screen  # Guardar la pantalla
        self.font = font  # Guardar la fuente como un objeto ya creado

        # Comenzar con un fadeout de la música actual
        pygame.mixer.music.fadeout(8000)  # Fundido de salida de la música actual en 5 segundos
        pygame.mixer.music.pause()  # Pausar la música

        # Crear botones
        self.menu_button = Button(image=pygame.image.load("assets/images/ui/tabla_menu_bt.png"), 
                                  pos=(1920 // 2.5, 1080 // 2), 
                                  text_input=get_text("menu"), font=self.font,  # Aquí se usa `self.font`
                                  base_color="#361612", hovering_color="#97ff00")
        
        self.quit_button = Button(image=pygame.image.load("assets/images/ui/tabla_exit_bt.png"), 
                                  pos=(1920 // 2.5, 1080 // 2 + 150), 
                                  text_input=get_text("exit"), font=self.font,  # Aquí también se usa `self.font`
                                  base_color="#361612", hovering_color="#ff0031")

        # Empezar con la música de Game Over
        GAMEOVER_MUSIC.play(-1, fade_ms= 1000)

    def run(self):
        while True:
            self.screen.blit(BG_IMAGE, (0, 0))
            mouse_pos = pygame.mouse.get_pos()

        # Crear una nueva fuente solo para el texto "Game Over" con un tamaño más grande
            gameover_font = get_font(120)  # Cambia el tamaño a 120 o al valor que desees

        # Crear texto de Game Over con la nueva fuente
            gameover_text = gameover_font.render(get_text("game_over"), True, "White")
            gameover_rect = gameover_text.get_rect(center=(1920 // 2.5, 1080 // 4))
            self.screen.blit(gameover_text, gameover_rect)

        # Actualizar botones (estos seguirán usando `self.font`)
            for button in [self.menu_button, self.quit_button]:
                button.changeColor(mouse_pos)
                button.update(self.screen)

        # Eventos del mouse y teclado
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.menu_button.checkForInput(mouse_pos):
                        GAMEOVER_MUSIC.stop()
                        music_playing = False
                        if not music_playing:
                            pygame.mixer.music.load("assets/sounds/music/Main Menu.mp3")
                            pygame.mixer.music.play(-1, fade_ms=3000) 
                            music_playing = True
                        from main_menu import main_menu
                        main_menu()
                    if self.quit_button.checkForInput(mouse_pos):
                        pygame.quit()
                        sys.exit()

            pygame.display.update()


# Para probar la pantalla de Game Over
if __name__ == "__main__":
    # Instanciar la pantalla de Game Over con SCREEN y la función get_font
    gameover_screen = GameOverScreen(SCREEN, get_font(60))  # Usar la fuente en tamaño 50
    gameover_screen.run()
