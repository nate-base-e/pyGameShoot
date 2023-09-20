import pygame

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)


class Character(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.image.load("assets/rocket_ship.jpg")
        self.rect = self.image.get_rect()

        self.x = 500
        self.y = 500

    def update(self):
        # Update the character's position

        self.x += 1
        self.y += 1

    def draw(self, screen):
        # Draw the character to the screen

        screen.blit(self.image, (self.x, self.y))


# Create a Sprite group
sprites = pygame.sprite.Group()

# Create a character object
character = Character()

# Add the character to the Sprite group
sprites.add(character)

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    bGimage = pygame.image.load("assets/galaxy.jpg")
    background_image = pygame.transform.scale(bGimage, screen.get_size())
    screen.blit(background_image, (0, 0))

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        character.y -= 300 * dt
    if keys[pygame.K_s]:
        character.y += 300 * dt
    if keys[pygame.K_a]:
        character.x -= 300 * dt
    if keys[pygame.K_d]:
        character.x += 300 * dt

    character.draw(screen)
    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()
