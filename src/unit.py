import pygame

import src.globals as globals
from src.utils import *

class Unit:
    spawn_change = None
    count = None
    max_count = None
    initial_hitpoints = 100

    def __init__(self,
                 radius = 10,
                 color = (0, 0, 255),
                 line_width = 4,
                 position=None,
                 speed=None,
                 hitpoints=initial_hitpoints,
                 attack=10):
        self.radius = radius
        self.color = color
        self.line_width = line_width
        if position is None:
            position = random_display_position(margin=radius*1.5)
        self.position = position
        if speed is None:
            speed = random_vector_circle(1, 3)
        self.speed = speed
        self.hitpoints = hitpoints
        self.attack = attack

    def step(self):
        self.position += self.speed
        
    def collide_display_border(self):
        width, height = globals.display.get_size()
        if self.position.x - self.radius < 0:
            self.position.x = self.radius
            self.speed.x *= -1
        elif self.position.x + self.radius > width:
            self.position.x = width - self.radius
            self.speed.x *= -1
        if self.position.y - self.radius < 0:
            self.position.y = self.radius
            self.speed.y *= -1
        elif self.position.y + self.radius > height:
            self.position.y = height - self.radius
            self.speed.y *= -1

    def get_position(self):
        return self.position
    
    def set_position(self, position):
        self.position = position

    def collision(self, other):
        self.hitpoints -= other.attack

    def is_alive(self):
        return self.hitpoints > 0
    
    def draw(self, surface):
        pygame.draw.circle(surface, self.color, self.position, self.radius, self.line_width)
