import sys
import os

# Permet de ce placer dans le dossier contenant les scripts SM
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + "/scripts/SM")

import pygame
import sounds
import json
from os.path import exists


import maze1
maze = maze1.Maze()

class SM:
    def __init__(self):
        pass

    def start(self):
        # Initialize Pygame
        pygame.init()
        pygame.mixer.init()

        sound_mana = sounds.SoundManager()

        # Screen dimensions
        desktopSize = pygame.display.get_desktop_sizes()

        SCREEN_WIDTH = desktopSize[0][0]
        SCREEN_HEIGHT = desktopSize[0][1]

        # Initialize the screen
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN) # Mode plein écran
        pygame.display.set_caption("Scary maze or not?")
        font = pygame.font.Font('sources/mouse/fonts/VCR_OSD_MONO.ttf', 50)

        #Position utilisable
        x = SCREEN_WIDTH * (50/1280)
        y = SCREEN_HEIGHT * (150/720)

        is_playing = False
        running = True 

        # Main loop
        while running:

            #Permet de savoir si le jeu est lancer ou non
            if is_playing:
                maze.start_maze()

            # Texte Start et sa collision 
            start = font.render(("START"), 1, (255, 255, 255))
            screen.blit(start, (SCREEN_WIDTH * (29/64), SCREEN_HEIGHT/2))
            start_rect = pygame.Rect(SCREEN_WIDTH * (7/16), SCREEN_HEIGHT/2, SCREEN_WIDTH * (1/8), SCREEN_HEIGHT * (5/72))

            # Texte Scary maze sans collision
            title = font.render(("SCARY MAZE"), 1, (255, 255, 255))
            screen.blit(title, (SCREEN_WIDTH * (13/64), SCREEN_HEIGHT * (5/64)))


            for event in pygame.event.get():
                #Permet de quitter so on appuie sur la croix
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                #Permet de quitter le jeu avec echap
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.mixer.stop()
                        running = False
                        is_playing = False
                        pygame.quit()
                #Si souris cliquer, lancement du jeu et petit son
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if start_rect.collidepoint(pygame.mouse.get_pos()):
                        sound_mana.play('click')
                        is_playing = True


            
            # Update the display
            pygame.display.flip()

if __name__ == "__main__":
    game = SM()
    game.start()