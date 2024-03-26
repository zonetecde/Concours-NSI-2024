import pygame
import sys
import math
import json
import random
from os.path import exists


# Initialize Pygame
pygame.init()

# Initialize el pymixer boi
pygame.mixer.init()
backgroundAmbientChannel = pygame.mixer.Channel(0)
alertsChannel = pygame.mixer.Channel(1)
miscChannel = pygame.mixer.Channel(2)
playerActionsChannel = pygame.mixer.Channel(3)

# Initialize all audio files
ambientLoop = pygame.mixer.Sound("sources/mouse/scripts/STR/STR_ASSETS/coreLoopAmbient.wav")
moduleClear = pygame.mixer.Sound("sources/mouse/scripts/STR/STR_ASSETS/beepButtonPress.wav")
coolantStartup = pygame.mixer.Sound("sources/mouse/scripts/STR/STR_ASSETS/coolantStartupProtocolInitiated.wav")
coreAtCriticalCut = pygame.mixer.Sound("sources/mouse/scripts/STR/STR_ASSETS/coreAtCriticalCut.wav")
coreMeltdownInTwoMinutes = pygame.mixer.Sound("sources/mouse/scripts/STR/STR_ASSETS/CoreMeltdownSelfDestructSequenceInitiated.wav")
playerClick = pygame.mixer.Sound("sources/mouse/scripts/STR/STR_ASSETS/highPitchedBeep.wav")
selfDestructInitiated = pygame.mixer.Sound("sources/mouse/scripts/STR/STR_ASSETS/InstantMeltdownProtocolInitiated.wav")
lockdown = pygame.mixer.Sound("sources/mouse/scripts/STR/STR_ASSETS/Lockdown.wav")
pbAlarm1 = pygame.mixer.Sound("sources/mouse/scripts/STR/STR_ASSETS/pbAlarm1.wav")
pbAlarm2 = pygame.mixer.Sound("sources/mouse/scripts/STR/STR_ASSETS/pbAlarm2.wav")
pbAlarm3 = pygame.mixer.Sound("sources/mouse/scripts/STR/STR_ASSETS/pbAlarm3.wav")
pbAlarm4 = pygame.mixer.Sound("sources/mouse/scripts/STR/STR_ASSETS/pbAlarm4.wav")
pbAlarm5 = pygame.mixer.Sound("sources/mouse/scripts/STR/STR_ASSETS/pbAlarm5.wav")
coreSafeguardNonFunctional = pygame.mixer.Sound("sources/mouse/scripts/STR/STR_ASSETS/prepareForReactorCoreMeltdown.wav")
safeModeDesactivated = pygame.mixer.Sound("sources/mouse/scripts/STR/STR_ASSETS/SafeModeDesactivated.wav")
coreOverheating = pygame.mixer.Sound("sources/mouse/scripts/STR/STR_ASSETS/warningCoreOverheating.wav")
finalExplosion = pygame.mixer.Sound("sources/mouse/scripts/STR/STR_ASSETS/finalExplosion.wav")

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
hoverList = []

running = True

def create_layout():
    modulesCentralZone = pygame.draw.rect(screen, (135, 135, 135), (0, SCREEN_HEIGHT/2, SCREEN_WIDTH, SCREEN_HEIGHT/2))
    modulesCentralZoneContour = pygame.draw.rect(screen, (125, 0, 0), (0, SCREEN_HEIGHT/2, SCREEN_WIDTH, SCREEN_HEIGHT/2), 5)
    
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
    
def module_create_bounding_box(moduleName, posX, posY, sizeX, sizeY, moduleColor, moduleDangerLevel, hoverText = ""):

    pygame.draw.rect(screen, moduleColor, (posX, posY, sizeX, sizeY), 0, 1)
    pygame.draw.rect(screen, (85, 85, 85), (posX, posY, sizeX, sizeY), 2, 1)
    pygame.draw.rect(screen, (85, 85, 85), (posX + 5, posY + 5, sizeX - 10, 35))
    
    pygame.draw.circle(screen, (50, 50, 50), (posX + sizeX - 23, posY + 23), 15)
    pygame.draw.circle(screen, (35, 35, 35), (posX + sizeX - 23, posY + 23), 15, 3)
    font = pygame.font.SysFont("monospace", 24)
    questionMark = font.render("?", 1, (255, 255, 255))
    screen.blit(questionMark, ((posX + sizeX - 30, posY + 10)))
    hoverList.append((posX + sizeX - 23, posY + 23, hoverText))
    
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

