import sys, pygame, time, random, thorpy, Graph

pygame.init()

display_size = display_width, display_height = 640, 480
black = 0, 0, 0
grey = 150, 150, 150
white = 255, 255, 255
red = 195, 75, 75
    
#initialize screen display
screen = pygame.display.set_mode(display_size)

#window title
pygame.display.set_caption('Graph Visualizer')

#clock = pygame.time.Clock()

#initialize empty graph
myGraph = Graph.Graph()

#function that gets called when text is entered into text field
def nodes_func_reaction(event):
    element_value = event.el.get_value()
    print("You Have inserted the following text: ", element_value)
    myGraph.setNodes(int(element_value))

#menu title
title_element = thorpy.make_text("Graph Visualizer", 20, (255,255,0))

#text field
numberOfNodes = thorpy.Inserter(name="Nodes:")
numberOfNodes.scale_to_title()

#how we react to the input for our text field
nodes_reaction = thorpy.Reaction(reacts_to=thorpy.constants.THORPY_EVENT,
                                reac_func=nodes_func_reaction,
                                event_args={"id":thorpy.constants.EVENT_INSERT})



numberOfEdges = thorpy.Inserter(name="Edges:", value="NOT WORKING")
numberOfEdges.scale_to_title()


#button to generate graph
generate_graph_button = thorpy.make_button("Generate Graph!", 
                                            func=myGraph.draw_graph, 
                                            params={"screen": screen, 
                                            "size": display_size, 
                                            "topleft": (200,0), 
                                            "startX":420,
                                            "startY":240})


#quit button
button = thorpy.make_button("Quit", func=thorpy.functions.quit_func)

#elements of menu
elements = [title_element, numberOfNodes, numberOfEdges, 
generate_graph_button, button]

#set our thorpy gui menu up
box = thorpy.Box(elements=elements)

#this is how we want our gui to react when input is entered
box.add_reaction(nodes_reaction)

#margins for nice fitment
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