import pygame
import sys
import math
import json
import random
from os.path import exists

# Initialize Pygame
pygame.init()

# Screen dimension
desktopSize = pygame.display.get_desktop_sizes()

SCREEN_WIDTH = desktopSize[0][0]
SCREEN_HEIGHT = desktopSize[0][1]

# Initialize the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Save The Reactor! Game")

# Clock for controlling the frame rate
clock = pygame.time.Clock()

screen.fill((0, 0, 0))

bg = pygame.image.load("sources/mouse/background/bg_str.png")
bg = pygame.transform.scale(bg, (SCREEN_WIDTH, SCREEN_HEIGHT))

temperatureBarLightsOn = 0
temperatureBarColors = [(0, 95, 0), (89, 82, 0), (95, 0, 0)]

buttonsList = []

running = True

def create_layout():
    modulesCentralZone = pygame.draw.rect(screen, (135, 135, 135), (0, SCREEN_HEIGHT/2, SCREEN_WIDTH, SCREEN_HEIGHT/2))
    modulesCentralZoneContour = pygame.draw.rect(screen, (125, 0, 0), (0, SCREEN_HEIGHT/2, SCREEN_WIDTH, SCREEN_HEIGHT/2), 5)
    
    modulesLeftZone = pygame.draw.rect(screen, (125, 125, 125), (0, SCREEN_HEIGHT * (5/36), SCREEN_WIDTH * 0.1875, SCREEN_HEIGHT * (13/36)))
    modulesLeftZoneContour = pygame.draw.rect(screen, (0, 0, 125), (0, SCREEN_HEIGHT * (5/36), SCREEN_WIDTH * 0.1875, SCREEN_HEIGHT * (13/36)), 3)
    
    modulesRightZone = pygame.draw.rect(screen, (125, 125, 125), (SCREEN_WIDTH * (13/16), SCREEN_HEIGHT * (5/36), SCREEN_WIDTH * (3/16), SCREEN_HEIGHT * (13/36)))
    modulesRightZoneContour = pygame.draw.rect(screen, (0, 0, 125), (SCREEN_WIDTH * (13/16), SCREEN_HEIGHT * (5/36), SCREEN_WIDTH * (3/16), SCREEN_HEIGHT * (13/36)), 3)

    temperatureBar = pygame.draw.rect(screen, (100, 100, 100), (SCREEN_WIDTH * (17/64), 0, SCREEN_WIDTH * (31/64), SCREEN_HEIGHT * (1 / 24)))
    temperatureBarContour = pygame.draw.rect(screen, (0, 0, 0), (SCREEN_WIDTH * (17/64), 0, SCREEN_WIDTH * (31/64), SCREEN_HEIGHT * (1 / 24)), 3)
    
    barX = SCREEN_WIDTH * (17/64) + 6
    for bar in range(60):
        barColorIndex = bar // 20
        barColor = temperatureBarColors[barColorIndex]
        colorR = barColor[0]
        colorG = barColor[1]
        colorB = barColor[2]
        if bar < temperatureBarLightsOn:
            if barColorIndex == 0:
                colorG += 140
            elif barColorIndex == 1:
                colorR += 140
                colorG += 140
            else:
                colorR += 140
        barColor = (colorR, colorG, colorB)
        tempIndicator = pygame.draw.rect(screen, barColor, (barX, 5, 5, SCREEN_HEIGHT * (1 / 24) - 10), 0, 2)
        barX += (SCREEN_WIDTH * (31/64)) / 60 - 0.1
    
    energyBar = pygame.draw.rect(screen, (25, 25, 25), (SCREEN_WIDTH * (207/512), SCREEN_HEIGHT * (65/144), SCREEN_WIDTH * (6/32), SCREEN_HEIGHT * (7/144)))
    energyBarContour = pygame.draw.rect(screen, (0, 0, 0), (SCREEN_WIDTH * (207/512), SCREEN_HEIGHT * (65/144), SCREEN_WIDTH * (6/32), SCREEN_HEIGHT * (7/144)), 3)
    
    reactorCore = pygame.draw.rect(screen, (185, 25, 25), (SCREEN_WIDTH * (27/64), SCREEN_HEIGHT * (1/9), SCREEN_WIDTH * (5/32), SCREEN_HEIGHT * (5/18)))
    reactorCoreContour = pygame.draw.rect(screen, (255, 255, 255), (SCREEN_WIDTH * (27/64), SCREEN_HEIGHT * (1/9), SCREEN_WIDTH * (5/32), SCREEN_HEIGHT * (5/18)), 5)
    

def module_create_bounding_box(moduleName, posX, posY, sizeX, sizeY, moduleColor, moduleDangerLevel):

    pygame.draw.rect(screen, moduleColor, (posX, posY, sizeX, sizeY), 0, 1)
    pygame.draw.rect(screen, (85, 85, 85), (posX, posY, sizeX, sizeY), 2, 1)
    pygame.draw.rect(screen, (85, 85, 85), (posX + 5, posY + 5, sizeX - 10, 35))
    pygame.draw.circle(screen, (50, 50, 50), (posX + sizeX - 23, posY + 23), 15)
    pygame.draw.circle(screen, (35, 35, 35), (posX + sizeX - 23, posY + 23), 15, 3)
    font = pygame.font.SysFont("monospace", 24)
    questionMark = font.render("?", 1, (255, 255, 255))
    screen.blit(questionMark, ((posX + sizeX - 30, posY + 10)))
    
    if moduleDangerLevel == 0:
        dangerDiodeColor = (0, 185, 0)
    elif moduleDangerLevel == 1:
        if moduleFlashingLightTime <= 30:
            dangerDiodeColor = (225, 225, 0)
        else:
            dangerDiodeColor = (25, 25, 25)          
    else:
        if moduleFlashingLightTime <= 15:
            dangerDiodeColor = (225, 0, 0)
        elif moduleFlashingLightTime > 30 and moduleFlashingLightTime <= 45:
            dangerDiodeColor = (225, 0, 0) 
        else:
            dangerDiodeColor = (25, 25, 25) 
    
    pygame.draw.circle(screen, dangerDiodeColor, (posX + 23, posY + 23), 15)
    pygame.draw.circle(screen, (50, 50, 50), (posX + 23, posY + 23), 15, 3)


