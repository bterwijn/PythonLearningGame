import pygame
from src.animation import Animation

class Explosion(Animation):
    def __init__(self, radius=10, color=(255, 0, 0), position=None):
        radius *= 2
        super().__init__(radius=radius, color=color, position=position)
        self.max_radius = radius * 8
        self.growth_rate = 7
        self.color_step = 200 / ((self.max_radius - radius) / self.growth_rate)

    def step(self):
        self.radius += self.growth_rate
        self.color = (max(0, self.color[0] - self.color_step),
                      max(0, self.color[1] - self.color_step),
                      max(0, self.color[2] - self.color_step))


    def is_running(self):
        return self.radius < self.max_radius

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, self.position, self.radius, 2)