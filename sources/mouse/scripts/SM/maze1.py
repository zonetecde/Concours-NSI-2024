import pygame
import sys
import json
from os.path import exists
import os

# Permet de ce placer dans le dossier contenant les scripts SM
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + "/scripts/SM")
class Maze:
    """
    Classe permettant de récupérer le niveau 
    """
    def __init__(self):
        pass
    def start_maze():
        # Initialize Pygame
        pygame.init()

        # Screen dimensions
        desktopSize = pygame.display.get_desktop_sizes()

        SCREEN_WIDTH = desktopSize[0][0]
        SCREEN_HEIGHT = desktopSize[0][1]

        # Initialize the screen
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN) # Mode plein écran
        pygame.display.set_caption("Scary maze or not?")

        # Clock for controlling the frame rate
        clock = pygame.time.Clock()
        starting_tick = pygame.time.get_ticks()

        screen.fill((0, 0, 0))

        #Position utilisable
        x = 50
        y = 150

        #Chargement bg si il y a 
        bg = None

        #Variable running
        running = True
        is_playing = False

        ractangle = (x, y, SCREEN_WIDTH/2, SCREEN_HEIGHT * 0.2)
        font = pygame.font.Font('sources/mouse/fonts/VCR_OSD_MONO.ttf', 50)
        # Main loop
        while running:
            
            current_tick = pygame.time.get_ticks() - starting_tick

            mouseX = pygame.mouse.get_pos()[0]
            mouseY = pygame.mouse.get_pos()[1]

            ## Création niveau 

            

            #Arrière plan
            screen.blit(screen, (0, 0))

            # Création début et fin
            deb = (100-10, 225-10, 10, 10)
            fin = (650-10, 225-10, 10, 10)
            # Création bord et mur
            pygame.draw.rect(screen, (255, 0, 0), ractangle)
            #Création carré debut et fin 
            pygame.draw.rect(screen, (35, 150, 245), deb)
            pygame.draw.rect(screen, (35, 150, 245), fin)
            # Met le cursor sur le départ
            if current_tick == 100:
                pygame.mouse.set_pos([95, 220])
            # Boucle qui vérifie que l'on est bien dans le niveau
            title = font.render(("Maze 1"), 1, (255, 255, 255))
            screen.blit(title, (SCREEN_WIDTH/2 - 95, SCREEN_HEIGHT/2 - 70))

            if mouseX > ractangle[0] and mouseX < ractangle[0] + ractangle[2] and mouseY > ractangle[1] and mouseY < ractangle[1] + ractangle[3]:
                pass
                #pygame.mouse.set_pos([95, 220])



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

            # Cap the frame rate
            clock.tick(60)
            # Update the display
            pygame.display.flip()
            #sys.exit()