import pygame
import sys
import math

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

# List to store circle information (tick, position)
circlesList = [
    #Time:ms, position, color, size, pointNumber
    #Example
    #(2000, (100, 100), (255, 0, 255), 35, 1),
    #(3000, (200, 200), (255, 255, 0), 35, 1),
    #(3100, (240, 240), (255, 225, 0), 35, 2),
    #(3200, (280, 280), (255, 195, 0), 35, 3),
    #(3300, (320, 320), (255, 165, 0), 35, 4) 
    (5398, (85, 86), (94, 167, 222), 35, 1), (5981, (275, 98), (114, 187, 242), 35, 2), (6659, (484, 101), (134, 207, 255), 35, 3), (7359, (633, 100), (154, 227, 255), 35, 4), (8090, (650, 630), (235, 196, 137), 35, 1), (8841, (511, 617), (255, 216, 157), 35, 2), (9485, (401, 640), (255, 236, 177), 35, 3), (10227, (250, 634), (255, 255, 197), 35, 4), (10961, (254, 314), (208, 40, 4), 35, 1), (12045, (490, 354), (228, 60, 24), 35, 2), (12408, (644, 359), (248, 80, 44), 35, 3), (13844, (919, 533), (84, 60, 59), 35, 1), (14460, (833, 524), (104, 80, 79), 35, 2), (14943, (666, 531), (124, 100, 99), 35, 3), (15342, (530, 517), (144, 120, 119), 35, 4), (16720, (866, 128), (15, 175, 72), 35, 1), (17783, (779, 130), (35, 195, 92), 35, 2), (18163, (620, 110), (55, 215, 112), 35, 3), (18975, (504, 115), (75, 235, 132), 35, 4), (19656, (427, 342), (255, 187, 129), 35, 1), (20366, (531, 345), (255, 207, 149), 35, 2), (21109, (618, 344), (255, 227, 169), 35, 3), (21774, (718, 352), (255, 247, 189), 35, 4), (22858, (1140, 105), (145, 75, 91), 35, 1), (23277, (1092, 157), (165, 95, 111), 35, 2), (23626, (1029, 243), (185, 115, 131), 35, 3), (23957, (978, 309), (205, 135, 151), 35, 4), (24470, (935, 362), (225, 155, 171), 35, 5), (24736, (850, 489), (245, 175, 191), 35, 6), (25086, (802, 535), (255, 195, 211), 35, 7), (25739, (764, 240), (75, 36, 163), 35, 1), (26222, (737, 269), (95, 56, 183), 35, 2), (26555, (681, 338), (115, 76, 203), 35, 3), (26887, (635, 382), (135, 96, 223), 35, 4), (27236, (592, 421), (155, 116, 243), 35, 5), (27604, (577, 444), (175, 136, 255), 35, 6), (27984, (502, 510), (195, 156, 255), 35, 7), (28651, (275, 527), (134, 148, 178), 35, 1), (29062, (308, 478), (154, 168, 198), 35, 2), (29432, (356, 447), (174, 188, 218), 35, 3), (29798, (435, 358), (194, 208, 238), 35, 4), (30158, (478, 316), (214, 228, 255), 35, 5), (30525, (559, 254), (234, 248, 255), 35, 6), (30872, (625, 181), (254, 255, 255), 35, 7), (31555, (625, 552), (27, 85, 241), 35, 1), (31923, (659, 499), (47, 105, 255), 35, 2), (32272, (689, 452), (67, 125, 255), 35, 3), (32984, (874, 572), (177, 190, 16), 35, 1), (33349, (889, 529), (197, 210, 36), 35, 2), (33680, (909, 504), (217, 230, 56), 35, 3), (34461, (989, 108), (125, 211, 153), 35, 1), (34845, (869, 108), (145, 231, 173), 35, 2), (35190, (752, 112), (165, 251, 193), 35, 3), (35570, (666, 115), (185, 255, 213), 35, 4), (35936, (572, 121), (205, 255, 233), 35, 5), (36304, (470, 126), (225, 255, 253), 35, 6), (36698, (343, 131), (245, 255, 255), 35, 7), (37481, (324, 336), (9, 0, 126), 35, 1), (37747, (412, 348), (29, 20, 146), 35, 2), (38098, (470, 348), (49, 40, 166), 35, 3), (38430, (601, 333), (69, 60, 186), 35, 4), (39113, (709, 409), (201, 10, 191), 35, 1), (39875, (849, 421), (221, 30, 211), 35, 2), (40642, (954, 425), (241, 50, 231), 35, 3), (41339, (1018, 243), (208, 28, 149), 35, 1), (42106, (904, 360), (228, 48, 169), 35, 2), (42818, (716, 244), (248, 68, 189), 35, 3), (43617, (604, 319), (255, 88, 209), 35, 4)
    ]

bg = pygame.image.load("src/mouse/background/gravity-falls.png")
pygame.mixer.music.load("src/mouse/music/GravityFalls.mp3")

pointFont = pygame.font.SysFont("monospace", 35, bold=True, italic=False)
WHITE = (255, 255, 255)

# List to store current shown circles
currentShownCircles = []

# Main game loop
running = True
renderMistake = False
playing = False
while running:
    # Clear the screen
    screen.blit(bg, (0, 0))
    
    current_tick = pygame.time.get_ticks()
    
    mouseX = pygame.mouse.get_pos()[0]
    mouseY = pygame.mouse.get_pos()[1]
    circleClickList = []
    
    if current_tick >= 5000:
        if playing == False:
            pygame.mixer.music.play()
            playing = True
    
    if current_tick < 5000:
        font = pygame.font.SysFont("monospace", 75, bold=False, italic=False)
        color = (255, 0, 0)
        label = font.render(str(5000 - current_tick), 1, color)
        screen.blit(label, (520, 320))
    
    # Draw circles based on the list
    for circle_info in circlesList:
        circle_tick, (x, y), color, size, pointNumber  = circle_info
        if current_tick >= circle_tick - 100 * size:
            pygame.draw.circle(screen, color, (x, y), size, width=int(((current_tick - circle_tick + 100 * size + 1))/(1)/100 + 1))
            circleLabel = pointFont.render(str(pointNumber), 1, WHITE)
            screen.blit(circleLabel, (x - 10,  y - 20))
            if int((current_tick - circle_tick + 100 * size + 1)/(1)/100 + 1) > size + 5:
                circlesList.remove(circle_info)
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
                circlesList.pop(0)
            else:
                font = pygame.font.SysFont("monospace", 75, bold=False, italic=False)
                color = (255, 0, 0)
                labelMistake = font.render("XXXXX", 1, color)
                mistakeTick = current_tick
                renderMistake = True
                
    if renderMistake == True:
        if mistakeTick > current_tick - 200:
            screen.blit(labelMistake, (520, 320))
        else:
            renderMistake = False    
            
    # Update the display
    pygame.display.flip()
    
    # Cap the frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()
sys.exit()