### OVERALL PARAMETERS ### IMP MAX!
OVERALL_difficulty = 3 # Ranges from 1 to 20
### 1 is VERY VERY VERY easy, 20 is VERY VERY VERY hard
### Min rcmd is 5, max rcmd is 15
OVERALL_days = 1

OVERALL_CORE_MELTDOWN_STARTED = False
OVERALL_CORE_MELTDOWN_STARTTICK = None
OVERALL_CORE_MELTDOWN_TIME_LEFT = 120000 # 2 minutes

moduleFlashingLightTime = 0

### INITIALIZING CORE PARAMETERS
core_temperature = 0
core_max_temperature = 4000
core_energy_demand = 300
core_energy_demand_list = [300, 450, 600, 900, 1200, 1550, 2000]
core_energy_provided = 0

GAME_OVER = False

### MODULE CLICK UNTIL GREEN
### INITIAL MODULE PARAMETERS (PPT = PRODUCTION PER TICK; TPT = TEMPERATURE PER TICK)
module_CTG_danger_level = 0
module_CTG_PPT = 0.2
module_CTG_TPT = 0.4
module_CTG_randomNumberGiven = pygame.time.get_ticks() + (random.randint(1, 3) * 30 * 1000) / OVERALL_difficulty
module_CTG_lateness_MOE = 5000 + 500 *  (20 - OVERALL_difficulty)
module_CTG_errored = False
module_CTG_firstTickTrue = False
### ADDITIONAL PARAMETERS
module_CTG_timesToClick = 0

def reInit_Module_click_until_green():
    global module_CTG_randomNumberGiven
    module_CTG_randomNumberGiven = pygame.time.get_ticks() + (random.randint(1, 3) * 30 * 1000) / OVERALL_difficulty

