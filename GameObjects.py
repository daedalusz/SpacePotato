import pyglet

# Any Physical Object in the Game
class GameObject(pyglet.sprite.Sprite):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.velocity = {'x': 0, 'y': 0}
        self.friction = 3

        #TODO - Add some Physics/collision detection stuff from Pymunk

    # Update state of this item. By default we just move our position based on our velocity
    def update(self, window, dt):

        self.x += self.velocity['x'] * dt
        self.y += self.velocity['y'] * dt

        self.velocity['x'] -= (self.velocity['x']*(self.friction))*dt
        self.velocity['y'] -= (self.velocity['y']*(self.friction))*dt


# Class to track player's ship and stats.
class PlayerShip(GameObject):
    score = 0
    name = ""
    acceleration = 100

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.x = 100
        self.y = 100

        if 'img' in kwargs:
            self.img = kwargs['img']

        if 'name' in kwargs:
            self.name = kwargs['name']

    def update(self, window, dt):
        super().update(window, dt)

        window_size = window.get_size()

        # Limit X Motion for Player
        if (self.x + self.width) > window_size[0]:
            self.x = window_size[0]-self.width
            self.velocity['x'] = 0
        elif self.x < 0:
            self.x = 0
            self.velocity['x'] = 0

        print(self.y)
        # Limit Y Motion for Player
        if (self.y + self.height) > window_size[1]:
            self.y = window_size[1] - self.height
            self.velocity['y'] = 0
        elif self.y < 0:
            self.y = 0
            self.velocity['y'] = 0
