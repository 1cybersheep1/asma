import pygame

from overcooked.render import colors
from overcooked import config
from overcooked.world import blocks


class Player:
    def __init__(self, name, row, col) -> None:
        self.name = name
        self.color = colors.random_color()
        self.row = row
        self.col = col

    def move(self, board, n_row, n_col):
        current = board[self.row][self.col]
        try:
            target_cell = board[n_row][n_col]
        except IndexError:
            return

        if isinstance(target_cell, blocks.Floor) and target_cell.empty:
            target_cell = board[n_row][n_col]
            target_cell.put(self)
            current.clear()
            self.row = n_row
            self.col = n_col


    def render(self, image):
        pygame.draw.polygon(image, self.color, [(config.TILE_SIZE*0.2, config.TILE_SIZE//2),(config.TILE_SIZE//2, config.TILE_SIZE*0.2),
                                                (config.TILE_SIZE*0.8, config.TILE_SIZE//2),(config.TILE_SIZE//2, config.TILE_SIZE*0.8)])
        pygame.draw.circle(image, (240,240,240), (config.TILE_SIZE//2, config.TILE_SIZE//5), config.TILE_SIZE//6)



