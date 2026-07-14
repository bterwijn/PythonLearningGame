import pygame
import random
import math

import src.globals as globals

def random_vector_rectangle(width, height):
    x = random.uniform(0, width)
    y = random.uniform(0, height)
    return pygame.Vector2(x,y)

def random_display_position(margin=20):
    width, height = globals.display.get_size()
    vec = random_vector_rectangle(width - 2 * margin, height - 2 * margin)
    vec.x += margin
    vec.y += margin
    return vec

def random_vector_circle(min_radius, max_radius):
    angle = random.uniform(0, 2*math.pi)
    radius = random.uniform(min_radius, max_radius)
    speed_x = radius * math.cos(angle)
    speed_y = radius * math.sin(angle)
    return pygame.Vector2(speed_x, speed_y)