
import pygame
import random
import src.globals as globals
from src.unit import Unit

class Troll(Unit):
    spawn_chance = 0.001
    count = 0
    max_count = 1
    image = pygame.image.load("assets/troll.png")

    def __init__(self, *args, **kwargs):
        width, height = Troll.image.get_size()
        super().__init__(*args, **kwargs,
                         radius=(width+height)/4,
                         attack=999999,
                         hitpoints=400)
        self.randomize_acceleration()
        Troll.count += 1

    def __del__(self):
        Troll.count -= 1

    def randomize_acceleration(self):
        self.acceleration = random.uniform(-0.2, 0.45)

    def step(self):
        if random.randint(1, 30) == 1:
            self.randomize_acceleration()
        direction = globals.player.get_position() - self.get_position()
        direction.normalize_ip()
        self.speed += direction * self.acceleration
        self.speed *= 0.95
        super().step()

    def draw(self, surface):
        dst = self.position.copy()
        width, height = Troll.image.get_size()
        dst.x -= width / 2
        dst.y -= height / 2
        surface.blit(Troll.image, dst)
