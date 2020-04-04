"""Module containing all unit class and the world class"""

import pymunk
import cfg
import math

class Player:
    """Playe class, should be controlled, explicitly"""

    """Player flap direction is has up component"""
    dir_up = False

    """Player flap direction is has down component"""
    dir_down = False

    """Player flap direction is has left component"""
    dir_left = False

    """Player flap direction is has right component"""
    dir_right = False

    def __init__(self, world, pos):
        """
        Player: add a circle body in the game world
        pos: (float, float)
        world: World
        """
        self.body = pymunk.Body(cfg.PLAYER_MASS, 1000)
        self.body.position = pos
        self.shape = pymunk.Circle(self.body, cfg.PLAYER_RADIUS)
        self.shape.collision_type = ColType.PLAYER
        self.body.velocity_func = self.velocity_func
        world.space.add(self.body, self.shape)
        world.player = self

    def velocity_func(self, body, gravity, damping, dt):
        """velocity_func for player, currently use default pymunk.update_velocity"""
        pymunk.Body.update_velocity(body, gravity, damping, dt)

    def flap(self):
        """Flap wings: add an impulse in a direction, direction must be a tuple with 2 number, does not need to be normalized"""

        # Compute direction to target for the flap
        dir = [self.dir_right - self.dir_left, self.dir_up - self.dir_down]
        # Norm of the direction
        norm = math.sqrt(dir[0]**2 + dir[1]**2)
        # Do not flap if the direction is (0, 0)
        if norm == 0: return
        # Coef to the direction: normalize direction and multiply by PLAYER_FLAP_IMPULSE
        coef = cfg.PLAYER_FLAP_IMPULSE / norm
        self.body.apply_impulse_at_local_point((dir[0]*coef, dir[1]*coef))

class Wall:
    def __init__(self, world, start, end):
        """
        Wall: add a segment body in the physic space
        world: World
        start: (float, float)
        end: (float, float)
        """
        self.body = pymunk.Body(1, 1, pymunk.Body.STATIC)
        self.body.position = 0, 0
        self.shape = pymunk.Segment(self.body, start, end, cfg.WALL_RADIUS)
        world.space.add(self.body, self.shape)

# TODO: on collision must kill the player
class DeadlyWall:
    def __init__(self, world, start, end):
        """
        Wall: add a segment body in the physic space
        world: World
        start: (float, float)
        end: (float, float)
        """
        self.body = pymunk.Body(1, 1, pymunk.Body.STATIC)
        self.body.position = 0, 0
        self.shape = pymunk.Segment(self.body, start, end, cfg.WALL_RADIUS)
        self.shape.collision_type = ColType.DEADLY_WALL
        self.shape.color = cfg.RED
        world.space.add(self.body, self.shape)

class World:
    """Game world, contains physic space and optionally player"""

    def __init__(self):
        """Instantiate space physic and player to None"""
        # Init physic space
        self.space = pymunk.Space()
        # TODO: Temporary maybe in the future we should use this gravity only for bird
        self.space.gravity = (0, cfg.PLAYER_GRAVITY)
        # TODO: Temporary maybe in the future we should use this damping only for bird
        self.space.damping = cfg.PLAYER_DAMPING

        player_deadly_wall_col = self.space.add_collision_handler(ColType.PLAYER, ColType.DEADLY_WALL)
        player_deadly_wall_col.data['world'] = self
        player_deadly_wall_col.begin = player_deadly_wall_col_begin

        # No player yet
        self.player = None
        self.game_over = False

class ColType():
    """Collision types used by units"""
    PLAYER = 0
    DEADLY_WALL = 1

def player_deadly_wall_col_begin(arbiter, space, data):
    data['world'].game_over = True
    return True