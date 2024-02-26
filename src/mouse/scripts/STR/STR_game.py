import pygame
import sys
import math
import json
from os.path import exists

# Initialize Pygame
pygame.init()

# Screen dimensions
desktopSize = pygame.display.get_desktop_sizes()

SCREEN_WIDTH = desktopSize[0][0]
SCREEN_HEIGHT = desktopSize[0][1]

# Initialize the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Save The Reactor! Game")

# Clock for controlling the frame rate
clock = pygame.time.Clock()

screen.fill((0, 0, 0))

bg = pygame.image.load("src/mouse/scripts/STR/INSP.jpg")

running = True
while running:
    screen.blit(bg, (0, 0))
    
    modulesCentralZone = pygame.draw.rect(screen, (135, 135, 135), (0, 360, 1280, 360))
    modulesCentralZoneContour = pygame.draw.rect(screen, (125, 0, 0), (0, 360, 1280, 360), 5)
    
    modulesLeftZone = pygame.draw.rect(screen, (125, 125, 125), (0, 100, 240, 260))
    modulesLeftZoneContour = pygame.draw.rect(screen, (0, 0, 125), (0, 100, 240, 260), 3)
    
    modulesRightZone = pygame.draw.rect(screen, (125, 125, 125), (1040, 100, 240, 260))
    modulesRightZoneContour = pygame.draw.rect(screen, (0, 0, 125), (1040, 100, 240, 260), 3)

    temperatureBar = pygame.draw.rect(screen, (100, 100, 100), (340, 0, 620, 30))
    temperatureBarContour = pygame.draw.rect(screen, (0, 0, 0), (340, 0, 620, 30), 3)
    
    energyBar = pygame.draw.rect(screen, (25, 25, 155), (580, 325, 120, 35))
    energyBarContour = pygame.draw.rect(screen, (0, 0, 0), (580, 325, 120, 35), 3)
    
    reactorCore = pygame.draw.rect(screen, (185, 25, 25), (540, 80, 200, 200))
    reactorCoreContour = pygame.draw.rect(screen, (255, 255, 255), (540, 80, 200, 200), 5)
    
    mouseX = pygame.mouse.get_pos()[0]
    mouseY = pygame.mouse.get_pos()[1]
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouseX = pygame.mouse.get_pos()[0]
            mouseY = pygame.mouse.get_pos()[1]
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
