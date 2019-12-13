import pygame
import thorpy
import DrawingAlgorithms as algo
from Graph import Graph
import time

WHITE = 255, 255, 255
RED = 195, 75, 75
GREY = 150, 150, 150
YELLOW = 255, 255, 0
BLACK = 0, 0, 0


class Menu:

    def __init__(self, display, topleft, size, canvasSize, drawingCanvas):
        self.display = display
        self.topleft = topleft
        self.size = size
        self.drawingCanvas = drawingCanvas
        self.title_element = thorpy.make_text('Graph Visualizer', 20, YELLOW)
        self.nodeCount = thorpy.Inserter(name="# of Nodes: ")
        self.probability = thorpy.Inserter(name="Probability: ")
        self.randomDraw = thorpy.make_button('Random Draw',
                                             func=drawingCanvas.draw_graph,
                                             params={'drawType': 'rand',
                                                     'menu': self})
        self.springDraw = thorpy.make_button('Spring Draw',
                                             func=drawingCanvas.draw_graph,
                                             params={'drawType': 'spring',
                                                     'menu': self})
        self.barycentricDraw = thorpy.make_button('Barycenter-Draw',
                                                  func=drawingCanvas.draw_graph,
                                                  params={'drawType': 'barycentric',
                                                          'menu': self})
        self.barycentricSpringDraw = thorpy.make_button('Barycentric-Spring',
                                                        func=drawingCanvas.draw_graph,
                                                        params={'drawType': 'barycentric-spring',
                                                                'menu': self})
        self.barycentricConvexHull = thorpy.make_button('Barycenter-Convex Hull',
                                                        func=drawingCanvas.draw_graph,
                                                        params={'drawType': 'barycentricHull',
                                                                'menu': self})
        self.fileName = thorpy.Inserter(name="FileName: ")
        self.saveImageButton = thorpy.make_button("Save Graph",
                                            func=drawingCanvas.draw_graph,
                                            params={'drawType': 'image',
                                                    'menu': self})
        self.clearButton = thorpy.make_button(
            'Clear', func=drawingCanvas.clear)
        self.quitButton = thorpy.make_button(
            'Quit', func=thorpy.functions.quit_func)
        self.elements = [self.title_element, self.nodeCount, self.probability, self.randomDraw,
                         self.springDraw, self.barycentricDraw, self.barycentricSpringDraw,
                         self.barycentricConvexHull, self.fileName, self.saveImageButton, self.clearButton, self.quitButton]
        self.box = thorpy.Box(elements=self.elements)
        self.box.fit_children(margins=(30, 30))
        self.itemMenu = thorpy.Menu(self.box)
        self.resize(size[0], size[1], canvasSize[0], canvasSize[1])

    def resize(self, width, height, cWidth, cHeight):
        self.box.set_topleft(self.topleft)
        self.size = (width, height)
        self.box.set_size(self.size)
        self.box.set_main_color(GREY)
        for element in self.itemMenu.get_population():
            element.surface = self.display

        self.drawingCanvas.width = cWidth
        self.drawingCanvas.height = cHeight
        self.drawingCanvas.clear()


class Canvas:
    surfaces = {}


    def __init__(self, display, topleft=(200, 0), width=440, height=480):
        self.display = display
        self.topleft = topleft
        self.width = width
        self.height = height
        self.clear()

    def clear(self):
        self.display.fill(WHITE, (self.topleft, (self.width, self.height)))
        #pygame.draw.rect(self.display, WHITE, (self.topleft, (self.width, self.height)))
        pygame.display.update()

    def display_loading(self):
        font = pygame.font.Font(pygame.font.get_default_font(), 12)
        text = font.render('Loading graph...', True, BLACK)
        self.display.blit(text, (self.width/2, self.height/2))
        pygame.display.flip()

    def save_graph(self, fileName):
        pygame.image.save(self.surfaces[list(self.surfaces.keys())[-1]], fileName)

    def draw_graph(self, drawType, menu):
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
        x1 = self.topleft[0] + 5
        y1 = self.topleft[1] + 5
        x2 = self.width - 5
        y2 = self.height - 5
        if drawType == 'rand':
            self.surfaces.clear()
            coordinates = algo.randomDraw(g, x1, y1, x2, y2, self, self.surfaces)
        if drawType == 'spring':
            self.surfaces.clear()
            coordinates = algo.spring(g, x1, y1, x2, y2, self, self.surfaces)
        if drawType == 'barycentric':
            self.surfaces.clear()
            coordinates = algo.barycenterDraw(
                g, x1, y1, x2, y2, self, self.surfaces)
        if drawType == 'barycentric-spring':
            self.surfaces.clear()
            coordinates = algo.barycenterDraw(
                g, x1, y1, x2, y2, self, self.surfaces)
            coordinates = algo.spring(
                g, x1, y1, x2, y2, self, self.surfaces, coordinates)
        if drawType == 'barycentricHull':
            self.surfaces.clear()
            coordinates = algo.barycenterDraw(
                g, x1, y1, x2, y2, self, self.surfaces, hull=True)
        if drawType == 'image':
            self.save_graph(menu.fileName.get_value())

        self.display_surfaces()

    def display_surfaces(self):
        for surface in self.surfaces:
            self.display.blit(self.surfaces[surface], (0, 0))
            pygame.display.flip()
            time.sleep(.0125)

    def get_next_surface(self, g, coordinates):
        surface = self.display.copy()
        surface.fill(WHITE, (self.topleft, (self.width, self.height)))
        for node in g.graph_dict:
            for edge in g.graph_dict[node]:
                pygame.gfxdraw.line(surface,
                                    coordinates[node][0], coordinates[node][1],
                                    coordinates[edge][0], coordinates[edge][1],
                                    (0, 0, 0))

        for node in coordinates:
            pygame.gfxdraw.filled_circle(surface,
                                         coordinates[node][0], coordinates[node][1],
                                         5, RED)
            pygame.gfxdraw.aacircle(surface,
                                    coordinates[node][0], coordinates[node][1],
                                    5, RED)
        return surface
