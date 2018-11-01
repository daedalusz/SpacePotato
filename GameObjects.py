import pyglet
import pymunk
import math
import time
from GameWindow import GameWindow
from Collisions import CollisionManager as cm


# Any Physical Object in the Game
# Includes both a sprite for display and a body for physics interactions.
class GameObject(pyglet.sprite.Sprite):

    mass = 10
    moment = 0


    def __init__(self, *args, **kwargs):
        self.window = kwargs.pop('window',None)
        self.space = self.window.space
        img = kwargs['img']            # Adjust the image anchor to the centre of the image. MUST be done here.
        img.anchor_x = img.width // 2
        img.anchor_y = img.height // 2

        if 'mass' in kwargs:
            self.mass = kwargs.pop('mass', None)

        if 'moment' in kwargs:
            self.moment = kwargs.pop('moment', None)

        super().__init__(*args, **kwargs)

        # pymunk Physics
        self.body = pymunk.Body(moment=0, mass=0)
        self.update_shape()
        # Sprite Stuff
        self.offsetx = 0
        self.offsety = 0
        self.batch = self.window.foreground_batch
        self.window.register_for_update(self)

    # Update x/y for sprite drawing. NOTE: This is part of the rendering loop
    def update(self, dt):
        # Update Sprite Position based on physics body location.
        self.rotation = math.degrees(-(self.body.angle))
        self.x = self.body.position.x
        self.y = self.body.position.y

    def add_to_space(self):
        if self.body not in self.space.bodies:
            self.space.add(self.body)

        if self.shape not in self.space.bodies:
            self.space.add(self.shape)

    # Update the size of our shape and relative location of the sprite to render
    def update_shape(self):

        if self.height < self.width:
            radius = self.height // 2
        else:
            radius = self.width // 2

        # TODO - I think this should use the shape.copy() function to preserve info
        new_shape = pymunk.shapes.Circle(body=self.body, radius=radius)
        new_shape.color = (255, 0, 0, 100)
        new_shape.mass = self.mass

        if hasattr(self, 'shape'):
            new_shape.color = self.shape.color
            new_shape.collision_type = self.shape.collision_type
            self.space.remove(self.shape)  # NOTE: You MUST remove the shape from the space first or it will fail!
            self.body.shapes.remove(self.shape)

        self.shape = new_shape
        self.add_to_space()
        self.space.reindex_shapes_for_body(self.body)

    def change_scale(self, scale):
        self.scale = scale
        self.update_shape()

    def remove(self):
        self.space.remove(self.shape)
        self.space.remove(self.body)
        self.window.remove_for_update(self)
        self.batch = None

# Generic Ship
class Ship(GameObject):

    acceleration = 500
    dampers = 5  # Controls inertial damping effectiveness.
    thrust = {'UP': False, 'DOWN': False, 'LEFT': False, 'RIGHT': False}  # directional thrust for GFX and damping
    fire_cooldown = 1000
    fire_cooldown_time = 0
    hp = 1000

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        # TODO - Make better shapes for collision detection
        self.shape.fricton = 1  # This only affects collisions, not general movement.
        self.shape.color = (0, 255, 0, 100)
        self.shape.collision_type = cm.ENEMY

        if 'img' in kwargs:
            self.img = kwargs['img']

        if 'name' in kwargs:
            self.name = kwargs['name']

    def update(self, dt):
        super().update(dt)

    # TODO -- Create a 'Weapon' class that can be equipped by ships.
    def fire(self):
        if time.time() >= self.fire_cooldown_time:
            bullet = Bullet(parent=self, window=self.window)
            bullet.on_launch()
            self.fire_cooldown_time = time.time() + self.fire_cooldown

    def add_to_space(self):

        if self.body not in self.space.bodies:
            self.space.add(self.body)

        if self.shape not in self.space.bodies:
            self.space.add(self.shape)

    def takeDamage(self, dmg, attacker):
        self.hp -= dmg
        print(str(self) + " took " + str(dmg) + "damage.")

        if self.hp <= 0:
            self.remove()


# TODO - Make a 'Ship' class that players an enemies can be subclassed from?
# Class to track player's ship and stats.
class PlayerShip(Ship):
    score = 0
    name = ""
    acceleration = 500
    dampers = 5       # Controls inertial damping effectiveness.
    thrust = {'UP': False, 'DOWN': False, 'LEFT': False, 'RIGHT': False}    # directional thrust for GFX and damping
    fire_cooldown = 0.1


    def __init__(self, *args, **kwargs):
        self.mass = 10
        self.moment = pymunk.inf
        super().__init__(*args, **kwargs)

        # TODO - Make better shapes for collision detection
        self.shape.fricton = 1  # This only affects collisions, not general movement.
        self.shape.color = (0, 255, 0, 100)
        self.shape.collision_type = cm.PLAYER

        if 'img' in kwargs:
            self.img = kwargs['img']

        if 'name' in kwargs:
            self.name = kwargs['name']

    def update(self, dt):
        rel_x = self.window.mouse_x - self.x
        rel_y = self.window.mouse_y - self.y
        ang = math.atan2(rel_y, rel_x)
        self.body.angle = ang
        super().update(dt)
        self.body.velocity *= 0.9


    # TODO -- Create a 'Weapon' class that can be equipped by ships.
    def fire(self):
        if time.time() >= self.fire_cooldown_time:
            bullet = Bullet(parent=self, window=self.window)
            bullet.on_launch()
            self.fire_cooldown_time = time.time() + self.fire_cooldown

    def touchEnemy(self, enemy, ke):
        print("BOOP! for " + str(ke))

# Generic Projectile Class
class Projectile(GameObject):
    damage = 10
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
        self.createTime = time.time()

    def update(self, dt):
        super().update(dt)
        if (self.createTime + self.lifetime) <= time.time():
            self.remove()


# A Basic Bullet
class Bullet(Projectile):
    damage = 100
    impulse = (9000, 0)
    thrust = (0, 0)
    parent = GameObject

    def __init__(self, *args, **kwargs):
        super().__init__(img=pyglet.resource.pyglet.resource.image("bullet.png"), *args, **kwargs)
        self.change_scale(0.2)

    def on_launch(self):
        super().on_launch()
        self.shape.collision_type = cm.PLAYER_WEAP
        self.body.position = self.parent.body.local_to_world((10, 0))  # TODO - This should vary more.
        self.body.angle = self.parent.body.angle    # Inherit parent object's angle
        self.body.velocity = self.body.velocity     # Inherit parent object's velocity
        self.body.apply_impulse_at_local_point(self.impulse, (0, 0))

    def update(self, dt):
        super().update(dt)
        self.body.apply_impulse_at_local_point(self.thrust, (0, 0))

    def touchEnemy(self, enemy, ke):
        self.remove()


