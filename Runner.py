import pygame
from Graph import Graph
from UI import canvas, menu

def main():
    #initialize pygame instance
    pygame.init()

    #dimensions for pygame window
    display_size = display_width, display_height = 640, 480

    #initialize screen display
    screen = pygame.display.set_mode(display_size)

    #window title
    pygame.display.set_caption('Graph Visualizer')

    #initialize empty graph
    myGraph = Graph(fileName='graphs.txt')

    #canvas instance (where graphs will be drawn)
    myCanvas = canvas(screen)

    #GUI menu to select what algorithm to display
    myMenu = menu(screen, (0,0), (200, 480), myGraph, myCanvas)

    #display menu
    myMenu.itemMenu.play()

if __name__ == "__main__":
    main()