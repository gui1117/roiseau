import pygame
import pymunk
import pymunk.pygame_util
import sys
import math

# Constants
FRAMERATE = 60
BLACK = 0, 0, 0
PLAYER_RADIUS = 1
WALL_RADIUS = 1
SPACE_SHOWN = 20
PLAYER_DAMPING = 0.5
PLAYER_GRAVITY = -23
PLAYER_FLAP_IMPULSE = 20
PLAYER_MASS = 1
DEBUG = True

# Init game
pygame.init()

# Set screen: surface on which everything is drawn
if DEBUG: screen = pygame.display.set_mode(size=(800, 600))
else: screen = pygame.display.set_mode(flags=pygame.FULLSCREEN)

# Init physic space
space = pymunk.Space()
# TODO: Temporary maybe in the future we should use this gravity only for bird
space.gravity = (0, PLAYER_GRAVITY)
# TODO: Temporary maybe in the future we should use this damping only for bird
space.damping = PLAYER_DAMPING

class Camera:
    def __init__(self, x, y, zoom):
        """Create a camera object.
        camera offer function to transform from physic space coordinate to screen coordinate
        """
        self.pos = (x, y)
        self.zoom = zoom

    def trans_pos(self, pos):
        """Transform a position `(number, number)` into screen coordinate)"""
        return (self.pos + pos) * self.zoom

    def trans_length(self, length):
        """Transform a lenght into screen coordinate"""
        return length * self.zoom

class DrawOptionsWithCamera(pymunk.pygame_util.DrawOptions):
    """Class that inherit DrawOptions and use camera to translate coordinate before drawing them"""

    def draw_circle(self, pos, angle, radius, outline_color, fill_color):
        """Change coordinate with camera and call draw_circle"""
        pos = camera.trans_pos(pos)
        radius = camera.trans_length(radius)
        super().draw_circle(pos, angle, radius, outline_color, fill_color)

    def draw_dot(self, size, pos, color):
        """Change coordinate with camera and call draw_dot"""
        pos = camera.trans_pos(pos)
        size = camera.tran_length(size)
        super().draw_dot(size, pos, color)

    def draw_fat_segment(self, a, b, radius, outline_color, fill_color):
        """Change coordinate with camera and call draw_fat_segment"""
        a = camera.trans_pos(a)
        b = camera.trans_pos(b)
        radius = camera.trans_length(radius)
        super().draw_fat_segment(a, b, radius, outline_color, fill_color)

    def draw_polygon(self, verts, radius, outline_color, fill_color):
        raise NotImplementedError
        # super.draw_polygon(verts, radius, outline_color, fill_color)

    def draw_segment(self, a, b, color):
        """Change coordinate with camera and call draw_segment"""
        a = camera.trans_pos(a)
        b = camera.trans_pos(b)
        super().draw_segment(a, b, color)

class Player:
    """Player flap direction is has up component"""
    dir_up = False

    """Player flap direction is has down component"""
    dir_down = False

    """Player flap direction is has left component"""
    dir_left = False

    """Player flap direction is has right component"""
    dir_right = False

    def __init__(self):
        """Player: add a circle body in the physic space"""
        self.body = pymunk.Body(PLAYER_MASS, 1000)
        self.body.position = 10, 10
        self.shape = pymunk.Circle(self.body, PLAYER_RADIUS)
        self.body.velocity_func = self.velocity_func
        space.add(self.body, self.shape)

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
        coef = PLAYER_FLAP_IMPULSE / norm
        self.body.apply_impulse_at_local_point((dir[0]*coef, dir[1]*coef))

class Wall:
    def __init__(self):
        """Wall: add a segment body in the physic space"""
        self.body = pymunk.Body(1, 1, pymunk.Body.STATIC)
        self.body.position = 0, 0
        a = 0, 0
        b = 18, 0
        self.shape = pymunk.Segment(self.body, a, b, WALL_RADIUS)
        space.add(self.body, self.shape)

if __name__ == "__main__":
    # Instantiate physical objects
    player = Player()
    wall = Wall()

    # Instantiate camera
    camera = Camera(0, 0, screen.get_height()/SPACE_SHOWN)

    # Instantiate debug_draw_options
    if DEBUG:
        debug_draw_options = DrawOptionsWithCamera(screen)

    # Instantiate clock: it is used to clamp framerate.
    clock = pygame.time.Clock()

    # Main loop, this will be executed forever until the game finishs
    while True:
        flap = False

        # Parse events
        for event in pygame.event.get():
            if (
                event.type == pygame.QUIT or
                event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
            ):
                sys.exit()
            elif (event.type == pygame.KEYDOWN or event.type == pygame.KEYUP) and event.key == pygame.K_i:
                player.dir_up = event.type == pygame.KEYDOWN
            elif (event.type == pygame.KEYDOWN or event.type == pygame.KEYUP) and event.key == pygame.K_k:
                player.dir_down = event.type == pygame.KEYDOWN
            elif (event.type == pygame.KEYDOWN or event.type == pygame.KEYUP) and event.key == pygame.K_j:
                player.dir_left = event.type == pygame.KEYDOWN
            elif (event.type == pygame.KEYDOWN or event.type == pygame.KEYUP) and event.key == pygame.K_l:
                player.dir_right = event.type == pygame.KEYDOWN
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                player.flap()

        # Update world
        space.step(1.0/FRAMERATE)

        # Draw world
        screen.fill(BLACK)

        if DEBUG:
            space.debug_draw(debug_draw_options)

        pygame.display.flip()

        # Wait for next frame
        clock.tick(FRAMERATE)
