from overcooked.world import player
from overcooked.world.player import Player
from overcooked.world import blocks, ingredients


simple_symbols = {
    "-": blocks.Table,
    " ": blocks.Floor,
    "/": blocks.CuttingBoard,
    "o": blocks.Stove,
    "*": blocks.Goal
}


ingredients = {
    "m": ingredients.Meat,
    "p": ingredients.Plate
}


def generate_position(symbol):
    if symbol in ingredients:
        return blocks.IngredientTable(ingredients[symbol])
    else:
        return simple_symbols[symbol]()
    

def generate_board(lines):
    board = []
    players = []

    for row, line in enumerate(lines):
        board_line = []
        for col, symbol in enumerate(line):
            if symbol.isdigit():
                p = Player(f"player_{symbol}", row, col)
                floor = blocks.Floor()
                players.append(p)
                floor.put(p)
                board_line.append(floor)
            else:
                board_line.append(generate_position(symbol))
        board.append(board_line)
    
    return board, players
