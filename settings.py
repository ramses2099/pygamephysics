import pygame
from pygame.math import Vector2 as vec

WIDTH = 1280
HEIGHT = 720
TITLE = "Physics tutorial"
TITLESIZE = 16
FONT = "assets/fonts/homespun.ttf"
FPS = 60

COLORS = {
    'black':(0, 0, 0),
    'white':(255, 255, 255),
    'red':(255, 0, 0),
    'green':(0, 255, 0),
    'blue':(0, 0, 255),
    'yellow':(255, 255, 0),
    'purple':(160,32,240)
}

INPUTS = {
    'escape':False,
    'space': False,
    'up': False,
    'down': False,
    'left': False,
    'right': False,
    'left_click': False,
    'right_click': False,
    'scroll_up': False,
    'scroll_down': False,
}

DIRECTION = ('horizontal','vertical')

IMAGE_SHIP = pygame.image.load('./assets/images/charaters/player/ship_A.png')