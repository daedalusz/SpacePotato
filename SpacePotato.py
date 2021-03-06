import pyglet

import pymunk
from InputHandler import PlayerControl
from GameWindow import GameWindow
from GameObjects import PlayerShip, Ship
global GameWindow # TODO - Get rid of this horrible global variable. It may not be needed at all anyway.
import pymunk.pyglet_util
from Collisions import CollisionManager
from Interface import HUD
from Effects import Effects

# Turn on debug shape rendering for pymunk
DEBUG = True


# Initialise Things #
def init():
    print("Initialising Potatoes...")
    window = GameWindow(width=1024, height=768)

    # Load a bunch of resources

    pyglet.resource.path = ["./resources/images", "./resources/sounds"]
    pyglet.resource.reindex()

    # Load Effects System
    window.effects = Effects(window)


    # Create Player Object.
    window.player = PlayerShip(img=pyglet.resource.image("potato.png"), window=window)
    window.player.change_scale(0.2)
    window.player.body.position = (100, 200)

    # Initialise HUD
    hud = HUD(window.player, window)


    ship_image = pyglet.resource.image("potato-green.png")
    ships = [Ship(img=ship_image, window=window), Ship(img=ship_image, window=window), Ship(img=ship_image, window=window)]

    ship_x = 500
    ship_y = 100
    for ship in ships:
        ship.body.position = (ship_x, ship_y)
        ship_x += 200
        ship.body.angle = 3.14159
        ship.body.angular_velocity = 10
        ship.change_scale(0.5)
        window.space.reindex_shapes_for_body(ship.body)

    # Kick off the Game's control loop.
    pyglet.clock.schedule_interval(window.master_update, 1 / 120.0)

    # Player Boundaries
    boundaries = [pymunk.Segment(window.space.static_body, (0, 0), (0, 768), 0.0),
                  pymunk.Segment(window.space.static_body, (1024, 0), (1024, 768), 0),
                  pymunk.Segment(window.space.static_body, (0, 0), (1024, 0), 0),
                  pymunk.Segment(window.space.static_body, (0, 768), (1024, 768), 0)]

    for l in boundaries:
        l.friction = 0.1
        l.collision_type = CollisionManager.WORLD
    window.space.add(boundaries)

    cm = CollisionManager(window)

    for shape in window.player.body.shapes:
        print(shape.collision_type)

    # TODO - Build something that loads levels.
    # Background
    background = pyglet.resource.image("background1.png")
    background_sprite = pyglet.sprite.Sprite(img=background)
    background_sprite.batch = window.background_batch
    background_sprite.x = 0
    background_sprite.y = 0
    window.background = background_sprite

    return window

GameWindow = init()
pyglet.app.run()



