import os
import math
import time
import pyglet
from pyglet.gl import *

from lepton import Particle, ParticleGroup, default_system
from lepton.renderer import BillboardRenderer
from lepton.texturizer import SpriteTexturizer
from lepton.emitter import StaticEmitter
from lepton.controller import Gravity, Lifetime, Movement, Fader, ColorBlender, Growth

""" Special Effects functions are located here.
NOTE: The original code for the explosions was taken from the Lepton examples. 
https://github.com/lordmauve/lepton
"""


class Effects:

    emitters = []
    groups = []

    def __init__(self, window):
        print("Initialising Effects...")

        self.window = window
        self.particle1_tex = pyglet.resource.image("particle1.png").get_texture()
        self.particle1_tex = pyglet.resource.image("particle2.png").get_texture()
        self.particle1_tex = pyglet.resource.image("particle3.png").get_texture()
        self.point1_tex = pyglet.resource.image("point1.png").get_texture()
        self.smoke1_tex = pyglet.resource.image("smoke1.png").get_texture()

    def emit_sparks(self, pos, count):
        sparks = ParticleGroup(
            controllers=[
                Lifetime(1),
                Movement(damping=0.93),
                Fader(fade_out_start=0.75, fade_out_end=1.0),
            ],
            renderer=BillboardRenderer(SpriteTexturizer(self.particle1_tex.id)))

        spark_emitter = StaticEmitter(
            template=Particle(
                position=(pos[0], pos[1], 0),
                color=(1, 1, 1)),
            deviation=Particle(
                position=(1, 1, 0),
                velocity=(100, 100, 0),
                age=1.5),
            size=[(6, 6, 0), (7, 7, 0), (12, 12, 0)])
        spark_emitter.emit(count, sparks)

    def explosion(self, pos, magnitude):

        sparks = ParticleGroup(
          controllers=[
              Lifetime(3),
              Movement(damping=0.93),
              Fader(fade_out_start=0.75, fade_out_end=3.0),
          ],
          renderer=BillboardRenderer(SpriteTexturizer(self.particle1_tex.id)))

        spark_emitter = StaticEmitter(
          template=Particle(
              position=(pos[0], pos[1], 0),
              color=(1, 1, 1)),
          deviation=Particle(
              position=(1, 1, 0),
              velocity=(300, 300, 0),
              age=1.5),
          size=[(3, 3, 0), (4, 4, 0), (5, 5, 0), (5, 5, 0), (6, 6, 0), (7, 7, 0)])
        spark_emitter.emit(magnitude, sparks)

        fire = ParticleGroup(
          controllers=[
              Lifetime(2),
              Movement(damping=0.95),
              Growth(60),
              Fader(fade_in_start=0, start_alpha=0, fade_in_end=0.5, max_alpha=0.6,
                    fade_out_start=1.0, fade_out_end=2.0)
          ],
          renderer=BillboardRenderer(SpriteTexturizer(self.smoke1_tex.id)))

        fire_emitter = StaticEmitter(
          template=Particle(
              position=(pos[0], pos[1], 0),
              size=(50, 50, 0)),
          deviation=Particle(
              position=(0.5, 0.5, 0),
              velocity=(70, 70, 0),
              size=(20, 20, 0),
              up=(0, 0, math.pi * 2),
              rotation=(0, 0, math.pi * 0.06),
              age=2, ),
          color=[(0.5, 0, 0), (0.5, 0.5, 0.5), (0.4, 0.1, 0.1), (0.85, 0.3, 0)],
        )
        fire_emitter.emit(400, fire)

