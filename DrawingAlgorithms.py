import math
import random
import time
import pygame

def floor_coordinates(coordinates):
        for coord in coordinates:
            coordinates[coord][0] = math.floor(coordinates[coord][0])
            coordinates[coord][1] = math.floor(coordinates[coord][1])
        return coordinates

def randomDraw(g, x1, y1, x2, y2):
    coordinates = {}
    for node in g.graph_dict:
        coordinates[node] = [random.randrange(x1, x2, 1), 
                            random.randrange(y1, y2, 1)]
    return coordinates

def spring(g, x1, y1, x2, y2, canvas):
    #lx = c1 * log d * (Delta x/d)
    #ly = c1 * log d * (Delta y/d)
    c1 = 2
    c2 = 100
    c3 = 1
    c4 = 0.3
    M = 100
    coordinates = randomDraw(g, 205, 5, 635, 475)
    forces = {}
    for i in range(0, M):
        for nodeFrom in g.graph_dict:
            for coord in coordinates:
                if coord != nodeFrom:
                    xdiff = coordinates[nodeFrom][0] - coordinates[coord][0]
                    ydiff = coordinates[nodeFrom][1] - coordinates[coord][1]
                    d = math.sqrt(xdiff**2 + ydiff**2)

                    if coord in g.graph_dict[nodeFrom]:
                        forces[nodeFrom] = [-c1 * math.log(d/c2) * (xdiff/d),
                                            -c1 * math.log(d/c2) * (ydiff/d)]
                    else:
                        forces[nodeFrom] = [c3 / d**2,
                                            c3 / d**2]

                    coordinates[nodeFrom][0] += c4*(forces[nodeFrom][0])
                    coordinates[nodeFrom][1] += c4*(forces[nodeFrom][1])

        coordinatesCopy = floor_coordinates(coordinates)
        canvas.display_graph(g, coordinatesCopy)
        time.sleep(.025)

    return coordinates    

    