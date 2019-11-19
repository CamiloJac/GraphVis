import pygame
from pygame.locals import *
import sys
from Graph import Graph
from UI import Canvas, Menu

def main():
    #initialize pygame instance
    pygame.init()

    #dimensions for pygame window
    display_size = display_width, display_height = 640, 480

    #initialize screen display
    SURFACE = HWACCEL|ASYNCBLIT|HWSURFACE|DOUBLEBUF|RESIZABLE
    screen = pygame.display.set_mode(display_size, SURFACE)

    #window title
    pygame.display.set_caption('Graph Visualizer')

    #initialize empty graph
    #myGraph = Graph(fileName='graphs.txt')

    #canvas instance (where graphs will be drawn)
    myCanvas = Canvas(screen)

    #GUI menu to select what algorithm to display
    myMenu = Menu(screen, (0,0), (200, 480), (640, 480), myCanvas)
    myMenu.itemMenu.blit_and_update()
    myCanvas.clear()

    playing_game=True
    clock = pygame.time.Clock()
    while playing_game:
        for event in pygame.event.get():
            if event.type == QUIT:
                playing_game = False
                pygame.display.quit()
                break
            elif event.type == VIDEORESIZE:
                myMenu.display = pygame.display.set_mode(event.dict['size'], SURFACE) 
                myMenu.resize(200, event.dict['h'], event.dict['w'], event.dict['h'])
                myMenu.itemMenu.blit_and_update() 
                pygame.display.update()

            myMenu.itemMenu.react(event)

        clock.tick(60)

if __name__ == "__main__":
    main()