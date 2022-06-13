import pygame

from overcooked import config

class Ingredient:
    def render(self, tile):
        pass

class Meat(Ingredient):
    def render(self, tile):
        pygame.draw.rect(tile.image, (254, 254, 0), [config.TILE_SIZE*0.1, config.TILE_SIZE*0.1, config.TILE_SIZE*0.8, config.TILE_SIZE*0.8])

class Plate(Ingredient):
    def render(self, tile):
        pygame.draw.rect(tile.image, (254, 254, 0), [config.TILE_SIZE*0.1, config.TILE_SIZE*0.1, config.TILE_SIZE*0.8, config.TILE_SIZE*0.8])
