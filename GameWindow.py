import pyglet
import pymunk
from lepton import default_system
from InputHandler import PlayerControl
from pyglet.gl import *

DEBUG = False

CollisionGroups = {
    "world": 1,
    "player": 2,
    "enemy": 3,
    "player_weapon": 4,
    "enemy_weapon": 5,
    "enemy_weapon_hit": 6,
}

# Class to track our game window and environment
class GameWindow(pyglet.window.Window):

    UpdateList = []
    mouse_x = 0
    mouse_y = 0
    mouse_button = 0

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.foreground_batch = pyglet.graphics.Batch()
        self.background_batch = pyglet.graphics.Batch()
        self.hud_batch = pyglet.graphics.Batch()
        self.debug_batch = pyglet.graphics.Batch()
        self.player_control = PlayerControl(self)
        self.space = pymunk.Space()
        self.space.damping = 1.0    # Effectively drag/friction for space... stupid but makes control feel nicer.

        glEnable(GL_BLEND)
        glShadeModel(GL_SMOOTH)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE)
        glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST);
        glDisable(GL_DEPTH_TEST)


        if DEBUG:
            self.debug_draw_options = pymunk.pyglet_util.DrawOptions()
            self.debug_draw_options.flags = pymunk.SpaceDebugDrawOptions.DRAW_SHAPES
            self.space.debug_draw(self.debug_draw_options)

    def on_mouse_motion(self, x, y, dx, dy):
        self.mouse_x = x
        self.mouse_y = y

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        self.mouse_x = x
        self.mouse_y = y

    def on_mouse_press(self, x, y, button, modifiers):
        print("Pressed")
        self.mouse_button = button

    def on_mouse_release(self, x, y, button, modifiers):
        print("Released")
        self.mouse_button = 0

    def on_draw(self):
        self.clear()
        self.background_batch.draw()
        glLoadIdentity()

        if DEBUG:
            self.space.debug_draw(self.debug_draw_options)

        self.foreground_batch.draw()
        self.hud_batch.draw()
        default_system.draw()


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
        # Advance Particle system
        default_system.update(dt)

        for game_object in self.UpdateList:
            game_object.update(dt)

        self.player_control.update_keys()