"""MODULE LAYOUT/EXAMPLE/BASE
### MODULE CONNECT THE DOTS 
### INITIAL MODULE PARAMETERS (PPT = PRODUCTION PER TICK; TPT = TEMPERATURE PER TICK)
module_CTD_danger_level = 0
module_CTD_PPT = 0.2
module_CTD_TPT = 0.4
module_CTD_randomNumberGiven = pygame.time.get_ticks() + (random.randint(1, 3) * 30 * 1000) / OVERALL_difficulty
module_CTD_lateness_MOE = 5000
module_CTD_errored = False
module_CTD_firstTickTrue = False
### ADDITIONAL PARAMETERS
def reInit_Module_target_practice():
    global module_CTD_randomNumberGiven
    module_CTD_randomNumberGiven = pygame.time.get_ticks() + (random.randint(1, 3) * 30 * 1000) / OVERALL_difficulty
def module_target_practice():
    global core_temperature, core_energy_provided
    global module_CTD_danger_level, module_CTD_lateness_MOE, module_CTD_PPT, module_CTD_randomNumberGiven, module_CTD_TPT, module_CTD_firstTickTrue, module_CTD_timesToClick
    module_create_bounding_box("Target practice", 0, SCREEN_HEIGHT * (2/4), SCREEN_WIDTH * (4/16), SCREEN_HEIGHT * (1/4), (105, 10, 10), module_CTD_danger_level)
    
    if module_CTD_randomNumberGiven < pygame.time.get_ticks() - module_CTD_lateness_MOE:
        module_CTD_danger_level = 2
        module_CTD_errored = True
    elif module_CTD_randomNumberGiven < pygame.time.get_ticks():
        module_CTD_danger_level = 1
        module_CTD_errored = True
    else:
        module_CTD_danger_level = 0
        module_CTD_errored = False
        
    if module_CTD_danger_level == 1:
        pass
    elif module_CTD_danger_level == 2:
        pass
    core_energy_provided += module_CTD_PPT
    
    # OPERATION METHOD
    # The light will turn red. Press it until it gets back to green.
    
    #Check if already errored, if not the initialize it
    if module_CTD_errored == True and module_CTD_firstTickTrue == False:
        #Init danger parameters
        
        
        #Set init danger as DONE
        
        
        pass
        
    if module_CTD_errored == True:
        pass
        
    #button = pygame.draw.circle(screen, buttonColor, (SCREEN_WIDTH * (2/16) / 2, SCREEN_HEIGHT * (3/4) + SCREEN_HEIGHT * (1/4) / 2 + 25), 50)
    #buttonsList.append(("CTD_MainButton_Clicked", "Circle", (SCREEN_WIDTH * (2/16) / 2, SCREEN_HEIGHT * (3/4) + SCREEN_HEIGHT * (1/4) / 2 + 25), 50))
### Functions for that module
def CTD_MainButton_Clicked():
        pass
"""


### OVERALL PARAMETERS ###
OVERALL_difficulty = 20 # Ranges from 1 to 20








### MODULE CLICK UNTIL GREEN
### INITIAL MODULE PARAMETERS (PPT = PRODUCTION PER TICK; TPT = TEMPERATURE PER TICK)
module_CTG_danger_level = 0
module_CTG_PPT = 0.2
module_CTG_TPT = 0.4
module_CTG_randomNumberGiven = pygame.time.get_ticks() + random.randint(1, 3) * 20 * 1000 * (21 - OVERALL_difficulty)
module_CTG_lateness_MOE = 5000
module_CTG_errored = False
module_CTG_firstTickTrue = False
### ADDITIONAL PARAMETERS
module_CTG_timesToClick = 0
def reInit_Module_click_until_green():
    global module_CTG_randomNumberGiven
    module_CTG_randomNumberGiven = pygame.time.get_ticks() + random.randint(1, 3) * 20 * 1000 * (21 - OVERALL_difficulty)
def module_click_until_green():
    global core_temperature, core_energy_provided, enabled
    global module_CTG_danger_level, module_CTG_lateness_MOE, module_CTG_PPT, module_CTG_randomNumberGiven, module_CTG_TPT, module_CTG_firstTickTrue, module_CTG_timesToClick
    module_create_bounding_box("Click until green", 0, SCREEN_HEIGHT * (3/4), SCREEN_WIDTH * (2/16), SCREEN_HEIGHT * (1/4), (105, 10, 10), module_CTG_danger_level)
    
    if module_CTG_randomNumberGiven < pygame.time.get_ticks() - module_CTG_lateness_MOE:
        module_CTG_danger_level = 2
        module_CTG_errored = True
    elif module_CTG_randomNumberGiven < pygame.time.get_ticks():
        module_CTG_danger_level = 1
        module_CTG_errored = True
    else:
        module_CTG_danger_level = 0
        module_CTG_errored = False
        
    if module_CTG_danger_level == 1:
        core_temperature += module_CTG_TPT
    elif module_CTG_danger_level == 2:
        core_temperature += 2 * module_CTG_TPT
    core_energy_provided += module_CTG_PPT
    
    # OPERATION METHOD
    # The light will turn red. Press it until it gets back to green.
    
    #Check if already errored, if not the initialize it
    if module_CTG_errored == True and module_CTG_firstTickTrue == False:
        #Init danger parameters
        module_CTG_timesToClick = random.randint(4, 12)
        
        #Set init danger as DONE
        module_CTG_firstTickTrue = True
        
    if module_CTG_errored == True:
        buttonColor = (255, 0, 0)
        if module_CTG_timesToClick == 0:
            module_CTG_errored = False
            module_CTG_firstTickTrue = False
            module_CTG_danger_level = 0
            reInit_Module_click_until_green()
    else:
        buttonColor = (10, 185, 10)
        
    button = pygame.draw.circle(screen, buttonColor, (SCREEN_WIDTH * (2/16) / 2, SCREEN_HEIGHT * (3/4) + SCREEN_HEIGHT * (1/4) / 2 + 25), 50)
    buttonsList.append(("CTG_MainButton_Clicked", "Circle", (SCREEN_WIDTH * (2/16) / 2, SCREEN_HEIGHT * (3/4) + SCREEN_HEIGHT * (1/4) / 2 + 25), 50))
### Functions for that module
def CTG_MainButton_Clicked():
    global module_CTG_timesToClick
    module_CTG_timesToClick -= 1
    if module_CTG_timesToClick < 0:
        module_CTG_timesToClick = 0
        
        
        
        
        
        




### MODULE TARGET PRACTICE  
### INITIAL MODULE PARAMETERS (PPT = PRODUCTION PER TICK; TPT = TEMPERATURE PER TICK)
module_TP_danger_level = 0
module_TP_PPT = 0.2
module_TP_TPT = 0.4
module_TP_randomNumberGiven = pygame.time.get_ticks() + (random.randint(1, 3) * 30 * 1000) / OVERALL_difficulty
module_TP_setTimeTick = pygame.time.get_ticks()
module_TP_lateness_MOE = 5000
module_TP_errored = False
module_TP_firstTickTrue = False
### RANDOMISATION PARAMETER
module_TP_randomizationTick = None
module_TP_targetsList = []
module_TP_targetsClicked = 0
### ADDITIONAL PARAMETERS
def reInit_Module_target_practice():
    global module_TP_randomNumberGiven
    module_TP_randomNumberGiven = pygame.time.get_ticks() + (random.randint(1, 3) * 30 * 1000) / OVERALL_difficulty
