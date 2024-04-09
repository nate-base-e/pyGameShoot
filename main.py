import pygame
from random import random
from pygame import mixer

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0
gravity = 1.0

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

# mixer.init()
# mixer.music.load('song.mp3')
# mixer.music.set_volume(0.2)
# mixer.music.play()

hit_sound = pygame.mixer.Sound('assets/audio/empty_can.wav')
hit_sound.set_volume(0.4)


class Character(pygame.sprite.Sprite):
    # https://www.techwithtim.net/tutorials/game-development-with-python/pygame-tutorial/pygame-collision
    def __init__(self, startx, starty, frame):
        super().__init__()
        self.x = startx
        self.y = starty
        self.num = frame
        self.sheet = pygame.image.load("assets/rocketsheet.png")
        self.rect = pygame.Rect(100 * (self.num - 1), 0, 100, 100)  # rect is independent of the screen frame
        image_su = pygame.Surface(self.rect.size, pygame.SRCALPHA, 32).convert_alpha()
        image_su.blit(self.sheet, (0, 0), self.rect)
        self.image = image_su

        self.vy = gravity
        self.vx = 0
        self.angle = 0

    def update(self, dt):
        # Update the character's position
        self.x += 0
        self.y += self.vy
        self.rect = pygame.Rect(100 * (self.num - 1), 0, 100, 100)
        image_su = pygame.Surface(self.rect.size, pygame.SRCALPHA, 32).convert_alpha()
        image_su.blit(self.sheet, (0, 0), self.rect)
        self.image = image_su
        self.rect.center = (self.x, self.y)

        # self.vy += gravity * dt

        # TODO add rect shift for animation
        # TODO gravity is increasing instead of constant

    def rotate(self, angle):
        self.angle += angle
        rotated_image = pygame.transform.rotozoom(self.image, self.angle, 1.0)

        new_center = self.original_rect.center + rotated_image.get_offset()
        rotated_rect = rotated_image.get_rect(center=(new_center[0], new_center[1]))

        self.image = rotated_image
        self.rect = rotated_rect


class Viking(pygame.sprite.Sprite):
    # https://www.techwithtim.net/tutorials/game-development-with-python/pygame-tutorial/pygame-collision
    def __init__(self, startx, starty, frame):
        super().__init__()
        self.x = startx
        self.y = starty
        self.num = frame
        self.sheet = pygame.image.load("assets/VikingNB3.png")
        self.rect = pygame.Rect(0, 0, 400, 400)  # rect is independent of the screen frame
        image_su = pygame.Surface(self.rect.size, pygame.SRCALPHA, 32).convert_alpha()
        image_su.blit(self.sheet, (0, 0), self.rect)
        self.image = image_su
        self.vy = 0
        self.vx = 0
        self.angle = 0


    def update(self, dt):
        # Update the character's position
        self.x += 0
        self.y += self.vy
        self.rect = pygame.Rect(0, 0, 400, 400)
        image_su = pygame.Surface(self.rect.size, pygame.SRCALPHA, 32).convert_alpha()
        image_su.blit(self.sheet, (0, 0), self.rect)
        self.image = image_su
        self.rect.center = (self.x, self.y)






class Flake(pygame.sprite.Sprite):
    def __init__(self, x, y, size):
        super().__init__()
        self.size = random() * 4 + 4
        self.speed = random() * 3 + 2
        self.x = x
        self.y = y
        self.image = pygame.Surface((self.size, self.size), pygame.SRCALPHA, 32).convert_alpha()
        # self.image.fill((255, 0, 0))
        pygame.draw.circle(self.image, (255, 255, 255), (self.size / 2, self.size / 2),
                           self.size / 2)  # center is center of rect image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        # moves the snow down could add side to side
        self.rect.move_ip(0, self.speed)
        # removes the snow when it falls off the screen
        if self.rect.top > screen.get_height():
            self.kill()


def draw_rounded_rect(surface, rect, radius, color):
    """
    Draws a rectangle with rounded corners.
    """
    rect = pygame.Rect(rect)
    border_rect = rect.inflate(-2 * radius, -2 * radius)
    pygame.draw.rect(surface, color, border_rect)
    corner_rect = pygame.Rect(rect.x, rect.y, 2 * radius, 2 * radius)
    pygame.draw.ellipse(surface, color, corner_rect)
    corner_rect.move_ip(rect.width - 2 * radius, 0)
    pygame.draw.ellipse(surface, color, corner_rect)
    corner_rect.move_ip(0, rect.height - 2 * radius)
    pygame.draw.ellipse(surface, color, corner_rect)
    corner_rect.move_ip(rect.width - 2 * radius, 0)
    pygame.draw.ellipse(surface, color, corner_rect)


