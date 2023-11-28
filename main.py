import pygame
from pygame import mixer

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0
gravity = 1.0
startx = 200
starty = 200


player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

# mixer.init()
# mixer.music.load('song.mp3')
# mixer.music.set_volume(0.2)
# mixer.music.play()

hit_sound = pygame.mixer.Sound('assets/audio/empty_can.wav')
hit_sound.set_volume(0.4)


class Character(pygame.sprite.Sprite):
#https://www.techwithtim.net/tutorials/game-development-with-python/pygame-tutorial/pygame-collision
    def __init__(self):
        super().__init__()

        self.characterSurface = None
        self.original_image = pygame.image.load("assets/rocket_ship.jpg")
        self.image = self.original_image
        self.original_rect = self.image.get_rect()

        self.x = startx
        self.y = starty
        self.vy = gravity
        self.vx = 0
        self.angle = 0

    def update(self,dt):

        # Update the character's position
        self.x += 0
        self.rect.x +=0
        self.y += self.vy
        self.rect.y += self.vy

        self.vy += gravity*dt

    def draw(self, screen):
        # Draw the character to the screen

        screen.blit(self.image, self.rect)

    def rotate(self,angle):
        self.angle += angle
        rotated_image = pygame.transform.rotozoom(self.image, self.angle, 1.0)

        new_center = self.original_rect.center + rotated_image.get_offset()
        rotated_rect = rotated_image.get_rect(center=(new_center[0], new_center[1]))

        self.image = rotated_image
        self.rect = rotated_rect



# Create a Sprite group
sprites = pygame.sprite.Group()

# Create a character object
character = Character()
character.rect = pygame.Rect(startx, starty, 50, 50)

# Add the character to the Sprite group
sprites.add(character)
bGimage = pygame.image.load("assets/galaxy.jpg")

#add ground to the game
ground_rect = pygame.Rect(0, screen.get_height() - 50, screen.get_width(), 50)
candrop = False
update = False
totTime = 0
framerate = 60 #fps

while running:
    if totTime>1/framerate:
        totTime-=1/framerate
        update = True

    #rotate item
    # if update:
    #     character.rotate(2)

    #apply gravity

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

    background_image = pygame.transform.scale(bGimage, screen.get_size())
    screen.blit(background_image, (0, 0))


    # this gets the keys that were pressed
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        character.y -= 300 * dt
        character.rect.y -= 300 *dt
    if keys[pygame.K_s]:
        character.y += 300 * dt
        character.rect.y += 300 * dt
    if keys[pygame.K_a]:
        character.x -= 300 * dt
        character.rect.x -= 300 * dt
    if keys[pygame.K_d]:
        character.x += 300 * dt
        character.rect.x += 300 * dt

    character.draw(screen)
    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000
#    pygame.draw.rect(screen, (255, 255, 255), ground_rect)
    totTime+=dt
    update = False

pygame.quit()



