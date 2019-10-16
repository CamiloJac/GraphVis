import math
import random

class Graph(object):

    #adj list
    graph_dict={}

    def __init__(self, fileName=None, graph_dict=False):
        ''' If there is a text file 
        passed in... parse it and build graph'''
        if fileName:
            file = open(fileName, 'r')
            nodeCount = int(file.readline())
            for c in range(nodeCount):
                currEdges = file.readline()
                currEdges = currEdges.split()
                for currEdge in currEdges:
                    self.addEdge(int(c), int(currEdge))
            file.close()

        '''We can take in a graph, if we do then
        just assign our graph dict to that one'''
        if graph_dict:
            self.graph_dict = graph_dict
        
    def addEdge(self, nodeFrom, nodeTo):
        if nodeFrom not in self.graph_dict:
            self.graph_dict[nodeFrom] = [nodeTo]
        else:
            self.graph_dict[nodeFrom].append(nodeTo)