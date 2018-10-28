import pyglet
import pymunk
from InputHandler import PlayerControl
from GameObjects import PlayerShip
global GameWindow # TODO - Get rid of this horrible global variable. It may not be needed at all anyway.




# Class to track our game window and environment
class GameWindow(pyglet.window.Window):

    UpdateList = []

    def __init__(self, **kwargs):
        self.foreground_batch = pyglet.graphics.Batch()
        self.background_batch = pyglet.graphics.Batch()
        self.player_control = PlayerControl(self)
        self.space = pymunk.Space()
        self.space.damping = 0.1    # Effectively drag/friction for space... stupid but makes control feel nicer.
        super().__init__(**kwargs)

    def on_draw(self):
        self.clear()
        self.background_batch.draw()
        self.foreground_batch.draw()

    def register_for_update(self, game_object):
        self.UpdateList.append(game_object)

    # Main update function that serves as the game's main loop.
    def master_update(self, dt):

        # Advance our physics simulation.
        self.space.step(dt)

        for game_object in self.UpdateList:
            game_object.update(self, dt)

        self.player_control.update_keys()


# Initialise Things #
def init():
    print("Initialising Potatoes...")
    window = GameWindow(width=1024, height=768)

    # Load a bunch of resources

    pyglet.resource.path = ["./resources/images", "./resources/sounds"]
    pyglet.resource.reindex()

    # Create Player Object.
    window.player = PlayerShip(img=pyglet.resource.image("potato.png"))
    window.player.batch = window.foreground_batch
    window.register_for_update(window.player)
    window.player.add_to_space(window.space)

    # Kick off the Game's control loop.
    pyglet.clock.schedule_interval(window.master_update, 1 / 120.0)

    return window


GameWindow = init()
pyglet.app.run()



