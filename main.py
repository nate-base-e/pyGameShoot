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
    def __init__(self,startx,starty,frame):
        super().__init__()
        self.x = startx
        self.y = starty
        self.num = frame
        self.sheet = pygame.image.load("assets/RocketSprite.png")
        self.rect = pygame.Rect(100*(self.num-1), 0, 100, 100) #rect is independent of the screen frame
        image_su = pygame.Surface(self.rect.size)
        image_su.blit(self.sheet, (0,0), self.rect)
        self.image = image_su


        self.vy = gravity
        self.vx = 0
        self.angle = 0

    def update(self, dt):
        # Update the character's position
        self.x += 0
        self.y += self.vy
        self.rect = pygame.Rect(100 * (self.num - 1), 0, 100, 100)
        image_su = pygame.Surface(self.rect.size)
        image_su.blit(self.sheet, (0,0), self.rect)
        self.image = image_su
        self.rect.center = (self.x, self.y)


        #self.vy += gravity * dt

        #TODO add rect shift for animation
        #TODO gravity is increasing instead of constant


    def rotate(self, angle):
        self.angle += angle
        rotated_image = pygame.transform.rotozoom(self.image, self.angle, 1.0)

        new_center = self.original_rect.center + rotated_image.get_offset()
        rotated_rect = rotated_image.get_rect(center=(new_center[0], new_center[1]))

        self.image = rotated_image
        self.rect = rotated_rect


class Flake(pygame.sprite.Sprite):
    def __init__(self, x, y, size):
        super().__init__()
        self.size = size
        self.speed = random()*3 + 2
        self.x = x
        self.y = y
        self.image = pygame.Surface((self.size, self.size))
        # self.image.fill((255, 0, 0))
        pygame.draw.circle(self.image, (255, 255, 255), (self.size / 2, self.size / 2),
                           self.size / 2)  # center is center of rect image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        self.y += self.speed
        #self.x += random()*4-2
        self.rect.center = (self.x, self.y)


# creating a group for the snow sprites
snow = pygame.sprite.Group()


def addFlake(x, y, size, group):
    snowFlake = Flake(x, y, size)
    group.add(snowFlake)


for i in range(20):
    addFlake(random() * screen.get_width(), 0, 8, snow)

# Create a Sprite group
sprites = pygame.sprite.Group()

# Create a character object
character = Character(100, 100, 1)

# Add the character to the Sprite group
sprites.add(character)
bGimage = pygame.image.load("assets/galaxy.jpg")

# add ground to the game
ground_rect = pygame.Rect(0, screen.get_height() - 50, screen.get_width(), 50)
candrop = False
update = False
totTime = 0
framerate = 60  # fps

while running:
    if totTime > 1 / framerate:
        totTime -= 1 / framerate
        update = True

    # rotate item
    # if update:
    #     character.rotate(2)

    # apply gravity

    if character.rect.colliderect(ground_rect):
        character.vy = 0
        character.update(dt)
        if not candrop:
            hit_sound.play()
            candrop = True
    else:
        character.update(dt)
        candrop = False

    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # drawing background
    background_image = pygame.transform.scale(bGimage, screen.get_size())
    screen.blit(background_image, (0, 0))

    snow.update()
    snow.draw(screen)

    # this gets the keys that were pressed
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        character.y -= 300 * dt
        character.num = 1
    if keys[pygame.K_s]:
        character.y += 300 * dt
        character.num = 2
    if keys[pygame.K_a]:
        character.x -= 300 * dt
        character.num = 3
    if keys[pygame.K_d]:
        character.x += 300 * dt
        character.num = 4

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
