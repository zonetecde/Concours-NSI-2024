import sys
import os

# Permet de ce placer dans le dossier contenant les scripts SM
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + "/scripts/SM")

import pygame
import json
from os.path import exists

import sounds

sound_mana = sounds.SoundManager()

# Screen dimensions
desktopSize = pygame.display.get_desktop_sizes()
SCREEN_WIDTH = desktopSize[0][0]
SCREEN_HEIGHT = desktopSize[0][1]

class Maze:
    """
    Classe permettant de récupérer le niveau 
    """
    def __init__(self):
        self.start = False
        self.spawn = ()
        self.x_lvl4 = SCREEN_WIDTH * (160/1280)
        self.x_mov_lvl5 = SCREEN_WIDTH * (250/1280)
        self.y1_mov_lvl6 = SCREEN_HEIGHT * (0/720)
        self.y2_mov_lvl6 = SCREEN_HEIGHT * (300/720)
        self.x_lvl8 = SCREEN_WIDTH * (355/1280)
        self.y1_lvl9 = SCREEN_HEIGHT * (70/720)
        self.y2_lvl9 = SCREEN_HEIGHT * (350/720)


    def start_maze(self):
        # Initialize Pygame
        pygame.init()
        pygame.mixer.init()

        

        # Initialize the screen
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN) # Mode plein écran
        pygame.display.set_caption("Scary maze or not?")


        screen.fill((0, 0, 0))

        #Position utilisable
        x = SCREEN_WIDTH * (50/1280)
        y = SCREEN_HEIGHT * (150/720)

        #Chargement bg si il y a 
        bg = None
        
        # Font for all of the game
        font = pygame.font.Font('sources/mouse/fonts/VCR_OSD_MONO.ttf', 50)

        #Variable running
        running = True
        song_played = False
        win = False
        niveau = 9
        
        all_timer = 0

        #for lvl4
        couleur_rect_inv = 0
        sfx = False

        #for lvl5
        position = "right"
        
        
        #for lvl6
        position1_lvl6 = "up"
        position2_lvl6 = "down"
        
        #for lvl7
        couleur_rect_invi = 0
        
        couleur_rect_fake = 255

        #for lvl8
        couleur_fin = 0
        couleur_rect_invicible = 0
        song_troll = False

        # for lvl8
        trap_color = 0

        #for lvl9
        timeTick = pygame.time.get_ticks()
        waitTime = 5000 #ms

        # Main loop
        while running:
            

            
        
            

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
                    timer = float(total_time)
                    all_timer += timer
                    all_timer = round(all_timer, 2)
                    screen.blit(screen, (0, 0))
                    time = font.render(("Time : " + str(timer)), 1, (255, 255, 255))
                    all_time = font.render(("Total time : " + str(all_timer)), 1, (255, 255, 255))
                    screen.blit(time, (SCREEN_WIDTH * (13/32), SCREEN_HEIGHT * 11/24))
                    screen.blit(all_time, (SCREEN_WIDTH * (13/32), SCREEN_HEIGHT * (37/72)))
                    
                    
                    wait1 = font.render(("."), 1, (255, 255, 255))
                    wait2 = font.render((".."), 1, (255, 255, 255))
                    wait3 = font.render(("..."), 1, (255, 255, 255))

                    for i in range (0, 3):
                        
                        if i == 0:
                            screen.blit(wait1, (SCREEN_WIDTH * (109/256), SCREEN_HEIGHT * (13/24)))
                        elif i == 1:
                            screen.blit(wait2, (SCREEN_WIDTH * (109/256), SCREEN_HEIGHT * (13/24)))
                        elif i == 2:
                            screen.blit(wait3, (SCREEN_WIDTH * (109/256), SCREEN_HEIGHT * (13/24)))
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
                
                # Stop the song to be played only once
                song_played = False
                #Arrière plan
                screen.fill((0, 0, 0))
                screen.blit(screen, (0, 0))

                # Création début et fin
                deb = (SCREEN_WIDTH * (9/128), SCREEN_HEIGHT * (43/144), SCREEN_WIDTH * (1/128), SCREEN_HEIGHT * (1/72))
                fin = (SCREEN_WIDTH * 0.5, SCREEN_HEIGHT * (43/144), SCREEN_WIDTH * (1/128), SCREEN_HEIGHT * (1/72))
                # Création bord et mur
                rect_zone = pygame.draw.rect(screen, (255, 0, 0), ractangle)
                #Création carré debut et fin 
                deb_rect = pygame.draw.rect(screen, (35, 150, 245), deb)
                fin_rect = pygame.draw.rect(screen, (35, 150, 245), fin)
                # Met le cursor sur le départ
                if not self.start:
                    pygame.mouse.set_pos([deb[0], deb[1]])
                    starting_tick = pygame.time.get_ticks()
                    self.start = True
                # Boucle qui vérifie que l'on est bien dans le niveau + affiche le titre du niveau
                title = font.render(("Maze 1"), 1, (255, 255, 255))
                screen.blit(title, (SCREEN_WIDTH * (109/256), SCREEN_HEIGHT * (29/72)))

                if not rect_zone.collidepoint(pygame.mouse.get_pos()):
                    sound_mana.play('OOB')
                    pygame.mouse.set_pos([deb[0], deb[1]])
                
                #Condition victory
                if fin_rect.collidepoint(pygame.mouse.get_pos()):
                    win = True
                    end_tick = pygame.time.get_ticks()
                    total_time = str((end_tick - starting_tick)/1000)[0:4]
                

            #Niveau 2
            elif niveau == 2  :
                ractangle = (x, y, SCREEN_WIDTH/2, SCREEN_HEIGHT * 0.2)
                ractangle2 = (SCREEN_WIDTH * (59/128) , SCREEN_HEIGHT * (11/18), SCREEN_WIDTH/2, SCREEN_HEIGHT * 0.2)
                
                # Stop the song to be played only once
                song_played = False
                #Arrière plan
                screen.fill((0, 0, 0))
                screen.blit(screen, (0, 0))

                # Création début et fin
                deb = (SCREEN_WIDTH * (9/128), SCREEN_HEIGHT * (43/144), SCREEN_WIDTH * (1/128), SCREEN_HEIGHT * (1/72))
                tp = (SCREEN_WIDTH * 0.5, SCREEN_HEIGHT * (43/144), SCREEN_WIDTH * (1/128), SCREEN_HEIGHT * (1/72))
                tp2 = (SCREEN_WIDTH/2, SCREEN_HEIGHT * (17/24), SCREEN_WIDTH * (1/128), SCREEN_HEIGHT * (1/72))
                fin = (SCREEN_WIDTH * (59/64), SCREEN_HEIGHT * (17/24), SCREEN_WIDTH * (1/128), SCREEN_HEIGHT * (1/72))
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
                    starting_tick = pygame.time.get_ticks()
                    self.start = True
                # Boucle qui vérifie que l'on est bien dans le niveau + affiche le titre du niveau
                title = font.render(("Maze 2"), 1, (255, 255, 255))
                screen.blit(title, (SCREEN_WIDTH * (109/256), SCREEN_HEIGHT * (35/72)))

                if not rect_zone.collidepoint(pygame.mouse.get_pos()):
                    if not rect_zone2.collidepoint(pygame.mouse.get_pos()):
                        sound_mana.play('OOB')
                        pygame.mouse.set_pos([deb[0], deb[1]])

                #Condition victory
                if fin_rect2.collidepoint(pygame.mouse.get_pos()):
                    win = True
                    end_tick = pygame.time.get_ticks()
                    total_time = str((end_tick - starting_tick)/1000)[0:4]
                #Nous téléportent si on est sur le tp
                if tp_rect.collidepoint(pygame.mouse.get_pos()):
                    sound_mana.play('tp')
                    pygame.mouse.set_pos([tp2[0], tp2[1]])


            #Niveau 3
            elif niveau == 3:
                ractangle = (SCREEN_WIDTH * (70/1280), SCREEN_HEIGHT * (200/720), SCREEN_WIDTH * (7/8), SCREEN_HEIGHT * (7/144))
                
                # Stop the song to be played only once
                song_played = False
                #Arrière plan
                screen.fill((0, 0, 0))
                screen.blit(screen, (0, 0))

                # Création début et fin
                deb = (SCREEN_WIDTH * (9/128), SCREEN_HEIGHT * (43/144), SCREEN_WIDTH * (1/128), SCREEN_HEIGHT * (1/72))
                fin = (SCREEN_WIDTH * (29/32), SCREEN_HEIGHT * (43/144), SCREEN_WIDTH * (1/128), SCREEN_HEIGHT * (1/72))
                # Création bord et mur
                rect_zone = pygame.draw.rect(screen, (255, 0, 0), ractangle)
                #Création carré debut et fin 
                deb_rect = pygame.draw.rect(screen, (35, 150, 245), deb)
                fin_rect = pygame.draw.rect(screen, (35, 150, 245), fin)
                # Met le cursor sur le départ
                if not self.start:
                    pygame.mouse.set_pos([deb[0], deb[1]])
                    starting_tick = pygame.time.get_ticks()
                    self.start = True
                # Boucle qui vérifie que l'on est bien dans le niveau + affiche le titre du niveau
                title = font.render(("Maze 3"), 1, (255, 255, 255))
                screen.blit(title, (SCREEN_WIDTH * (109/256), SCREEN_HEIGHT* (7/36)))

                if not rect_zone.collidepoint(pygame.mouse.get_pos()):
                    sound_mana.play('OOB')
                    pygame.mouse.set_pos([deb[0], deb[1]])
                
                #Condition victory
                if fin_rect.collidepoint(pygame.mouse.get_pos()):
                    win = True
                    end_tick = pygame.time.get_ticks()
                    total_time = str((end_tick - starting_tick)/1000)[0:4]


            #Niveau 4
            elif niveau == 4:
                ractangle_inv = ((self.x_lvl4 , SCREEN_HEIGHT * (170/720), SCREEN_WIDTH * (680/1280), SCREEN_HEIGHT * 0.14))
                carre_fin = ((SCREEN_WIDTH * (750/1280), SCREEN_HEIGHT * (170/720), SCREEN_WIDTH * (100/1280), SCREEN_HEIGHT * 0.14))
                ractangle = (x , SCREEN_HEIGHT * (170/720), SCREEN_WIDTH * (100/1280), SCREEN_HEIGHT * (300/720))
                ractangle2 = (x, SCREEN_HEIGHT * (370/720), SCREEN_WIDTH * (200/1280), SCREEN_HEIGHT * (100/720))

                
                # Stop the song to be played only once
                song_played = False
                #Arrière plan
                screen.fill((0, 0, 0))
                screen.blit(screen, (0, 0))

                # Création début et fin
                deb = (SCREEN_WIDTH * (9/128), SCREEN_HEIGHT * (43/144), SCREEN_WIDTH * (1/128), SCREEN_HEIGHT * (1/72))
                fin = (SCREEN_WIDTH * 0.62, SCREEN_HEIGHT * (43/144), SCREEN_WIDTH * (1/128), SCREEN_HEIGHT * (1/72))
                trig = (SCREEN_WIDTH * (200/1280), SCREEN_HEIGHT * (420/720), SCREEN_WIDTH * (1/128), SCREEN_HEIGHT * (1/72))
                # Création bord et mur
                
                rect_zone_inv = pygame.draw.rect(screen, (couleur_rect_inv, 0, 0), ractangle_inv)
                carre_zone = pygame.draw.rect(screen, (255, 0, 0), carre_fin)
                rect_zone1 = pygame.draw.rect(screen, (255, 0, 0), ractangle)
                rect_zone2 = pygame.draw.rect(screen, (255, 0, 0), ractangle2)
                #Création carré debut et fin 
                deb_rect = pygame.draw.rect(screen, (35, 150, 245), deb)
                fin_rect = pygame.draw.rect(screen, (35, 150, 245), fin)
                trigger = pygame.draw.rect(screen, (30, 250, 30), trig)
                # Met le cursor sur le départ
                if not self.start:
                    pygame.mouse.set_pos([deb[0], deb[1]])
                    starting_tick = pygame.time.get_ticks()
                    self.start = True
                    
                # Boucle qui vérifie que l'on est bien dans le niveau + affiche le titre du niveau
                title = font.render(("Maze 4"), 1, (255, 255, 255))
                screen.blit(title, (SCREEN_WIDTH * (109/256), SCREEN_HEIGHT* (6/36)))

                if not rect_zone_inv.collidepoint(pygame.mouse.get_pos()):
                    if not rect_zone1.collidepoint(pygame.mouse.get_pos()):
                        if not rect_zone2.collidepoint(pygame.mouse.get_pos()):
                            if not carre_zone.collidepoint(pygame.mouse.get_pos()):
                                sound_mana.play('OOB')
                                pygame.mouse.set_pos([deb[0], deb[1]])
                
                #Condition victory
                if fin_rect.collidepoint(pygame.mouse.get_pos()):
                    win = True
                    end_tick = pygame.time.get_ticks()
                    total_time = str((end_tick - starting_tick)/1000)[0:4]
                #Si on est dans le trigger le rectangle apparait
                if trigger.collidepoint(pygame.mouse.get_pos()):
                    if not sfx:
                        sound_mana.play('switch')
                        couleur_rect_inv = 255
                        sfx = True
                        self.x_lvl4 = SCREEN_WIDTH * (100/1280)

            #Niveau 5
            elif niveau == 5:
                carre_deb = (x, y, SCREEN_WIDTH * (200/1280), SCREEN_HEIGHT * 0.2)
                carre_fin = (SCREEN_WIDTH * (800/1280), y, SCREEN_WIDTH * (150/1280), SCREEN_HEIGHT * 0.2)
                ractangle = (self.x_mov_lvl5, y , SCREEN_WIDTH * (300/1280), SCREEN_HEIGHT * 0.2)
                
                # Stop the song to be played only once
                song_played = False
                #Arrière plan
                screen.fill((0, 0, 0))
                screen.blit(screen, (0, 0))
                #Titre caché derrière
                title = font.render(("Maze 5"), 1, (255, 255, 255))
                screen.blit(title, (SCREEN_WIDTH * (120/256), SCREEN_HEIGHT * (24/72)))

                # Création début et fin
                deb = (SCREEN_WIDTH * (9/128), SCREEN_HEIGHT * (43/144), SCREEN_WIDTH * (1/128), SCREEN_HEIGHT * (1/72))
                fin = (SCREEN_WIDTH * 0.72, SCREEN_HEIGHT * (43/144), SCREEN_WIDTH * (1/128), SCREEN_HEIGHT * (1/72))
                # Création bord et mur
                rect_zone = pygame.draw.rect(screen, (255, 0, 0), ractangle)
                carre_zone = pygame.draw.rect(screen, (255, 0, 0), carre_deb)
                carre_zone2 = pygame.draw.rect(screen, (255, 0, 0), carre_fin)
                #Création carré debut et fin 
                deb_rect = pygame.draw.rect(screen, (35, 150, 245), deb)
                fin_rect = pygame.draw.rect(screen, (35, 150, 245), fin)
                # Met le cursor sur le départ
                if not self.start:
                    pygame.mouse.set_pos([deb[0], deb[1]])
                    starting_tick = pygame.time.get_ticks()
                    self.start = True
                # Boucle qui vérifie que l'on est bien dans le niveau + affiche le titre du niveau
                

                if not carre_zone.collidepoint(pygame.mouse.get_pos()):
                    if not rect_zone.collidepoint(pygame.mouse.get_pos()):
                        if not carre_zone2.collidepoint(pygame.mouse.get_pos()):
                            sound_mana.play('OOB')
                            pygame.mouse.set_pos([deb[0], deb[1]])
                
                #Permet de faire bouger le rectangle
                if self.x_mov_lvl5 >= SCREEN_WIDTH * (150/1280) and position == "left":
                    rect_zone.move(self.x_mov_lvl5, y)
                    self.x_mov_lvl5 += 1
                    if self.x_mov_lvl5 == SCREEN_WIDTH * (650/1280):
                        position = "right"
                    pygame.display.flip()
                elif self.x_mov_lvl5 <= SCREEN_WIDTH * (650/1280):
                    rect_zone.move(self.x_mov_lvl5, y)
                    self.x_mov_lvl5 -= 1
                    if self.x_mov_lvl5 == SCREEN_WIDTH * (150/1280):
                        position = "left"
                    pygame.display.flip()

                #Condition victory
                if fin_rect.collidepoint(pygame.mouse.get_pos()):
                    win = True
                    end_tick = pygame.time.get_ticks()
                    total_time = str((end_tick - starting_tick)/1000)[0:4]




            #Niveau 6
            elif niveau == 6:
                carre_deb = (x, y, SCREEN_WIDTH * (200/1280), SCREEN_HEIGHT * 0.2)
                carre_fin = (SCREEN_WIDTH *(800/1280), y, SCREEN_WIDTH * (150/1280), SCREEN_HEIGHT * 0.2)
                ractangle = (SCREEN_WIDTH * (250/1280), self.y1_mov_lvl6 , SCREEN_WIDTH * (300/1280), SCREEN_HEIGHT * 0.2)
                ractangle2 = (SCREEN_WIDTH * (550/1280), self.y2_mov_lvl6, SCREEN_WIDTH * (300/1280), SCREEN_HEIGHT * 0.2)
                
                # Stop the song to be played only once
                song_played = False
                #Arrière plan
                screen.fill((0, 0, 0))
                screen.blit(screen, (0, 0))
                #Titre caché derrière
                title = font.render(("Maze 6"), 1, (255, 255, 255))
                screen.blit(title, (SCREEN_WIDTH * (120/256), SCREEN_HEIGHT * (24/72)))

                # Création début et fin
                deb = (SCREEN_WIDTH * (9/128), SCREEN_HEIGHT * (43/144), SCREEN_WIDTH * (1/128), SCREEN_HEIGHT * (1/72))
                fin = (SCREEN_WIDTH * 0.72, SCREEN_HEIGHT * (43/144), SCREEN_WIDTH * (1/128), SCREEN_HEIGHT * (1/72))
                # Création bord et mur
                rect_zone = pygame.draw.rect(screen, (255, 0, 0), ractangle)
                rect2_zone = pygame.draw.rect(screen, (255, 0, 0), ractangle2)
                carre_zone = pygame.draw.rect(screen, (255, 0, 0), carre_deb)
                carre_zone2 = pygame.draw.rect(screen, (255, 0, 0), carre_fin)
                #Création carré debut et fin 
                deb_rect = pygame.draw.rect(screen, (35, 150, 245), deb)
                fin_rect = pygame.draw.rect(screen, (35, 150, 245), fin)
                # Met le cursor sur le départ
                if not self.start:
                    pygame.mouse.set_pos([deb[0], deb[1]])
                    starting_tick = pygame.time.get_ticks()
                    self.start = True
                # Boucle qui vérifie que l'on est bien dans le niveau 
                if not carre_zone.collidepoint(pygame.mouse.get_pos()):
                    if not rect_zone.collidepoint(pygame.mouse.get_pos()):
                        if not rect2_zone.collidepoint(pygame.mouse.get_pos()):
                            if not carre_zone2.collidepoint(pygame.mouse.get_pos()):
                                sound_mana.play('OOB')
                                pygame.mouse.set_pos([deb[0], deb[1]])
                
                #Permet de faire bouger le rectangle1
                if self.y1_mov_lvl6 >= SCREEN_HEIGHT * (0/720) and position1_lvl6 == "up":
                    rect_zone.move(SCREEN_WIDTH * (250/1280), self.y1_mov_lvl6)
                    self.y1_mov_lvl6 += 1
                    if self.y1_mov_lvl6 == SCREEN_HEIGHT * (300/720):
                        position1_lvl6 = "down"
                    pygame.display.flip()
                elif self.y1_mov_lvl6 <= SCREEN_HEIGHT * (300/720):
                    rect_zone.move(SCREEN_WIDTH * (250/1280), self.y1_mov_lvl6)
                    self.y1_mov_lvl6 -= 1
                    if self.y1_mov_lvl6 == SCREEN_HEIGHT * (0/720):
                        position1_lvl6 = "up"
                    pygame.display.flip()

                #Permet de faire bouger le rectangle2
                if self.y2_mov_lvl6 >= SCREEN_HEIGHT * (0/720) and position2_lvl6 == "up":
                    rect2_zone.move(SCREEN_WIDTH * (450/1280), self.y2_mov_lvl6)
                    self.y2_mov_lvl6 += 1
                    if self.y2_mov_lvl6 == SCREEN_HEIGHT * (300/720):
                        position2_lvl6 = "down"
                    pygame.display.flip()
                elif self.y2_mov_lvl6 <= SCREEN_HEIGHT * (300/720):
                    rect2_zone.move(SCREEN_WIDTH * (450/1280), self.y2_mov_lvl6)
                    self.y2_mov_lvl6 -= 1
                    if self.y2_mov_lvl6 == SCREEN_HEIGHT * (0/720):
                        print(self.y2_mov_lvl6)
                        position2_lvl6 = "up"
                    pygame.display.flip()

                #Condition victory
                if fin_rect.collidepoint(pygame.mouse.get_pos()):
                    win = True
                    end_tick = pygame.time.get_ticks()
                    total_time = str((end_tick - starting_tick)/1000)[0:4]



            #Niveau 7
            elif niveau == 7:
                ractangle_inv1 = (SCREEN_WIDTH * (250/1280) , SCREEN_HEIGHT * (170/720), SCREEN_WIDTH * (100/1280), SCREEN_HEIGHT * (300/720))
                ractangle_inv2 = (SCREEN_WIDTH * (250/1280), SCREEN_HEIGHT * (450/720), SCREEN_WIDTH * (600/1280), SCREEN_HEIGHT * 0.14)
                ractangle_inv3 = (SCREEN_WIDTH * (750/1280), SCREEN_HEIGHT * (170/720), SCREEN_WIDTH * (100/1280), SCREEN_HEIGHT * (300/720))
                carre_fin = ((SCREEN_WIDTH * (750/1280), SCREEN_HEIGHT * (170/720), SCREEN_WIDTH * (100/1280), SCREEN_HEIGHT * 0.14))
                
                ractangle = (x, SCREEN_HEIGHT * (170/720), SCREEN_WIDTH * (300/1280), SCREEN_HEIGHT * (100/720))
                fake_rect = (x, SCREEN_HEIGHT * (170/720), SCREEN_WIDTH * (800/1280), SCREEN_HEIGHT * (100/720))

                
                # Stop the song to be played only once
                song_played = False
                #Arrière plan
                screen.fill((0, 0, 0))
                screen.blit(screen, (0, 0))

                # Création début et fin
                deb = (SCREEN_WIDTH * (9/128), SCREEN_HEIGHT * (43/144), SCREEN_WIDTH * (1/128), SCREEN_HEIGHT * (1/72))
                fin = (SCREEN_WIDTH * (0.62), SCREEN_HEIGHT * (43/144), SCREEN_WIDTH * (1/128), SCREEN_HEIGHT * (1/72))
                trig = (SCREEN_WIDTH * (330/1280), SCREEN_HEIGHT * (170/720), SCREEN_WIDTH * (2/128), SCREEN_HEIGHT * (10/72))
                

                #Création du fake chemin
                fake_rect = pygame.draw.rect(screen, (couleur_rect_fake, 0, 0), fake_rect)

                #Texte cacher sous le fake 
                if couleur_rect_fake == 0:
                    title = font.render(("Maze 7"), 1, (255, 255, 255))
                    screen.blit(title, (SCREEN_WIDTH * (109/256), SCREEN_HEIGHT* (9/36)))
                

                # Création bord et mur
                rect_zone_inv = pygame.draw.rect(screen, (couleur_rect_invi, 0, 0), ractangle_inv1)
                rect_zone_inv2 = pygame.draw.rect(screen, (couleur_rect_invi, 0, 0), ractangle_inv2)
                rect_zone_inv3 = pygame.draw.rect(screen, (couleur_rect_invi, 0, 0), ractangle_inv3)
                carre_zone = pygame.draw.rect(screen, (255, 0, 0), carre_fin)
                rect_zone1 = pygame.draw.rect(screen, (255, 0, 0), ractangle)
                
                
                #Création carré debut et fin 
                deb_rect = pygame.draw.rect(screen, (35, 150, 245), deb)
                fin_rect = pygame.draw.rect(screen, (35, 150, 245), fin)
                trigger = pygame.draw.rect(screen, (255, 0, 0), trig)
                # Met le cursor sur le départ
                if not self.start:
                    pygame.mouse.set_pos([deb[0], deb[1]])
                    starting_tick = pygame.time.get_ticks()
                    self.start = True
                    
                # Boucle qui vérifie que l'on est bien dans le niveau 
                if not rect_zone_inv.collidepoint(pygame.mouse.get_pos()):
                    if not rect_zone_inv2.collidepoint(pygame.mouse.get_pos()):
                        if not rect_zone_inv3.collidepoint(pygame.mouse.get_pos()):
                            if not rect_zone1.collidepoint(pygame.mouse.get_pos()):
                                if not carre_zone.collidepoint(pygame.mouse.get_pos()):
                                    sound_mana.play('OOB')
                                    pygame.mouse.set_pos([deb[0], deb[1]])
                
                #Condition victory
                if fin_rect.collidepoint(pygame.mouse.get_pos()):
                    win = True
                    end_tick = pygame.time.get_ticks()
                    total_time = str((end_tick - starting_tick)/1000)[0:4]
                #Si on est dans le trigger le rectangle apparait
                if trigger.collidepoint(pygame.mouse.get_pos()):
                    sound_mana.play('giggle')
                    couleur_rect_invi = 255
                    couleur_rect_fake = 0

            #Niveau 8
            elif niveau == 8:
                ractangle = (x, SCREEN_HEIGHT * (170/720), SCREEN_WIDTH * (300/1280), SCREEN_HEIGHT * (100/720))
                ractangle1 = (SCREEN_WIDTH * (200/1280) , SCREEN_HEIGHT * (170/720), SCREEN_WIDTH * (100/1280), SCREEN_HEIGHT * (300/720))
                ractangle2 = (SCREEN_WIDTH * (200/1280), SCREEN_HEIGHT * (450/720), SCREEN_WIDTH * (450/1280), SCREEN_HEIGHT * 0.11)
                ractangle3 = (SCREEN_WIDTH * (570/1280), SCREEN_HEIGHT * (80/720), SCREEN_WIDTH * (80/1280), SCREEN_HEIGHT * (400/720))
                ractangle4 = (SCREEN_WIDTH * (570/1280), SCREEN_HEIGHT * (30/720), SCREEN_WIDTH * (550/1280), SCREEN_HEIGHT * 0.09)
                ractangle5 = (SCREEN_WIDTH * (1100/1280), SCREEN_HEIGHT * (30/720), SCREEN_WIDTH * (70/1280), SCREEN_HEIGHT * (590/720))
                ractangle6 = (SCREEN_WIDTH * (700/1280), SCREEN_HEIGHT * (570/720), SCREEN_WIDTH * (40/1280), SCREEN_HEIGHT * 0.08)
                ractangle7 = (SCREEN_WIDTH * (700/1280), SCREEN_HEIGHT * (350/720), SCREEN_WIDTH * (60/1280), SCREEN_HEIGHT * (250/720))
                ractangle8 = (SCREEN_WIDTH * (700/1280), SCREEN_HEIGHT * (350/720), SCREEN_WIDTH * (250/1280), SCREEN_HEIGHT * 0.06)
                ractangle9 = (SCREEN_WIDTH * (930/1280), SCREEN_HEIGHT * (190/720), SCREEN_WIDTH * (20/1280), SCREEN_HEIGHT * (160/720))
                ractangle10 = (SCREEN_WIDTH * (800/1280), SCREEN_HEIGHT * (190/720), SCREEN_WIDTH * (150/1280), SCREEN_HEIGHT * 0.025)

                carre_fin = ((SCREEN_WIDTH * (750/1280), SCREEN_HEIGHT * (170/720), SCREEN_WIDTH * (100/1280), SCREEN_HEIGHT * 0.11))
                     
                rect_inv = (self.x_lvl8, SCREEN_HEIGHT * (5/720), SCREEN_WIDTH * (45/1280), SCREEN_HEIGHT * (170/720))

                
                # Stop the song to be played only once
                song_played = False
                #Arrière plan
                screen.fill((0, 0, 0))
                screen.blit(screen, (0, 0))

                # Création début et fin
                deb = (SCREEN_WIDTH * (9/128), SCREEN_HEIGHT * (43/144), SCREEN_WIDTH * (1/128), SCREEN_HEIGHT * (1/72))
                fake_fin = (SCREEN_WIDTH * 0.62, SCREEN_HEIGHT * (43/144), SCREEN_WIDTH * (1/128), SCREEN_HEIGHT * (1/72))
                fin = (SCREEN_WIDTH * (325/1280), SCREEN_HEIGHT * (20/720), SCREEN_WIDTH * (1/128), SCREEN_HEIGHT * (1/72))
                

                

                #Creation titre
                title = font.render(("Maze 8"), 1, (255, 255, 255))
                screen.blit(title, (SCREEN_WIDTH * (355/1280), SCREEN_HEIGHT* (165/720)))
                

                # Création bord et mur
                rect_inv = pygame.draw.rect(screen, (couleur_rect_invicible, 0, 0), rect_inv)
                
                rect_zone = pygame.draw.rect(screen, (255, 0, 0), ractangle1)
                rect_zone1 = pygame.draw.rect(screen, (255, 0, 0), ractangle)
                rect_zone2 = pygame.draw.rect(screen, (255, 0, 0), ractangle2)
                rect_zone3 = pygame.draw.rect(screen, (255, 0, 0), ractangle3)
                rect_zone4 = pygame.draw.rect(screen, (255, 0, 0), ractangle4)
                rect_zone5 = pygame.draw.rect(screen, (255, 0, 0), ractangle5)
                rect_zone6 = pygame.draw.rect(screen, (255, 0, 0), ractangle6)
                rect_zone7 = pygame.draw.rect(screen, (255, 0, 0), ractangle7)
                rect_zone8 = pygame.draw.rect(screen, (255, 0, 0), ractangle8)
                rect_zone9 = pygame.draw.rect(screen, (255, 0, 0), ractangle9)
                rect_zone10 = pygame.draw.rect(screen, (255, 0, 0), ractangle10)

                carre_zone = pygame.draw.rect(screen, (255, 0, 0), carre_fin)
                
                
                
                
                #Création carré debut et fin 
                deb_rect = pygame.draw.rect(screen, (35, 150, 245), deb)
                fin_rect = pygame.draw.rect(screen, (0, 0, couleur_fin), fin)
                fake_fin_rect= pygame.draw.rect(screen, (35, 150, 245), fake_fin)
                # Met le cursor sur le départ
                if not self.start:
                    pygame.mouse.set_pos([deb[0], deb[1]])
                    starting_tick = pygame.time.get_ticks()
                    self.start = True
                    self.spawn = deb
                    
                # Boucle qui vérifie que l'on est bien dans le niveau 
                if not rect_zone.collidepoint(pygame.mouse.get_pos()):
                    if not rect_zone2.collidepoint(pygame.mouse.get_pos()):
                        if not rect_zone3.collidepoint(pygame.mouse.get_pos()):
                            if not rect_zone1.collidepoint(pygame.mouse.get_pos()):
                                if not rect_zone4.collidepoint(pygame.mouse.get_pos()):
                                    if not rect_zone5.collidepoint(pygame.mouse.get_pos()):
                                        if not rect_zone6.collidepoint(pygame.mouse.get_pos()):
                                            if not rect_zone7.collidepoint(pygame.mouse.get_pos()):
                                                if not rect_zone8.collidepoint(pygame.mouse.get_pos()):
                                                    if not rect_zone9.collidepoint(pygame.mouse.get_pos()):
                                                        if not rect_zone10.collidepoint(pygame.mouse.get_pos()):
                                                            if not rect_inv.collidepoint(pygame.mouse.get_pos()):
                                                                if not carre_zone.collidepoint(pygame.mouse.get_pos()):
                                                                    sound_mana.play('OOB')
                                                                    pygame.mouse.set_pos([self.spawn[0], self.spawn[1]])
                                                
                #Condition victory
                if fin_rect.collidepoint(pygame.mouse.get_pos()):
                    win = True
                    end_tick = pygame.time.get_ticks()
                    total_time = str((end_tick - starting_tick)/1000)[0:4]
                #Si on est dans le trigger le rectangle apparait
                if fake_fin_rect.collidepoint(pygame.mouse.get_pos()):
                    if song_troll == False:
                        sound_mana.play('giggle')
                        couleur_rect_invicible = 255
                        couleur_fin = 255
                        song_troll = True
                        self.spawn = fake_fin
                        self.x_lvl8 = SCREEN_WIDTH * (305/1280)
                        rect_inv.move(self.x_lvl8, SCREEN_HEIGHT * (10/720))





            #Niveau 9
            elif niveau == 9:
                ractangle = (x, SCREEN_HEIGHT * (170/720), SCREEN_WIDTH * (300/1280), SCREEN_HEIGHT * (100/720))
                ractangle2 = (SCREEN_WIDTH * (250/1280), SCREEN_HEIGHT * (450/720), SCREEN_WIDTH * (600/1280), SCREEN_HEIGHT * 0.14)
                ractangle3 = (SCREEN_WIDTH * (750/1280), SCREEN_HEIGHT * (170/720), SCREEN_WIDTH * (100/1280), SCREEN_HEIGHT * (300/720))
                carre_fin = ((SCREEN_WIDTH * (750/1280), SCREEN_HEIGHT * (170/720), SCREEN_WIDTH * (100/1280), SCREEN_HEIGHT * 0.14))
                rect_0 = (x, SCREEN_HEIGHT * (170/720), SCREEN_WIDTH * (800/1280), SCREEN_HEIGHT * (100/720))


                #100 de différence avec le chemin
                trap1 = (SCREEN_WIDTH * (350/1280), self.y1_lvl9, SCREEN_WIDTH * (50/1280), SCREEN_HEIGHT * (100/720))
                trap2 = (SCREEN_WIDTH * (500/1280), self.y1_lvl9, SCREEN_WIDTH * (50/1280), SCREEN_HEIGHT * (100/720))
                trap3 = (SCREEN_WIDTH * (650/1280), self.y1_lvl9, SCREEN_WIDTH * (50/1280), SCREEN_HEIGHT * (100/720))

                trap4 = (SCREEN_WIDTH * (450/1280), self.y2_lvl9, SCREEN_WIDTH * (50/1280), SCREEN_HEIGHT * (100/720))
                trap5 = (SCREEN_WIDTH * (550/1280), self.y2_lvl9, SCREEN_WIDTH * (50/1280), SCREEN_HEIGHT * (100/720))
                trap6 = (SCREEN_WIDTH * (650/1280), self.y2_lvl9, SCREEN_WIDTH * (50/1280), SCREEN_HEIGHT * (100/720))
                # Stop the song to be played only once
                song_played = False
                #Arrière plan
                screen.fill((0, 0, 0))
                screen.blit(screen, (0, 0))

                # Création début et fin
                deb = (SCREEN_WIDTH * (9/128), SCREEN_HEIGHT * (43/144), SCREEN_WIDTH * (1/128), SCREEN_HEIGHT * (1/72))
                fin = (SCREEN_WIDTH * (280/1280), SCREEN_HEIGHT * (490/720), SCREEN_WIDTH * (1/128), SCREEN_HEIGHT * (1/72))
                trig = (SCREEN_WIDTH * (330/1280), SCREEN_HEIGHT * (170/720), SCREEN_WIDTH * (2/128), SCREEN_HEIGHT * (10/72))
                

                #Texte cacher sous le fake 
                if couleur_rect_fake == 0:
                    title = font.render(("Maze 9"), 1, (255, 255, 255))
                    screen.blit(title, (SCREEN_WIDTH * (109/256), SCREEN_HEIGHT* (9/36)))
                

                # Création bord et mur
                real_rect = pygame.draw.rect(screen, (255, 0, 0), rect_0)
                rect_zone1 = pygame.draw.rect(screen, (255, 0, 0), ractangle)
                rect_zone2 = pygame.draw.rect(screen, (255, 0, 0), ractangle2)
                rect_zone3 = pygame.draw.rect(screen, (255, 0, 0), ractangle3)
                carre_zone = pygame.draw.rect(screen, (255, 0, 0), carre_fin)

                trap1 = pygame.draw.rect(screen, (trap_color, trap_color, trap_color), trap1)
                trap2 = pygame.draw.rect(screen, (trap_color, trap_color, trap_color), trap2)
                trap3 = pygame.draw.rect(screen, (trap_color, trap_color, trap_color), trap3)
                trap4 = pygame.draw.rect(screen, (trap_color, trap_color, trap_color), trap4)
                trap5 = pygame.draw.rect(screen, (trap_color, trap_color, trap_color), trap5)
                trap6 = pygame.draw.rect(screen, (trap_color, trap_color, trap_color), trap6)
                
                #Création carré debut et fin 
                deb_rect = pygame.draw.rect(screen, (35, 150, 245), deb)
                fin_rect = pygame.draw.rect(screen, (35, 150, 245), fin)
                
                # Met le cursor sur le départ
                if not self.start:
                    pygame.mouse.set_pos([deb[0], deb[1]])
                    starting_tick = pygame.time.get_ticks()
                    self.start = True
                    
                # Boucle qui vérifie que l'on est bien dans le niveau 
                
                if not rect_zone2.collidepoint(pygame.mouse.get_pos()):
                    if not rect_zone3.collidepoint(pygame.mouse.get_pos()):
                        if not rect_zone1.collidepoint(pygame.mouse.get_pos()):
                            if not carre_zone.collidepoint(pygame.mouse.get_pos()):
                                if not real_rect.collidepoint(pygame.mouse.get_pos()):
                                    sound_mana.play('OOB')
                                    pygame.mouse.set_pos([deb[0], deb[1]])
                    
                #Condition victory
                if fin_rect.collidepoint(pygame.mouse.get_pos()):
                    win = True
                    end_tick = pygame.time.get_ticks()
                    total_time = str((end_tick - starting_tick)/1000)[0:4]

                if timeTick > pygame.time.get_ticks() + waitTime:
                    trap_color = 128
                    sound_mana.play("spike")
                    timeTick = pygame.time.get_ticks()

                


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