import pymunk
from GameWindow import GameWindow

# A class to manage our collisions
class CollisionManager:

    WORLD = 1
    PLAYER = 2
    ENEMY = 3
    PLAYER_WEAP = 4
    ENEMY_WEAP = 5


    def __init__(self, window):
        self.window = window
        self.space = window.space

        #Set up Collision Handlers

        h_player_world = self.space.add_collision_handler(self.PLAYER, self.WORLD)
        h_player_world.post_solve = self.collide_player_world   #Using post_solve so we get KE numbers

        h_player_enemy = self.space.add_collision_handler(self.PLAYER, self.ENEMY)
        h_player_enemy.post_solve = self.collide_player_enemy

        h_enemy_world = self.space.add_collision_handler(self.ENEMY, self.WORLD)
        h_enemy_world.begin = self.collide_enemy_world

        h_player_weap_enemy = self.space.add_collision_handler(self.PLAYER_WEAP, self.ENEMY)
        h_player_weap_enemy.post_solve = self.collide_player_weap_enemy


        print("CM Initialised")

    def collide_player_enemy(self, arb, space, data):

        objs = []
        for shape in arb.shapes:
            objs.append(self.get_obj_by_body(shape.body))

        # Collision shapes are provided in order according to how the add_collision_handler is set up.
        # player is always first in our config.
        objs[0].touchEnemy(objs[1], arb.total_ke)

        return True

    def collide_player_weap_enemy(self, arb, space, data):
        print("Weapon Hit")
        objs = []
        for shape in arb.shapes:
            objs.append(self.get_obj_by_body(shape.body))

        objs[0].touchEnemy(objs[1], int(arb.total_ke)) # Projectile
        objs[1].takeDamage(objs[0].damage, objs[0])  # Enemy

        return True

    def collide_player_world(self, arb, space, data):
        print("WORLD HIT")
        return True


    def collide_enemy_world(self, arb, space, data):
        return True


# Get a handle on the GameObject via it's body.
    def get_obj_by_body(self, body):
        # TODO - This seems ugly and inefficient. Make it better.
        for game_object in self.window.UpdateList:
            if game_object.body == body:
                return game_object
