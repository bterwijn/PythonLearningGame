
import src.globals as globals
from src.unit import Unit

class Token(Unit):

    spawn_chance = 0.005
    count = 0
    max_count = 3

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, color=(0, 255, 0), radius=10, line_width=2)
        Token.count += 1

    def __del__(self):
        Token.count -= 1
