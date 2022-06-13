import pygame


class TileGroup(pygame.sprite.Group):
    def draw(self, screen):
        for sprite in self.sprites():
            sprite.draw(screen)
