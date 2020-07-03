"""Module containing all unit class and the world class"""

import pymunk
import cfg
import math
import sys

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
        world.space.add(self.body, self.shape)
        world.player = self

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
        cfg.FLAP_SND.play()

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
        self.shape = pymunk.Segment(self.body, start, end, cfg.WALL_RADIUS)
        self.shape.collision_type = ColType.DEADLY_WALL
        self.shape.color = cfg.RED
        world.space.add(self.body, self.shape)

class Jumper():
    def __init__(self, world, pos):
        """
        Jumper: jump regularly toward hero
        """
        # TODO: make it more configurable from svg
        self.body = pymunk.Body(1, 1, pymunk.Body.DYNAMIC)
        self.body.position = pos
        self.body.velocity_func = lambda body, _g, d, dt: pymunk.Body.update_velocity(body, (0, 0), d, dt)
        self.shape = pymunk.Circle(self.body, cfg.JUMPER_RADIUS)
        self.shape.collision_type = ColType.JUMPER
        self.shape.color = cfg.YELLOW
        self.next_jump = 0
        world.space.add(self.body, self.shape)
        world.to_update.append(self)

    def update(self, world, dt):
        self.next_jump -= dt
        if self.next_jump <= 0:
            self.next_jump = cfg.JUMPER_JUMP_TIME
            if world.player:
                aim = world.player.body.position - self.body.position
                aim_norm = math.sqrt(aim[0]**2 + aim[1]**2)
                if aim_norm != 0:
                    impulse = (aim[0]/aim_norm*cfg.JUMPER_JUMP_IMPULSE, aim[1]/aim_norm*cfg.JUMPER_JUMP_IMPULSE)
                    self.body.apply_impulse_at_local_point(impulse)

class Flies():
    # TODO: maybe add wind
    # TODO: maybe from svg: velocity and other parameter
    def __init__(self, world):
        """
        Flying circle, they simulate an infinite number of circle, space as n a grid.
        But to do so it just place 1 circle in the world and move to the nearest to player.
        """
        self.body = pymunk.Body(1, 1, pymunk.Body.DYNAMIC)
        self.body.velocity = (10, 7)
        self.shape = pymunk.Circle(self.body, cfg.FLIES_RADIUS, (cfg.FLIES_SPACE/2, cfg.FLIES_SPACE/2))
        self.shape.sensor = True
        self.shape.color = cfg.FUCHSIA
        self.shape.collision_type = ColType.FLIES
        # Set the damping to 1 and gravity to 0 for this unit
        self.body.velocity_func = lambda body, _g, _d, dt: pymunk.Body.update_velocity(body, (0, 0), 1, dt)
        world.space.add(self.body, self.shape)
        world.to_update.append(self)
        # TODO: did we made that it doesn't collide with anything but player ????

    def update(self, world, dt):
        if world.player:
            self.body.position = (self.body.position - world.player.body.position) % cfg.FLIES_SPACE \
                + world.player.body.position + (-cfg.FLIES_SPACE, -cfg.FLIES_SPACE)

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

        player_flies_col = self.space.add_collision_handler(ColType.PLAYER, ColType.FLIES)
        player_flies_col.data['world'] = self
        player_flies_col.pre_solve = player_flies_col_begin

        player_jumper_col = self.space.add_collision_handler(ColType.PLAYER, ColType.JUMPER)
        player_jumper_col.data['world'] = self
        player_jumper_col.pre_solve = player_jumper_col_begin

        self.player = None # No player yet
        self.game_over = False
        self.to_update = []

class ColType():
    """Collision types used by units"""
    PLAYER = 1
    DEADLY_WALL = 2
    FLIES = 3
    JUMPER = 4

def player_deadly_wall_col_begin(arbiter, space, data):
    """define begin collision between player and deadly wall, i.e. instant death"""
    data['world'].game_over = True
    return True

def player_flies_col_begin(arbiter, space, data):
    """define begin collision between player and flies, i.e. instant death"""
    data['world'].game_over = True
    return True

def player_jumper_col_begin(arbiter, space, data):
    """define begin collision between player and jumper, i.e. instant death"""
    data['world'].game_over = True
    return True