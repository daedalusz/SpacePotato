import pyglet
import pymunk

# Any Physical Object in the Game
class GameObject(pyglet.sprite.Sprite):

    def __init__(self, space=pymunk.Space ,*args, **kwargs):
        super().__init__(*args, **kwargs)

        # pymunk Physics
        self.body = pymunk.Body(moment=0,mass=0)
        self.body.position = (100, 100)
        self.shape = pymunk.shapes.Circle(body=self.body, radius=100)
        self.shape.mass = 100

        # TODO - Add a default shape?


    # Update state of this item. By default we just move our position based on our velocity
    def update(self, window, dt):
        # Update Sprite Position based on physics body location.
        print(self.body.position)
        self.x = self.body.position.x
        self.y = self.body.position.y


    def add_to_space(self, space):
        space.add(self.body)
        space.add(self.shape)


# Class to track player's ship and stats.
class PlayerShip(GameObject):
    score = 0
    name = ""
    acceleration = 500
    dampers = 5       # Controls inertial damping effectiveness.
    thrust = {'UP': False, 'DOWN': False, 'LEFT': False, 'RIGHT': False}    # directional thrust for GFX and damping

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.shape = pymunk.shapes.Circle(body=self.body,radius=100)
        self.shape.mass = 10
        self.shape.fricton = 1  # This only affects collisions, not general movement.

        if 'img' in kwargs:
            self.img = kwargs['img']

        if 'name' in kwargs:
            self.name = kwargs['name']

    def update(self, window, dt):
        super().update(window, dt)


