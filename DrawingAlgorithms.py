import math
import random
import time
import pygame

def floor_coordinates(coordinates):
    for coord in coordinates:
        coordinates[coord][0] = math.floor(coordinates[coord][0])
        coordinates[coord][1] = math.floor(coordinates[coord][1])
    return coordinates

def normalize_coordinates(coordinates, x1, y1, x2, y2):
    xMin = x1
    yMin = y1
    for coord in coordinates:
        if coordinates[coord][0] < xMin:
            xMin = coordinates[coord][0]

        if coordinates[coord][1] < yMin:
            yMin = coordinates[coord][1]

    xDiff = x1-xMin
    if xDiff > 0:
        for coord in coordinates:
            coordinates[coord][0] += xDiff

    yDiff = y1-yMin
    if yDiff > 0:
        for coord in coordinates:
            coordinates[coord][1] += yDiff

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
    c4 = 0.3
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
        #print("xtotal: ", xtotal, " ytotal: ", ytotal)
        #just get a copy of the coordinates (floored) for displaying
        coordinatesCopy = floor_coordinates(coordinates)
        coordinatesCopy = normalize_coordinates(coordinates, x1, y1, x2, y2)
        canvas.display_graph(g, coordinatesCopy)
        time.sleep(.025)

    return coordinates

def getPolygon(g, center):
    sublist = [node for node in g.graph_dict]
    sublist = sublist[0:6]
    partition = {}
    for node in sublist:
        partition[node] = [0.0, 0.0]

    i = 0
    for node in partition:
        partition[node] = [math.ceil(center[0] + 100 * math.cos(i * (2 * math.pi) / len(partition))),
                            math.ceil(center[1] + 100 * math.sin(i * (2 * math.pi) / len(partition)))]
        i+=1
    return partition

def sumEdges(g, nodeV, coordinates):
    summationX = 0
    summationY = 0
    for nodeU in g.graph_dict[nodeV]:
        summationX += coordinates[nodeU][0]
        summationY += coordinates[nodeU][1]
    return [summationX, summationY]

def barycenterDraw(g, x1, y1, x2, y2, canvas):
    center = [420, 240]
    coordinates = getPolygon(g, center)
    fixedVertices = coordinates.copy()

    #place each free vertex at origin
    for node in g.graph_dict:
        if node in fixedVertices:
            continue
        else:
            coordinates[node] = center.copy()

    #place free vertices according to fixed vertices
    for node in g.graph_dict:
        if node in fixedVertices:
            continue
        else:
            summation = sumEdges(g, node, coordinates)
            oneOverDeg = 1 / len(g.graph_dict[node])
            coordinates[node][0] = math.ceil(oneOverDeg * summation[0])
            coordinates[node][1] = math.ceil(oneOverDeg * summation[1])

    return coordinates

#convex hull
#tree drawings -- put leaves on outside
#start with barycentic and plug into spring
#clean up (try out for more graphs)
