from ast import In
import pygame
import cv2
from overcooked import config
from overcooked.world.utils import generate_board

from overcooked.render.screen import create_screen
from overcooked.render import colors


MOVEMENTS = {
    "left": (0, -1),
    "up": (-1, 0),
    "right": (0, 1),
    "down": (1, 0),
    "stay": (0, 0)
}

class World:
    def __init__(self, level_txt) -> None:
        with open(level_txt) as f:
            lines = f.readlines()
            lines = [l.strip() for l in lines]
        self.board, self.players = generate_board(lines)
        self.players_by_name = {p.name:p for p in self.players}
        self.screen = None
    
    

    def get_cell(self, row, column):
        return self.board[row, column]

    def move(self, player, direction):
        offset = MOVEMENTS[direction]
        player.move(self.board, player.row+offset[0], player.col+offset[1])

    def execute_action(self, player, action):
        if action != 4:
            direction = list(MOVEMENTS.keys())[action]
            self.move(self.players_by_name[player], direction)
            if self.players_by_name[player].row == 3 and self.players_by_name[player].col == 1:
                return 1, True
            return 0, False

    def array(self):
        screen = self.render()
        array = pygame.surfarray.pixels3d(screen)
        array = cv2.rotate(array, cv2.cv2.ROTATE_90_CLOCKWISE)
        array = cv2.flip(array, 1)
        array = cv2.cvtColor(array, cv2.COLOR_RGB2BGR)
        return array

    def render(self):
        if self.screen is None:
            pygame.init()
            self.screen = create_screen(self.board)

        self.screen.fill(colors.WHITE)

        for row in range(len(self.board)):
            for column in range(len(self.board[row])):
                self.board[row][column].render(self.screen, column * config.TILE_SIZE, row * config.TILE_SIZE)

        pygame.display.flip()

        return self.screen


    def interactive_render(self):
        pygame.init()
        self.screen = create_screen(self.board)

        carryOn = True
        clock = pygame.time.Clock()

        player = self.players[0]

        while carryOn:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    carryOn = False
                elif event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_ESCAPE:
                        carryOn = False
                    elif event.key==pygame.K_LEFT:
                        self.move(player, 'left')
                    elif event.key==pygame.K_RIGHT:
                        self.move(player, 'right')
                    elif event.key==pygame.K_DOWN:
                        self.move(player, 'down')
                    elif event.key==pygame.K_UP:
                        self.move(player, 'up')
                

            screen.fill(colors.WHITE)

            for row in range(len(self.board)):
                for column in range(len(self.board[row])):
                    self.board[row][column].render(screen, column * config.TILE_SIZE, row * config.TILE_SIZE)

            pygame.display.flip()
            clock.tick(60)

        pygame.quit()