def module_target_practice():
    global core_temperature, core_energy_provided
    global module_TP_danger_level, module_TP_lateness_MOE, module_TP_PPT, module_TP_randomNumberGiven, module_TP_TPT, module_TP_firstTickTrue, module_TP_timesToClick, module_TP_setTimeTick, module_TP_errored, module_TP_targetsList, module_TP_targetsClicked, module_TP_randomizationTick
    module_create_bounding_box("Target practice", 0, SCREEN_HEIGHT * (2/4), SCREEN_WIDTH * (4/16), SCREEN_HEIGHT * (1/4), (105, 10, 10), module_TP_danger_level)
    
    # OPERATION METHOD
    # Red dots will appear, click them to make them disappear
    # If more than 5 circles: module danger level is 1
    # If more than 8 circles: module danger level is 2
                
    interiorPannel = pygame.draw.rect(screen, (10, 10, 10), (SCREEN_WIDTH * (1/128), SCREEN_HEIGHT * (41/72), SCREEN_WIDTH * (15/64), SCREEN_HEIGHT * (1/6)), 0, 30)    
    interiorPannelContour = pygame.draw.rect(screen, (45, 45, 45), (SCREEN_WIDTH * (1/128), SCREEN_HEIGHT * (41/72), SCREEN_WIDTH * (15/64), SCREEN_HEIGHT * (1/6)), 3, 30)
    
    tickDifference = int((module_TP_randomNumberGiven - module_TP_setTimeTick) // 4)
    circlesToDraw = pygame.time.get_ticks() // tickDifference
    circlesToDraw -= module_TP_targetsClicked
    circlesDrawnNumber = len(module_TP_targetsList)
    if circlesToDraw > 0:
        for i in range(circlesToDraw):
            if circlesDrawnNumber > i:
                circleXposition = module_TP_targetsList[i][0]
                circleYposition = module_TP_targetsList[i][1]
                pygame.draw.circle(screen, (200, 10, 10), (circleXposition, circleYposition), 8)
            else:
                circleRandomPositionX = random.randint(30, SCREEN_WIDTH * (4/16) - 30)
                circleRandomPositionY = random.randint(SCREEN_HEIGHT * (2/4) + 60, SCREEN_HEIGHT * (3/4) - 20)
                pygame.draw.circle(screen, (200, 10, 10), (circleRandomPositionX, circleRandomPositionY), 8)
                module_TP_targetsList.append((circleRandomPositionX, circleRandomPositionY))
                
    for button in module_TP_targetsList:
        buttonsList.append(("TP_circle_Clicked", "Circle", (button[0], button[1]), 8))
                
    if len(module_TP_targetsList) >= 8:
        module_TP_danger_level = 2
        core_temperature += 2 * module_CTG_TPT
    elif len(module_TP_targetsList) >= 5:
        module_TP_danger_level = 1
        core_temperature += module_CTG_TPT
    else:
        module_TP_danger_level = 0
### Functions for that module
def TP_circle_Clicked():
    global module_TP_targetsClicked, module_TP_targetsList
    mouseX = pygame.mouse.get_pos()[0]
    mouseY = pygame.mouse.get_pos()[1]
    for circle in module_TP_targetsList:
        if math.sqrt((mouseX - circle[0]) ** 2 + (mouseY - circle[1]) ** 2) < 8:
            module_TP_targetsList.pop(module_TP_targetsList.index(circle))
            module_TP_targetsClicked += 1
        
        
        
        
        
        
        
        
        
### MODULE TETRIS
### INITIAL MODULE PARAMETERS (PPT = PRODUCTION PER TICK; TPT = TEMPERATURE PER TICK)
module_TETRIS_danger_level = 0
module_TETRIS_PPT = 0.2
module_TETRIS_TPT = 0.4
module_TETRIS_randomNumberGiven = pygame.time.get_ticks() + (random.randint(1, 3) * 30 * 1000) / OVERALL_difficulty
module_TETRIS_lateness_MOE = 5000
module_TETRIS_errored = False
module_TETRIS_firstTickTrue = False
### ADDITIONAL PARAMETERS
module_TETRIS_attempts = 0
module_TETRIS_attemptInProgress = False
module_TETRIS_bricksColor = (180, 35, 35)
module_TETRIS_gapPosition = 0
module_TETRIS_movingBlockX = 3
module_TETRIS_movingBlockY = 0
module_TETRIS_movingBlockDelay = 500
module_TETRIS_movingStage = 0
module_TETRIS_timestamp = 0
module_TETRIS_failure = False
module_TETRIS_failTime = None
module_TETRIS_movable = True
module_TETRIS_win = False
def reInit_Module_tetris():
    global module_TETRIS_randomNumberGiven
    module_TETRIS_randomNumberGiven = pygame.time.get_ticks() + (random.randint(1, 3) * 30 * 1000) / OVERALL_difficulty
def module_tetris():
    global core_temperature, core_energy_provided
    global module_TETRIS_danger_level, module_TETRIS_lateness_MOE, module_TETRIS_PPT, module_TETRIS_randomNumberGiven, module_TETRIS_TPT, module_TETRIS_firstTickTrue, module_TETRIS_timesToClick, module_TETRIS_errored, module_TETRIS_attempts, module_TETRIS_attemptInProgress, module_TETRIS_bricksColor, module_TETRIS_gapPosition, module_TETRIS_movingBlockX, module_TETRIS_movingBlockY, module_TETRIS_movingBlockDelay, module_TETRIS_movingStage, module_TETRIS_timestamp, module_TETRIS_failure, module_TETRIS_failTime, module_TETRIS_movable, module_TETRIS_win
    module_create_bounding_box("Tetris", SCREEN_WIDTH * (4/16), SCREEN_HEIGHT * (2/4), SCREEN_WIDTH * (2/16), SCREEN_HEIGHT * (2/4), (105, 10, 10), module_TETRIS_danger_level)
    
    if module_TETRIS_randomNumberGiven < pygame.time.get_ticks() - module_TETRIS_lateness_MOE and module_TETRIS_attempts > 3:
        module_TETRIS_danger_level = 2
        module_TETRIS_errored = True
    elif module_TETRIS_randomNumberGiven < pygame.time.get_ticks():
        module_TETRIS_danger_level = 1
        module_TETRIS_errored = True
    else:
        module_TETRIS_danger_level = 0
        module_TETRIS_errored = False
        
    if module_TETRIS_danger_level == 1:
        core_temperature += module_TETRIS_TPT
    elif module_TETRIS_danger_level == 2:
        core_temperature += 2 * module_TETRIS_TPT
    core_energy_provided += module_TP_PPT
    
    # OPERATION METHOD
    # Once the module is errored, a tetris game will start and you have to orient the block in the hole to clear all lines.
    
    #Check if already errored, if not the initialize it
    if module_TETRIS_errored == True and module_TETRIS_firstTickTrue == False:
        #Init danger parameters
        module_TETRIS_attempts = 0
        #Set init danger as DONE
        module_TETRIS_firstTickTrue = True
    
    if module_TETRIS_errored == True and module_TETRIS_attemptInProgress == False:
        #Init parameters
        module_TETRIS_gapPosition = random.randint(0, 4)
        module_TETRIS_bricksColor = (random.randint(65, 255), random.randint(65, 255), random.randint(65, 255))
        module_TETRIS_movingBlockX = random.randint(0, 4)
        while module_TETRIS_movingBlockX == module_TETRIS_gapPosition:
            module_TETRIS_movingBlockX = random.randint(0, 4)
        module_TETRIS_movingBlockY = 0
        module_TETRIS_timestamp = pygame.time.get_ticks()
        #Init attempt
        module_TETRIS_attempts += 1
        module_TETRIS_movable = True
        module_TETRIS_attemptInProgress = True
     
    if module_TETRIS_errored == True and module_TETRIS_attemptInProgress == True and module_TETRIS_failure == False and module_TETRIS_win == False and module_TETRIS_movable == True:
        for posX in range(5):
            for posY in range(4):
                if posX != module_TETRIS_gapPosition:
                    pygame.draw.rect(screen, module_TETRIS_bricksColor, (SCREEN_WIDTH * (4/16) + 10 + posX * (SCREEN_WIDTH * (2/16) / 5 - 4), SCREEN_HEIGHT * (7/8) - 4 + posY * (SCREEN_HEIGHT * (1/8) / 4 - 2.5), SCREEN_WIDTH * (2/16) / 5 - 4, SCREEN_HEIGHT * (1/8) / 4), 0, 1)
                    pygame.draw.rect(screen, (25, 25, 25),              (SCREEN_WIDTH * (4/16) + 10 + posX * (SCREEN_WIDTH * (2/16) / 5 - 4), SCREEN_HEIGHT * (7/8) - 4 + posY * (SCREEN_HEIGHT * (1/8) / 4 - 2.5), SCREEN_WIDTH * (2/16) / 5 - 4, SCREEN_HEIGHT * (1/8) / 4), 1, 1)
    
        tempYposition = module_TETRIS_movingBlockY
        
        if tempYposition == 9:
            if module_TETRIS_movingBlockX != module_TETRIS_gapPosition:
                module_TETRIS_failTime = pygame.time.get_ticks()
                module_TETRIS_failure = True
                
        if tempYposition >= 9:
            module_TETRIS_movingBlockX = module_TETRIS_gapPosition
            
        if tempYposition == 12:
            module_TETRIS_win = True
                
        for blockIndex in range(4):
            if tempYposition >= 0:
                pygame.draw.rect(screen, module_TETRIS_bricksColor, (SCREEN_WIDTH * (4/16) + 10 + module_TETRIS_movingBlockX * (SCREEN_WIDTH * (2/16) / 5 - 4), SCREEN_HEIGHT * (5/8) - 4 + tempYposition * (SCREEN_HEIGHT * (1/8) / 4 - 2.5),  SCREEN_WIDTH * (2/16) / 5 - 4, SCREEN_HEIGHT * (1/8) / 4), 0, 1)
                pygame.draw.rect(screen, (25, 25, 25),              (SCREEN_WIDTH * (4/16) + 10 + module_TETRIS_movingBlockX * (SCREEN_WIDTH * (2/16) / 5 - 4), SCREEN_HEIGHT * (5/8) - 4 + tempYposition * (SCREEN_HEIGHT * (1/8) / 4 - 2.5),  SCREEN_WIDTH * (2/16) / 5 - 4, SCREEN_HEIGHT * (1/8) / 4), 1, 1)
                tempYposition -= 1
        
        if pygame.time.get_ticks() > module_TETRIS_timestamp + module_TETRIS_movingBlockDelay:
            module_TETRIS_movingBlockY += 1
            module_TETRIS_timestamp = pygame.time.get_ticks()
    
    if module_TETRIS_errored == True and module_TETRIS_attemptInProgress == True and module_TETRIS_failure == True:
        gameOverFont = pygame.font.Font("sources/mouse/fonts/VCR_OSD_MONO.ttf", 20)
        textLabel1 = gameOverFont.render("RIP TETRIS", 1, (255, 0, 0))     
        screen.blit(textLabel1, (SCREEN_WIDTH * (4/16) + 15, SCREEN_HEIGHT * (5/8) + 4))
        textLabel2 = gameOverFont.render("*BONK*", 1, (255, 255, 0))     
        screen.blit(textLabel2, (SCREEN_WIDTH * (9/32), SCREEN_HEIGHT * (7/8)))
        if pygame.time.get_ticks() > module_TETRIS_failTime + 2000:
            module_TETRIS_attemptInProgress = False
            module_TETRIS_failure = False
    
    if module_TETRIS_errored == True and module_TETRIS_attemptInProgress == True and module_TETRIS_win == True:
        module_TETRIS_errored = False
        module_TETRIS_attemptInProgress = False
        module_TETRIS_win = False
        module_TETRIS_firstTickTrue = False
        reInit_Module_tetris()
    
    pygame.draw.rect(screen, (45, 45, 45), (SCREEN_WIDTH * (4/16) + 10, SCREEN_HEIGHT * (5/8) - 4, SCREEN_WIDTH * (2/16) - 20, SCREEN_HEIGHT * (3/8) - 6), 2, 1)
            
    pygame.draw.rect(screen, (185, 125, 15), (SCREEN_WIDTH * (4/16) + 10, SCREEN_HEIGHT * (1/2) + 50, SCREEN_WIDTH * (1/16) - 20, SCREEN_HEIGHT * (1/16) - 20), 0, 3)
    pygame.draw.rect(screen, (45, 45, 45), (SCREEN_WIDTH * (4/16) + 10, SCREEN_HEIGHT * (1/2) + 50, SCREEN_WIDTH * (1/16) - 20, SCREEN_HEIGHT * (1/16) - 20), 2, 3)
    tetrisTextFont = pygame.font.SysFont('monospace', 20)
    labelLeftArrow = tetrisTextFont.render("◄◄◄", 1, (0, 0, 0))
    screen.blit(labelLeftArrow, (SCREEN_WIDTH * (4/16) + 20, SCREEN_HEIGHT * (1/2) + 52))
    buttonsList.append(("TETRIS_LeftClicked", "Rectangle", ((SCREEN_WIDTH * (4/16) + 10, SCREEN_HEIGHT * (1/2) + 50, SCREEN_WIDTH * (1/16) - 20, SCREEN_HEIGHT * (1/16) - 20))))
    
    pygame.draw.rect(screen, (185, 125, 15), (SCREEN_WIDTH * (5/16) + 10, SCREEN_HEIGHT * (1/2) + 50, SCREEN_WIDTH * (1/16) - 20, SCREEN_HEIGHT * (1/16) - 20), 0, 3)
    pygame.draw.rect(screen, (45, 45, 45), (SCREEN_WIDTH * (5/16) + 10, SCREEN_HEIGHT * (1/2) + 50, SCREEN_WIDTH * (1/16) - 20, SCREEN_HEIGHT * (1/16) - 20), 2, 3)
    tetrisTextFont = pygame.font.SysFont('monospace', 20)
    labelRightArrow = tetrisTextFont.render("►►►", 1, (0, 0, 0))
    screen.blit(labelRightArrow, (SCREEN_WIDTH * (5/16) + 25, SCREEN_HEIGHT * (1/2) + 52))
    buttonsList.append(("TETRIS_RightClicked", "Rectangle", ((SCREEN_WIDTH * (5/16) + 10, SCREEN_HEIGHT * (1/2) + 50, SCREEN_WIDTH * (1/16) - 20, SCREEN_HEIGHT * (1/16) - 20))))
    
### Functions for that module
def TETRIS_LeftClicked():
    global module_TETRIS_movingBlockX
    module_TETRIS_movingBlockX -= 1
    if module_TETRIS_movingBlockX < 0:
        module_TETRIS_movingBlockX = 0
def TETRIS_RightClicked():
    global module_TETRIS_movingBlockX
    module_TETRIS_movingBlockX += 1
    if module_TETRIS_movingBlockX > 4:
        module_TETRIS_movingBlockX = 4
    
    
    
    
    
    
    
    
    
    
    
### MODULE IT POPS
### INITIAL MODULE PARAMETERS (PPT = PRODUCTION PER TICK; TPT = TEMPERATURE PER TICK)
module_IP_danger_level = 0
module_IP_PPT = 0.2
module_IP_TPT = 0.4
module_IP_randomNumberGiven = pygame.time.get_ticks() + (random.randint(1, 3) * 30 * 1000) / OVERALL_difficulty
module_IP_lateness_MOE = 5000
module_IP_errored = False
module_IP_firstTickTrue = False
### ADDITIONAL PARAMETERS
module_IP_buttonsIndex = [0, 0, 0, 0]
def reInit_Module_it_pops():
    global module_IP_randomNumberGiven
    module_IP_randomNumberGiven = pygame.time.get_ticks() + (random.randint(1, 3) * 30 * 1000) / OVERALL_difficulty
def module_it_pops():
    global core_temperature, core_energy_provided
    global module_IP_danger_level, module_IP_lateness_MOE, module_IP_PPT, module_IP_randomNumberGiven, module_IP_TPT, module_IP_firstTickTrue, module_IP_timesToClick, module_IP_buttonsIndex
    module_create_bounding_box("It pops", SCREEN_WIDTH * (2/16), SCREEN_HEIGHT * (3/4), SCREEN_WIDTH * (2/16), SCREEN_HEIGHT * (1/4), (105, 10, 10), module_IP_danger_level)
    
    if module_IP_randomNumberGiven < pygame.time.get_ticks() - module_IP_lateness_MOE:
        module_IP_danger_level = 2
        module_IP_errored = True
    elif module_IP_randomNumberGiven < pygame.time.get_ticks():
        module_IP_danger_level = 1
        module_IP_errored = True
    else:
        module_IP_danger_level = 0
        module_IP_errored = False
        
    if module_IP_danger_level == 1:
        core_temperature += module_IP_TPT
    elif module_IP_danger_level == 2:
        core_temperature += 2 * module_IP_TPT
    core_energy_provided += module_IP_PPT
    
    # OPERATION METHOD
    # Once the module is errored, the 4 buttons will light up. Click them to make them the same color and the module will be disarmed.
    colorList = [(0, (155, 15, 15)), (1, (15, 155, 15)), (2, (15, 15, 155)), (3, (155, 155, 15)), (4, (155, 15, 155)), (5, (15, 155, 155)), (6, (255, 255, 255))]
    #Check if already errored, if not the initialize it
    if module_IP_errored == True and module_IP_firstTickTrue == False:
        #Init danger parameters
        for index in range(len(module_IP_buttonsIndex)):
            random.seed(pygame.time.get_ticks() - random.randint(1, 1000) * 1000)
            button = random.randint(0, 6)
            module_IP_buttonsIndex[index] = button
        while module_IP_buttonsIndex[1] == module_IP_buttonsIndex[2] or module_IP_buttonsIndex[2] == module_IP_buttonsIndex[3] or module_IP_buttonsIndex[3] == module_IP_buttonsIndex[0] or module_IP_buttonsIndex[0] == module_IP_buttonsIndex[1]:
            for index in range(len(module_IP_buttonsIndex)):
                random.seed(pygame.time.get_ticks() - random.randint(1, 1000) * 1000)
                button = random.randint(0, 6)
                module_IP_buttonsIndex[index] = button
        #Set init danger as DONE
        module_IP_firstTickTrue = True
        
    if module_IP_errored == True:
        button = pygame.draw.circle(screen, (55, 55, 55), (SCREEN_WIDTH * (7/64) + SCREEN_WIDTH * (3/32) / 2, SCREEN_HEIGHT * (53/64) + SCREEN_HEIGHT * (1/4) / 2), 25)
        button = pygame.draw.circle(screen, colorList[module_IP_buttonsIndex[0]][1], (SCREEN_WIDTH * (7/64) + SCREEN_WIDTH * (3/32) / 2, SCREEN_HEIGHT * (53/64) + SCREEN_HEIGHT * (1/4) / 2), 21)
        buttonsList.append(("IP_DownLeftClicked", "Circle", (SCREEN_WIDTH * (7/64) + SCREEN_WIDTH * (3/32) / 2, SCREEN_HEIGHT * (13/16) + SCREEN_HEIGHT * (1/4) / 2), 25))
        
        button = pygame.draw.circle(screen, (55, 55, 55), (SCREEN_WIDTH * (7/64) + SCREEN_WIDTH * (3/32) / 2, SCREEN_HEIGHT * (47/64) + SCREEN_HEIGHT * (1/4) / 2), 25)
        button = pygame.draw.circle(screen, colorList[module_IP_buttonsIndex[1]][1], (SCREEN_WIDTH * (7/64) + SCREEN_WIDTH * (3/32) / 2, SCREEN_HEIGHT * (47/64) + SCREEN_HEIGHT * (1/4) / 2), 21)
        buttonsList.append(("IP_TopLeftClicked", "Circle", (SCREEN_WIDTH * (7/64) + SCREEN_WIDTH * (3/32) / 2, SCREEN_HEIGHT * (47/64) + SCREEN_HEIGHT * (1/4) / 2), 25))
        
        button = pygame.draw.circle(screen, (55, 55, 55), (SCREEN_WIDTH * (11/64) + SCREEN_WIDTH * (3/32) / 2, SCREEN_HEIGHT * (53/64) + SCREEN_HEIGHT * (1/4) / 2), 25)
        button = pygame.draw.circle(screen, colorList[module_IP_buttonsIndex[2]][1], (SCREEN_WIDTH * (11/64) + SCREEN_WIDTH * (3/32) / 2, SCREEN_HEIGHT * (53/64) + SCREEN_HEIGHT * (1/4) / 2), 21)
        buttonsList.append(("IP_DownRightClicked", "Circle", (SCREEN_WIDTH * (11/64) + SCREEN_WIDTH * (3/32) / 2, SCREEN_HEIGHT * (53/64) + SCREEN_HEIGHT * (1/4) / 2), 25))
        
        button = pygame.draw.circle(screen, (55, 55, 55), (SCREEN_WIDTH * (11/64) + SCREEN_WIDTH * (3/32) / 2, SCREEN_HEIGHT * (47/64) + SCREEN_HEIGHT * (1/4) / 2), 25)
        button = pygame.draw.circle(screen, colorList[module_IP_buttonsIndex[3]][1], (SCREEN_WIDTH * (11/64) + SCREEN_WIDTH * (3/32) / 2, SCREEN_HEIGHT * (47/64) + SCREEN_HEIGHT * (1/4) / 2), 21)
        buttonsList.append(("IP_TopRightClicked", "Circle", (SCREEN_WIDTH * (11/64) + SCREEN_WIDTH * (3/32) / 2, SCREEN_HEIGHT * (47/64) + SCREEN_HEIGHT * (1/4) / 2), 25))
        
        if module_IP_buttonsIndex[0] == module_IP_buttonsIndex[1] ==  module_IP_buttonsIndex[2] == module_IP_buttonsIndex[3]:
            module_IP_errored = False
            module_IP_firstTickTrue = False
            reInit_Module_it_pops()
    else:
        button = pygame.draw.circle(screen, (55, 55, 55), (SCREEN_WIDTH * (7/64) + SCREEN_WIDTH * (3/32) / 2, SCREEN_HEIGHT * (53/64) + SCREEN_HEIGHT * (1/4) / 2), 25)
        button = pygame.draw.circle(screen, (135, 135, 135), (SCREEN_WIDTH * (7/64) + SCREEN_WIDTH * (3/32) / 2, SCREEN_HEIGHT * (53/64) + SCREEN_HEIGHT * (1/4) / 2), 21)
        buttonsList.append(("IP_DownLeftClicked", "Circle", (SCREEN_WIDTH * (7/64) + SCREEN_WIDTH * (3/32) / 2, SCREEN_HEIGHT * (13/16) + SCREEN_HEIGHT * (1/4) / 2), 25))
        
        button = pygame.draw.circle(screen, (55, 55, 55), (SCREEN_WIDTH * (7/64) + SCREEN_WIDTH * (3/32) / 2, SCREEN_HEIGHT * (47/64) + SCREEN_HEIGHT * (1/4) / 2), 25)
        button = pygame.draw.circle(screen, (135, 135, 135), (SCREEN_WIDTH * (7/64) + SCREEN_WIDTH * (3/32) / 2, SCREEN_HEIGHT * (47/64) + SCREEN_HEIGHT * (1/4) / 2), 21)
        buttonsList.append(("IP_TopLeftClicked", "Circle", (SCREEN_WIDTH * (7/64) + SCREEN_WIDTH * (3/32) / 2, SCREEN_HEIGHT * (47/64) + SCREEN_HEIGHT * (1/4) / 2), 25))
        
        button = pygame.draw.circle(screen, (55, 55, 55), (SCREEN_WIDTH * (11/64) + SCREEN_WIDTH * (3/32) / 2, SCREEN_HEIGHT * (53/64) + SCREEN_HEIGHT * (1/4) / 2), 25)
        button = pygame.draw.circle(screen, (135, 135, 135), (SCREEN_WIDTH * (11/64) + SCREEN_WIDTH * (3/32) / 2, SCREEN_HEIGHT * (53/64) + SCREEN_HEIGHT * (1/4) / 2), 21)
        buttonsList.append(("IP_DownRightClicked", "Circle", (SCREEN_WIDTH * (11/64) + SCREEN_WIDTH * (3/32) / 2, SCREEN_HEIGHT * (53/64) + SCREEN_HEIGHT * (1/4) / 2), 25))
        
        button = pygame.draw.circle(screen, (55, 55, 55), (SCREEN_WIDTH * (11/64) + SCREEN_WIDTH * (3/32) / 2, SCREEN_HEIGHT * (47/64) + SCREEN_HEIGHT * (1/4) / 2), 25)
        button = pygame.draw.circle(screen, (135, 135, 135), (SCREEN_WIDTH * (11/64) + SCREEN_WIDTH * (3/32) / 2, SCREEN_HEIGHT * (47/64) + SCREEN_HEIGHT * (1/4) / 2), 21)
        buttonsList.append(("IP_TopRightClicked", "Circle", (SCREEN_WIDTH * (11/64) + SCREEN_WIDTH * (3/32) / 2, SCREEN_HEIGHT * (47/64) + SCREEN_HEIGHT * (1/4) / 2), 25))
### Functions for that module
def IP_DownLeftClicked():
    global module_IP_buttonsIndex
    module_IP_buttonsIndex[0] += 1
    if module_IP_buttonsIndex[0] > 6:
        module_IP_buttonsIndex[0] = 0
def IP_TopLeftClicked():
    global module_IP_buttonsIndex
    module_IP_buttonsIndex[1] += 1
    if module_IP_buttonsIndex[1] > 6:
        module_IP_buttonsIndex[1] = 0
def IP_DownRightClicked():
    global module_IP_buttonsIndex
    module_IP_buttonsIndex[2] += 1
    if module_IP_buttonsIndex[2] > 6:
        module_IP_buttonsIndex[2] = 0
def IP_TopRightClicked():
    global module_IP_buttonsIndex
    module_IP_buttonsIndex[3] += 1
    if module_IP_buttonsIndex[3] > 6:
        module_IP_buttonsIndex[3] = 0










### MODULE CONNECT THE DOTS 
### INITIAL MODULE PARAMETERS (PPT = PRODUCTION PER TICK; TPT = TEMPERATURE PER TICK)
module_CTD_danger_level = 0
module_CTD_PPT = 0.2
module_CTD_TPT = 0.4
module_CTD_randomNumberGiven = pygame.time.get_ticks() + (random.randint(1, 3) * 30 * 1000) / OVERALL_difficulty
module_CTD_lateness_MOE = 5000
module_CTD_errored = False
module_CTD_firstTickTrue = False
### ADDITIONAL PARAMETERS
module_CTD_patternsList = [
    [
        (SCREEN_WIDTH * (1000/1280), SCREEN_HEIGHT * (500/720)), (SCREEN_WIDTH * (1075/1280), SCREEN_HEIGHT * (500/720)), (SCREEN_WIDTH * (1115/1280), SCREEN_HEIGHT * (450/720)), (SCREEN_WIDTH * (1150/1280), SCREEN_HEIGHT * (500/720)), (SCREEN_WIDTH * (1225/1280), SCREEN_HEIGHT * (500/720)), (SCREEN_WIDTH * (1160/1280), SCREEN_HEIGHT * (550/720)), (SCREEN_WIDTH * (1200/1280), SCREEN_HEIGHT * (550/720)), (SCREEN_WIDTH * (1115/1280), SCREEN_HEIGHT * (550/720)), (SCREEN_WIDTH * (1030/1280), SCREEN_HEIGHT * (550/720)), (SCREEN_WIDTH * (1070/1280), SCREEN_HEIGHT * (550/720)), (SCREEN_WIDTH * (1000/1280), SCREEN_HEIGHT * (500/720))
    ],
    [
        (SCREEN_WIDTH * (1050/1280), SCREEN_HEIGHT * (650/720)), (SCREEN_WIDTH * (1125/1280), SCREEN_HEIGHT * (450/720)), (SCREEN_WIDTH * (1200/1280), SCREEN_HEIGHT * (650/720)), (SCREEN_WIDTH * (1020/1280), SCREEN_HEIGHT * (525/720)), (SCREEN_WIDTH * (1230/1280), SCREEN_HEIGHT * (525/720)), (SCREEN_WIDTH * (1050/1280), SCREEN_HEIGHT * (650/720))
    ],
    [
        (SCREEN_WIDTH * (1000/1280), SCREEN_HEIGHT * (450/720)), (SCREEN_WIDTH * (1050/1280), SCREEN_HEIGHT * (450/720)), (SCREEN_WIDTH * (1075/1280), SCREEN_HEIGHT * (475/720)), (SCREEN_WIDTH * (1075/1280), SCREEN_HEIGHT * (500/720)), (SCREEN_WIDTH * (1100/1280), SCREEN_HEIGHT * (500/720)), (SCREEN_WIDTH * (1100/1280), SCREEN_HEIGHT * (475/720)), (SCREEN_WIDTH * (1125/1280), SCREEN_HEIGHT * (475/720)), (SCREEN_WIDTH * (1125/1280), SCREEN_HEIGHT * (500/720)), (SCREEN_WIDTH * (1150/1280), SCREEN_HEIGHT * (500/720)), (SCREEN_WIDTH * (1150/1280), SCREEN_HEIGHT * (475/720)), (SCREEN_WIDTH * (1175/1280), SCREEN_HEIGHT * (450/720)), (SCREEN_WIDTH * (1225/1280), SCREEN_HEIGHT * (450/720)), (SCREEN_WIDTH * (1150/1280), SCREEN_HEIGHT * (550/720)), (SCREEN_WIDTH * (1150/1280), SCREEN_HEIGHT * (625/720)), (SCREEN_WIDTH * (1175/1280), SCREEN_HEIGHT * (625/720)), (SCREEN_WIDTH * (1175/1280), SCREEN_HEIGHT * (650/720)), (SCREEN_WIDTH * (1150/1280), SCREEN_HEIGHT * (650/720)), (SCREEN_WIDTH * (1112.5/1280), SCREEN_HEIGHT * (680/720)), (SCREEN_WIDTH * (1075/1280), SCREEN_HEIGHT * (650/720)), (SCREEN_WIDTH * (1050/1280), SCREEN_HEIGHT * (650/720)), (SCREEN_WIDTH * (1050/1280), SCREEN_HEIGHT * (625/720)), (SCREEN_WIDTH * (1075/1280), SCREEN_HEIGHT * (625/720)), (SCREEN_WIDTH * (1075/1280), SCREEN_HEIGHT * (550/720)), (SCREEN_WIDTH * (1000/1280), SCREEN_HEIGHT * (450/720))
    ]
]
module_CTD_patternChosen = []
module_CTD_patternProgressionIndex = 0
def reInit_Module_connect_the_dots():
    global module_CTD_randomNumberGiven
    module_CTD_randomNumberGiven = pygame.time.get_ticks() + (random.randint(1, 3) * 30 * 1000) / OVERALL_difficulty
def module_connect_the_dots():
    global core_temperature, core_energy_provided
    global module_CTD_danger_level, module_CTD_lateness_MOE, module_CTD_PPT, module_CTD_randomNumberGiven, module_CTD_TPT, module_CTD_firstTickTrue, module_CTD_timesToClick, module_CTD_patternChosen, module_CTD_patternProgressionIndex, module_CTD_patternsList
    module_create_bounding_box("Connect the dots", SCREEN_WIDTH * (3/4), SCREEN_HEIGHT * (2/4), SCREEN_WIDTH * (1/4), SCREEN_HEIGHT * (2/4), (105, 10, 10), module_CTD_danger_level)
    
    if module_CTD_randomNumberGiven < pygame.time.get_ticks() - module_CTD_lateness_MOE:
        module_CTD_danger_level = 2
        core_temperature += 2 * module_CTD_TPT
        module_CTD_errored = True
    elif module_CTD_randomNumberGiven < pygame.time.get_ticks():
        module_CTD_danger_level = 1
        core_temperature += module_CTD_TPT
        module_CTD_errored = True
    else:
        module_CTD_danger_level = 0
        module_CTD_errored = False
        
    if module_CTD_danger_level == 1:
        pass
    elif module_CTD_danger_level == 2:
        pass
    core_energy_provided += module_CTD_PPT
    
    pygame.draw.rect(screen, (55, 55, 55), (SCREEN_WIDTH * (3/4) + 10, SCREEN_HEIGHT * (2/4) + 55, SCREEN_WIDTH * (1/4) - 20, SCREEN_HEIGHT * (2/4) - 65), 0, 10)
    pygame.draw.rect(screen, (0, 0, 0), (SCREEN_WIDTH * (3/4) + 10, SCREEN_HEIGHT * (2/4) + 55, SCREEN_WIDTH * (1/4) - 20, SCREEN_HEIGHT * (2/4) - 65), 3, 10)   
    
    # OPERATION METHOD
    # Once the module gets errored, buttons will pop. Click on them in order to connect the dots and draw a shape.
    
    #Check if already errored, if not the initialize it
    if module_CTD_errored == True and module_CTD_firstTickTrue == False:
        #Init danger parameters
        module_CTD_patternChosen = random.randint(0, len(module_CTD_patternsList) - 1)
        module_CTD_patternProgressionIndex = 0
        #Set init danger as DONE
        module_CTD_firstTickTrue = True
        
    if module_CTD_errored == True:
        buttonColor = (255, 0, 0)
        button = pygame.draw.circle(screen, buttonColor, module_CTD_patternsList[module_CTD_patternChosen][module_CTD_patternProgressionIndex], 10)
        buttonsList.append(("CTD_NextDot_Clicked", "Circle", module_CTD_patternsList[module_CTD_patternChosen][module_CTD_patternProgressionIndex], 10))
        for i in range(len(module_CTD_patternsList[module_CTD_patternChosen])):
            if module_CTD_patternProgressionIndex > i:
                pygame.draw.line(screen, (255, 0, 0), module_CTD_patternsList[module_CTD_patternChosen][i], module_CTD_patternsList[module_CTD_patternChosen][i + 1], 5)
### Functions for that module
def CTD_NextDot_Clicked():
    global module_CTD_patternProgressionIndex, module_CTD_patternChosen
    module_CTD_patternProgressionIndex += 1
    if module_CTD_patternProgressionIndex > len(module_CTD_patternsList[module_CTD_patternChosen]) - 1:
        module_CTD_errored = False
        module_CTD_firstTickTrue = False
        module_CTD_patternProgressionIndex = 0
        reInit_Module_connect_the_dots()
     
    
    
    
    
    
    
    
    
### MODULE CODE
### INITIAL MODULE PARAMETERS (PPT = PRODUCTION PER TICK; TPT = TEMPERATURE PER TICK)
module_CD_danger_level = 0
module_CD_PPT = 0.2
module_CD_TPT = 0.4
module_CD_randomNumberGiven = pygame.time.get_ticks() + (random.randint(1, 3) * 30 * 1000) / OVERALL_difficulty
module_CD_lateness_MOE = 5000
module_CD_errored = False
module_CD_firstTickTrue = False
### ADDITIONAL PARAMETERS
module_CD_setCode = None
module_CD_inputCode = None
def reInit_Module_code():
    global module_CD_randomNumberGiven
    module_CD_randomNumberGiven = pygame.time.get_ticks() + (random.randint(1, 3) * 30 * 1000) / OVERALL_difficulty
def module_code():
    global core_temperature, core_energy_provided
    global module_CD_danger_level, module_CD_lateness_MOE, module_CD_PPT, module_CD_randomNumberGiven, module_CD_TPT, module_CD_firstTickTrue, module_CD_timesToClick
    module_create_bounding_box("Code", SCREEN_WIDTH * (10/16), SCREEN_HEIGHT * (5/8), SCREEN_WIDTH * (2/16), SCREEN_HEIGHT * (3/8), (105, 10, 10), module_CD_danger_level)
    
    if module_CD_randomNumberGiven < pygame.time.get_ticks() - module_CD_lateness_MOE:
        module_CD_danger_level = 2
        module_CD_errored = True
    elif module_CD_randomNumberGiven < pygame.time.get_ticks():
        module_CD_danger_level = 1
        module_CD_errored = True
    else:
        module_CD_danger_level = 0
        module_CD_errored = False
        
    if module_CD_danger_level == 1:
        core_temperature += module_CD_TPT
    elif module_CD_danger_level == 2:
        core_temperature += 2 * module_CD_TPT
    core_energy_provided += module_CD_PPT
    
    # OPERATION METHOD
    # A code will be shown. Input it to reset the module.
    
    #Check if already errored, if not the initialize it
    if module_CD_errored == True and module_CD_firstTickTrue == False:
        #Init danger parameters
        module_CD_setCode = random.randint(1000, 9999)
        module_CD_inputCode = None
        #Set init danger as DONE
        module_CD_firstTickTrue = True
        
    pygame.draw.rect(screen, (0, 0, 0), (SCREEN_WIDTH * (10/16) + 10, SCREEN_HEIGHT * (6/8) + 55, SCREEN_WIDTH * (2/16) / 3 - 20, SCREEN_HEIGHT * (2/8) / 3 - 65), 0)
    
    #button = pygame.draw.circle(screen, buttonColor, (SCREEN_WIDTH * (2/16) / 2, SCREEN_HEIGHT * (3/4) + SCREEN_HEIGHT * (1/4) / 2 + 25), 50)
    #buttonsList.append(("CD_MainButton_Clicked", "Circle", (SCREEN_WIDTH * (2/16) / 2, SCREEN_HEIGHT * (3/4) + SCREEN_HEIGHT * (1/4) / 2 + 25), 50))
### Functions for that module
def CD_1_Clicked():
    global module_CD_inputCode
    if len(module_CD_inputCode) < 4:
        module_CD_inputCode += "1"
def CD_2_Clicked():
    global module_CD_inputCode
    if len(module_CD_inputCode) < 4:
        module_CD_inputCode += "2"
def CD_3_Clicked():
    global module_CD_inputCode
    if len(module_CD_inputCode) < 4:
        module_CD_inputCode += "3"
def CD_4_Clicked():
    global module_CD_inputCode
    if len(module_CD_inputCode) < 4:
        module_CD_inputCode += "4"
def CD_5_Clicked():
    global module_CD_inputCode
    if len(module_CD_inputCode) < 4:
        module_CD_inputCode += "5"
def CD_6_Clicked():
    global module_CD_inputCode
    if len(module_CD_inputCode) < 4:
        module_CD_inputCode += "6"
def CD_7_Clicked():
    global module_CD_inputCode
    if len(module_CD_inputCode) < 4:
        module_CD_inputCode += "7"  
def CD_8_Clicked():
    global module_CD_inputCode
    if len(module_CD_inputCode) < 4:
        module_CD_inputCode += "8"
def CD_9_Clicked():
    global module_CD_inputCode
    if len(module_CD_inputCode) < 4:
        module_CD_inputCode += "9"
def CD_0_Clicked():
    global module_CD_inputCode
    if len(module_CD_inputCode) < 4:
        module_CD_inputCode += "0"
def CD_back_Clicked():
    global module_CD_inputCode
    if len(module_CD_inputCode) > 0:
        module_CD_inputCode = module_CD_inputCode[:-1]
def CD_enter_Clicked():
    global module_CD_inputCode, module_CD_setCode, module_CD_errored, module_CD_firstTickTrue
    if module_CD_inputCode == str(module_CD_setCode):
        module_CD_errored = False
        module_CD_firstTickTrue = False
        reInit_Module_code()
    
    
    
    
    
    
    
    
    
"""
### RANDOMISATION SETTINGS
randomizer_DIFF = 20 # Ranges from 1 to 20
def handleModulesRandomization():
"""


def energyBarIndications():
    global core_energy_provided, core_energy_demand
    font = pygame.font.Font('sources/mouse/fonts/VCR_OSD_MONO.ttf', 25)
    text = font.render(str(round(core_energy_provided)) + "/" + str(core_energy_demand), 1, (25, 25, 180))
    textRect = text.get_rect()
    textRect.center = (SCREEN_WIDTH * (1/2), SCREEN_HEIGHT * (68.5/144))
    screen.blit(text, textRect)

moduleFlashingLightTime = 0

### INITIALIZING CORE PARAMETERS
core_temperature = 0
core_max_temperature = 4000
core_energy_demand = 300
core_energy_provided = 0


def Render_Text(what, color, where):
    font = pygame.font.SysFont('monospace', 30)
    text = font.render(what, 1, pygame.Color(color))
    screen.blit(text, where)

### MAIN LOOP
while running:
    screen.fill((0, 0, 0))
    screen.blit(bg, (0, 0))
    
    #Create the layout
    create_layout()
    
    #Modules handler
    module_click_until_green()
    module_target_practice()
    module_tetris()
    module_it_pops()
    module_connect_the_dots()
    module_code()
    
    #Misc handler
    energyBarIndications()
    
    mouseX = pygame.mouse.get_pos()[0]
    mouseY = pygame.mouse.get_pos()[1]
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouseX = pygame.mouse.get_pos()[0]
            mouseY = pygame.mouse.get_pos()[1]
            
            for clickable in range(len(buttonsList)):
                if buttonsList[clickable][1] == "Circle":
                    if math.sqrt((mouseX - buttonsList[clickable][2][0]) ** 2 + (mouseY - buttonsList[clickable][2][1]) ** 2) < buttonsList[clickable][3]:
                        function = globals()[buttonsList[clickable][0]]
                        function()
                if buttonsList[clickable][1] == "Rectangle":
                    if buttonsList[clickable][2][0] <= mouseX <= buttonsList[clickable][2][0] + buttonsList[clickable][2][2] and buttonsList[clickable][2][1] <= mouseY <= buttonsList[clickable][2][1] + buttonsList[clickable][2][3]:
                        function = globals()[buttonsList[clickable][0]]
                        function()
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.mixer.stop()
                running = False
                
    Render_Text(str(int(clock.get_fps())), (255,0,0), (0,0))
    
    # Update the display
    pygame.display.flip()

    #Update values
    moduleFlashingLightTime += 1
    if moduleFlashingLightTime == 60:
        moduleFlashingLightTime = 0
    
    temperatureBarLightsOn = core_temperature // 60
    
    buttonsList = []
    
    # Cap the frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()
sys.exit()

