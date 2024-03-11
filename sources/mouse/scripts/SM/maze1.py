import pygame
import sys
import json
from os.path import exists
import os
import sounds

sound_mana = sounds.SoundManager()

# Permet de ce placer dans le dossier contenant les scripts SM
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + "/scripts/SM")
class Maze:
    """
    Classe permettant de récupérer le niveau 
    """
    def __init__(self):
        self.start = False
    def start_chrono(self):
        # Clock for controlling the frame rate
        clock = pygame.time.Clock()
        starting_tick = pygame.time.get_ticks()


    def start_maze(self):
        # Initialize Pygame
        pygame.init()
        pygame.mixer.init()

        # Screen dimensions
        desktopSize = pygame.display.get_desktop_sizes()

        SCREEN_WIDTH = desktopSize[0][0]
        SCREEN_HEIGHT = desktopSize[0][1]
        

        # Initialize the screen
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN) # Mode plein écran
        pygame.display.set_caption("Scary maze or not?")


        screen.fill((0, 0, 0))

        #Position utilisable
        x = 50
        y = 150

        #Chargement bg si il y a 
        bg = None

        #Variable running
        running = True
        song_played = False
        win = False
        niveau = 1

        
        font = pygame.font.Font('sources/mouse/fonts/VCR_OSD_MONO.ttf', 50)
        # Main loop
        while running:
            

            starting_tick = 0
            current_tick = pygame.time.get_ticks() - starting_tick
            

            mouseX = pygame.mouse.get_pos()[0]
            mouseY = pygame.mouse.get_pos()[1]

            # Dès que on réussi le niveau + lvl suivant
            if song_played == False:
                if win == True:
                    sound_mana.play('confetti')
                    screen.fill((0, 0, 0))
                    win = False
                    song_played = True
                    self.start = False
                    timer = current_tick / 1000
                    screen.blit(screen, (0, 0))
                    time = font.render(("Total Time : " + str(timer)), 1, (255, 255, 255))
                    screen.blit(time, (SCREEN_WIDTH/2 - 120, SCREEN_HEIGHT/2 - 30))
                    
                    
                    wait1 = font.render(("."), 1, (255, 255, 255))
                    wait2 = font.render((".."), 1, (255, 255, 255))
                    wait3 = font.render(("..."), 1, (255, 255, 255))

                    for i in range (0, 3):
                        
                        if i == 0:
                            screen.blit(wait1, (SCREEN_WIDTH/2 - 105, SCREEN_HEIGHT/2 - 10))
                        elif i == 1:
                            screen.blit(wait2, (SCREEN_WIDTH/2 - 105, SCREEN_HEIGHT/2 - 10))
                        elif i == 2:
                            screen.blit(wait3, (SCREEN_WIDTH/2 - 105, SCREEN_HEIGHT/2 - 10))
                            # Update the display
                        pygame.display.flip()
                        pygame.time.delay(1000)
                    
                    pygame.time.delay(1000)

                    #Lancement du niveau suivant
                    niveau += 1
                    


            
            ## Création niveau 

            #Niveau 1
            if niveau == 1:
                ractangle = (x, y, SCREEN_WIDTH/2, SCREEN_HEIGHT * 0.2)
                starting_tick = pygame.time.get_ticks()
                # Clock for controlling the frame rate
                self.start_chrono()
                song_played = False
                #Arrière plan
                screen.fill((0, 0, 0))
                screen.blit(screen, (0, 0))

                # Création début et fin
                deb = (SCREEN_WIDTH * (9/128), SCREEN_HEIGHT * (43/144), SCREEN_WIDTH * (1/128), SCREEN_HEIGHT * (1/72))
                fin = (650-10, 225-10, 10, 10)
                # Création bord et mur
                rect_zone = pygame.draw.rect(screen, (255, 0, 0), ractangle)
                #Création carré debut et fin 
                deb_rect = pygame.draw.rect(screen, (35, 150, 245), deb)
                fin_rect = pygame.draw.rect(screen, (35, 150, 245), fin)
                # Met le cursor sur le départ
                if not self.start:
                    pygame.mouse.set_pos([95, 220])
                    self.start = True
                # Boucle qui vérifie que l'on est bien dans le niveau + affiche le titre du niveau
                title = font.render(("Maze 1"), 1, (255, 255, 255))
                screen.blit(title, (SCREEN_WIDTH/2 - 95, SCREEN_HEIGHT/2 - 70))

                if not rect_zone.collidepoint(pygame.mouse.get_pos()):
                    sound_mana.play('OOB')
                    pygame.mouse.set_pos([95, 220])
                
                if fin_rect.collidepoint(pygame.mouse.get_pos()):
                    win = True
                

            #Niveau 2
            if niveau == 2  :
                ractangle = (x, y, SCREEN_WIDTH/2, SCREEN_HEIGHT * 0.2)
                ractangle2 = (SCREEN_WIDTH/2 - 50 , 300 + SCREEN_HEIGHT * 0.2, SCREEN_WIDTH/2, SCREEN_HEIGHT * 0.2)
                
                # Clock for controlling the frame rate
                self.start_chrono()

                tp_used = False
                song_played = False
                #Arrière plan
                screen.fill((0, 0, 0))
                screen.blit(screen, (0, 0))

                # Création début et fin
                deb = (100-10, 225-10, 10, 10)
                tp = (650-10, 225-10, 10, 10)
                tp2 = (650-10, 510, 10, 10)
                fin = (1180, 510, 10, 10)
                # Création bord et mur
                rect_zone = pygame.draw.rect(screen, (255, 0, 0), ractangle)
                rect_zone2 = pygame.draw.rect(screen, (255, 0, 0), ractangle2)
                #Création carré debut et fin 
                deb_rect = pygame.draw.rect(screen, (35, 150, 245), deb)
                fin_rect2 = pygame.draw.rect(screen, (35, 150, 245), fin)
                tp_rect = pygame.draw.rect(screen, (230, 230, 50), tp)
                tp2_rect = pygame.draw.rect(screen, (230, 230, 50), tp2)
                # Met le cursor sur le départ
                if not self.start:
                    pygame.mouse.set_pos([95, 220])
                    self.start = True
                # Boucle qui vérifie que l'on est bien dans le niveau + affiche le titre du niveau
                title = font.render(("Maze 2"), 1, (255, 255, 255))
                screen.blit(title, (SCREEN_WIDTH/2 - 95, SCREEN_HEIGHT/2 - 10))

                if not rect_zone.collidepoint(pygame.mouse.get_pos()):
                    if not rect_zone2.collidepoint(pygame.mouse.get_pos()):
                        sound_mana.play('OOB')
                        pygame.mouse.set_pos([95, 220])

                if fin_rect2.collidepoint(pygame.mouse.get_pos()):
                    win = True
                if tp_rect.collidepoint(pygame.mouse.get_pos()):
                    sound_mana.play('tp')
                    pygame.mouse.set_pos([645, 515])


            #Niveau 3
            if niveau == 3:
                ractangle = (x + 20, y + 50, SCREEN_WIDTH - 160, 35)
                starting_tick = pygame.time.get_ticks()
                # Clock for controlling the frame rate
                self.start_chrono()
                song_played = False
                #Arrière plan
                screen.fill((0, 0, 0))
                screen.blit(screen, (0, 0))

                # Création début et fin
                deb = (100-10, 225-10, 10, 10)
                fin = (1170-10, 225-10, 10, 10)
                # Création bord et mur
                rect_zone = pygame.draw.rect(screen, (255, 0, 0), ractangle)
                #Création carré debut et fin 
                deb_rect = pygame.draw.rect(screen, (35, 150, 245), deb)
                fin_rect = pygame.draw.rect(screen, (35, 150, 245), fin)
                # Met le cursor sur le départ
                if not self.start:
                    pygame.mouse.set_pos([95, 220])
                    self.start = True
                # Boucle qui vérifie que l'on est bien dans le niveau + affiche le titre du niveau
                title = font.render(("Maze 3"), 1, (255, 255, 255))
                screen.blit(title, (SCREEN_WIDTH/2 - 95, SCREEN_HEIGHT/2 - 220))

                if not rect_zone.collidepoint(pygame.mouse.get_pos()):
                    sound_mana.play('OOB')
                    pygame.mouse.set_pos([95, 220])
                
                if fin_rect.collidepoint(pygame.mouse.get_pos()):
                    win = True


            #Pour gérer les évenements
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
                
            
            
            # Cap the frame rate
            # clock.tick(60)
            # Update the display
            if running:
                pygame.display.flip()
            #sys.exit()

if __name__ == "__main__":
    maze = Maze()
    maze.start_maze()