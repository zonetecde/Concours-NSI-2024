import pygame
import sys
import math
import json
from os.path import exists

class Rosu:
    #Création objet ROSU
    @staticmethod
    #Lancement du jeu 
    def start_rosu():
        
        try:
            ##Initialisation des variables :
            
            #Création de la sauvegarde si elle n'existe pas
            if not exists("src/mouse/scripts/ROSU/savefile.json"):
                with open("src/mouse/scripts/ROSU/savefile.json", "w") as f:
                    json.dump(
                        { "Gravity Falls" : { "Best Score" : "-----", "Grade" : "None", "Accuracy" : "None"}, "Okami" : { "Best Score" : "-----", "Grade" : "None", "Accuracy" : "None"}, "Zelda -- Hidden Village" : { "Best Score" : "-----", "Grade" : "None", "Accuracy" : "None"}}
                        , f)
            #Récupération des données de la sauvegarde        
            savefile = open("src/mouse/scripts/ROSU/savefile.json")
            tempData = json.load(savefile)
            data = []
            for save in tempData:
                data.append((save, tempData[save]))

            #Récupération des maps avec leurs musiques et le background
            storage = open("src/mouse/scripts/ROSU/data/storage.json")
            storage = json.load(storage)


            # Initialize Pygame
            pygame.init()

            # Screen dimensions
            SCREEN_WIDTH = 1280
            SCREEN_HEIGHT = 720

            # Initialize the screen
            screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
            pygame.display.set_caption("ROSU! Game")

            # Clock for controlling the frame rate
            clock = pygame.time.Clock()

            screen.fill((0, 0, 0))

            rectZones = []

            running = True
            bgImage = None
            selected = ""
            

            playSong = None
            
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
                for i in range(len(storage)):
                    pygame.draw.rect(screen, (255, 255, 255), (x, y, 600, 150), 3, 2, 2, 2, 2, 2)
                    
                    textFont = pygame.font.SysFont("monospace", 35, bold=True, italic=False)
                    songInfos = textFont.render(str(storage[i][0]), 1, (255, 255, 255))
                    screen.blit(songInfos, (x + 10, y + 5))
                    
                    songInfos = textFont.render(str(storage[i][3]), 1, (255, 255, 255))
                    screen.blit(songInfos, (x + 10, y + 110))
                    
                    #Si la souris est mise sur le rectangle, la map s'affiche
                    if mouseX > x and mouseX < x + 600 and mouseY > y and mouseY < y + 150:
                        bgImage = pygame.image.load(storage[i][2])
                        selected = storage[i][0]
                        
                    rectZones.append((i, x, y, x + 600, y + 150)) 
                    y += 160
                
                #Récupération des best score de la map et affichage de ces derniers
                obj = 0
                for item in data:
                    if str(item[0]) == str(selected):
                        songName = str(item[0])
                        saveDict = data[obj][1]
                        bestScore = saveDict["Best Score"]
                        grade = saveDict["Grade"]
                        accuracy = saveDict["Accuracy"]
                        
                        #Affichage des infos lié aux meilleurs score de la map
                        textFont = pygame.font.SysFont("monospace", 35, bold=True, italic=False)
                        nameLabel = textFont.render((songName), 1, (255, 255, 255))
                        screen.blit(nameLabel, (650, 10))
                        
                        textFont = pygame.font.SysFont("monospace", 35, bold=True, italic=False)
                        scoreLabel = textFont.render(("Best score: " + str(bestScore)), 1, (255, 255, 255))
                        screen.blit(scoreLabel, (650, 120))
                        
                        textFont = pygame.font.SysFont("monospace", 35, bold=True, italic=False)
                        scoreLabel = textFont.render(("Accuracy: " + str(accuracy)), 1, (255, 255, 255))
                        screen.blit(scoreLabel, (650, 180))
                        
                        textFont = pygame.font.SysFont("monospace", 35, bold=True, italic=False)
                        scoreLabel = textFont.render(("Grade: " + str(grade)), 1, (255, 255, 255))
                        screen.blit(scoreLabel, (650, 240))
                        
                    obj += 1
                                
                for event in pygame.event.get():
                    #Si appuie sur la croix, quitter le jeu
                    if event.type == pygame.QUIT:
                        running = False
                    #Si souris cliquer, lancement de la map choisie
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouseX = pygame.mouse.get_pos()[0]
                        mouseY = pygame.mouse.get_pos()[1]
                        for j in range(len(rectZones)):
                            if mouseX > rectZones[j][1] and mouseX < rectZones[j][3] and mouseY > rectZones[j][2] and mouseY < rectZones[j][4]:
                                import ROSU_game as game
                                game.GAMELOOP(j)
                                savefile = open("src/mouse/scripts/ROSU/savefile.json")
                                tempData = json.load(savefile)
                                data = []
                                for save in tempData:
                                    data.append((save, tempData[save]))
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


if __name__ == "__main__":
    Rosu.start_rosu()
