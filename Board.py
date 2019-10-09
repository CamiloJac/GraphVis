import sys, pygame, time, random, thorpy, Graph

pygame.init()

display_size = display_width, display_height = 640, 480
black = 0, 0, 0
grey = 150, 150, 150
white = 255, 255, 255
red = 195, 75, 75
    
#initialize screen display
screen = pygame.display.set_mode(display_size)

pygame.display.set_caption('Graph Visualizer')

clock = pygame.time.Clock()

myGraph = Graph.Graph()

def nodes_func_reaction(event):
    element_value = event.el.get_value()
    print("You Have inserted the following text: ", element_value)
    myGraph.setNodes(int(element_value))

title_element = thorpy.make_text("Graph Visualizer", 20, (255,255,0))

numberOfNodes = thorpy.Inserter(name="Nodes:")
numberOfNodes.scale_to_title()

nodes_reaction = thorpy.Reaction(reacts_to=thorpy.constants.THORPY_EVENT,
                                reac_func=nodes_func_reaction,
                                event_args={"id":thorpy.constants.EVENT_INSERT})



numberOfEdges = thorpy.Inserter(name="Edges:", value="NOT WORKING")
numberOfEdges.scale_to_title()


generate_graph_button = thorpy.make_button("Generate Graph!", 
                                            func=myGraph.draw_graph, 
                                            params={"screen": screen, 
                                            "size": display_size, 
                                            "topleft": (200,0), 
                                            "startX":420,
                                            "startY":240})

#generate_graph_button_reaction = thorpy.Reaction(reacts_to=thorpy.constants.THORPY_EVENT,
#                                                reac_func=myGraph.draw_graph(screen, display_size, (200,0), (220, 240)),
#                                                event_args={"id":thorpy.constants.EVENT_PRESS})



button = thorpy.make_button("Quit", func=thorpy.functions.quit_func)

elements = [title_element, numberOfNodes, numberOfEdges, 
generate_graph_button, button]



box = thorpy.Box(elements=elements)
box.add_reaction(nodes_reaction)
#box.add_reaction(generate_graph_button_reaction)
box.fit_children(margins=(30,30))
#we regroup all elements on a menu, even if we do not launch the menu
menu = thorpy.Menu(box)
#important : set the screen as surface for all elements
for element in menu.get_population():
    element.surface = screen

box.set_main_color((150, 150, 150))
#use the elements normally...
box.set_topleft((0,0))
box.set_size((200, 480))


def game_loop():
    gameExit = False

    while not gameExit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            menu.react(event) #the menu automatically integrate your elements
        pygame.display.update()
        box.blit()
        box.update()
        menu.play()
        

screen.fill(white)
game_loop()