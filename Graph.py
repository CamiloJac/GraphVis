import pygame, math, random

red = 195, 75, 75
white = 255, 255, 255

    

class Graph(object):

    #adj list
    graph_dict={}

    def __init__(self, graph_dict=False):
        '''We can take in a graph, if we do then
        just assign our graph dict to that one'''
        if graph_dict:
            self.graph_dict = graph_dict
        
    def setNodes(self, nodes):
        #this is to set nodes, we clear first then set
        self.graph_dict.clear()
        for i in range(nodes):
            self.graph_dict[i] = []
        
    def addEdge(self, nodeFrom, nodeTo):
        if nodeFrom not in self.graph_dict:
            self[nodeFrom] = [nodeTo]
        else:
            self.graph_dict[nodeFrom].append(nodeTo)   

    def showEdges(self):
        for node in self.graph_dict:
            for neighbor in self.graph_dict[node]:
                print("(",node,", ", neighbor, ")")

    def draw_graph(self, screen, size, topleft, startX, startY):
        #first clear the canvas
        pygame.draw.rect(screen, white, (topleft, (440, 480)))

        offset = 0
        for node in self.graph_dict:
            pygame.draw.circle(screen, red, (random.randrange(215,625, 1), random.randrange(15,465, 1)), 15)
            pygame.display.update()