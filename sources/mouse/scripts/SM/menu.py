import sys
import os

# Permet de ce placer dans le dossier contenant les scripts SM
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + "/scripts/SM")

import pygame
import sounds
import json
from os.path import exists

import maze

class SM:
    """ Classe permettant de gérer le menu du jeu
    """
    def __init__(self):
        self.folder = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.maze = maze.Maze()

    def start(self, langue):
        """ Fonction permettant de lancer le menu de l'exercice

        Elle dessine le menu avec pygame et permet de lancer l'exercice

        Args:
            langue (str): La langue de l'application
        """
        
        # Initialize Pygame
        pygame.init()
        pygame.mixer.init()

        # Init sound manager
        sound_mana = sounds.SoundManager()

        # Screen dimensions
        desktopSize = pygame.display.get_desktop_sizes()
        SCREEN_WIDTH = desktopSize[0][0]
        SCREEN_HEIGHT = desktopSize[0][1]

        # Initialize the screen
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN) # Mode plein écran
        pygame.display.set_caption("SM")

        # Initialize the font
        font = pygame.font.Font(self.folder + '/fonts/VCR_OSD_MONO.ttf', 50)

        #Pour vérifier que le jeu se joue
        is_playing = False
        running = True 

        # Main loop
        while running:
            # Screen dimensions
            desktopSize = pygame.display.get_desktop_sizes()
            SCREEN_WIDTH = desktopSize[0][0]
            SCREEN_HEIGHT = desktopSize[0][1]

            #Permet de savoir si le jeu est lancer ou non
            if is_playing:
                self.maze.start_maze(langue)

            # Texte Start et sa collision 
            start = font.render(("DÉMARRER" if langue == "fr" else "START"), 1, (255, 255, 255))
            screen.blit(start, (SCREEN_WIDTH * (28/64), SCREEN_HEIGHT/2))

            start_rect = pygame.Rect(SCREEN_WIDTH * (7/16), SCREEN_HEIGHT/2, SCREEN_WIDTH * (1/8), SCREEN_HEIGHT * (5/72))
            
            click = font.render(("(cliquez)" if langue == "fr" else "(click)"), 1, (255, 255, 255))
            screen.blit(click, (SCREEN_WIDTH * (28/64), SCREEN_HEIGHT * (400/720)))

            title = font.render(("SM Aide contre Parkinson" if langue == "fr" else "SM Parkinson Eradicator"), 1, (255, 255, 255))
            screen.blit(title, (SCREEN_WIDTH * (21/64), SCREEN_HEIGHT * (5/64)))

            texte = font.render(("Entraînez-vous dans ces labyrinthes pour atténuer la maladie" if langue == "fr" else "Train in these mazes to alleviate the disease"), 1, (255, 255, 255))
            screen.blit(texte, (SCREEN_WIDTH * ((70 if langue == "fr" else 200)/1280), SCREEN_HEIGHT * (520/720)))

            texte2 = font.render((("Il y a 10 niveaux à compléter." if langue == "fr" else "There are 10 levels to complete.")), 1, (255, 255, 255))
            screen.blit(texte2, (SCREEN_WIDTH * (294/1280), SCREEN_HEIGHT * (570/720)))

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
            if running:
                pygame.display.flip()

if __name__ == "__main__":
    game = SM()
    game.start("fr")