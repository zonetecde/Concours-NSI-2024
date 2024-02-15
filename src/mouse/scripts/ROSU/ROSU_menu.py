import pygame
import sys
import math
import json
from os.path import exists

class Rosu:
    @staticmethod
    def start_rosu():
        if not exists("src/mouse/scripts/ROSU/savefile.json"):
            with open("src/mouse/scripts/ROSU/savefile.json", "w") as f:
                json.dump(
                    { "Gravity Falls" : { "Best Score" : "-----", "Grade" : "None", "Accuracy" : "None"}, "Okami" : { "Best Score" : "-----", "Grade" : "None", "Accuracy" : "None"}, "Zelda -- Hidden Village" : { "Best Score" : "-----", "Grade" : "None", "Accuracy" : "None"}}
                    , f)
                
        savefile = open("src/mouse/scripts/ROSU/savefile.json")
        tempData = json.load(savefile)
        data = []
        for save in tempData:
            data.append((save, tempData[save]))

        import ROSU_storage as storage

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
        while running:
            mouseX = pygame.mouse.get_pos()[0]
            mouseY = pygame.mouse.get_pos()[1]
            
            if bgImage != None:
                screen.blit(bgImage, (0, 0))
            
            x, y = 10, 10
            rectZones = []
            for i in range(len(storage.Storage)):
                pygame.draw.rect(screen, (255, 255, 255), (x, y, 600, 150), 3, 2, 2, 2, 2, 2)
                
                textFont = pygame.font.SysFont("monospace", 35, bold=True, italic=False)
                songInfos = textFont.render(str(storage.Storage[i][0]), 1, (255, 255, 255))
                screen.blit(songInfos, (x + 10, y + 5))
                
                songInfos = textFont.render(str(storage.Storage[i][3]), 1, (255, 255, 255))
                screen.blit(songInfos, (x + 10, y + 110))
                
                if mouseX > x and mouseX < x + 600 and mouseY > y and mouseY < y + 150:
                    bgImage = pygame.image.load(storage.Storage[i][2])
                    selected = storage.Storage[i][0]
                    
                rectZones.append((i, x, y, x + 600, y + 150)) 
                y += 160
            
            obj = 0
            for item in data:
                if str(item[0]) == str(selected):
                    songName = str(item[0])
                    saveDict = data[obj][1]
                    bestScore = saveDict["Best Score"]
                    grade = saveDict["Grade"]
                    accuracy = saveDict["Accuracy"]
                    
                    
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
                if event.type == pygame.QUIT:
                    running = False
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