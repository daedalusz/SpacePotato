import pyglet
import pymunk
from InputHandler import PlayerControl
from GameWindow import GameWindow
from GameObjects import PlayerShip
global GameWindow # TODO - Get rid of this horrible global variable. It may not be needed at all anyway.
import pymunk.pyglet_util

# Turn on debug shape rendering for pymunk
DEBUG = True



# Initialise Things #
def init():
    print("Initialising Potatoes...")
    window = GameWindow(width=1024, height=768)

    # Load a bunch of resources

    pyglet.resource.path = ["./resources/images", "./resources/sounds"]
    pyglet.resource.reindex()

    # Create Player Object.
    window.player = PlayerShip(img=pyglet.resource.image("potato.png"), window=window)
    window.player.change_scale(0.2)
    window.player.batch = window.foreground_batch
    window.register_for_update(window.player)

    # Kick off the Game's control loop.
    pyglet.clock.schedule_interval(window.master_update, 1 / 120.0)

    return window


GameWindow = init()
pyglet.app.run()



