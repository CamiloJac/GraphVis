import random

def randomDraw(g, x1, y1, x2, y2):
    coordinates = {}
    for node in g:
        coordinates[node] = (random.randrange(x1, x2, 1), random.randrange(y1, y2, 1))
    return coordinates