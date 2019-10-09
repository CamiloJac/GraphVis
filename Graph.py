import pygame, math

red = 195, 75, 75
white = 255, 255, 255

class Graph(object):
    graph_dict={}

    def __init__(self, graph_dict=False):
        if graph_dict:
            self.graph_dict = graph_dict
        
    def setNodes(self, nodes):
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
        pygame.draw.rect(screen, white, (topleft, (440, 480)))
        offset = 0
        for node in self.graph_dict:
            pygame.draw.circle(screen, red, (startX + offset, startY + offset), 15)
            offset += 35
            pygame.display.update()