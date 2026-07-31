
import pygame
import random
import src.globals as globals
from src.unit import Unit

class Troll(Unit):
    spawn_chance = 0.005
    count = 0
    max_count = 1
    image = pygame.image.load("assets/troll.png")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs,
                         radius=125,
                         attack=999999,
                         hitpoints=400)
        self.randomize_acceleration()
        Troll.count += 1

    def __del__(self):
        Troll.count -= 1

    def randomize_acceleration(self):
        self.acceleration = random.uniform(-1.0, 0.5)

    def step(self):
        if random.randint(1, 60) == 1:
            self.randomize_acceleration()
        direction = globals.player.get_position() - self.get_position()
        direction.normalize_ip()
        self.speed += direction * self.acceleration
        self.speed *= 0.98
        super().step()

    def draw(self, surface):
        dst = self.position.copy()
        dst.x -= 125
        dst.y -= 125
        surface.blit(Troll.image, dst)
