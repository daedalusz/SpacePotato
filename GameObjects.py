import pyglet
import pymunk

# Any Physical Object in the Game
class GameObject(pyglet.sprite.Sprite):

    def __init__(self,space=pymunk.space,mass=10, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # pymunk Physics
        self.body = pymunk.Body(moment=0,mass=0)
        self.body.position = (100, 100)
        self.space = space
        self.mass = mass
        self.update_shape()


        # TODO - Add a default shape?

    # Update x/y for sprite drawing. NOTE: This is part of the rendering loop
    def update(self, window, dt):
        # Update Sprite Position based on physics body location.

        self.x = self.body.position.x - self.offsetx
        self.y = self.body.position.y - self.offsety
        print(self.body.mass)

    def add_to_space(self):
        if self.body not in self.space.bodies:
            self.space.add(self.body)

        if self.shape not in self.space.bodies:
            self.space.add(self.shape)

    # Update the size of our shape and relative location of the sprite to render
    def update_shape(self):

        self.offsetx = self.width // 2
        self.offsety = self.height // 2

        if self.height < self.width:
            radius = self.height // 2
        else:
            radius = self.width // 2

        new_shape = pymunk.shapes.Circle(body=self.body, radius=radius)
        new_shape.mass = self.mass
        new_shape.color = (255, 0, 0, 100)

        if hasattr(self, 'shape'):
            self.space.remove(self.shape)  # NOTE: You MUST remove the shape from the space first or it will fail!
            self.body.shapes.remove(self.shape)

        self.shape = new_shape
        self.add_to_space()

    def change_scale(self, scale):
        print("Resizing to " + str(scale))
        self.scale = scale
        self.update_shape()



# Class to track player's ship and stats.
class PlayerShip(GameObject):
    score = 0
    name = ""
    acceleration = 500
    dampers = 5       # Controls inertial damping effectiveness.
    thrust = {'UP': False, 'DOWN': False, 'LEFT': False, 'RIGHT': False}    # directional thrust for GFX and damping

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        # TODO - Make better shapes for collision detectio
        self.shape.fricton = 1  # This only affects collisions, not general movement.
        self.shape.color = (0, 255, 0, 100)

        if 'img' in kwargs:
            self.img = kwargs['img']

        if 'name' in kwargs:
            self.name = kwargs['name']

    def update(self, window, dt):
        super().update(window, dt)


