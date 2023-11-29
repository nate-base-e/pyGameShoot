import pygame
import random

# Initialize pygame
pygame.init()

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Set up the display
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Pygame Rectangle with Font")

# Define the font
font = pygame.font.Font(None, 32)

# Create the rectangle
rectangle = pygame.Rect(100, 100, 200, 100)
color = WHITE

# Create the lines of font
text1 = font.render("Line 1", True, BLACK)
text2 = font.render("Line 2", True, BLACK)
text3 = font.render("Line 3", True, BLACK)

class box:

    def __init__(self,xloc,yloc,isDrawn):
        self.xloc = xloc
        self.yloc = yloc
        self.isDrawn = isDrawn

    def draw(self):
        screen.blit(rectangle)
recs = []
for i in range(100):
    #change y and x values
    #change draw or not
    recs.append(box(0,0))

# Create the selection arrow
arrow_pos = (rectangle.left + rectangle.width - 30, rectangle.top + 30)
arrow_color = RED

# Define the selection
selection = 0

# Main loop
running = True
while running:
    # Check for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Check for mouse clicks
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()

            # Check if the mouse clicked inside the rectangle
            if rectangle.collidepoint(mouse_pos):
                # Check which line of font was clicked
                if text1.get_rect(center=(rectangle.centerx,rectangle.centery-32)).collidepoint(mouse_pos):
                    selection = 0
                elif text2.get_rect(center=(rectangle.centerx+0, rectangle.centery)).collidepoint(mouse_pos):
                    selection = 1
                elif text3.get_rect(center=(rectangle.centerx+0, rectangle.centery+32)).collidepoint(mouse_pos):
                    selection = 2

    # Fill the background
    screen.fill(BLACK)

    # Draw the rectangle
    pygame.draw.rect(screen, color, rectangle)

    # Draw the lines of font
    screen.blit(text1, text1.get_rect(center=(rectangle.centerx,rectangle.centery-32)))
    screen.blit(text2, text2.get_rect(center=(rectangle.centerx,rectangle.centery)))
    screen.blit(text3, text3.get_rect(center=(rectangle.centerx,rectangle.centery+32)))

    # Draw the selection arrow
    if selection == 0:
        arrow_pos = (rectangle.left + rectangle.width - 30, rectangle.top + 15)
        arrow_color = RED
    elif selection == 1:
        arrow_pos = (rectangle.left + rectangle.width - 30, rectangle.top + 45)
        arrow_color = GREEN
    elif selection == 2:
        arrow_pos = (rectangle.left + rectangle.width - 30, rectangle.top + 80)
        arrow_color = BLUE

    pygame.draw.polygon(screen, arrow_color, [(arrow_pos[0], arrow_pos[1]), (arrow_pos[0] + 10, arrow_pos[1] + 5), (arrow_pos[0] + 10, arrow_pos[1] - 5)])

    # Update the display
    pygame.display.flip()

# Quit pygame
pygame.quit()