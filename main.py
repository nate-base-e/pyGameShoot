import pygame
from pygame import mixer

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0
gravity = 1.0
startx = 0
starty = 0


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

        self.image = pygame.image.load("assets/RocketSprite.png").convert_alpha()
        self.rect = pygame.Rect(startx,starty,100,100)

        self.x = startx
        self.y = starty
        self.vy = gravity
        self.vx = 0

    def update(self,dt):

        # Update the character's position
        self.x += 0
        self.rect.x +=0
        self.y += self.vy
        self.rect.y += self.vy

        self.vy += gravity*dt

    def draw(self, screen,num):
        #num is 1-4 for direction
        # Draw the character to the screen
        image = pygame.Surface((100*num,100)).convert_alpha()#this is the end
        image.blit(self.image,(0,0),(100*(num-1),0,100,100))#this is the beginning
        screen.blit(image,(0,0))


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

while running:
    #apply gravity

    if character.rect.colliderect(ground_rect):
        character.vy = 0
        character.update(dt)
        if not candrop:
            hit_sound.play()
            candrop = True
    else:
        character.update(dt)


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
    if keys[pygame.K_s]:
        character.y += 300 * dt
    if keys[pygame.K_a]:
        character.x -= 300 * dt
    if keys[pygame.K_d]:
        character.x += 300 * dt

    character.draw(screen,4)
    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000
#    pygame.draw.rect(screen, (255, 255, 255), ground_rect)

pygame.quit()



