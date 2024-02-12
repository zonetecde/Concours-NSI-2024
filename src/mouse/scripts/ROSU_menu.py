import pygame
import sys
import math

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

songs = [("Gourmet Race", ("Easy", 2))]

running = True
while running:
    screen.fill((0, 0, 0))
    
    
    
    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()
sys.exit()