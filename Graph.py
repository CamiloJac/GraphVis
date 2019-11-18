import math
import random

class Graph(object):

    #adj list
    graph_dict={}

    def __init__(self, fileName=None, graph_dict=False, erdos_renyi=False, n=10, p=0.5):
        self.graph_dict.clear()
        if erdos_renyi:
            for node in range(n):
                self.graph_dict[node] = set()
            self.erdos_renyi_generation(p)
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
            self.graph_dict[nodeFrom] = {nodeTo}
        else:
            self.graph_dict[nodeFrom].add(nodeTo)

    def erdos_renyi_generation(self, p):
        for nodeFrom in self.graph_dict:
            for nodeTo in self.graph_dict:
                if nodeFrom != nodeTo:
                    r = random.random()
                    if r <= p:
                        self.addEdge(nodeFrom, nodeTo)
                    else:
                        continue
