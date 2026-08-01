
class Animation:

    def __init__(self,
                 radius = 10,
                 color = (0, 0, 255),
                 position=None,
                ):
        self.radius = radius
        self.color = color
        self.position = position

    def step(self):
        self.position += self.speed

    def collision(self, other):
        self.hitpoints -= other.attack

    def is_running(self):
        return True
    
    def draw(self, surface):
        pass
