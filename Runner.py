import pygame
import sys
from Graph import Graph
from UI import Canvas, Menu

def main():
    #initialize pygame instance
    pygame.init()

    #dimensions for pygame window
    display_size = display_width, display_height = 640, 480

    #initialize screen display
    screen = pygame.display.set_mode(display_size, pygame.VIDEORESIZE)

    #window title
    pygame.display.set_caption('Graph Visualizer')

    #initialize empty graph
    myGraph = Graph(fileName='graphs.txt')

    #canvas instance (where graphs will be drawn)
    myCanvas = Canvas(screen)

    #GUI menu to select what algorithm to display
    myMenu = Menu(screen, (0,0), (200, 480), myGraph, myCanvas)

    #display menu
    myMenu.itemMenu.play()

if __name__ == "__main__":
    main()