class Button:
    def __init__(self, x, y, width, height, text, font_size, default_color, hover_color, click_color, shadow_color,
                 callback):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.font_size = font_size
        self.font = pygame.font.SysFont(None, font_size)
        self.default_color = default_color
        self.hover_color = hover_color
        self.click_color = click_color
        self.shadow_color = shadow_color
        self.current_color = self.default_color
        self.callback = callback  # Function to execute on click

    def draw(self, screen):
        # Render the text
        text_surface = self.font.render(self.text, True, (0, 0, 0))
        text_x = self.x + (self.width - text_surface.get_width()) // 2
        text_y = self.y + (self.height - text_surface.get_height()) // 2

        # Draw the shadow with a slight offset
        shadow_offset = 2  # Adjust this value for shadow intensity
        draw_rounded_rect(screen, (self.x + shadow_offset, self.y + shadow_offset, self.width, self.height), 5,
                          self.shadow_color)

        # Draw the button with rounded corners
        draw_rounded_rect(screen, (self.x, self.y, self.width, self.height), 5, self.current_color)

        # Draw the text on the button
        screen.blit(text_surface, (text_x, text_y))

    def handle_event(self, event):
        # Check if mouse is hovering over the button
        mouse_pos = pygame.mouse.get_pos()
        if self.x < mouse_pos[0] < self.x + self.width and self.y < mouse_pos[1] < self.y + self.height:
            self.current_color = self.hover_color
            # Check for click event
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.current_color = self.click_color
                if self.callback:
                    self.callback()  # Execute callback function
        else:
            self.current_color = self.default_color


# creating a group for the snow sprites
snow = pygame.sprite.Group()


def button_clicked():
    print("Button Clicked!")


def addFlake(x, y, size, group):
    snowFlake = Flake(x, y, size)
    group.add(snowFlake)


for i in range(20):
    addFlake(random() * screen.get_width(), 0, 8, snow)

# Create a Sprite group
sprites = pygame.sprite.Group()

# Create a character object
viking = Viking(400,300,0)
character = Character(100, 100, 1)


button = Button(100, 100, 200, 50, "Click Me", 30, (200, 240, 20), (255, 15, 100), (100, 100, 255), (100, 100, 100),
                button_clicked)

# Add the character to the Sprite group
sprites.add(character)
sprites.add(viking)

bGimage = pygame.image.load("assets/galaxy.jpg")

# add ground to the game
ground_rect = pygame.Rect(0, screen.get_height() - 50, screen.get_width(), 50)
candrop = False
update = False
totTime = 0
framerate = 60  # fps
bgx = 0

while running:
    # button event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        button.handle_event(event)

    if totTime > 1 / framerate:
        totTime -= 1 / framerate
        update = True

    # add a new snowflake on every frame
    if update:
        addFlake(random() * screen.get_width(), 0, 8, snow)

    if character.rect.colliderect(ground_rect):
        character.vy = 0
        character.update(dt)
        if not candrop:
            hit_sound.play()
            candrop = True
    else:
        character.update(dt)
        candrop = False

    viking.vy = 0
    viking.update(dt)

    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # drawing background
    background_image = pygame.transform.scale(bGimage, (screen.get_width() * 2, screen.get_height() * 2))
    screen.blit(background_image, (bgx, 0))

    snow.update()
    snow.draw(screen)
    button.draw(screen)
    # this gets the keys that were pressed
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        character.y -= 300 * dt
        character.num = 4
    if keys[pygame.K_s]:
        character.y += 300 * dt
        character.num = 2
    if keys[pygame.K_a]:
        character.x -= 300 * dt
        character.num = 3
        if bgx + 300 * dt < 0:
            bgx += 300 * dt
    if keys[pygame.K_d]:
        character.x += 300 * dt
        character.num = 1
        if bgx - 300 * dt > -screen.get_width():
            bgx -= 300 * dt

    sprites.draw(screen)
    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000
    #    pygame.draw.rect(screen, (255, 255, 255), ground_rect)
    totTime += dt
    update = False

pygame.quit()
