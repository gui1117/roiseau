import cfg
import populate_from_svg
import units
import utils
import pymunk
import pymunk.pygame_util
import sys
import math
import pygame

# Set screen: surface on which everything is drawn
if cfg.DEBUG:
    screen = pygame.display.set_mode(size=(800, 600))
else:
    screen = pygame.display.set_mode(flags=pygame.FULLSCREEN)

font = pygame.font.SysFont('', 20)
game_over_surface = font.render("Game over", True, cfg.WHITE)

if __name__ == "__main__":
    # Create the game world
    world = units.World()

    # Instantiate physical objects
    populate_from_svg.populate_with_file(world, 'dessin.svg')
    # units.Flies(world)

    # Instantiate camera
    camera = utils.Camera(0, 0, screen.get_width(
    )/2, screen.get_height()/2, screen.get_height()/cfg.SPACE_SHOWN)

    # Instantiate debug_draw_options
    if cfg.DEBUG:
        debug_draw_options = utils.DrawOptionsWithCamera(screen, camera)

    # Instantiate clock: it is used to clamp framerate.
    clock = pygame.time.Clock()

    # Main loop, this will be executed forever until the game finishs
    while True:
        flap = False

# TODO: make that you have to press down a bit before flying: the times pressed is the force (with a maximum is current)
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
                if world.player and not world.game_over:
                    world.player.flap()

        # Update world
        dt = 1.0/cfg.FRAMERATE
        for to_update in world.to_update:
            to_update.update(world, dt)
        world.space.step(dt)

        # Draw world
        screen.fill(cfg.BLACK)

        # Update camera position in physic space to follow the player if any
        if world.player:
            camera.pos = world.player.body.position

        if cfg.DEBUG:
            world.space.debug_draw(debug_draw_options)

        if world.game_over:
            x = screen.get_width()/2 - game_over_surface.get_width()/2
            y = screen.get_height()/2 - game_over_surface.get_height()/2
            screen.blit(game_over_surface, (x, y))

        pygame.display.flip()

        # Wait for next frame
        clock.tick(cfg.FRAMERATE)
