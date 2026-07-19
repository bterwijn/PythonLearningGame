
import src.globals as globals
from src.unit import Unit

class Seeker(Unit):
    spawn_chance = 0.002
    count = 0
    max_count = 3

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs,
                         color=(0, 0, 255),  # red, green, blue
                         radius=14,
                         line_width=8,
                         attack=15,
                         hitpoints=40)
        Seeker.count += 1

    def __del__(self):
        Seeker.count -= 1

    def step(self):  # overwrite normal Unit step
        direction = globals.player.get_position() - self.get_position()  # direction to player
        direction.normalize_ip()  # make direction vector length 1
        acceleration = 0.15
        self.speed += direction * acceleration  # accelerate towards player
        self.speed *= 0.95  # add some friction
        super().step()  # do normal Unit step