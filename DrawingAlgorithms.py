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
    c1 = 1
    c2 = 200
    c3 = 200
    c4 = 0.13456789
    M = 300
    coordinates = randomDraw(g, 205, 5, 635, 475) #bounds of canvas frame +- radius of nodes
    for i in range(0, M):
        forces = {}
        for nodeFrom in g.graph_dict:
            for nodeTo in g.graph_dict:
                if nodeFrom != nodeTo:
                    xdiff = coordinates[nodeFrom][0] - coordinates[nodeTo][0]
                    ydiff = coordinates[nodeFrom][1] - coordinates[nodeTo][1]
                    d = math.sqrt(xdiff**2 + ydiff**2)
                    currentForce = [0.0, 0.0]
                    
                    if nodeTo in g.graph_dict[nodeFrom]:
                        #if nodeTo is in the neighborhood of nodeFrom
                        #lx = c1 * log d * (Delta x/d)
                        #ly = c1 * log d * (Delta y/d)
                        currentForce = [-c1 * math.log(d/c2) * (xdiff/d),
                                        -c1 * math.log(d/c2) * (ydiff/d)]                     
                    else:
                        #if nodeTo is NOT adjacent to nodeFrom
                        currentForce = [(c3 / d**2) * (xdiff/d),
                                        (c3 / d**2) * (ydiff/d)]

                    if nodeFrom in forces:
                        forces[nodeFrom][0] += currentForce[0]
                        forces[nodeFrom][1] += currentForce[1]
                    else:
                        forces[nodeFrom] = currentForce

        xtotal = 0
        ytotal = 0
        for nodeFrom in coordinates:
            coordinates[nodeFrom][0] += c4*(forces[nodeFrom][0])
            coordinates[nodeFrom][1] += c4*(forces[nodeFrom][1])
            xtotal += forces[nodeFrom][0]
            ytotal += forces[nodeFrom][1]
        print("xtotal: ", xtotal, " ytotal: ", ytotal)
        #just get a copy of the coordinates (floored) for displaying
        coordinatesCopy = floor_coordinates(coordinates)
        canvas.display_graph(g, coordinatesCopy)
        time.sleep(.025)

    return coordinates    

    