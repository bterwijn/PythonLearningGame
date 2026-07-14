
import src.globals as globals
from src.unit import Unit

class Hazard(Unit):

    spawn_chance = 0.01
    count = 0
    max_count = 6

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, 
                         color=(255, 0, 0), 
                         radius=12, 
                         line_width=3,
                         attack=25)
        Hazard.count += 1

    def __del__(self):
        Hazard.count -= 1