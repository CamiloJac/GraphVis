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
    screen = pygame.display.set_mode(display_size, HWSURFACE|DOUBLEBUF|RESIZABLE)

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
        pygame.event.pump()
        event=pygame.event.wait()
        if event.type == QUIT:
            playing_game = False
            pygame.display.quit()
            break
        elif event.type == VIDEORESIZE:
            myMenu.display = pygame.display.set_mode(event.dict['size'], HWSURFACE|DOUBLEBUF|RESIZABLE) 
            myMenu.resize(200, event.dict['h'], event.dict['w'], event.dict['h'])
            myMenu.itemMenu.blit_and_update() 
            
        pygame.display.update()  
        clock.tick(60)
        myMenu.itemMenu.react(event)

if __name__ == "__main__":
    main()