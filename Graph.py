import pygame, math, random

red = 195, 75, 75
white = 255, 255, 255

    

class Graph(object):

    #adj list
    graph_dict={}

    def __init__(self, fileName=None, graph_dict=False):

        ''' If there is a text file passed in... parse it 
        and build graph'''
        if fileName:
            file = open(fileName, 'r')
            nodeCount = int(file.readline())
            for c in range(nodeCount):
                currEdges = file.readline()
                currEdges = currEdges.split()
                for currEdge in currEdges:
                    self.addEdge(int(c), int(currEdge))


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
            self.graph_dict[nodeFrom] = [nodeTo]
        else:
            self.graph_dict[nodeFrom].append(nodeTo)   

    def showEdges(self):
        for node in self.graph_dict:
            for neighbor in self.graph_dict[node]:
                print("(",node,", ", neighbor, ")")