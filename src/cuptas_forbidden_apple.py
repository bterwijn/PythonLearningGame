
import pygame
import random
import src.globals as globals
import src.utils as utils
from time import sleep
from src.cupta import Cupta
from src.player import Player
from src.troll import Troll
from src.unit import Unit

class CuptasForbiddenApple(Unit):
    image = pygame.image.load("assets/cupta.png")

    SPEED = 3

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs,
                         color=(0, 0, 255),  # red, green, blue
                         radius=32,
                         line_width=8,
                         attack=0,
                         hitpoints=40)
        self.speed = pygame.Vector2(
            CuptasForbiddenApple.SPEED * random.choice([-1, 1]),
            CuptasForbiddenApple.SPEED * random.choice([-1, 1])
        )
        self.collected = False

    def step(self):
        super().step()

    def collision(self, other):
        if isinstance(other, Player):
            print("Cupta's ancient powers course through your veins. You are healed.")
            globals.player.hitpoints += 100
            self.collected = True
        elif isinstance(other, Troll):
            print("Oh no! Cupta's dark magic have been bestowed upon the troll!")
            for _ in range(17):
                globals.units.append(Troll(position=utils.random_position(away_from=globals.player.get_position())))
            self.collected = True
        elif isinstance(other, Cupta):
            print("Cupta devours the apple and laughs. His veins glow purple and his eyes become a deep black. For millenia he waited in the caverns beneath the Earth for his powers to return, and you let him. He stares at you intently for several seconds then pounces. In a fraction of a second his fangs are slicing through your flesh. You feel them drain your life. You lose.")
            self.collected = True
            globals.player.hitpoints = -999999999999999999999
            sleep(3)

    def draw(self, surface: pygame.Surface):
        W = 64
        H = 64
        SRC = pygame.Rect(W * 0, H * 3, W, H)
        dst = pygame.Rect(self.position.x - (W / 2.0), self.position.y - (H / 2.0), W, H)
        surface.blit(CuptasForbiddenApple.image, dst, SRC)

    def is_alive(self):
        return not self.collected
