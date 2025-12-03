import pygame
import math

# Bilder nur einmal global laden → deutlich schneller
CAR_IMG = pygame.image.load('images/car.png')
PAD_NORMAL = pygame.image.load('images/race_pads.png')
PAD_HIT = pygame.image.load('images/collision.png')
TROPHY_IMG = pygame.image.load('images/trophy.png')


class CarSprite(pygame.sprite.Sprite):
    MAX_FORWARD_SPEED = 10
    MAX_REVERSE_SPEED = 10
    ACCELERATION = 2
    TURN_SPEED = 10

    def __init__(self, image, position):
        super().__init__()
        self.src_image = CAR_IMG  # argument image wird ignoriert → immer echtes Asset
        self.position = position
        self.speed = 0
        self.direction = 0
        self.k_left = self.k_right = self.k_down = self.k_up = 0

    def update(self, deltat):
        # Geschwindigkeit
        self.speed += (self.k_up + self.k_down)
        self.speed = max(-self.MAX_REVERSE_SPEED,
                         min(self.speed, self.MAX_FORWARD_SPEED))

        # Rotation
        self.direction += (self.k_right + self.k_left)

        # Bewegung per Physik
        x, y = self.position
        rad = math.radians(self.direction)
        x += -self.speed * math.sin(rad)
        y += -self.speed * math.cos(rad)
        self.position = (x, y)

        # Bild rotieren → rect aktualisieren
        rot = pygame.transform.rotate(self.src_image.convert_alpha(), self.direction)
        self.image = rot
        self.rect = self.image.get_rect()
        self.rect.center = self.position


class PadSprite(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.normal = PAD_NORMAL
        self.hit = PAD_HIT
        self.image = self.normal
        self.rect = self.image.get_rect()
        self.rect.center = position

    # Rein für Visualisierung (GA nutzt kein update hier)
    def update(self, hit_list):
        self.image = self.hit if self in hit_list else self.normal


class Trophy(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.image = TROPHY_IMG
        self.rect = self.image.get_rect()
        self.rect.center = position