import pygame
import pymunk
import pymunk.pygame_util
import sys
import math
import utils
import units
import cfg
import populate_from_svg

# Init game
pygame.init()

# Set screen: surface on which everything is drawn
if cfg.DEBUG: screen = pygame.display.set_mode(size=(800, 600))
else: screen = pygame.display.set_mode(flags=pygame.FULLSCREEN)


class World:
    """Game world, contains physic space and player"""

    def __init__(self):
        """Instantiate space physic and player to None"""
        # Init physic space
        self.space = pymunk.Space()
        # TODO: Temporary maybe in the future we should use this gravity only for bird
        self.space.gravity = (0, cfg.PLAYER_GRAVITY)
        # TODO: Temporary maybe in the future we should use this damping only for bird
        self.space.damping = cfg.PLAYER_DAMPING

        # No player yet
        self.player = None

if __name__ == "__main__":
    # Create the game world
    world = World()

    # Instantiate physical objects
    populate_from_svg.populate_with_file(world, 'dessin.svg')

    # Instantiate camera
    camera = utils.Camera(0, 0, screen.get_width()/2, screen.get_height()/2, screen.get_height()/cfg.SPACE_SHOWN)

    # Instantiate debug_draw_options
    if cfg.DEBUG:
        debug_draw_options = utils.DrawOptionsWithCamera(screen, camera)

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
                if world.player:
                    world.player.dir_up = event.type == pygame.KEYDOWN
            elif (event.type == pygame.KEYDOWN or event.type == pygame.KEYUP) and event.key == pygame.K_k:
                if world.player:
                    world.player.dir_down = event.type == pygame.KEYDOWN
            elif (event.type == pygame.KEYDOWN or event.type == pygame.KEYUP) and event.key == pygame.K_j:
                if world.player:
                    world.player.dir_left = event.type == pygame.KEYDOWN
            elif (event.type == pygame.KEYDOWN or event.type == pygame.KEYUP) and event.key == pygame.K_l:
                if world.player:
                    world.player.dir_right = event.type == pygame.KEYDOWN
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if world.player:
                    world.player.flap()

        # Update world
        world.space.step(1.0/cfg.FRAMERATE)

        # Draw world
        screen.fill(cfg.BLACK)

        # Update camera position in physic space to follow the player if any
        if world.player:
            camera.pos = world.player.body.position

        if cfg.DEBUG:
            world.space.debug_draw(debug_draw_options)

        pygame.display.flip()

        # Wait for next frame
        clock.tick(cfg.FRAMERATE)
