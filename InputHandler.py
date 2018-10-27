from pyglet.window import Window, key

class PlayerControl:

    def __init__(self, window, **kwargs):
        self.window = window
        self.keys = key.KeyStateHandler()
        window.push_handlers(self.keys)

    def update_keys(self):
        player_ship = self.window.player

        if self.keys[key.LEFT]:
            player_ship.velocity['x'] += -player_ship.acceleration

        if self.keys[key.RIGHT]:
            player_ship.velocity['x'] += +player_ship.acceleration

        if self.keys[key.UP]:
            player_ship.velocity['y'] += +player_ship.acceleration

        if self.keys[key.DOWN]:
            player_ship.velocity['y'] += -player_ship.acceleration