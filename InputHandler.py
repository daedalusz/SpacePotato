from pyglet.window import Window, key
import pyglet

class PlayerControl:

    def __init__(self, window, **kwargs):
        self.window = window
        self.keys = key.KeyStateHandler()
        window.push_handlers(self.keys)

    def update_keys(self):
        player_ship = self.window.player
        impulse = player_ship.acceleration

        player_ship.thrust = {'UP': False, 'DOWN': False, 'LEFT': False, 'RIGHT': False}

        if self.keys[key.LEFT]:
            player_ship.body.apply_impulse_at_local_point((-impulse, 0), (0, 0))
            player_ship.thrust['LEFT'] = True

        if self.keys[key.RIGHT]:
            player_ship.body.apply_impulse_at_local_point((impulse, 0), (0, 0))
            player_ship.thrust['RIGHT'] = True

        if self.keys[key.UP]:
            player_ship.body.apply_impulse_at_local_point((0, impulse), (0, 0))
            player_ship.thrust['UP'] = True

        if self.keys[key.DOWN]:
            player_ship.body.apply_impulse_at_local_point((0, -impulse), (0, 0))
            player_ship.thrust['DOWN'] = True

