def GAMELOOP(musicIndex):
    import pygame
    import sys
    import math
    import json
    
    storage = open("src/mouse/scripts/ROSU/data/storage.json")
    storage = json.load(storage)
    
    savefile = open("src/mouse/scripts/ROSU/savefile.json")
    rawData = json.load(savefile)
    data = []
    for save in rawData:
        data.append((save, rawData[save]))
    
    obj = 0
    bestScore = 0
    bestGrade = "F"
    bestAccuracy = "0%"
    for item in data:
        if str(item[0]) == str(storage[musicIndex][0]):
            songName = str(item[0])
            saveDict = data[obj][1]
            bestScore = saveDict["Best Score"]
            bestGrade = saveDict["Grade"]
            bestAccuracy = saveDict["Accuracy"]
            
        obj += 1
        
    if bestScore == "-----": bestScore = 0
    if bestGrade == "None": bestGrade = "F"
    if bestAccuracy == "None": bestAccuracy = "0%"

    circlesList, backgroundImage, audio = storage[musicIndex][4].copy(), storage[musicIndex][2], storage[musicIndex][1]
    circlesListIngame = circlesList

    # Screen dimensions
    SCREEN_WIDTH = 1280
    SCREEN_HEIGHT = 720

    # Initialize the screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)

    # Colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    pygame.display.set_caption("ROSU! Game")

    bg = pygame.image.load(backgroundImage)

    pygame.mixer.init()
    pygame.mixer.music.load(audio)

    pointFont = pygame.font.SysFont("monospace", 35, bold=True, italic=False)

    # Main game loop
    running = True
    renderMistake = False
    playing = False

    clock = pygame.time.Clock()
    startingTick = pygame.time.get_ticks()

    totalNotes = len(circlesListIngame)
    playerMiss = 0
    
    score = 0
    saved = False
    
    multiplicator = 1
    #white running == True:
    while not (185 == 175):
        # Clear the screen
        screen.blit(bg, (0, 0))

        current_tick = pygame.time.get_ticks() - startingTick

        mouseX = pygame.mouse.get_pos()[0]
        mouseY = pygame.mouse.get_pos()[1]
        circleClickList = []

        if current_tick >= 5000:
            if playing == False:
                pygame.mixer.music.play()
                playing = True

        if current_tick < 5000:
            font = pygame.font.SysFont(
                "monospace", 75, bold=False, italic=False)
            color = (255, 0, 0)
            label = font.render(str(5000 - current_tick), 1, color)
            screen.blit(label, (520, 320))

        # Draw circles based on the list
        for circle_info in circlesListIngame:
            circle_tick, (x, y), color, size, pointNumber = circle_info
            if current_tick >= circle_tick - 100 * size:
                pygame.draw.circle(screen, color, (x, y), size, width=int(
                    ((current_tick - circle_tick + 100 * size + 1))/(1)/100 + 1))
                circleLabel = pointFont.render(str(pointNumber), 1, WHITE)
                screen.blit(circleLabel, (x - 10,  y - 20))
                if int((current_tick - circle_tick + 100 * size + 1)/(1)/100 + 1) > size + 5:
                    circlesListIngame.remove(circle_info)
                    playerMiss += 1
                else:
                    circleClickList.append(((x, y), size, circle_tick))

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if len(circleClickList) == 0:
                    pass
                elif math.sqrt((mouseX - circleClickList[0][0][0]) ** 2 + (mouseY - circleClickList[0][0][1]) ** 2) < circleClickList[0][1]:
                    score += 50 * multiplicator
                    multiplicator += 0.01
                    circlesListIngame.pop(0)
                else:
                    font = pygame.font.SysFont("monospace", 75, bold=False, italic=False)
                    color = (255, 0, 0)
                    labelMistake = font.render("XXXXX", 1, color)
                    mistakeTick = current_tick
                    renderMistake = True
                    playerMiss += 1
                    multiplicator = 1
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.mixer.stop()
                    return

        if renderMistake == True:
            if mistakeTick > current_tick - 200:
                screen.blit(labelMistake, (520, 320))
            else:
                renderMistake = False

        if len(circlesListIngame) == 0 and current_tick > 6000:
            font = pygame.font.SysFont("monospace", 75, bold=False, italic=False)
            color = (255, 0, 0)

            pygame.draw.rect(screen, (135, 135, 135),(390, 40, 480, 100), 0, 10, 10, 10, 10, 10)
            textLabel = font.render("Complete!", 1, BLACK)
            screen.blit(textLabel, (400, 50))

            if playerMiss > 100:
                rectLength = 520
            elif playerMiss > 10:
                rectLength = 470
            else:
                rectLength = 420
            pygame.draw.rect(screen, (135, 135, 135),(40, 190, rectLength, 100), 0, 10, 10, 10, 10, 10)
            textLabel = font.render(str("Missed: " + str(playerMiss)), 1, BLACK)
            screen.blit(textLabel, (50, 200))

            accuracy = float(str((totalNotes - playerMiss)/totalNotes * 100)[0:5])
            pygame.draw.rect(screen, (135, 135, 135), (40, 290, 750, 100), 0, 10, 10, 10, 10, 10)
            textLabel = font.render(str("Accuracy: " + str((totalNotes - playerMiss)/totalNotes * 100)[0:5] + "%"), 1, BLACK)
            screen.blit(textLabel, (50, 300))
            
            pygame.draw.rect(screen, (135, 135, 135), (40, 390, 750, 100), 0, 10, 10, 10, 10, 10)
            scoreLabel = font.render(str("Score: " + str(score)), 1, BLACK)
            screen.blit(scoreLabel, (50, 400))

            font2 = pygame.font.SysFont("monospace", 35, bold=False, italic=False)
            pygame.draw.rect(screen, (135, 135, 135),(190, 640, 860, 100), 0, 10, 10, 10, 10, 10)
            textLabel = font2.render(str("Press \"escape\" to get back to the menu."), 1, BLACK)
            screen.blit(textLabel, (200, 650))
            
            if saved == False:
                
                if score > bestScore:
                    bestScore = score
                
                bestAccuracy = float(str(bestAccuracy)[:-1])
                
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
                
                rawData.update({songName : {"Best Score" : bestScore, "Grade" : bestGrade, "Accuracy" : bestAccuracy}})
                open("src/mouse/scripts/ROSU/savefile.json", "w").close()
                with open("src/mouse/scripts/ROSU/savefile.json", "w") as savefile:
                    json.dump(rawData, savefile)
                saved = True

        # Update the display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(60)

    return
