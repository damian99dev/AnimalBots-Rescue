import pygame
import sys
import cv2
from moviepy import VideoFileClip
from main_menu import main_menu

pygame.init()

SCREEN = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)
pygame.display.set_caption("AnimalBots Rescue")

def play_intro_video(video_path):
    # Usar moviepy para extraer información del video
    video_clip = VideoFileClip(video_path)
    audio = video_clip.audio
    audio.write_audiofile("temp_audio.mp3")  # Extraer audio temporalmente

    fps = video_clip.fps  # Obtener FPS del video para sincronización

    # Iniciar el audio con Pygame
    pygame.mixer.init()
    pygame.mixer.music.load("temp_audio.mp3")
    pygame.mixer.music.play()

    # Reproducción de video usando OpenCV
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: No se pudo cargar el video.")
        return

    clock = pygame.time.Clock()

    while True:
        ret, frame = cap.read()
        if not ret:  # Si el video ha terminado, salir del bucle
            break

        frame = cv2.flip(frame, 1)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (1820, 920))
        frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
        frame_surface = pygame.surfarray.make_surface(frame)

        # Dibuja el frame en la pantalla
        SCREEN.blit(frame_surface, (0, 0))

        # Manejo de eventos de Pygame
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                cap.release()
                pygame.mixer.music.stop()
                pygame.quit()
                sys.exit()

        # Actualiza la pantalla
        pygame.display.update()

        # Sincronización exacta con los FPS del video
        clock.tick(fps)

    cap.release()
    pygame.mixer.music.stop()  # Detener el audio al final

if __name__ == "__main__":
    play_intro_video("assets/images/backgrounds/michi.mp4")
main_menu()