def module_click_until_green():
    global core_temperature, core_energy_provided, enabled
    global module_CTG_danger_level, module_CTG_lateness_MOE, module_CTG_PPT, module_CTG_randomNumberGiven, module_CTG_TPT, module_CTG_firstTickTrue, module_CTG_timesToClick
    module_create_bounding_box("Click until green", 0, SCREEN_HEIGHT * (3/4), SCREEN_WIDTH * (2/16), SCREEN_HEIGHT * (1/4), (105, 10, 10), module_CTG_danger_level, "The button will turn red. Press it until it gets back to green.")
    
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
module_TP_lateness_MOE = 5000 + 500 *  (20 - OVERALL_difficulty)
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
    module_create_bounding_box("Target practice", 0, SCREEN_HEIGHT * (2/4), SCREEN_WIDTH * (4/16), SCREEN_HEIGHT * (1/4), (105, 10, 10), module_TP_danger_level, "Targets will appear. Shoot them as soon as you can.")
    
    # OPERATION METHOD
    # Red dots will appear, click them to make them disappear
    # If more than 5 circles: module danger level is 1
    # If more than 8 circles: module danger level is 2
                
    interiorPannel = pygame.draw.rect(screen, (10, 10, 10), (SCREEN_WIDTH * (1/128), SCREEN_HEIGHT * (41/72), SCREEN_WIDTH * (15/64), SCREEN_HEIGHT * (1/6)), 0, 30)    
    interiorPannelContour = pygame.draw.rect(screen, (45, 45, 45), (SCREEN_WIDTH * (1/128), SCREEN_HEIGHT * (41/72), SCREEN_WIDTH * (15/64), SCREEN_HEIGHT * (1/6)), 3, 30)
    
    tickDifference = int((module_TP_randomNumberGiven - module_TP_setTimeTick) // 2)
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
                circleRandomPositionX = random.randint(30, int(SCREEN_WIDTH * (4/16) - 30))
                circleRandomPositionY = random.randint(int(SCREEN_HEIGHT * (2/4) + 60), int(SCREEN_HEIGHT * (3/4) - 20))
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
module_TETRIS_lateness_MOE = 5000 + 500 *  (20 - OVERALL_difficulty)
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
    module_create_bounding_box("Tetris", SCREEN_WIDTH * (4/16), SCREEN_HEIGHT * (2/4), SCREEN_WIDTH * (2/16), SCREEN_HEIGHT * (2/4), (105, 10, 10), module_TETRIS_danger_level, "If there's a hole, there's a goal. Correctly place the tetris block.")
    
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
    
    pygame.draw.rect(screen, (75, 75, 75), (SCREEN_WIDTH * (4/16) + 10, SCREEN_HEIGHT * (5/8) - 4, SCREEN_WIDTH * (2/16) - 20, SCREEN_HEIGHT * (3/8) - 6), 0, 1)
    
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
module_IP_randomNumberGiven = pygame.time.get_ticks() + (random.randint(2, 5) * 30 * 1000) / OVERALL_difficulty
module_IP_lateness_MOE = 5000 + 500 *  (20 - OVERALL_difficulty)
module_IP_errored = False
module_IP_firstTickTrue = False
### ADDITIONAL PARAMETERS
module_IP_buttonsIndex = [0, 0, 0, 0]

def reInit_Module_it_pops():
    global module_IP_randomNumberGiven
    module_IP_randomNumberGiven = pygame.time.get_ticks() + (random.randint(2, 5) * 30 * 1000) / OVERALL_difficulty

def module_it_pops():
    global core_temperature, core_energy_provided
    global module_IP_danger_level, module_IP_lateness_MOE, module_IP_PPT, module_IP_randomNumberGiven, module_IP_TPT, module_IP_firstTickTrue, module_IP_timesToClick, module_IP_buttonsIndex
    module_create_bounding_box("It pops", SCREEN_WIDTH * (2/16), SCREEN_HEIGHT * (3/4), SCREEN_WIDTH * (2/16), SCREEN_HEIGHT * (1/4), (105, 10, 10), module_IP_danger_level, "Click each button until they are the same color.")
    
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
module_CTD_randomNumberGiven = pygame.time.get_ticks() + (random.randint(3, 6) * 30 * 1000) / OVERALL_difficulty
module_CTD_lateness_MOE = 5000 + 500 *  (20 - OVERALL_difficulty)
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
    module_CTD_randomNumberGiven = pygame.time.get_ticks() + (random.randint(3, 6) * 30 * 1000) / OVERALL_difficulty
def module_connect_the_dots():
    global core_temperature, core_energy_provided
    global module_CTD_danger_level, module_CTD_lateness_MOE, module_CTD_PPT, module_CTD_randomNumberGiven, module_CTD_TPT, module_CTD_firstTickTrue, module_CTD_timesToClick, module_CTD_patternChosen, module_CTD_patternProgressionIndex, module_CTD_patternsList
    module_create_bounding_box("Connect the dots", SCREEN_WIDTH * (3/4), SCREEN_HEIGHT * (2/4), SCREEN_WIDTH * (1/4), SCREEN_HEIGHT * (2/4), (105, 10, 10), module_CTD_danger_level, "Click on the dots do draw a shape and clear the module.")
    
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
module_CD_lateness_MOE = 5000 + 500 *  (20 - OVERALL_difficulty)
module_CD_errored = False
module_CD_firstTickTrue = False
### ADDITIONAL PARAMETERS
module_CD_setCode = None
module_CD_inputCode = ""

def reInit_Module_code():
    global module_CD_randomNumberGiven
    module_CD_randomNumberGiven = pygame.time.get_ticks() + (random.randint(1, 3) * 30 * 1000) / OVERALL_difficulty

def module_code():
    global core_temperature, core_energy_provided
    global module_CD_danger_level, module_CD_lateness_MOE, module_CD_PPT, module_CD_randomNumberGiven, module_CD_TPT, module_CD_firstTickTrue, module_CD_timesToClick, module_CD_setCode, module_CD_inputCode
    module_create_bounding_box("Code", SCREEN_WIDTH * (10/16), SCREEN_HEIGHT * (5/8), SCREEN_WIDTH * (2/16), SCREEN_HEIGHT * (3/8), (105, 10, 10), module_CD_danger_level, "Input the correct code to clear the module.")
    
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
    
    pygame.draw.rect(screen, (45, 45, 45), (SCREEN_WIDTH * (10/16) + 10, SCREEN_HEIGHT * (5/8) + 55, SCREEN_WIDTH * (2/16) - 16, SCREEN_HEIGHT * (3/8) - 65), 0, 2)
    pygame.draw.rect(screen, (95, 95, 95), (SCREEN_WIDTH * (10/16) + 10, SCREEN_HEIGHT * (5/8) + 55, SCREEN_WIDTH * (2/16) - 16, SCREEN_HEIGHT * (3/8) - 65), 3, 2)
    
    #Check if already errored, if not the initialize it
    if module_CD_errored == True and module_CD_firstTickTrue == False:
        #Init danger parameters
        module_CD_setCode = random.randint(1000, 9999)
        module_CD_inputCode = ""
        #Set init danger as DONE
        module_CD_firstTickTrue = True
    
    for height in range(4):
        for width in range (3):
            button = pygame.draw.rect(screen, (0, 0, 0), (SCREEN_WIDTH * (10/16) + 13 + width * (SCREEN_HEIGHT * (2/8) / 3 - 12.5) , SCREEN_HEIGHT * (6/8) + 45 + height * (SCREEN_WIDTH * (2/16) / 3 - 21), SCREEN_WIDTH * (2/16) / 3 - 10, SCREEN_HEIGHT * (2/8) / 4 - 20), 0, 2)
            button = pygame.draw.rect(screen, (135, 135, 135), (SCREEN_WIDTH * (10/16) + 13 + width * (SCREEN_HEIGHT * (2/8) / 3 - 12.5) , SCREEN_HEIGHT * (6/8) + 45 + height * (SCREEN_WIDTH * (2/16) / 3 - 21), SCREEN_WIDTH * (2/16) / 3 - 10, SCREEN_HEIGHT * (2/8) / 4 - 20), 2, 2)
            buttonsList.append((str("CD_" + str(width + 3 * height + 1) + "_Clicked"), "Rectangle", (SCREEN_WIDTH * (10/16) + 13 + width * (SCREEN_HEIGHT * (2/8) / 3 - 12.5) , SCREEN_HEIGHT * (6/8) + 45 + height * (SCREEN_WIDTH * (2/16) / 3 - 21), SCREEN_WIDTH * (2/16) / 3 - 10, SCREEN_HEIGHT * (2/8) / 4 - 20)))
            
            font = pygame.font.Font('sources/mouse/fonts/VCR_OSD_MONO.ttf', 20)
            if width + 3 * height + 1 == 10:
                text = font.render(str("X"), 1, (180, 15, 15))
            elif width + 3 * height + 1 == 11:
                text = font.render(str("0"), 1, (180, 15, 15))
            elif width + 3 * height + 1 == 12:
                text = font.render(str("OK"), 1, (180, 15, 15))
            else:
                text = font.render(str(width + 3 * height + 1), 1, (180, 15, 15))
            textRect = text.get_rect()
            textRect.center = (SCREEN_WIDTH * (10/16) + 35 + width * (SCREEN_HEIGHT * (2/8) / 3 - 12.5) , SCREEN_HEIGHT * (6/8) + 57.5 + height * (SCREEN_WIDTH * (2/16) / 3 - 21))
            screen.blit(text, textRect)
            
    pygame.draw.rect(screen, ( 35,  35,  35), (SCREEN_WIDTH * (10/16) + 12.5, SCREEN_HEIGHT * (45/64) + 2, SCREEN_WIDTH * (2/16) - 20, SCREEN_HEIGHT * (2/16) - 55), 0, 2)
    pygame.draw.rect(screen, (135, 135, 135), (SCREEN_WIDTH * (10/16) + 12.5, SCREEN_HEIGHT * (45/64) + 2, SCREEN_WIDTH * (2/16) - 20, SCREEN_HEIGHT * (2/16) - 55), 2, 2)
    
    font = pygame.font.Font('sources/mouse/fonts/VCR_OSD_MONO.ttf', 35)
    if module_CD_errored == True:
        text = font.render(str(module_CD_setCode), 1, (180, 15, 15))
    else:
        text = font.render("", 1, (180, 15, 15))
    textRect = text.get_rect()
    textRect.center = (SCREEN_WIDTH * (21.75/32) + 12.5, SCREEN_HEIGHT * (46.5/64) + 2)
    screen.blit(text, textRect)
    
    pygame.draw.rect(screen, ( 35,  35,  35), (SCREEN_WIDTH * (10/16) + 12.5, SCREEN_HEIGHT * (96.5/128) + 2, SCREEN_WIDTH * (2/16) - 20, SCREEN_HEIGHT * (2/16) - 55), 0, 2)
    pygame.draw.rect(screen, (135, 135, 135), (SCREEN_WIDTH * (10/16) + 12.5, SCREEN_HEIGHT * (96.5/128) + 2, SCREEN_WIDTH * (2/16) - 20, SCREEN_HEIGHT * (2/16) - 55), 2, 2)
    
    font = pygame.font.Font('sources/mouse/fonts/VCR_OSD_MONO.ttf', 35)
    if module_CD_errored == True:
        text = font.render(str(module_CD_inputCode), 1, (180, 15, 15))
    else:
        text = font.render("", 1, (180, 15, 15))
    textRect = text.get_rect()
    textRect.center = (SCREEN_WIDTH * (21.75/32) + 12.5, SCREEN_HEIGHT * (99/128) + 2)
    screen.blit(text, textRect)   
    
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
def CD_11_Clicked():
    global module_CD_inputCode
    if len(module_CD_inputCode) < 4:
        module_CD_inputCode += "0"
def CD_10_Clicked():
    global module_CD_inputCode
    if len(module_CD_inputCode) > 0:
        module_CD_inputCode = module_CD_inputCode[:-1]
def CD_12_Clicked():
    global module_CD_inputCode, module_CD_setCode, module_CD_errored, module_CD_firstTickTrue
    if module_CD_inputCode == str(module_CD_setCode):
        module_CD_errored = False
        module_CD_firstTickTrue = False
        reInit_Module_code()
    
### MODULE COOL IT DOWN
### INITIAL MODULE PARAMETERS (PPT = PRODUCTION PER TICK; TPT = TEMPERATURE PER TICK)
module_CID_danger_level = 0
module_CID_PPT = 0.2
module_CID_TPT = 0.4
module_CID_randomNumberGiven = pygame.time.get_ticks() + (random.randint(1, 3) * 30 * 1000) / OVERALL_difficulty
module_CID_lateness_MOE = 5000 + 500 *  (20 - OVERALL_difficulty)
module_CID_errored = False
module_CID_firstTickTrue = False
### ADDITIONAL PARAMETERS
module_CID_setTimeTick = pygame.time.get_ticks()
module_CID_timesClicked = 0
def change_speed_module_cool_it_down():
    pass
def module_cool_it_down():
    global core_temperature, core_energy_provided
    global module_CID_danger_level, module_CID_lateness_MOE, module_CID_PPT, module_CID_randomNumberGiven, module_CID_TPT, module_CID_firstTickTrue, module_CID_timesToClick
    global module_CID_setTimeTick, module_CID_timesClicked
    module_create_bounding_box("Cool It Down", SCREEN_WIDTH * (6/16), SCREEN_HEIGHT * (2/4), SCREEN_WIDTH * (6/16), SCREEN_HEIGHT * (1/8), (105, 10, 10), module_CID_danger_level, "Press the blue button so that the bar stay at a safe level.")
    
    # OPERATION METHOD
    # The bar will slowly increase, press a button repeatedly to decrease that bar progress.
        
    tickDifference = int((module_CID_randomNumberGiven - module_CID_setTimeTick) // 4)
    barsToDraw = pygame.time.get_ticks() // tickDifference
    barsToDraw -= module_CID_timesClicked
    
    pygame.draw.rect(screen, (0, 0, 0), (SCREEN_WIDTH * (6/16) + 10, SCREEN_HEIGHT * (2/4) + 50, SCREEN_WIDTH * (5/16) - 30, SCREEN_HEIGHT * (1 / 24)), 0, 2)
    pygame.draw.rect(screen, (35, 35, 35), (SCREEN_WIDTH * (6/16) + 10, SCREEN_HEIGHT * (2/4) + 50, SCREEN_WIDTH * (5/16) - 30, SCREEN_HEIGHT * (1 / 24)), 2, 2)
    
    barX = SCREEN_WIDTH * (6/16) + 20
    for bar in range(30):
        barColorIndex = bar // 10
        barColor = temperatureBarColors[barColorIndex]
        colorR = barColor[0]
        colorG = barColor[1]
        colorB = barColor[2]
        if bar < barsToDraw:
            if barColorIndex == 0:
                colorG += 140
            elif barColorIndex == 1:
                colorR += 140
                colorG += 140
            else:
                colorR += 140
        barColor = (colorR, colorG, colorB)
        tempIndicator = pygame.draw.rect(screen, barColor, (barX, SCREEN_HEIGHT * (2/4) + 55, 5, SCREEN_HEIGHT * (1 / 24) - 10), 0, 2)
        barX += (SCREEN_WIDTH * (6/16)) / 40 - 0.1
    
    if barsToDraw >= 20:
        module_CID_danger_level = 2
        module_CID_errored = True
    elif barsToDraw >= 10:
        module_CID_danger_level = 1
        module_CID_errored = True
    else:
        module_CID_danger_level = 0
        module_CID_errored = False
        
    if module_CID_danger_level == 1:
        core_temperature += module_CID_TPT
    elif module_CID_danger_level == 2:
        core_temperature += 2 * module_CID_TPT
    core_energy_provided += module_CID_PPT
    
    button = pygame.draw.rect(screen, (55, 55, 135), (SCREEN_WIDTH * (11/16), SCREEN_HEIGHT * (2/4) + 50, SCREEN_WIDTH * (1/16) - 20, SCREEN_HEIGHT * (1 / 24)), 0, 2)
    pygame.draw.rect(screen, (35, 35, 135), (SCREEN_WIDTH * (11/16), SCREEN_HEIGHT * (2/4) + 50, SCREEN_WIDTH * (1/16) - 20, SCREEN_HEIGHT * (1 / 24)), 2, 2)
    buttonsList.append(("CID_MainButton_Clicked", "Rectangle", (SCREEN_WIDTH * (11/16), SCREEN_HEIGHT * (2/4) + 50, SCREEN_WIDTH * (1/16) - 20, SCREEN_HEIGHT * (1 / 24))))

### Functions for that module
def CID_MainButton_Clicked():
        global module_CID_timesClicked
        tickDifference = int((module_CID_randomNumberGiven - module_CID_setTimeTick) // 4)
        barsToDraw = pygame.time.get_ticks() // tickDifference
        barsToDraw -= module_CID_timesClicked
        if barsToDraw > 0:
            module_CID_timesClicked += 1
            
            
            
            





coreColorR = 255
coreColorG = 0
coreColorB = 0
coreColor = (coreColorR, coreColorG, coreColorB)
def draw_core():
    global coreColorR, coreColorG, coreColorB
    if coreColorG < 255 and coreColorR == 255 and coreColorB == 0:
        coreColorG += 5
    elif coreColorG == 255 and coreColorR > 0 and coreColorB == 0:
        coreColorR -= 5
    elif coreColorR == 0 and coreColorG == 255 and coreColorB < 255:
        coreColorB += 5
    elif coreColorR == 0 and coreColorG > 0 and coreColorB == 255:
        coreColorG -= 5
    elif coreColorR < 255 and coreColorG == 0 and coreColorB == 255:
        coreColorR += 5
    elif coreColorR == 255 and coreColorG == 0 and coreColorB > 0:
        coreColorB -= 5
            
    coreColor = (coreColorR, coreColorG, coreColorB)
    pygame.draw.circle(screen, coreColor, (SCREEN_WIDTH * (1/2) - 2.5, SCREEN_HEIGHT * (1/4)), 100, 0) 
            
            
backgroundAmbientChannel.play(ambientLoop, loops = -1)

coolStrtupAlreadyPlayed = False
firstAlarmPlayed = False
firstOverheatWarnPlayed = False
thirdAlarmPlayed = False
coreCritCutPlayed = False
fifthAlarmPlayed = False
fourthAlarmPlayed = False
meltdownAnnouncementPlayed = False
beforeLastAnnouncementPlayed = False
lastAnnouncementPlayed = False
finalPlayed = False
### MODULE CENTRAL UNIT
def module_central_unit(previousTemp):
    global core_temperature, core_energy_provided, core_energy_demand, core_energy_demand_list, OVERALL_difficulty, OVERALL_days
    global coolStrtupAlreadyPlayed, firstOverheatWarnPlayed, firstAlarmPlayed, thirdAlarmPlayed, coreCritCutPlayed, fourthAlarmPlayed, fifthAlarmPlayed, meltdownAnnouncementPlayed, beforeLastAnnouncementPlayed, lastAnnouncementPlayed, finalPlayed
    global OVERALL_CORE_MELTDOWN_STARTED, OVERALL_CORE_MELTDOWN_STARTTICK, GAME_OVER
    module_create_bounding_box("Target practice", SCREEN_WIDTH * (6/16), SCREEN_HEIGHT * (5/8), SCREEN_WIDTH * (4/16), SCREEN_HEIGHT * (3/8), (105, 10, 10), 0, "Overview module for basic informations about the current game.")
    
    if pygame.time.get_ticks() > 5000 and pygame.time.get_ticks() < 5500:
        alertsChannel.play(safeModeDesactivated)
        
    if coolStrtupAlreadyPlayed == False and core_temperature > 0:
        alertsChannel.play(coolantStartup)
        coolStrtupAlreadyPlayed = True
        
    if core_temperature > 2000 and firstAlarmPlayed == False:
        alarm1Channel = pygame.mixer.Channel(4)
        alarm1Channel.stop()
        alarm1Channel.play(pbAlarm1, loops = 10)
        firstAlarmPlayed = True
    
    if core_temperature > 2500 and firstOverheatWarnPlayed == False:
        alertsChannel.stop()
        alertsChannel.play(coreOverheating)
        alarm2Channel = pygame.mixer.Channel(5)
        alarm2Channel.stop()
        alarm2Channel.play(pbAlarm2, loops = 3)
        firstOverheatWarnPlayed = True
        
    if core_temperature > 3000 and thirdAlarmPlayed == False:
        alarm3Channel = pygame.mixer.Channel(6)
        alarm3Channel.stop()
        alarm3Channel.play(pbAlarm3, loops = 2)
        thirdAlarmPlayed = True
        
    if core_temperature > 3200 and coreCritCutPlayed == False:
        alertsChannel.stop()
        alertsChannel.play(coreAtCriticalCut)
        coreCritCutPlayed = True
        
    if core_temperature > 3500 and fifthAlarmPlayed == False:
        alarm5Channel = pygame.mixer.Channel(4)
        alarm5Channel.stop()
        alarm5Channel.play(pbAlarm5)
        fifthAlarmPlayed = True
        
    if core_temperature > 3800 and fourthAlarmPlayed == False:
        alarm4Channel = pygame.mixer.Channel(5)
        alarm4Channel.stop()
        alarm4Channel.play(pbAlarm4)
        fourthAlarmPlayed = True
        
    if core_temperature > 4000 and meltdownAnnouncementPlayed == False:
        alertsChannel.stop()
        alertsChannel.play(coreMeltdownInTwoMinutes)
        OVERALL_CORE_MELTDOWN_STARTED = True
        OVERALL_CORE_MELTDOWN_STARTTICK = pygame.time.get_ticks()
        meltdownAnnouncementPlayed = True  
        
    if core_energy_provided > core_energy_demand:
        change_set = False
        if OVERALL_days >= 7:
            core_energy_provided = 0
            OVERALL_days += 1
            if OVERALL_difficulty < 20:
                OVERALL_difficulty += 1
        for demand in core_energy_demand_list:
            if demand == core_energy_demand and demand != core_energy_demand_list[-1] and change_set == False:
                core_energy_demand = core_energy_demand_list[core_energy_demand_list.index(demand) + 1]
                core_energy_provided = 0
                OVERALL_days += 1
                OVERALL_difficulty += 1
                change_set = True
    
    if OVERALL_CORE_MELTDOWN_STARTED == True:
        if (OVERALL_CORE_MELTDOWN_STARTTICK + 120000 - pygame.time.get_ticks()) // 1000 < 70 and beforeLastAnnouncementPlayed == False:
            alertsChannel.play(lockdown)
            beforeLastAnnouncementPlayed = True
            
        if (OVERALL_CORE_MELTDOWN_STARTTICK + 120000 - pygame.time.get_ticks()) // 1000 < 20 and lastAnnouncementPlayed == False:
            alertsChannel.play(selfDestructInitiated)
            lastAnnouncementPlayed = True
            
        if (OVERALL_CORE_MELTDOWN_STARTTICK + 120000 - pygame.time.get_ticks()) // 1000 < 0 and finalPlayed == False:
            pygame.mixer.stop()
            alertsChannel.play(finalExplosion)
            GAME_OVER = True
            finalPlayed = True
                
    pygame.draw.rect(screen, (0, 0, 0), (SCREEN_WIDTH * (6/16) + 5, SCREEN_HEIGHT * (5/8) + 55, SCREEN_WIDTH * (4/16) - 10, SCREEN_HEIGHT * (3/8) - 65), 0, 2)
    pygame.draw.rect(screen, (45, 45, 45), (SCREEN_WIDTH * (6/16) + 5, SCREEN_HEIGHT * (5/8) + 55, SCREEN_WIDTH * (4/16) - 10, SCREEN_HEIGHT * (3/8) - 65), 2, 2)
    
    font = pygame.font.Font('sources/mouse/fonts/VCR_OSD_MONO.ttf', 25)
    currentDayText = font.render("Day " + str(OVERALL_days), 1, (25, 25, 180))
    currentDifficutlyText = font.render("Difficulty: " + str(OVERALL_difficulty), 1, (25, 25, 180))
    temperatureRateText = font.render("Temp. rate: " + str(round(core_temperature - previousTemp, 1)), 1, (25, 25, 180))
    screen.blit(currentDayText, (SCREEN_WIDTH * (6/16) + 10, SCREEN_HEIGHT * (5/8) + 55))
    screen.blit(currentDifficutlyText, (SCREEN_WIDTH * (6/16) + 10, SCREEN_HEIGHT * (5/8) + 85))
    screen.blit(temperatureRateText, (SCREEN_WIDTH * (6/16) + 10, SCREEN_HEIGHT * (5/8) + 115))
    
    if OVERALL_CORE_MELTDOWN_STARTED == True:
        imminentDangerText = font.render("IMMINENT DANGER", 1, (255, 25, 25))
        timeLeftText = font.render("Time left: " + str((OVERALL_CORE_MELTDOWN_STARTTICK + 120000 - pygame.time.get_ticks()) // 1000) + "s", 1, (255, 25, 25))
        screen.blit(imminentDangerText, (SCREEN_WIDTH * (6/16) + 10, SCREEN_HEIGHT * (5/8) + 175))
        screen.blit(timeLeftText, (SCREEN_WIDTH * (6/16) + 10, SCREEN_HEIGHT * (5/8) + 205))

def energyBarIndications():
    global core_energy_provided, core_energy_demand
    font = pygame.font.Font('sources/mouse/fonts/VCR_OSD_MONO.ttf', 25)
    text = font.render(str(round(core_energy_provided)) + "/" + str(core_energy_demand), 1, (25, 25, 180))
    textRect = text.get_rect()
    textRect.center = (SCREEN_WIDTH * (1/2), SCREEN_HEIGHT * (68.5/144))
    screen.blit(text, textRect)

def Render_Text(what, color, where):
    font = pygame.font.SysFont('monospace', 30)
    text = font.render(what, 1, pygame.Color(color))
    screen.blit(text, where)

### MAIN LOOP
while running:
    if not GAME_OVER:
        screen.fill((0, 0, 0))
        screen.blit(bg, (0, 0))
        
        beforeTemp = core_temperature
        
        #Create the layout
        create_layout()
        draw_core()
        
        #Modules handler
        module_click_until_green()
        module_target_practice()
        module_tetris()
        module_it_pops()
        module_connect_the_dots()
        module_code()
        module_cool_it_down()
        
        #Central unit module
        core_temperature -= 1.0
        if core_temperature < 0:
            core_temperature = 0
            
        module_central_unit(beforeTemp)
        
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
        
        mouseX = pygame.mouse.get_pos()[0]
        mouseY = pygame.mouse.get_pos()[1]
        
        for item in range(len(hoverList)):
            if math.sqrt((mouseX - hoverList[item][0]) ** 2 + (mouseY - hoverList[item][1]) ** 2) < 15:
                font = pygame.font.Font('sources/mouse/fonts/VCR_OSD_MONO.ttf', 30)
                text = font.render(str(hoverList[item][2]), 1, (25, 25, 180))
                background = pygame.Surface((text.get_width() + 10, text.get_height() + 10))
                background.fill((0, 0, 0))
                background.blit(text, (5, 5))
                screen.blit(background, (SCREEN_WIDTH * (1/2) - background.get_width() / 2, SCREEN_HEIGHT * (1/2) - background.get_height() / 2))
            
        
        # Update the display
        pygame.display.flip()

        #Update values
        moduleFlashingLightTime += 1
        if moduleFlashingLightTime == 60:
            moduleFlashingLightTime = 0
            
        temperatureBarLightsOn = core_temperature // 60
        
        buttonsList = []
        hoverList = []
        
        if OVERALL_CORE_MELTDOWN_STARTED == True:
            OVERALL_CORE_MELTDOWN_TIME_LEFT = OVERALL_CORE_MELTDOWN_STARTTICK - pygame.time.get_ticks()
            
    else:
        screen.fill((0, 0, 0))
        endTextFont = pygame.font.Font('sources/mouse/fonts/VCR_OSD_MONO.ttf', 50)
        dayReached = endTextFont.render("Days survived: " + str(OVERALL_days), 1, (255, 255, 255))
        congratsText = endTextFont.render("Congratulations!", 1, (255, 255, 255))
        pressEscToExitText = endTextFont.render("Press ESC to exit", 1, (255, 255, 255))
        screen.blit(dayReached, (SCREEN_WIDTH * (1/2) - dayReached.get_width() / 2, SCREEN_HEIGHT * (1/2) - dayReached.get_height() / 2))
        screen.blit(congratsText, (SCREEN_WIDTH * (1/2) - congratsText.get_width() / 2, SCREEN_HEIGHT * (1/2) - congratsText.get_height() / 2 + 50))
        screen.blit(pressEscToExitText, (SCREEN_WIDTH * (1/2) - pressEscToExitText.get_width() / 2, SCREEN_HEIGHT * (1/2) - pressEscToExitText.get_height() / 2 + 100))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
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

