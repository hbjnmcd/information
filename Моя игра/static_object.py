import pygame
import res

class StaticObject:
    def __init__(self, image_path, position, interactive=False, name=None):
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect(topleft=position)
        self.interactive = interactive
        self.name = name

    def draw(self, surface, camera_offset):
        surface.blit(self.image, (self.rect.x - camera_offset[0], self.rect.y - camera_offset[1]))
