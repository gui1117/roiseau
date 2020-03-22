import pygame
import pymunk
import pymunk.pygame_util
import sys
import math

# Constants
FRAMERATE = 60
BLACK = 0, 0, 0
GRAVITY = 0, -1 
PLAYER_RADIUS = 1
WALL_RADIUS = 1
SPACE_SHOWN = 20
DEBUG = True

# Init game
pygame.init()

# Set screen: surface on which everything is drawn
if DEBUG: screen = pygame.display.set_mode(size=(800, 600))
else: screen = pygame.display.set_mode(flags=pygame.FULLSCREEN)

# Init physic space
space = pymunk.Space()
space.gravity = GRAVITY

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
    def __init__(self):
        """Player: add a circle body in the physic space"""
        self.body = pymunk.Body(1, 1000)
        self.body.position = 10, 10
        self.shape = pymunk.Circle(self.body, PLAYER_RADIUS)
        space.add(self.body, self.shape)

class Wall:
    def __init__(self):
        """Wall: add a segment body in the physic space"""
        self.body = pymunk.Body(1, 1, pymunk.Body.STATIC)
        self.body.position = 0, 0
        a = 0, 0
        b = 10, 0
        self.shape = pymunk.Segment(self.body, a, b, WALL_RADIUS)
        space.add(self.body, self.shape)

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

    # Parse events
    for event in pygame.event.get():
        if (
            event.type == pygame.QUIT or
            event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
        ):
            sys.exit()

    # Update world
    space.step(0.2)

    # Draw world
    screen.fill(BLACK)

    if DEBUG:
        space.DEBUG_draw(debug_draw_options)
    
    pygame.display.flip()

    # Wait for next frame
    clock.tick(FRAMERATE)
