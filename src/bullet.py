
import src.globals as globals
from src.unit import Unit

class Bullet(Unit):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs,
                         color=(255, 255, 255),  # red, green, blue
                         radius=4,
                         line_width=4,
                         attack=9,
                         hitpoints=1)

    def collide_border(self):
        self.hitpoints = -1  # destroy the bullet when it hits a border