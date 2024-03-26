import sys
import os
import sounds
import pygame

# Permet de ce placer dans le dossier contenant les scripts VW
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + "/scripts/vw")

import vw_engine
ASSETS_FOLDER = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + "/assets/"

class VW_Menu:
    """Affiche le menu du jeu Verbal Warfare
    """
    def __init__(self):
        self.folder = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    def start(self):
        """Lance le menu de l'exercice
        """
        # Initialize Pygame
        #sound_mana = sounds.SoundManager()
        pygame.init()
        pygame.mixer.init()

        # Screen dimensions
        desktopSize = pygame.display.get_desktop_sizes()

        SCREEN_WIDTH = desktopSize[0][0]
        SCREEN_HEIGHT = desktopSize[0][1]

        # Initialize the screen
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN) # Mode plein écran
        pygame.display.set_caption("Verbal Warfare")
        font = pygame.font.SysFont('arial', 50)

        # Charge l'image de sous fond
        background1 = pygame.image.load(ASSETS_FOLDER + "background.jpg")
        background1 = pygame.transform.scale(background1, (SCREEN_WIDTH, SCREEN_HEIGHT))
        
        # Charge l'image de sous fond
        background = pygame.image.load(ASSETS_FOLDER + "menu.png")
        background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

        # set background color to light red (the png is transparant)
        screen.fill((255, 0, 0))

        is_playing = False
        running = True 
        difficulte = 1
        
        # Main loop
        while running:
            # Draw background image
            screen.blit(background1, (0, 0))
            screen.blit(background, (0, 0))

            # Texte Start et sa collision 
            start = font.render(("DEMARRER"), 1, (255, 255, 255))
            screen.blit(start, (SCREEN_WIDTH * (29/64), SCREEN_HEIGHT/2))
            start_rect = pygame.Rect(SCREEN_WIDTH * (7/16), SCREEN_HEIGHT/2, SCREEN_WIDTH * (1/8), SCREEN_HEIGHT * (5/72))
            

            # Texte vw sans collision
            title = font.render(("VERBAL WARFARE"), 1, (255, 255, 255))
            screen.blit(title, (SCREEN_WIDTH * (13/64), SCREEN_HEIGHT * (5/64)))
            
            # Texte Difficulté et ses boutons
            texte3 = font.render(("Difficulté : "), 1, (255, 255, 255))
            screen.blit(texte3, (SCREEN_WIDTH * (90/1280), SCREEN_HEIGHT * (620/720)))

            # Bouton Facile
            facile_rect = pygame.Rect(SCREEN_WIDTH * (300/1280), SCREEN_HEIGHT * (600/720), SCREEN_WIDTH * (1/8), SCREEN_HEIGHT * (5/72))
            facile = font.render(("Facile"), 1, (255, 255, 255))
            if difficulte == 1:
                facile = font.render(("Facile"), 1, (255, 0, 0))  # Set the color to red if selected
            screen.blit(facile, (SCREEN_WIDTH * (300/1280), SCREEN_HEIGHT * (620/720)))

            # Bouton Moyen
            moyen_rect = pygame.Rect(SCREEN_WIDTH * (500/1280), SCREEN_HEIGHT * (620/720), SCREEN_WIDTH * (1/8), SCREEN_HEIGHT * (5/72))
            moyen = font.render(("Moyen"), 1, (255, 255, 255))
            if difficulte == 2:
                moyen = font.render(("Moyen"), 1, (255, 0, 0))  # Set the color to red if selected
            screen.blit(moyen, (SCREEN_WIDTH * (500/1280), SCREEN_HEIGHT * (620/720)))

            # Bouton Difficile
            difficile_rect = pygame.Rect(SCREEN_WIDTH * (700/1280), SCREEN_HEIGHT * (620/720), SCREEN_WIDTH * (1/8), SCREEN_HEIGHT * (5/72))
            difficile = font.render(("Difficile"), 1, (255, 255, 255))
            if difficulte == 3:
                difficile = font.render(("Difficile"), 1, (255, 0, 0))  # Set the color to red if selected
            screen.blit(difficile, (SCREEN_WIDTH * (700/1280), SCREEN_HEIGHT * (620/720)))

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
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if start_rect.collidepoint(pygame.mouse.get_pos()):
                        is_playing = True
                    elif facile_rect.collidepoint(pygame.mouse.get_pos()):
                        difficulte = 1
                    elif moyen_rect.collidepoint(pygame.mouse.get_pos()):
                        difficulte = 2
                    elif difficile_rect.collidepoint(pygame.mouse.get_pos()):
                        difficulte = 3
                        #Permet de savoir si le jeu est lance ou non
            if is_playing:
                vw_engine.Engine().start(difficulte)
                break
                    
            # Update the display
            if running:
                pygame.display.flip()


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
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if start_rect.collidepoint(pygame.mouse.get_pos()):
                        is_playing = True


            
            # Update the display
            if running:
                pygame.display.flip()

if __name__ == "__main__":
    game = VW_Menu()
    game.start()
