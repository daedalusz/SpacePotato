import pyglet
import pymunk
import time
from GameWindow import GameWindow

# Any Physical Object in the Game
# Includes both a sprite for display and a body for physics interactions.
class GameObject(pyglet.sprite.Sprite):

    def __init__(self, mass=10, *args, **kwargs):

        self.window = kwargs.pop('window',None)
        self.space = self.window.space

        super().__init__(*args, **kwargs)

        # pymunk Physics
        self.body = pymunk.Body(moment=0,mass=0)
        self.body.position = (100, 100)
        self.mass = mass
        self.update_shape()
        self.x = 0
        self.y = 0
        self.offsetx = 0
        self.offsety = 0

    # Update x/y for sprite drawing. NOTE: This is part of the rendering loop
    def update(self, dt):
        # Update Sprite Position based on physics body location.

        self.x = self.body.position.x - self.offsetx
        self.y = self.body.position.y - self.offsety

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

    def remove(self):
        print("Removed " + str(self))
        self.space.remove(self.shape)
        self.space.remove(self.body)
        self.window.remove_for_update(self)
        #self.batch = None



# TODO - Make a 'Ship' class that players an enemies can be subclassed from?
# Class to track player's ship and stats.
class PlayerShip(GameObject):
    score = 0
    name = ""
    acceleration = 500
    dampers = 5       # Controls inertial damping effectiveness.
    thrust = {'UP': False, 'DOWN': False, 'LEFT': False, 'RIGHT': False}    # directional thrust for GFX and damping
    fire_cooldown = 0

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        # TODO - Make better shapes for collision detection
        self.shape.fricton = 1  # This only affects collisions, not general movement.
        self.shape.color = (0, 255, 0, 100)

        if 'img' in kwargs:
            self.img = kwargs['img']

        if 'name' in kwargs:
            self.name = kwargs['name']

    def update(self, dt):
        super().update(dt)

    # TODO -- Create a 'Weapon' class that can be equipped by ships.
    def fire(self):
        print("Fire Space:" + str(self.space))
        bullet = Bullet(parent=self, window=self.window)
        bullet.batch = self.window.foreground_batch
        self.window.register_for_update(bullet)
        bullet.on_launch()


# Generic Projectile Class
class Projectile(GameObject):
    damage = 1
    impulse = (0, 500)  # Power the projectile is launched with
    thrust = (0, 0)  # Thrust the projectile will produce
    lifetime = 2   # How long should the projectile exist?
    createTime = 0    # Time the projectile was created

    def __init__(self, *args, **kwargs):

        if 'parent' in kwargs:
            self.parent = kwargs.pop('parent', None)

        super().__init__(*args, **kwargs)

    # Called when the projectile is fired.
    def on_launch(self):
        print("Fired!")
        self.createTime = time.time()

    def update(self, dt):
        super().update(dt)
        if (self.createTime + self.lifetime) <= time.time():
            self.remove()


# A Basic Bullet
class Bullet(Projectile):
    damage = 10
    impulse = (0, 100)
    thrust = (0, 100)
    parent = GameObject

    def __init__(self, *args, **kwargs):
        super().__init__(img=pyglet.resource.pyglet.resource.image("bullet.png"), *args, **kwargs)
        self.change_scale(0.2)

    def on_launch(self):
        super().on_launch()
        self.body.position = self.parent.body.position + (0, 10)  # TODO - This should vary more.
        self.body.angle = self.parent.body.angle    # Inherit parent object's angle
        self.body.velocity = self.body.velocity     # Inherit parent object's velocity
        self.body.apply_impulse_at_local_point(self.impulse, (0, 0))

    def update(self, dt):
        super().update(dt)
        self.body.apply_impulse_at_local_point(self.thrust, (0, 0))




