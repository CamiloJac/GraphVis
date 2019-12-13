import math
import random
import time
import pygame

def floor_coordinates(coordinates):
    for coord in coordinates:
        coordinates[coord][0] = math.floor(coordinates[coord][0])
        coordinates[coord][1] = math.floor(coordinates[coord][1])

    return coordinates

def normalize_coordinates(coordinates, xMin, yMin, xMax, yMax):
    xDiffMin = 0
    xDiffMax = 0
    yDiffMin = 0
    yDiffMax = 0

    for coord in coordinates:
        if coordinates[coord][0] < xMin:
            if xMin - coordinates[coord][0] > xDiffMin:
                xDiffMin = xMin - coordinates[coord][0]
            coordinates[coord][0] += xDiffMin

        if coordinates[coord][1] < yMin:
            if yMin - coordinates[coord][1] > yDiffMin:
                yDiffMin = yMin - coordinates[coord][1]
            coordinates[coord][1] += yDiffMin

        if coordinates[coord][0] > xMax:
            if xMax - coordinates[coord][0] > xDiffMax:
                xDiffMax = xMax - coordinates[coord][0]
            coordinates[coord][0] -= xDiffMax

        if coordinates[coord][1] > yMax:
            if yDiffMax - coordinates[coord][1] > yDiffMax:
                yDiffMax = yMax - coordinates[coord][1]
            coordinates[coord][1] -= yDiffMax

    for coord in coordinates:
        if coordinates[coord][0] + xDiffMin < xMax:
            coordinates[coord][0] += xDiffMin
        
        if coordinates[coord][1] + yDiffMin < yMax:
            coordinates[coord][1] += yDiffMin
        
        if coordinates[coord][0] - xDiffMax > xMin:
            coordinates[coord][0] -= xDiffMax
        
        if coordinates[coord][1] - yDiffMax > yMin:
            coordinates[coord][1] -= yDiffMax
        
    return coordinates

def randomDraw(g, x1, y1, x2, y2, canvas=None, surfaces=None):
    coordinates = {}
    for node in g.graph_dict:
        coordinates[node] = [random.randrange(x1, x2, 1),
                            random.randrange(y1, y2, 1)]
    if canvas and surfaces:
        surfaces[0] = canvas.get_next_surface(g, coordinates)
    return coordinates

def spring(g, x1, y1, x2, y2, canvas, surfaces, coordinates=None):
    coordinatesCopyList = {}
    canvas.clear()
    canvas.display_loading()
    c1 = 1
    c2 = y2/2
    c3 = y2/2
    c4 = 0.3
    M = 300
    if not coordinates:
        coordinates = randomDraw(g, x1, y1, x2, y2) #bounds of canvas frame +- radius of nodes

    for i in range(0, M):
        forces = {}
        coordinatesCopyList[i] = {}
        for nodeFrom in g.graph_dict:
            for nodeTo in g.graph_dict:
                if nodeFrom != nodeTo:
                    xdiff = coordinates[nodeFrom][0] - coordinates[nodeTo][0]
                    ydiff = coordinates[nodeFrom][1] - coordinates[nodeTo][1]
                    d = math.sqrt(xdiff**2 + ydiff**2)
                    if d == 0:
                        d = 1
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
        #just get a copy of the coordinates (floored) for displaying
        coordinatesCopy = floor_coordinates(coordinates)
        coordinatesCopy = normalize_coordinates(coordinates, x1, y1, x2, y2)
        #canvas.display_graph(g, coordinatesCopy)
        surfaces[i] = canvas.get_next_surface(g, coordinatesCopy)

    return coordinates

def orientation(p, q, r):
    val = (q[1] - p[1]) * (r[0] - q[0]) - \
          (q[0] - p[0]) * (r[1] - q[1])
    
    if val == 0:
        return 0
    elif val > 0:
        return 1
    else:
        return 2

def convexHull(g, coordinates):
    if len(coordinates) < 3:
        return
    
    # Get left most point
    leftMost = min(coordinates, key=coordinates.get)
    p = leftMost
    hull = {}
    q = 0

    while True:
        
        # Append current point to hull
        hull[p] = coordinates[p]

        q = (p + 1) % len(coordinates)

        for node in coordinates:
            if orientation(coordinates[p], coordinates[node], coordinates[q]) == 2:
                q = node
        
        p = q

        if p == leftMost:
            break

    return hull

def getPolygon(g, center, canvas):
    sublist = [node for node in g.graph_dict]
    sublist = sublist[0:random.randrange(3, len(g.graph_dict))]
    partition = {}
    for node in sublist:
        partition[node] = [0.0, 0.0]

    i = 0
    for node in partition:
        partition[node] = [math.ceil(center[0] + (canvas.height/2) * math.cos(i * (2 * math.pi) / len(partition))),
                            math.ceil(center[1] + (canvas.height/2) * math.sin(i * (2 * math.pi) / len(partition)))]
        i+=1
    return partition

def sumEdges(g, nodeV, coordinates):
    summationX = 0
    summationY = 0
    for nodeU in g.graph_dict[nodeV]:
        summationX += coordinates[nodeU][0]
        summationY += coordinates[nodeU][1]
    return [summationX, summationY]

def barycenterDraw(g, x1, y1, x2, y2, canvas, surfaces, hull=False):
    canvas.clear()
    canvas.display_loading()

    center = [(x1+x2)/2, y2/2]
    if not hull:
        coordinates = getPolygon(g, center, canvas)
    else:
        coordinates = randomDraw(g, x1, y1, x2, y2)
        coordinates = convexHull(g, coordinates)

    fixedVertices = coordinates.copy()

    #place each free vertex at origin
    for node in g.graph_dict:
        if node in fixedVertices:
            continue
        else:
            coordinates[node] = center.copy()

    #place free vertices according to fixed vertices
    i = 1
    if not hull:
        i = 200

    for i in range(0, i):
        for node in g.graph_dict:
            if node in fixedVertices:
                continue
            else:
                summation = sumEdges(g, node, coordinates)
                if len(g.graph_dict[node]) > 0:
                    oneOverDeg = 1 / len(g.graph_dict[node])
                else:
                    oneOverDeg = 1 / random.random()
                coordinates[node][0] = math.ceil(oneOverDeg * summation[0])
                coordinates[node][1] = math.ceil(oneOverDeg * summation[1])

        coordinates = normalize_coordinates(coordinates, x1, y1, x2, y2)
        surfaces[i] = canvas.get_next_surface(g, coordinates)

    return coordinates

#convex hull
#tree drawings -- put leaves on outside
#start with barycentic and plug into spring
#clean up (try out for more graphs)
#generate trees by picking random previous parent
#find spanning tree, run bfs on vertex, make bfs, get leaves as polygon 