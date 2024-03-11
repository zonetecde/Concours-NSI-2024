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

bg = pygame.image.load("sources\mouse\scripts\STR\INSP.jpg")

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
    
    energyBar = pygame.draw.rect(screen, (25, 25, 155), (SCREEN_WIDTH * (29/64), SCREEN_HEIGHT * (65/144), SCREEN_WIDTH * (3/32), SCREEN_HEIGHT * (7/144)))
    energyBarContour = pygame.draw.rect(screen, (0, 0, 0), (SCREEN_WIDTH * (29/64), SCREEN_HEIGHT * (65/144), SCREEN_WIDTH * (3/32), SCREEN_HEIGHT * (7/144)), 3)
    
    reactorCore = pygame.draw.rect(screen, (185, 25, 25), (SCREEN_WIDTH * (27/64), SCREEN_HEIGHT * (1/9), SCREEN_WIDTH * (5/32), SCREEN_HEIGHT * (5/18)))
    reactorCoreContour = pygame.draw.rect(screen, (255, 255, 255), (SCREEN_WIDTH * (27/64), SCREEN_HEIGHT * (1/9), SCREEN_WIDTH * (5/32), SCREEN_HEIGHT * (5/18)), 5)
    

def module_create_bounding_box(moduleName, posX, posY, sizeX, sizeY, moduleColor, moduleDangerLevel):

    pygame.draw.rect(screen, moduleColor, (posX, posY, sizeX, sizeY), 0, 1)
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

"""

### OVERALL PARAMETERS ###
OVERALL_difficulty = 20 # Ranges from 1 to 20

### INITIAL MODULE PARAMETERS (PPT = PRODUCTION PER TICK; TPT = TEMPERATURE PER TICK)
module_CTG_danger_level = 0
module_CTG_PPT = 0.2
module_CTG_TPT = 0.4
module_CTG_randomNumberGiven = pygame.time.get_ticks() + random.randint(1, 3) * 30 * 1000 * (21 - OVERALL_difficulty)
module_CTG_lateness_MOE = 5000
module_CTG_errored = False
module_CTG_firstTickTrue = False
### RANDOMISATION PARAMETER
module_CTG_randomizationTick = None
### ADDITIONAL PARAMETERS
module_CTG_timesToClick = 0
def reInit_Module_click_until_green():
    global module_CTG_randomNumberGiven
    module_CTG_randomNumberGiven = pygame.time.get_ticks() + random.randint(1, 3) * 30 * 1000 * (21 - OVERALL_difficulty)
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
    
    
"""
### RANDOMISATION SETTINGS
randomizer_DIFF = 20 # Ranges from 1 to 20
def handleModulesRandomization():
"""


def energyBarIndications():
    pass

moduleFlashingLightTime = 0

### INITIALIZING CORE PARAMETERS
core_temperature = 0
core_max_temperature = 4000
core_energy_demand = 300
core_energy_provided = 0

### MAIN LOOP
while running:
    screen.fill((0, 0, 0))
    screen.blit(bg, (0, 0))
    
    #Create the layout
    create_layout()
    
    #Modules handler
    module_click_until_green()
    
    
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
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.mixer.stop()
                running = False
                
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

