import sys, pygame, time, random, thorpy, Graph, UI

def game_loop(itemMenu, itemBox, canvas):
    gameExit = False

    while not gameExit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()  

            itemMenu.react(event)
        pygame.display.update()
        itemBox.blit()
        itemBox.update()
        itemMenu.play()

def main():
    pygame.init()

    display_size = display_width, display_height = 640, 480

    
    #initialize screen display
    screen = pygame.display.set_mode(display_size)

    #window title
    pygame.display.set_caption('Graph Visualizer')

    #initialize empty graph
    myGraph = Graph.Graph(fileName='graphs.txt')
    canvas = UI.canvas(screen)
    menu = UI.menu(screen, (0,0), (200, 480), myGraph, canvas)
    game_loop(menu.itemMenu, menu.box, canvas)

if __name__ == "__main__":
    main()