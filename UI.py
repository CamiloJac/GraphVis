import pygame
import thorpy
import DrawingAlgorithms as algo
from Graph import Graph

white = 255,255,255
red = 195, 75, 75
grey = 150, 150, 150
yellow = 255, 255, 0

class Menu:

    def __init__(cls, display, topleft, size, g, drawingCanvas):
        cls.g = g
        cls.display = display
        title_element = thorpy.make_text('Graph Visualizer', 20, yellow)
        cls.nodeCount = thorpy.Inserter(name="# of Nodes: ")
        cls.probability = thorpy.Inserter(name="Probability: ")
        randomDraw = thorpy.make_button('Random Draw',
                                        func=drawingCanvas.draw_graph,
                                        params={'g':g,
                                        'drawType':'rand',
                                        'menu': cls})
        springDraw = thorpy.make_button('Spring Draw',
                                        func=drawingCanvas.draw_graph,
                                        params={'g':g,
                                        'drawType':'spring',
                                        'menu': cls})
        barycentricDraw = thorpy.make_button('Barycenter-Draw',
                                        func=drawingCanvas.draw_graph,
                                        params={'g':g,
                                        'drawType':'barycentric',
                                        'menu': cls})
        barycentricSpringDraw = thorpy.make_button('Barycentric-Spring',
                                                    func=drawingCanvas.draw_graph,
                                                    params={'g':g,
                                                            'drawType':'barycentric-spring',
                                                            'menu': cls})
        barycentricConvexHull = thorpy.make_button('Barycenter-Convex Hull', 
                                                    func=drawingCanvas.draw_graph,
                                                    params={'g':g,
                                                            'drawType':'barycentricHull',
                                                            'menu': cls})
        clearButton = thorpy.make_button('Clear',
                                        func=drawingCanvas.clear)

        quitButton = thorpy.make_button('Quit', func=thorpy.functions.quit_func)
        cls.elements = [title_element, cls.nodeCount, cls.probability, randomDraw, springDraw, barycentricDraw, barycentricSpringDraw, \
                        barycentricConvexHull, clearButton, quitButton]
        cls.box = thorpy.Box(elements=cls.elements)
        cls.box.fit_children(margins=(30,30))
        cls.itemMenu = thorpy.Menu(cls.box)
        for element in cls.itemMenu.get_population():
            element.surface = cls.display

        cls.box.set_main_color(grey)
        cls.box.set_topleft(topleft)
        cls.box.set_size(size)

class Canvas:

    def __init__(cls, display, topleft=(200,0), width=440, height=480):
        cls.display = display
        cls.topleft = topleft
        cls.width = width
        cls.height = height
        cls.clear()

    def clear(cls):
        pygame.draw.rect(cls.display, white, (cls.topleft, (cls.width, cls.height)))
        pygame.display.update()

    def draw_graph(cls, g, drawType, menu):
        try:
            nodeCount = int(menu.nodeCount.get_value())
        except ValueError:
            print('invalid node count')
            return
        
        try:
            probability = float(menu.probability.get_value())
            if probability >= 1:
                print('probability must be > 0 and < 1')
                return
        except ValueError:
            print('invalid probability')
            return
        g = Graph(erdos_renyi=True, n=nodeCount, p=probability)
        x1 = 205
        y1 = 5
        x2 = 635
        y2 = 475
        if drawType == 'rand':
            coordinates = algo.randomDraw(g, x1, y1, x2, y2)
        if drawType == 'spring':
            coordinates = algo.spring(g, x1, y1, x2, y2, cls)
        if drawType == 'barycentric':
            coordinates = algo.barycenterDraw(g, x1, y1, x2, y2, cls)
        if drawType == 'barycentric-spring':
            coordinates = algo.barycenterDraw(g, x1, y1, x2, y2, cls)
            coordinates = algo.spring(g, x1, y1, x2, y2, cls, coordinates)
        if drawType == 'barycentricHull':
            coordinates = algo.barycenterDraw(g, x1, y1, x2, y2, cls, hull=True)

        cls.display_graph(g, coordinates)

    def display_graph(cls, g, coordinates):
        cls.clear()
        for node in g.graph_dict:
            for edge in g.graph_dict[node]:
                pygame.gfxdraw.line(cls.display,
                                    coordinates[node][0], coordinates[node][1],
                                    coordinates[edge][0], coordinates[edge][1],
                                    (0,0,0))


        for node in coordinates:
            pygame.gfxdraw.filled_circle(cls.display,
                                        coordinates[node][0], coordinates[node][1],
                                        5, red)
            pygame.gfxdraw.aacircle(cls.display,
                                    coordinates[node][0], coordinates[node][1],
                                    5, red)
        pygame.display.update()
