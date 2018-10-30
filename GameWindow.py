import pyglet
import pymunk
from InputHandler import PlayerControl

DEBUG = True


# Class to track our game window and environment
class GameWindow(pyglet.window.Window):

    UpdateList = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.foreground_batch = pyglet.graphics.Batch()
        self.background_batch = pyglet.graphics.Batch()
        self.debug_batch = pyglet.graphics.Batch()
        self.player_control = PlayerControl(self)
        self.space = pymunk.Space()
        self.space.damping = 0.1    # Effectively drag/friction for space... stupid but makes control feel nicer.

        if DEBUG:
            self.debug_draw_options = pymunk.pyglet_util.DrawOptions()
            self.debug_draw_options.flags = pymunk.SpaceDebugDrawOptions.DRAW_SHAPES
            self.space.debug_draw(self.debug_draw_options)



    def on_draw(self):
        self.clear()
        self.background_batch.draw()
        if DEBUG:
            self.space.debug_draw(self.debug_draw_options)
        self.foreground_batch.draw()

    def register_for_update(self, game_object):
        if game_object not in self.UpdateList:
            self.UpdateList.append(game_object)
        else:
            print("Warning: Tried to register " + str(game_object) + " for update with GameWindow twice.")

    def remove_for_update(self, game_object):
        self.UpdateList.remove(game_object)

    # Main update function that serves as the game's main loop.
    def master_update(self, dt):
        # Advance our physics simulation.
        self.space.step(dt)

        for game_object in self.UpdateList:
            game_object.update(dt)

        self.player_control.update_keys()
