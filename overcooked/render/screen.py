import pygame

from overcooked import config


def create_screen(board):
    screen_width = len(board[0]) * config.TILE_SIZE
    screen_height = len(board[1]) * config.TILE_SIZE
    size = (screen_width, screen_height)
    screen = pygame.display.set_mode(size=size)
    pygame.display.set_caption("Overcooked")
    
    return screen