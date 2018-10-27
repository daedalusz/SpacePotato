import pyglet

class PlayerShip



""" Initialise ALL THE THINGS """
def init():
    print("Initialising Potatoes...")
    window = pyglet.window.Window(width=1024, height=768)


""" Start Running the main loop"""
def start():
    pyglet.app.run()

init()
start()

