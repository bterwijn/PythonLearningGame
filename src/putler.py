
import pygame
import random
import src.globals as globals
from src.unit import Unit

class Putler(Unit):
    spawn_chance = 0.0005
    count = 0
    max_count = 1
    images = [pygame.image.load("assets/putler1.png"),
              pygame.image.load("assets/putler2.png"),
              pygame.image.load("assets/putler3.png"),
              pygame.image.load("assets/putler4.png"),
              pygame.image.load("assets/putler5.png")]
    contract = pygame.image.load("assets/contract.png")

    def __init__(self, *args, **kwargs):
        width, height = Putler.images[0].get_size()
        super().__init__(*args, **kwargs,
                         radius=(width+height)/4,
                         attack=1,
                         hitpoints=300,
                         color=(0, 255, 0),
                         )
        self.change_image()
        self.holes = []
        Putler.count += 1

    def __del__(self):
        Putler.count -= 1
        globals.player.token_count += 2

    def change_image(self):
        self.image_index = random.randrange(0, len(Putler.images))
        self.show_contract = random.choice([True, False])
        if self.show_contract:
            contract_angle = random.uniform(0, 360)
            width, height = Putler.images[self.image_index].get_size()
            c_width, c_height = Putler.contract.get_size()
            self.contract_vec = pygame.Vector2((c_width+c_height+width+height)/5, 0)
            self.contract_vec.rotate_ip(contract_angle)
            self.contract_vec.x-= c_width / 2
            self.contract_vec.y-= c_height / 2

    def step(self):
        super().step()
        if random.randint(1, 100) == 1:
            self.change_image()
        direction = self.get_position() - globals.player.get_position()
        distance = direction.length()
        if distance < 150:
            direction.normalize_ip()
            self.speed = direction * 4        

    def collision(self, other):
        super().collision(other)
        h = pygame.Vector2(random.uniform(0, self.radius), 0)
        h.rotate_ip(random.uniform(0, 360))
        self.holes.append(h)

    def draw(self, surface):
        dst = self.position.copy()
        width, height = Putler.images[self.image_index].get_size()
        if self.show_contract:
            surface.blit(Putler.contract, dst + self.contract_vec)
        dst.x -= width / 2
        dst.y -= height / 2
        surface.blit(Putler.images[self.image_index], dst)
        for hole in self.holes:
            hole_pos = self.position + hole
            pygame.draw.circle(surface, (0, 0, 0), hole_pos, 7)
        
