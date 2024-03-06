import pygame
import sys
import math
import json
import os
    
# Permet de ce placer dans le dossier contenant les scripts ROSU
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + "/scripts/Rosu")

from storage import Niveau, niveaux
from sauvegarde import Sauvegarde

class Engine:
    try:
        savefile_path = os.path.dirname(os.path.abspath(__file__)) + "/savefile.json"
        parent_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) 

        def start_level(self, niveau: Niveau):
            """ Méthode permettant de lancer un niveau de l'exercice ROSU!
            """
            TEXT_BACKGROUND_COLOR = (169, 191, 250)
            
            # Récupération des données de la sauvegarde        
            savefile = open(self.savefile_path)
            sauvegardes = json.load(savefile)


            #Initialisation  des variables
            bestScore = 0
            bestGrade = "F"
            bestAccuracy = "0%"

            #Récupération des éléments de la sauvegarde
            for sauvegarde in sauvegardes:
                if sauvegarde["nom_niveau"] == niveau.nom:
                    bestScore = sauvegarde["meilleur_score"]
                    bestGrade = sauvegarde["note"]
                    bestAccuracy = sauvegarde["precision"]
                    
            #Si fichier nouveau, on adapte les variables    
            if bestScore == "-----": bestScore = 0
            if bestGrade == "None": bestGrade = "F"
            if bestAccuracy == "None": bestAccuracy = "0%"

            circlesList, backgroundImage, audio = niveau.data.copy(), niveau.image_fond, niveau.musique
            circlesListIngame = circlesList

            # Screen dimensions
            desktopSize = pygame.display.get_desktop_sizes()

            SCREEN_WIDTH = desktopSize[0][0]
            SCREEN_HEIGHT = desktopSize[0][1]

            # Initialize the screen
            screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)

            # Colors
            WHITE = (255, 255, 255)
            BLACK = (0, 0, 0)

            pygame.display.set_caption("ROSU! Game")

            #Fond charger
            bg = pygame.image.load(backgroundImage)
            bg = pygame.transform.scale(bg, (SCREEN_WIDTH, SCREEN_HEIGHT))

            #Musique charger
            pygame.mixer.init()
            pygame.mixer.music.load(audio)

            pointFont = pygame.font.Font(Engine.parent_dir + '/fonts/Cabin-Regular.ttf', 50)

            # Main game loop
            ## Initialisation Variables
            #Celles qui permettent de savoir si le jeu la musique  tourne
            renderMistake = False
            playing = False
            running = True

            #Lancement de la clock et récupéaration du "premier" tick
            clock = pygame.time.Clock()
            startingTick = pygame.time.get_ticks()

            #Variable du score
            totalNotes = len(circlesListIngame)
            playerMiss = 0
            score = 0
            saved = False 
            multiplicator = 1

            while running == True:
                # Clear the screen
                screen.blit(bg, (0, 0))

                current_tick = pygame.time.get_ticks() - startingTick

                mouseX = pygame.mouse.get_pos()[0]
                mouseY = pygame.mouse.get_pos()[1]
                circleClickList = []

                #Lancement de la musique après 5 secondes
                if current_tick >= 5000:
                    if playing == False:
                        pygame.mixer.music.play()
                        playing = True

                # Dessine les cercles 
                i  = 0
                for circle_info in circlesListIngame:
                    circle_tick, (x, y), color, size, pointNumber = circle_info
                    # Le cercle doit il être cliqué ? 
                    is_to_be_clicked = i == 0
                    i += 1
                    
                    if current_tick >= circle_tick - 100 * (size * (SCREEN_HEIGHT/720)):
                        # Dessine le cercle
                        if not is_to_be_clicked:
                            pygame.draw.circle(screen, color, (x * (SCREEN_WIDTH/1280), y * (SCREEN_HEIGHT/720)), (size * (SCREEN_HEIGHT/720)), width=int(((current_tick - circle_tick + 100 * (size * (SCREEN_HEIGHT/720)) + 1))/(1)/100 + 1))       
                        else:
                            # le dessine avec un contours rouge
                            pygame.draw.circle(screen, (255, 0, 0), (x * (SCREEN_WIDTH / 1280), y * (SCREEN_HEIGHT / 720)),
                                (size * (SCREEN_HEIGHT / 720) + 5), width=5)

                            pygame.draw.circle(screen, color, (x * (SCREEN_WIDTH/1280), y * (SCREEN_HEIGHT/720)), (size * (SCREEN_HEIGHT/720)), width=int(((current_tick - circle_tick + 100 * (size * (SCREEN_HEIGHT/720)) + 1))/(1)/100 + 1))      

                        # Ecris le numéro du cercle
                        circleLabel = pointFont.render(str(pointNumber), 1, WHITE)
                        screen.blit(circleLabel, (x * (SCREEN_WIDTH/1280) - (12 if pointNumber != 1 else 10), y * (SCREEN_HEIGHT/720) - 29))

                        # Si le cercle est raté, on le retire
                        if int((current_tick - circle_tick + 100 * (size * (SCREEN_HEIGHT/720)) + 1)/(1)/100 + 1) > (size * (SCREEN_HEIGHT/720)) + 2:
                            circlesListIngame.remove(circle_info)
                            playerMiss += 1
                        else:
                            circleClickList.append(((x * (SCREEN_WIDTH / 1280), y * (SCREEN_HEIGHT / 720)), (size * (SCREEN_HEIGHT/720)), circle_tick))

                # Handle events
                for event in pygame.event.get():
                    #Si appuie sur la croix, quitter le jeu 
                    if event.type == pygame.QUIT:
                        running = False
                    #Vérification des cercles clickés et ajout du score
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        # Vérifie que la partie a commencé
                        if current_tick > 5000:
                            if len(circleClickList) == 0:
                                pass
                            #Si bien clické on ajoute des points + on augmente le mutiplicateur et on pense à retirer le cercle
                            elif math.sqrt((mouseX - circleClickList[0][0][0]) ** 2 + (mouseY - circleClickList[0][0][1]) ** 2) < circleClickList[0][1]:
                                score += 50 * multiplicator
                                multiplicator += 0.01
                                circlesListIngame.pop(0)
                            #Sinon remise du score à 0 et du multiplicateur à 1 + affichage du text RATÉ 
                            else:
                                font = pygame.font.Font(Engine.parent_dir + '/fonts/Cabin-Regular.ttf', 80)
                                color = (255, 0, 0)
                                labelMistake = font.render("RATÉ", 1, color)
                                mistakeTick = current_tick
                                renderMistake = True
                                playerMiss += 1
                                multiplicator = 1
                        #Si on appuie sur échappe on quitte le jeu
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            pygame.mixer.stop()
                            return

                #Si on fait une erreur, on nous le dit
                if renderMistake == True:
                    if mistakeTick > current_tick - 200:
                        screen.blit(labelMistake, (SCREEN_WIDTH * 0.45, SCREEN_HEIGHT * 0.45))
                    else:
                        renderMistake = False
                
                #Affichage du temps pendant les 5 secondes de départ
                if current_tick < 5000:
                    font = pygame.font.Font(Engine.parent_dir + '/fonts/Cabin-Regular.ttf', 80)

                    color = (200, 0, 0)

                    label = font.render(str(5000 - current_tick), 1, color)
                    screen.blit(label, (SCREEN_WIDTH * 0.45, SCREEN_HEIGHT * 0.45))

                
                #Affichage du score en fin de partie
                if len(circlesListIngame) == 0 and current_tick > 6000:
                    font = pygame.font.Font(Engine.parent_dir + '/fonts/Cabin-Regular.ttf', 65)
                    color = (255, 0, 0)
                    
                    #Text complete! et le rectangle gris derrière ce dernier
                    pygame.draw.rect(screen, TEXT_BACKGROUND_COLOR,(SCREEN_WIDTH * 0.3125, 40, 480, 100), 0, 10, 10, 10, 10, 10)
                    textLabel = font.render("Level completed!", 1, BLACK)
                    screen.blit(textLabel, (SCREEN_WIDTH * 0.3125, 50))

                    #Modification de la taille du rectagle selon le nombre d'erreurs 
                    if playerMiss > 100:
                        rectLength = 520
                    elif playerMiss > 10:
                        rectLength = 470
                    else:
                        rectLength = 420
                    
                    #Nombre d'erreurs et son rectangle
                    pygame.draw.rect(screen, TEXT_BACKGROUND_COLOR,(40, SCREEN_HEIGHT * 0.28 - 10, rectLength, 100), 0, 10, 10, 10, 10, 10)
                    textLabel = font.render(str("Missed: " + str(playerMiss)), 1, BLACK)
                    screen.blit(textLabel, (50, SCREEN_HEIGHT * 0.28))

                    #Accuracy et son rectangle
                    accuracy = float(str((totalNotes - playerMiss)/totalNotes * 100)[0:5])
                    pygame.draw.rect(screen, TEXT_BACKGROUND_COLOR, (40, SCREEN_HEIGHT * 0.42 - 10, 750, 100), 0, 10, 10, 10, 10, 10)
                    textLabel = font.render(str("Accuracy: " + str((totalNotes - playerMiss)/totalNotes * 100)[0:5] + "%"), 1, BLACK)
                    screen.blit(textLabel, (50, SCREEN_HEIGHT * 0.42))
                    pygame.draw.rect(screen, TEXT_BACKGROUND_COLOR, (40, SCREEN_HEIGHT * 0.55 - 10, 750, 100), 0, 10, 10, 10, 10, 10)
                    scoreLabel = font.render(str("Score: " + str(score)), 1, BLACK)
                    screen.blit(scoreLabel, (50, SCREEN_HEIGHT * 0.55))

                    #Retour possible et son rectangle
                    font2 = pygame.font.Font(Engine.parent_dir + '/fonts/Cabin-Regular.ttf', 40)
                    pygame.draw.rect(screen, TEXT_BACKGROUND_COLOR,(190, SCREEN_HEIGHT * 0.90 - 10, 860, 100), 0, 10, 10, 10, 10, 10)
                    textLabel = font2.render(str("Press \"escape\" to get back to the menu."), 1, BLACK)
                    screen.blit(textLabel, (200, SCREEN_HEIGHT * 0.90))
                    
                    #Enregistrement du score et remplacement si il est meilleur
                    if saved == False:
                        
                        if score > bestScore:
                            bestScore = score
                        
                        try:
                            bestAccuracy = float(str(bestAccuracy)[:-1])
                        except:
                            bestAccuracy = 0
                        
                        if accuracy > bestAccuracy:
                            bestAccuracy = accuracy
                            
                        gradeList = [("F", 0), ("D", 1), ("C", 2), ("B", 3), ("A", 4), ("A+", 5), ("S", ), ("SS", 7), ("SSS", 8)]
                        
                        if accuracy >= 100 and playerMiss == 0:
                            grade = "SSS"
                        elif accuracy > 98.5:
                            grade = "SS"
                        elif accuracy > 96:
                            grade = "S"
                        elif accuracy > 92.5:
                            grade = "A+"
                        elif accuracy > 88:
                            grade = "A"
                        elif accuracy > 76:
                            grade = "B"
                        elif accuracy > 60:
                            grade = "C"
                        elif accuracy > 40:
                            grade = "D"
                        else:
                            grade = "F"
                            
                        gradeIndex = None
                        bestGradeIndex = None
                        for gradeListIndex in range(len(gradeList)):
                            if grade == gradeList[gradeListIndex][0]:
                                gradeIndex = gradeList[gradeListIndex][1]
                            if bestGrade == gradeList[gradeListIndex][0]:
                                bestGradeIndex = gradeList[gradeListIndex][1]
                                
                        if gradeIndex >= bestGradeIndex:
                            bestGrade = grade
                            
                        bestAccuracy = str(bestAccuracy) + "%"
                        
                        # Update du fichier json pour la sauvegarde 
                        
                        # Suppression de l'ancienne sauvegarde
                        sauvegardes = [sauvegarde for sauvegarde in sauvegardes if sauvegarde["nom_niveau"] != niveau.nom]
                        
                        # Ajout de la nouvelle sauvegarde
                        sauvegardes.append((Sauvegarde(niveau.nom, bestScore, bestGrade, bestAccuracy).__dict__))

                        with open(self.savefile_path, "w") as savefile:
                            json_string = json.dumps(sauvegardes, indent=4)
                            savefile.write(json_string)

                        saved = True

                # Update the display
                pygame.display.flip()

                # Cap the frame rate
                clock.tick(60)

            return
    except Exception as e:
        print('game: Erreur à la ligne {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
        print(e)
