import pygame
import sys
import math

import ROSU_storage as storage

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

# Initialize the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("ROSU! Game")

# Clock for controlling the frame rate
clock = pygame.time.Clock()

screen.fill((0, 0, 0))

running = True
bgImage = None
while running:
    mouseX = pygame.mouse.get_pos()[0]
    mouseY = pygame.mouse.get_pos()[1]
    
    if bgImage != None:
        screen.blit(bgImage, (0, 0))
    
    x, y = 10, 10
    for i in range(len(storage.Storage)):
        pygame.draw.rect(screen, (255, 255, 255), (x, y, 600, 150), 3, 2, 2, 2, 2, 2)
        if mouseX > x and mouseX < x + 600 and mouseY > y and mouseY < y + 150:
            bgImage = pygame.image.load(storage.Storage[i][2])
        y += 160
        
        
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()
sys.exit()