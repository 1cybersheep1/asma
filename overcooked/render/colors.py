import numpy as np


BLACK = ( 0, 0, 0)
WHITE = ( 255, 255, 255)
GREEN = ( 0, 255, 0)
RED = ( 255, 0, 0)


def random_color():
    return list(np.random.choice(range(256), size=3))