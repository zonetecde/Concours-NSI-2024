import pygame
import sys
import math
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Initialize the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("ROSU! Game")

# Clock for controlling the frame rate
clock = pygame.time.Clock()

# List to store circle information (Time:ms, position, color, size, pointGroup, pointNumber)
circlesList = []

pygame.mixer.music.load("src/mouse/music/GravityFalls.mp3")

# Main game loop
running = True
playing = False
pointNumber = 1
colorX = random.randint(0, 255)
colorY = random.randint(0, 255)
colorZ = random.randint(0, 255)
pointColor = (colorX, colorY, colorZ)
while running:
    # Clear the screen
    screen.fill(BLACK)
    
    mouseX = pygame.mouse.get_pos()[0]
    mouseY = pygame.mouse.get_pos()[1]
    
    current_tick = pygame.time.get_ticks()
                
    if current_tick < 5000:
        font = pygame.font.SysFont("monospace", 75, bold=False, italic=False)
        color = (255, 0, 0)
        label = font.render(str(current_tick), 1, color)
        screen.blit(label, (520, 320))
        
    if current_tick >= 5000:
        if playing == False:
            pygame.mixer.music.play()
            playing = True
    
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            circlesList.append((current_tick, (mouseX, mouseY), pointColor, 35, pointNumber))
            colorX += 20
            colorY += 20
            colorZ += 20
            if colorX > 255: colorX = 255
            if colorY > 255: colorY = 255
            if colorZ > 255: colorZ = 255
            pointColor = (colorX, colorY, colorZ)
            pointNumber += 1
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                pointNumber = 1
                colorX = random.randint(0, 255)
                colorY = random.randint(0, 255)
                colorZ = random.randint(0, 255)
                pointColor = (colorX, colorY, colorZ)  
            print(circlesList)
            
    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()
sys.exit()
