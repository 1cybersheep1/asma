import pygame

from overcooked import config
from overcooked.render import colors


class SimpleTile(pygame.sprite.Sprite):
    
    def __init__(self, x, y, color):
        super().__init__()
        
        self.image = pygame.Surface([config.TILE_SIZE, config.TILE_SIZE])
        self.image.fill(colors.WHITE)
        self.image.set_colorkey(colors.WHITE)
 
        pygame.draw.rect(self.image, color, [0, 0, config.TILE_SIZE, config.TILE_SIZE])
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw(self, screen):
        screen.blit(self.image, self.rect)
