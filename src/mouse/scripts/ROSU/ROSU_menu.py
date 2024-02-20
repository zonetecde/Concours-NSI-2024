import pygame
import sys
import json
from os.path import exists
import os

# Permet de ce placer dans le dossier contenant les scripts ROSU
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + "/scripts/ROSU")

from ROSU_game import Engine
from ROSU_storage import niveaux
from Sauvegarde import Sauvegarde

class Rosu:
    """ Classe permettant de lancer l'exercice ROSU!    
    """

    @staticmethod
    def start_rosu():
        """ Méthode permettant de lancer l'exercice ROSU!
        """
    
        try:
            # Chemin du fichier de sauvegarde
            savefile_path = os.path.dirname(os.path.abspath(__file__)) + "/savefile.json"

            #Création du fichier de sauvegarde si il n'existe pas
            if not exists(savefile_path):
                with open(savefile_path, "w") as savefile:
                    sauvegardes = []

                    for niveau in niveaux:
                        sauvegardes.append(Sauvegarde(niveau.nom, "-----", "None", 0))

                    json_string = json.dumps([ob.__dict__ for ob in sauvegardes], indent=4)
                    savefile.write(json_string)

            # Récupération des données de la sauvegarde        
            savefile = open(savefile_path)
            sauvegardes = json.load(savefile)

            # Initialize Pygame
            pygame.init()

            # Screen dimensions
            desktopSize = pygame.display.get_desktop_sizes()

            SCREEN_WIDTH = desktopSize[0][0]
            SCREEN_HEIGHT = desktopSize[0][1]

            # Initialize the screen
            screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) # Mode plein écran
            pygame.display.set_caption("ROSU! Game")

            # Clock for controlling the frame rate
            clock = pygame.time.Clock()

            screen.fill((0, 0, 0))

            rectZones = []

            running = True
            bgImage = None
            nom_niveau_selectionne = ""
                        
            # Main loop
            while running:
                mouseX = pygame.mouse.get_pos()[0]
                mouseY = pygame.mouse.get_pos()[1]
                
                # Si pas d'image le fond est mis en noir
                if bgImage != None:
                    screen.blit(bgImage, (0, 0))
                
                x, y = 10, 10
                rectZones = []
                #Création d'un rectangle pour chaque map
                for i in range(len(niveaux)):
                    pygame.draw.rect(screen, (255, 255, 255), (x, y, 600, 150), 3, 2, 2, 2, 2, 2)
                    
                    textFont = pygame.font.SysFont("monospace", 35, bold=True, italic=False)
                    songInfos = textFont.render(str(niveaux[i].nom), 1, (255, 255, 255))
                    screen.blit(songInfos, (x + 10, y + 5))
                    
                    songInfos = textFont.render(f"Difficulté : {str(niveaux[i].difficulte)}/20", 1, (255, 255, 255))
                    screen.blit(songInfos, (x + 10, y + 110))
                    
                    #Si la souris est mise sur le rectangle, la map s'affiche
                    if mouseX > x and mouseX < x + 600 and mouseY > y and mouseY < y + 150:
                        bgImage = pygame.image.load(niveaux[i].image_fond)
                        nom_niveau_selectionne = niveaux[i].nom
                        
                    rectZones.append((i, x, y, x + 600, y + 150)) 
                    y += 160
                
                # Récupération des best score de la map et affichage de ces derniers
                for sauvegarde in sauvegardes:
                    if sauvegarde["nom_niveau"] == nom_niveau_selectionne:
                        bestScore = sauvegarde["meilleur_score"]
                        grade = sauvegarde["note"]
                        accuracy = str(sauvegarde["precision"])
                        
                        #Affichage des infos lié aux meilleurs score de la map
                        textFont = pygame.font.SysFont("monospace", 35, bold=True, italic=False)
                        nameLabel = textFont.render((sauvegarde["nom_niveau"]), 1, (255, 255, 255))
                        screen.blit(nameLabel, (650, 10))
                        
                        textFont = pygame.font.SysFont("monospace", 35, bold=True, italic=False)
                        scoreLabel = textFont.render(("Meilleur score : " + str(bestScore)), 1, (255, 255, 255))
                        screen.blit(scoreLabel, (650, 120))
                        
                        textFont = pygame.font.SysFont("monospace", 35, bold=True, italic=False)
                        scoreLabel = textFont.render(("Précision : " + str(accuracy)), 1, (255, 255, 255))
                        screen.blit(scoreLabel, (650, 180))
                        
                        textFont = pygame.font.SysFont("monospace", 35, bold=True, italic=False)
                        scoreLabel = textFont.render(("Note : " + str(grade)), 1, (255, 255, 255))
                        screen.blit(scoreLabel, (650, 240))
                                                        
                for event in pygame.event.get():
                    #Si appuie sur la croix, quitter le jeu
                    if event.type == pygame.QUIT:
                        running = False
                    #Si souris cliquer, lancement de la map choisie
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouseX = pygame.mouse.get_pos()[0]
                        mouseY = pygame.mouse.get_pos()[1]

                        # Où rect_index est l'index du rectangle cliqué sur le menu
                        for rect_index in range(len(rectZones)):
                            if mouseX > rectZones[rect_index][1] and mouseX < rectZones[rect_index][3] and mouseY > rectZones[rect_index][2] and mouseY < rectZones[rect_index][4]:
                              
                                game_engine = Engine()
                                game_engine.start_level(niveaux[rect_index])
                                


                    #Permet de quitter le jeu avec echap
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            pygame.mixer.stop()
                            running = False
                # Update the display
                pygame.display.flip()

                # Cap the frame rate
                clock.tick(60)

            # Quit Pygame
            pygame.quit()
            sys.exit()
        except Exception as e:
            print('Erreur à la ligne {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
            print(e)


if __name__ == "__main__":
    Rosu.start_rosu()
