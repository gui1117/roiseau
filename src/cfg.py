"""Configuration module, contains various constants"""

import pygame

# Init game first, used to load sounds
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()

FRAMERATE = 60

BLACK = 0, 0, 0
WHITE = 255, 255, 255
RED = 255, 0, 0
FUCHSIA = 255, 0, 255
YELLOW = 255, 255, 0

SPACE_SHOWN = 40

WALL_RADIUS = 1

PLAYER_RADIUS = 1
PLAYER_DAMPING = 0.5
PLAYER_GRAVITY = -23
PLAYER_FLAP_IMPULSE = 20
PLAYER_MASS = 1

FLIES_RADIUS = 1
FLIES_SPACE = 20

JUMPER_RADIUS = 1
JUMPER_MASS = 1
JUMPER_JUMP_TIME = 0.5
JUMPER_JUMP_IMPULSE = 30

DEBUG = True

FLAP_SND = pygame.mixer.Sound(file="sounds/flap.wav")