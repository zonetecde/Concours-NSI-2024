import sys
import os
import sounds
import pygame

# Permet de ce placer dans le dossier contenant les scripts VW
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + "/scripts/vw")

import vw_engine

class VW:
    def __init__(self):
        self.folder = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    def start(self):
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

        #Position utilisable
        x = SCREEN_WIDTH * (50/1280)
        y = SCREEN_HEIGHT * (150/720)

        is_playing = False
        running = True 

        # Main loop
        while running:
            #Permet de savoir si le jeu est lance ou non
            if is_playing:
                vw_engine.Jeu().start()
                break

            # Texte Start et sa collision 
            start = font.render(("START"), 1, (255, 255, 255))
            screen.blit(start, (SCREEN_WIDTH * (29/64), SCREEN_HEIGHT/2))
            start_rect = pygame.Rect(SCREEN_WIDTH * (7/16), SCREEN_HEIGHT/2, SCREEN_WIDTH * (1/8), SCREEN_HEIGHT * (5/72))
            
            font2 = pygame.font.SysFont("monospace", 35, bold=True, italic=False)
            click = font2.render(("(click)"), 1, (255, 255, 255))
            screen.blit(click, (SCREEN_WIDTH * (29/64), SCREEN_HEIGHT * (400/720)))


            # Texte Scary maze sans collision
            title = font.render(("VERBAL WARFARE"), 1, (255, 255, 255))
            screen.blit(title, (SCREEN_WIDTH * (13/64), SCREEN_HEIGHT * (5/64)))

            #Texte explicatif du jeu
            texte = font.render(("MENU 0% COPIE DE SM"), 1, (255, 255, 255))
            screen.blit(texte, (SCREEN_WIDTH * (150/1280), SCREEN_HEIGHT * (520/720)))

            texte2 = font.render(("Je maintiens que kill the rayane ça aurait plus rigolo"), 1, (255, 255, 255))
            screen.blit(texte2, (SCREEN_WIDTH * (120/1280), SCREEN_HEIGHT * (570/720)))

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
    game = VW()
    game.start()
