import res
import pygame
import random
from pygame.sprite import Sprite

MAP_WIDTH, MAP_HEIGHT = 1400, 1100

class Apple(Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(res.apple)
        #self.image = pygame.Surface((30, 30))  # Создаем квадратное яблоко
        #self.image.fill((255, 0, 0))  # Заполняем красным цветом
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, MAP_WIDTH - self.rect.width)
        self.rect.y = random.randint(0, MAP_HEIGHT - self.rect.height)
