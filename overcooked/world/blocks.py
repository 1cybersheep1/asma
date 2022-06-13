import pygame

from overcooked.world.holder import Holder
from overcooked.world.processor import Processor
from overcooked.render.tiles import SimpleTile
from overcooked import config

class Floor():
    def __init__(self):
        self.player = None
        
    @property
    def empty(self):
        return self.player == None

    def put(self, player):
        self.player = player

    def clear(self):
        self.player = None

    def render(self, screen, x, y):
        tile = SimpleTile(x, y, (204, 189, 161))

        if not self.empty:
            self.player.render(tile.image)

        tile.draw(screen)
    

class Table(Holder):
    def render(self, screen, x, y):
        tile = SimpleTile(x, y, (155, 101, 0))
        super().render(tile)
        tile.draw(screen)


    
class IngredientTable(Holder):
    def __init__(self, ingredient):
        self.ingredient = ingredient
        super().__init__()
    
    def interact(self, holding):
        if holding is not None:
            self.put(holding)
        else:
            if self.empty:
                return self.ingredient()
            else:
                return self.get()


class CuttingBoard(Processor):
    def __init__(self):
        super().__init__(processing_time=0)
        
    def process(self, obj):
        obj.cutted = True
        return obj
    
    def render(self, screen, x, y):
        tile = SimpleTile(x, y, (155, 101, 0))
        pygame.draw.rect(tile.image, (254, 254, 254), [config.TILE_SIZE*0.1, config.TILE_SIZE*0.1, config.TILE_SIZE*0.8, config.TILE_SIZE*0.8])
        tile.draw(screen)
        

class Stove(Processor):
    def __init__(self):
        super().__init__(processing_time=3)
        
    def process(self, obj):
        obj.cooked = True
        return obj

    def render(self, screen, x, y):
        tile = SimpleTile(x, y, (100, 100, 100))
        pygame.draw.circle(tile.image, (20, 20, 20), (config.TILE_SIZE//4, config.TILE_SIZE//4), config.TILE_SIZE//6)
        pygame.draw.circle(tile.image, (20, 20, 20), (3*config.TILE_SIZE//4, config.TILE_SIZE//4), config.TILE_SIZE//6)
        pygame.draw.circle(tile.image, (20, 20, 20), (config.TILE_SIZE//4, 3*config.TILE_SIZE//4), config.TILE_SIZE//6)
        pygame.draw.circle(tile.image, (20, 20, 20), (3*config.TILE_SIZE//4, 3*config.TILE_SIZE//4), config.TILE_SIZE//6)
        tile.draw(screen)
    
class Goal(Holder):
    def render(self, screen, x, y):
        tile = SimpleTile(x, y, (130, 147, 173))
        tile.draw(screen)