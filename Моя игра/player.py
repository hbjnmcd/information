import pygame
import res

class Player:
    def __init__(self, image_path):
        self.image = pygame.image.load(image_path)  # Загружаем изображение
        self.rect = self.image.get_rect(center=(600, 450))

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def draw(self, surface, camera_offset):
        # Рисуем игрока с учетом смещения камеры
        surface.blit(self.image, (self.rect.x - camera_offset[0], self.rect.y - camera_offset[1]))