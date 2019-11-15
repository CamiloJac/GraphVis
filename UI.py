import pygame
import thorpy
import DrawingAlgorithms as algo

white = 255,255,255
red = 195, 75, 75
grey = 150, 150, 150
yellow = 255, 255, 0

class menu:

    def __init__(self, display, topleft, size, g, drawingCanvas):
        self.g = g
        self.display = display
        title_element = thorpy.make_text('Graph Visualizer', 20, yellow)
        randomDraw = thorpy.make_button('Random Draw',
                                        func=drawingCanvas.draw_graph,
                                        params={'g':g,
                                        'drawType':'rand'})
        springDraw = thorpy.make_button('Spring Draw',
                                        func=drawingCanvas.draw_graph,
                                        params={'g':g,
                                        'drawType':'spring'})
        barycentricDraw = thorpy.make_button('Barycenter-Draw',
                                        func=drawingCanvas.draw_graph,
                                        params={'g':g,
                                        'drawType':'barycentric'})
        barycentricSpringDraw = thorpy.make_button('Barycentric-Spring',
                                                    func=drawingCanvas.draw_graph,
                                                    params={'g':g,
                                                            'drawType':'barycentric-spring'})
        barycentricConvexHull = thorpy.make_button('Barycenter-Convex Hull', 
                                                    func=drawingCanvas.draw_graph,
                                                    params={'g':g,
                                                            'drawType':'barycentricHull'})
        clearButton = thorpy.make_button('Clear',
                                        func=drawingCanvas.clear)

        quitButton = thorpy.make_button('Quit', func=thorpy.functions.quit_func)
        self.elements = [title_element, randomDraw, springDraw, barycentricDraw, barycentricSpringDraw, \
                        barycentricConvexHull, clearButton, quitButton]
        self.box = thorpy.Box(elements=self.elements)
        self.box.fit_children(margins=(30,30))
        self.itemMenu = thorpy.Menu(self.box)
        for element in self.itemMenu.get_population():
            element.surface = self.display

        self.box.set_main_color(grey)
        self.box.set_topleft(topleft)
        self.box.set_size(size)

class canvas:

    def __init__(self, display, topleft=(200,0), width=440, height=480):
        self.display = display
        self.topleft = topleft
        self.width = width
        self.height = height
        self.clear()

    def clear(self):
        pygame.draw.rect(self.display, white, (self.topleft, (self.width, self.height)))
        pygame.display.update()

    def draw_graph(self, g, drawType):
        x1 = 205
        y1 = 5
        x2 = 635
        y2 = 475
        if drawType == 'rand':
            coordinates = algo.randomDraw(g, x1, y1, x2, y2)
        if drawType == 'spring':
            coordinates = algo.spring(g, x1, y1, x2, y2, self)
        if drawType == 'barycentric':
            coordinates = algo.barycenterDraw(g, x1, y1, x2, y2, self)
        if drawType == 'barycentric-spring':
            coordinates = algo.barycenterDraw(g, x1, y1, x2, y2, self)
            coordinates = algo.spring(g, x1, y1, x2, y2, self, coordinates)
        if drawType == 'barycentricHull':
            coordinates = algo.barycenterDraw(g, x1, y1, x2, y2, self, hull=True)

        self.display_graph(g, coordinates)

    def display_graph(self, g, coordinates):
        self.clear()
        for node in g.graph_dict:
            for edge in g.graph_dict[node]:
                pygame.gfxdraw.line(self.display,
                                    coordinates[node][0], coordinates[node][1],
                                    coordinates[edge][0], coordinates[edge][1],
                                    (0,0,0))


        for node in coordinates:
            pygame.gfxdraw.filled_circle(self.display,
                                        coordinates[node][0], coordinates[node][1],
                                        5, red)
            pygame.gfxdraw.aacircle(self.display,
                                    coordinates[node][0], coordinates[node][1],
                                    5, red)
        pygame.display.update()
