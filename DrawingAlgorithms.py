import math
import random
import time
import pygame


white = 255,255,255
red = 195, 75, 75

def randomDraw(g, x1, y1, x2, y2):
    coordinates = {}
    for node in g.graph_dict:
        coordinates[node] = [random.randrange(x1, x2, 1), 
                            random.randrange(y1, y2, 1)]
    return coordinates

def spring(g, x1, y1, x2, y2, display):
    #lx = c1 * log d * (Delta x/d)
    #ly = c1 * log d * (Delta y/d)
    c1 = 2
    c2 = 1
    c3 = 1
    c4 = 0.1
    M = 100
    coordinates = randomDraw(g, 400, 220, 420, 240)
    forces = {}
    for i in range(0, M):
        for nodeFrom in g.graph_dict:
            for coord in coordinates:
                if coord != nodeFrom:
                    xdiff = coordinates[nodeFrom][0] - coordinates[coord][0]
                    ydiff = coordinates[nodeFrom][1] - coordinates[coord][1]
                    d = math.sqrt(math.pow(xdiff,2) + math.pow(ydiff,2))
                    if coord in g.graph_dict[nodeFrom]:
                        forces[nodeFrom] = [c1 * math.log(d/c2) * (xdiff/d),
                                    c1 * math.log(d/c2) * (ydiff/d)]
                    else:
                        forces[nodeFrom] = [c3 / math.pow(xdiff, 2),
                                    c3 / math.pow(ydiff, 2)]
                    coordinates[nodeFrom][0] += c4*(forces[nodeFrom][0])
                    coordinates[nodeFrom][1] += c4*(forces[nodeFrom][1])

        for coord in coordinates:
            coordinates[coord][0] = math.floor(coordinates[coord][0])
            coordinates[coord][1] = math.floor(coordinates[coord][1])
        pygame.draw.rect(display, white, ((200,0), (440, 480)))
        for node in g.graph_dict:
            for edge in g.graph_dict[node]:
                pygame.gfxdraw.line(display, 
                                    coordinates[node][0], coordinates[node][1], 
                                    coordinates[edge][0], coordinates[edge][1], 
                                    (0,0,0))


        for node in coordinates:
            pygame.gfxdraw.filled_circle(display,
                                        coordinates[node][0], coordinates[node][1], 
                                        5, red)
            pygame.gfxdraw.aacircle(display,
                                    coordinates[node][0], coordinates[node][1], 
                                    5, red)
        pygame.display.update()
        time.sleep(.25)
    
    return coordinates    
