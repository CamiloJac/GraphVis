import pygame, thorpy, DrawingAlgorithms as algo

class menu:
    title_element = None
    elements = []
    box = None
    def __init__(self):
        self.title_element = 'Graph Visualizer'
        randomDraw = thorpy.make_button("Random Draw",
                                        func=drawGraph, 
                                        params={})

        box = thorpy.Box(elements=elements)
    
    def draw_graph_reaction(event):
        canvas.draw_graph(g)


class canvas:
    colors = {'white':(255,255,255)}
    display = None
    width = None
    height = None
    topleft = None
    def __init__(self, display, topleft=(240,0), width=440, height=480):
        self.display = display
        self.topleft = topleft
        self.width = width
        self.height = height
        self.clear()
    
    def clear(self):
        pygame.draw.rect(display, colors['white'], (topleft, (width, height)))
    
    def draw_graph(self, g, drawType):
        coordinates = {}
        if drawType == 'rand':
            algo.randomDraw(g, )