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
        self.folder = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) 
        #Savoir si le niveau a commencer ou non
        self.start = False
        self.spawn = ()

        #Pour lvl4
        self.x_lvl4 = SCREEN_WIDTH * (160/1280)

        #Pour lvl5
        self.x_mov_lvl5 = SCREEN_WIDTH * (250/1280)

        #Pour lvl6
        self.y1_mov_lvl6 = SCREEN_HEIGHT * (0/720)
        self.y2_mov_lvl6 = SCREEN_HEIGHT * (300/720)

        #Pour lvl9 (ancien lvl8)
        self.x_lvl8 = SCREEN_WIDTH * (355/1280)

        #Pour lvl8 (ancien lvl9)
        self.y1_lvl9 = SCREEN_HEIGHT * (70/720)
        self.y2_lvl9 = SCREEN_HEIGHT * (350/720)

        #Pour lvl10
        self.y_Sreal = SCREEN_HEIGHT * (250/720)
        self.y_Smove = SCREEN_HEIGHT * (350/720)
        
        self.x_Mmove = SCREEN_WIDTH * (450/1280)
        self.y_Mappear = SCREEN_HEIGHT * (260/720)

        self.x_Pappear = SCREEN_WIDTH * (750/1280)
        self.x_spikeP = SCREEN_WIDTH * (660/1280)

        self.y_realK = SCREEN_HEIGHT * (325/720)

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
        
        font = pygame.font.Font(self.folder + '/fonts/VCR_OSD_MONO.ttf', 50)

        #Variable running
        running = True
        song_played = False
        win = False
        niveau = 1
        
        #Total Timer
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


        #for lvl9
        trap_color = 0
        timeTick = pygame.time.get_ticks()
        waitTime = 1000 #ms
        position_lvl9 = "up"

        #for lvl10

        color_fake_S = 255
        positionS = "up"
        positionM = "left"
        color_Mappear = 0
        color_Mtp1 = 0
        color_Mtp2 = 0
        color_Pappear = 0
        trap_colorP = 0
        timeTickP = pygame.time.get_ticks()
        waitTime = 1000 #ms
        position_P = "right"
        color_realK = 0
        color_end1K = 255
        color_end2K = 0
        color_real_endK = 0
        song_troll1 = False
        song_troll2 = False
        song_egg = False
        color_temp1 = 0
        color_temp2 = 255
        newCursor = False
        song_switch1 = False
        song_switch2 = False


        #for lvl11
        texte_write = False

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

            #Niveau 9
            elif niveau == 9:
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
                if not any(rect.collidepoint(pygame.mouse.get_pos()) for rect in [rect_zone, rect_zone2, rect_zone3, rect_zone1, rect_zone4, rect_zone5, rect_zone6, rect_zone7, rect_zone8, rect_zone9, rect_zone10, rect_inv, carre_zone]):
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





            #Niveau 8
            elif niveau == 8:
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
                    
                #Vérifie si on s'est bouffé un spike
                if trap1.collidepoint(pygame.mouse.get_pos()) or trap2.collidepoint(pygame.mouse.get_pos()) or trap3.collidepoint(pygame.mouse.get_pos()) or trap4.collidepoint(pygame.mouse.get_pos()) or trap5.collidepoint(pygame.mouse.get_pos()) or trap6.collidepoint(pygame.mouse.get_pos()):
                    sound_mana.play('OOB')
                    pygame.mouse.set_pos([deb[0], deb[1]])


                #Condition victory
                if fin_rect.collidepoint(pygame.mouse.get_pos()):
                    win = True
                    end_tick = pygame.time.get_ticks()
                    total_time = str((end_tick - starting_tick)/1000)[0:4]

                if timeTick + waitTime < pygame.time.get_ticks() :
                    if position_lvl9 == "up":
                        trap_color = 128
                        sound_mana.play("spike")
                        self.y1_lvl9 = SCREEN_WIDTH * (170/1280)
                        self.y2_lvl9 = SCREEN_WIDTH * (450/1280)
                        timeTick = pygame.time.get_ticks()
                        position_lvl9 = "down"
                    else:
                        trap_color = 0
                        sound_mana.play("spike")
                        self.y1_lvl9 = SCREEN_WIDTH * (70/1280)
                        self.y2_lvl9 = SCREEN_WIDTH * (350/1280)
                        timeTick = pygame.time.get_ticks()
                        position_lvl9 = "up"

                
            # Niveau 10
            elif niveau == 10:
                ractangle_S1 = (SCREEN_WIDTH * (0/1280), SCREEN_HEIGHT * (50/720), SCREEN_WIDTH * (300/1280), SCREEN_HEIGHT * (100/720))
                ractangle_S2 = (SCREEN_WIDTH * (0/1280), SCREEN_HEIGHT * (250/720), SCREEN_WIDTH * (300/1280), SCREEN_HEIGHT * (100/720))
                ractangle_S3 = (SCREEN_WIDTH * (0/1280), SCREEN_HEIGHT * (450/720), SCREEN_WIDTH * (300/1280), SCREEN_HEIGHT * (100/720))

                ractangle_Sreal = (SCREEN_WIDTH * (0/1280), self.y_Sreal, SCREEN_WIDTH * (100/1280), SCREEN_HEIGHT * (100/720))
                ractangle_Sfake = (SCREEN_WIDTH * (200/1280), SCREEN_HEIGHT * (150/720), SCREEN_WIDTH * (100/1280), SCREEN_HEIGHT * (100/720))
                ractangle_Smove = (SCREEN_WIDTH * (200/1280), self.y_Smove, SCREEN_WIDTH * (100/1280), SCREEN_HEIGHT * (100/720))


                ractangle_M1 = (SCREEN_WIDTH * (330/1280), SCREEN_HEIGHT * (50/720), SCREEN_WIDTH * (80/1280), SCREEN_HEIGHT * (500/720))
                ractangle_M2 = (SCREEN_WIDTH * (550/1280), SCREEN_HEIGHT * (50/720), SCREEN_WIDTH * (80/1280), SCREEN_HEIGHT * (200/720))
                ractangle_M3 = (SCREEN_WIDTH * (410/1280), SCREEN_HEIGHT * (130/720), SCREEN_WIDTH * (50/1280), SCREEN_HEIGHT * (100/720))
                ractangle_M4 = (SCREEN_WIDTH * (500/1280), SCREEN_HEIGHT * (130/720), SCREEN_WIDTH * (50/1280), SCREEN_HEIGHT * (100/720))
                ractangle_Mmove = (self.x_Mmove, SCREEN_HEIGHT * (230/720), SCREEN_WIDTH * (60/1280), SCREEN_HEIGHT * (100/720))
                ractangle_Mappear = (SCREEN_WIDTH * (550/1280), self.y_Mappear, SCREEN_WIDTH * (80/1280), SCREEN_HEIGHT * (300/720))

                ractangle_P1 = (self.x_Pappear, SCREEN_HEIGHT * (50/720), SCREEN_WIDTH * (220/1280), SCREEN_HEIGHT * (100/720))
                ractangle_P2 = (SCREEN_WIDTH * (660/1280), SCREEN_HEIGHT * (50/720), SCREEN_WIDTH * (80/1280), SCREEN_HEIGHT * (500/720))
                ractangle_P3 = (SCREEN_WIDTH * (660/1280), SCREEN_HEIGHT * (250/720), SCREEN_WIDTH * (200/1280), SCREEN_HEIGHT * (80/720))
                ractangle_P4 = (SCREEN_WIDTH * (860/1280), SCREEN_HEIGHT * (150/720), SCREEN_WIDTH * (100/1280), SCREEN_HEIGHT * (100/720))
                trap1_P = (self.x_spikeP, SCREEN_HEIGHT * (150/720), SCREEN_WIDTH * (80/1280), SCREEN_HEIGHT * (40/720))
                trap2_P = (self.x_spikeP, SCREEN_HEIGHT * (210/720), SCREEN_WIDTH * (80/1280), SCREEN_HEIGHT * (40/720))
                trap3_P = (self.x_spikeP, SCREEN_HEIGHT * (330/720), SCREEN_WIDTH * (80/1280), SCREEN_HEIGHT * (40/720))
                trap4_P = (self.x_spikeP, SCREEN_HEIGHT * (390/720), SCREEN_WIDTH * (80/1280), SCREEN_HEIGHT * (40/720))
                trap5_P = (self.x_spikeP, SCREEN_HEIGHT * (450/720), SCREEN_WIDTH * (80/1280), SCREEN_HEIGHT * (40/720))

                ractangle_K1 = (SCREEN_WIDTH * (1170/1280), SCREEN_HEIGHT * (50/720), SCREEN_WIDTH * (100/1280), SCREEN_HEIGHT * (160/720))
                ractangle_K2 = (SCREEN_WIDTH * (990/1280), SCREEN_HEIGHT * (50/720), SCREEN_WIDTH * (100/1280), SCREEN_HEIGHT * (500/720))
                ractangle_K3 = (SCREEN_WIDTH * (1090/1280), SCREEN_HEIGHT * (190/720), SCREEN_WIDTH * (90/1280), SCREEN_HEIGHT * (130/720))
                ractangle_K4 = (SCREEN_WIDTH * (1135/1280), self.y_realK, SCREEN_WIDTH * (80/1280), SCREEN_HEIGHT * (90/720))
                ractangle_K5 = (SCREEN_WIDTH * (1170/1280), SCREEN_HEIGHT * (410/720), SCREEN_WIDTH * (100/1280), SCREEN_HEIGHT * (140/720))
                
                
                # Stop the song to be played only once
                song_played = False
                #Arrière plan
                screen.fill((0, 0, 0))
                screen.blit(screen, (0, 0))

                # Création début et fin
                deb = (SCREEN_WIDTH * (10/1280), SCREEN_HEIGHT * (90/720), SCREEN_WIDTH * (1/128), SCREEN_HEIGHT * (1/72))
                fin = (SCREEN_WIDTH * (1210/1280), SCREEN_HEIGHT * (490/720), SCREEN_WIDTH * (1/128), SCREEN_HEIGHT * (1/72))

                trigS = (SCREEN_WIDTH * (200/1280), SCREEN_HEIGHT * (130/720), SCREEN_WIDTH * (100/1280), SCREEN_HEIGHT * (20/720))
                trigM = (SCREEN_WIDTH * (580/1280), SCREEN_HEIGHT * (80/720), SCREEN_WIDTH * (1/128), SCREEN_HEIGHT * (1/72))
                trigP = (SCREEN_WIDTH * (690/1280), SCREEN_HEIGHT * (520/720), SCREEN_WIDTH * (1/128), SCREEN_HEIGHT * (1/72))

                trig_egg = (SCREEN_WIDTH * (760/1280), SCREEN_HEIGHT * (250/720), SCREEN_WIDTH * (80/1280), SCREEN_HEIGHT * (80/720))

                tp1 = (SCREEN_WIDTH * (10/1280), SCREEN_HEIGHT * (490/720), SCREEN_WIDTH * (1/128), SCREEN_HEIGHT * (1/72))
                tp1_end = (SCREEN_WIDTH * (360/1280), SCREEN_HEIGHT * (490/720), SCREEN_WIDTH * (1/128), SCREEN_HEIGHT * (1/72))
                tp2 = (SCREEN_WIDTH * (580/1280), SCREEN_HEIGHT * (490/720), SCREEN_WIDTH * (1/128), SCREEN_HEIGHT * (1/72))
                tp2_end = (SCREEN_WIDTH * (690/1280), SCREEN_HEIGHT * (80/720), SCREEN_WIDTH * (1/128), SCREEN_HEIGHT * (1/72))
                tp3 = (SCREEN_WIDTH * (900/1280), SCREEN_HEIGHT * (190/720), SCREEN_WIDTH * (1/128), SCREEN_HEIGHT * (1/72))
                tp3_end = (SCREEN_WIDTH * (1030/1280), SCREEN_HEIGHT * (490/720), SCREEN_WIDTH * (1/128), SCREEN_HEIGHT * (1/72))


                fake_end1 = (SCREEN_WIDTH * (1210/1280), SCREEN_HEIGHT * (70/720), SCREEN_WIDTH * (1/128), SCREEN_HEIGHT * (1/72))
                fake_end2 = (SCREEN_WIDTH * (1030/1280), SCREEN_HEIGHT * (70/720), SCREEN_WIDTH * (1/128), SCREEN_HEIGHT * (1/72))
                # Création bord et mur
                rect_Sfake = pygame.draw.rect(screen, (color_fake_S, 0, 0), ractangle_Sfake)
                rect_Sreal = pygame.draw.rect(screen, (255, 0, 0), ractangle_Sreal)
                rect_Smove = pygame.draw.rect(screen, (255, 0, 0), ractangle_Smove)
                rect_S1 = pygame.draw.rect(screen, (255, 0, 0), ractangle_S1)
                rect_S2 = pygame.draw.rect(screen, (255, 0, 0), ractangle_S2)
                rect_S3 = pygame.draw.rect(screen, (255, 0, 0), ractangle_S3)
                

                rect_Mappear = pygame.draw.rect(screen, (color_Mappear, 0, 0), ractangle_Mappear)
                rect_Mmove = pygame.draw.rect(screen, (255, 0, 0), ractangle_Mmove)
                rect_M1 = pygame.draw.rect(screen, (255, 0, 0), ractangle_M1)
                rect_M2 = pygame.draw.rect(screen, (255, 0, 0), ractangle_M2)
                rect_M3 = pygame.draw.rect(screen, (255, 0, 0), ractangle_M3)
                rect_M4 = pygame.draw.rect(screen, (255, 0, 0), ractangle_M4)


                rect_P1 = pygame.draw.rect(screen, (color_Pappear, 0, 0), ractangle_P1)
                rect_P2 = pygame.draw.rect(screen, (255, 0, 0), ractangle_P2)
                rect_P3 = pygame.draw.rect(screen, (255, 0, 0), ractangle_P3)
                rect_P4 = pygame.draw.rect(screen, (255, 0, 0), ractangle_P4)
                trap1_P = pygame.draw.rect(screen, (trap_colorP, trap_colorP, trap_colorP), trap1_P)
                trap2_P = pygame.draw.rect(screen, (trap_colorP, trap_colorP, trap_colorP), trap2_P)
                trap3_P = pygame.draw.rect(screen, (trap_colorP, trap_colorP, trap_colorP), trap3_P)
                trap4_P = pygame.draw.rect(screen, (trap_colorP, trap_colorP, trap_colorP), trap4_P)
                trap5_P = pygame.draw.rect(screen, (trap_colorP, trap_colorP, trap_colorP), trap5_P)


                rect_K1 = pygame.draw.rect(screen, (255, 0, 0), ractangle_K1)
                rect_K2 = pygame.draw.rect(screen, (255, 0, 0), ractangle_K2)
                rect_K3 = pygame.draw.rect(screen, (255, 0, 0), ractangle_K3)
                rect_K4 = pygame.draw.rect(screen, (color_realK, 0, 0), ractangle_K4)
                rect_K5 = pygame.draw.rect(screen, (color_realK, 0, 0), ractangle_K5)



                #Création carré debut et fin 
                deb_rect = pygame.draw.rect(screen, (35, 150, 245), deb)
                fin_rect = pygame.draw.rect(screen, (0, 0, color_real_endK), fin)
                trigger = pygame.draw.rect(screen, (255, 0, 0), trigS)
                trigger2 = pygame.draw.rect(screen, (10, 240, 10), trigM)
                trigger3 = pygame.draw.rect(screen, (10, 240, 10), trigP)
                trigger_egg = pygame.draw.rect(screen, (240, 0, 0), trig_egg)
                tp1 = pygame.draw.rect(screen, (160, 240, 30), tp1)
                tp1_end = pygame.draw.rect(screen, (160, 240, 30), tp1_end)
                tp2 = pygame.draw.rect(screen, (color_Mtp1, color_Mtp2, 0), tp2)
                tp2_end = pygame.draw.rect(screen, (160, 240, 30), tp2_end)
                tp3 = pygame.draw.rect(screen, (160, 240, 30), tp3)
                tp3_end = pygame.draw.rect(screen, (160, 240, 30), tp3_end)
                fake_end1 = pygame.draw.rect(screen, (color_temp1, 0, color_end1K), fake_end1)
                fake_end2 = pygame.draw.rect(screen, (color_temp2, 0, color_end2K), fake_end2)

                # Met le cursor sur le départ
                if not self.start:
                    pygame.mouse.set_pos([deb[0], deb[1]])
                    starting_tick = pygame.time.get_ticks()
                    self.start = True
                # Boucle qui vérifie que l'on est bien dans le niveau + affiche le titre du niveau
                title = font.render(("Maze 10"), 1, (255, 255, 255))
                screen.blit(title, (SCREEN_WIDTH * (109/256), SCREEN_HEIGHT * (60/72)))
                
                if trap1_P.collidepoint(pygame.mouse.get_pos()) or trap2_P.collidepoint(pygame.mouse.get_pos()) or trap3_P.collidepoint(pygame.mouse.get_pos()) or trap4_P.collidepoint(pygame.mouse.get_pos()) or trap5_P.collidepoint(pygame.mouse.get_pos()):
                    sound_mana.play('OOB')
                    pygame.mouse.set_pos([deb[0], deb[1]])

                rectangles = [rect_S1, rect_S2, rect_S3, rect_Smove, rect_Sreal, rect_P1, rect_P2, rect_P3, rect_P4, rect_M1, rect_M2, rect_M3, rect_M4, rect_Mmove, rect_Mappear, rect_K1, rect_K2, rect_K3, rect_K4, rect_K5]

                if not any(rect.collidepoint(pygame.mouse.get_pos()) for rect in rectangles):
                    sound_mana.play('OOB')
                    pygame.mouse.set_pos([deb[0], deb[1]])


                if self.y_Smove >= SCREEN_HEIGHT * (250/720) and positionS == "up":
                    rect_Smove.move(SCREEN_WIDTH * (200/1280), self.y_Smove)
                    self.y_Smove += 1
                    if self.y_Smove == SCREEN_HEIGHT * (450/720):
                        positionS = "down"
                    pygame.display.flip()
                elif self.y_Smove <= SCREEN_HEIGHT * (450/720):
                    rect_Smove.move(SCREEN_WIDTH * (200/1280), self.y_Smove)
                    self.y_Smove -= 1
                    if self.y_Smove == SCREEN_HEIGHT * (250/720):
                        positionS = "up"
                    pygame.display.flip()

                if self.x_Mmove >= SCREEN_WIDTH * (415/1280) and positionM == "left":
                    rect_Smove.move(self.x_Mmove, SCREEN_HEIGHT * (230/720))
                    self.x_Mmove += 1
                    if self.x_Mmove == SCREEN_WIDTH * (485/1280):
                        positionM = "right"
                    pygame.display.flip()
                elif self.x_Mmove <= SCREEN_WIDTH * (485/1280):
                    rect_Smove.move(self.x_Mmove, SCREEN_HEIGHT * (230/720))
                    self.x_Mmove -= 1
                    if self.x_Mmove == SCREEN_WIDTH * (415/1280):
                        positionM = "left"
                    pygame.display.flip()
                
                if tp1.collidepoint(pygame.mouse.get_pos()):
                    sound_mana.play("tp")
                    pygame.mouse.set_pos([tp1_end[0], tp1_end[1]])
                
                if tp2.collidepoint(pygame.mouse.get_pos()):
                    sound_mana.play("tp")
                    pygame.mouse.set_pos([tp2_end[0], tp2_end[1]])

                if tp3.collidepoint(pygame.mouse.get_pos()):
                    sound_mana.play("tp")
                    pygame.mouse.set_pos([tp3_end[0], tp3_end[1]])



                #Condition victory
                if fin_rect.collidepoint(pygame.mouse.get_pos()):
                    win = True
                    end_tick = pygame.time.get_ticks()
                    total_time = str((end_tick - starting_tick)/1000)[0:4]

                if trigger.collidepoint(pygame.mouse.get_pos()):
                    color_fake_S = 0
                    self.y_Sreal = 150
                    sound_mana.play("giggle")
                
                if not song_switch1:
                    if trigger2.collidepoint(pygame.mouse.get_pos()):
                        self.y_Mappear = SCREEN_HEIGHT * (250/720)
                        color_Mappear = 255
                        color_Mtp1 = 160
                        color_Mtp2 = 240
                        sound_mana.play('switch')
                        song_switch1 = True
                
                if not song_switch2:
                    if trigger3.collidepoint(pygame.mouse.get_pos()):
                        self.x_Pappear = SCREEN_WIDTH * (740/1280)
                        color_Pappear = 255
                        sound_mana.play('switch')
                        song_switch2 = True

                if timeTickP + waitTime < pygame.time.get_ticks() :
                    if position_P == "right":
                        trap_colorP = 128
                        sound_mana.play("spike")
                        self.x_spikeP = SCREEN_WIDTH * (660/1280)
                        timeTickP = pygame.time.get_ticks()
                        position_P = "left"
                    else:
                        trap_colorP = 0
                        self.x_spikeP = SCREEN_WIDTH * (740/1280)
                        timeTickP = pygame.time.get_ticks()
                        position_P = "right"


                if fake_end1.collidepoint(pygame.mouse.get_pos()):
                    if not song_troll1:
                        sound_mana.play('giggle')
                        color_end1K = 0
                        color_end2K = 255
                        song_troll1 = True
                        color_temp1 = 255
                        color_temp2 = 0

                if fake_end2.collidepoint(pygame.mouse.get_pos()):
                    if not song_troll2 and song_troll1:
                        sound_mana.play('giggle')
                        self.y_realK = SCREEN_HEIGHT * (320/720)
                        color_realK = 255
                        color_real_endK = 255
                        color_end2K = 0
                        song_troll2 = True
                        color_temp2 = 255
                

                if not song_egg :
                    if trigger_egg.collidepoint(pygame.mouse.get_pos()):
                        pygame.mouse.set_visible(False)
                        sound_mana.play('egg')
                        newCursor = True
                        song_egg = True



            #End of the game 
            elif niveau == 11:
                #Arrière plan
                if not self.start:
                    screen.fill((0, 0, 0))
                    screen.blit(screen, (0, 0))
                    self.start == True

                if not texte_write:
                    for i in range(0,3):

                        if i == 0:
                            # Texte congrats
                            congrat = font.render(("CONGRATULATION FOR BEATING THE GAME"), 1, (255, 255, 255))
                            screen.blit(congrat, (SCREEN_WIDTH * (120/1280), SCREEN_HEIGHT* (50/720)))

                        if i == 1:

                            # Texte lie
                            start = font.render(("That means you don't have Parkinson anymore"), 1, (255, 255, 255))
                            screen.blit(start, (SCREEN_WIDTH * (20/1280), SCREEN_HEIGHT* (150/720)))
                        
                        if i == 2:
                            # Texte correction 
                            font2 = pygame.font.SysFont("monospace", 35, bold=True, italic=False)
                            correct = font2.render(("(well it can't vanish)"), 1, (255, 255, 255))
                            screen.blit(correct, (SCREEN_WIDTH * (820/1280), SCREEN_HEIGHT* (190/720)))
                            # Texte proud
                            texte = font.render(("But at least you practised and it's a start"), 1, (255, 255, 255))
                            screen.blit(texte, (SCREEN_WIDTH * (10/1280), SCREEN_HEIGHT * (250/720)))

                        pygame.display.flip()
                        pygame.time.delay(1000)


                    for j in range(0,1):
                        if j == 0:
                            # Texte time + tryagain
                            finaltime = font.render(("Your final time is : " + str(all_timer)), 1, (255, 255, 255))
                            screen.blit(finaltime, (SCREEN_WIDTH * (120/1280), SCREEN_HEIGHT * (520/720)))
                            tryagain = font.render(("Try to do better next time ;)"), 1, (255, 255, 255))
                            screen.blit(tryagain, (SCREEN_WIDTH * (120/1280), SCREEN_HEIGHT * (580/720)))
                        
                        pygame.display.flip()
                        pygame.time.delay(5000)

                    texte_write = True
            
                if texte_write:
                    screen.fill((0, 0, 0))
                    screen.blit(screen, (0, 0))
                    end = font.render(("Press ESCAPE to get out of here."), 1, (255, 255, 255))
                    screen.blit(end, (SCREEN_WIDTH * (160/1280), SCREEN_HEIGHT * (310/720)))
            

            




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
                
            if newCursor == True:
                cursor_img = pygame.image.load('sources/mouse/assets/cursor_egg.png')
                cursor_img_rect = cursor_img.get_rect()
                cursor_img_rect.center = pygame.mouse.get_pos()  # update position 
                #pygame.transform.scale(cursor_img, (32, 32))
                screen.blit(cursor_img, cursor_img_rect) # draw the cursor
            
            # Cap the frame rate
            # clock.tick(60)
            # Update the display
            if running:
                pygame.display.flip()
            #sys.exit()

if __name__ == "__main__":
    maze = Maze()
    maze.start_maze()