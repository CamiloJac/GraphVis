import math
import random

def randomDraw(g, x1, y1, x2, y2):
    coordinates = {}
    for node in g.graph_dict:
        coordinates[node] = (random.randrange(x1, x2, 1), random.randrange(y1, y2, 1))
    return coordinates

def baryCentric(g, x1, y1, x2, y2):
    #lx = c1 * log d * (Delta x/d)
    #ly = c1 * log d * (Delta y/d)


    width = x2-x1
    height = y2-y1
    area = width * height
    coordinates = randomDraw(g, x1, y1, x2, y2)
    k = math.sqrt(area*len(coordinates))
