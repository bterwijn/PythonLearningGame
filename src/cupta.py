
import pygame
import random
import src.globals as globals
from src.unit import Unit
from src.utils import random_display_position
import src.globals

SPRITE_WIDTH = 64
SPRITE_HEIGHT = 64

def get_sprite(row, col):
    return pygame.Rect(col * SPRITE_WIDTH, row * SPRITE_HEIGHT, SPRITE_WIDTH, SPRITE_HEIGHT)

class Cupta(Unit):
    spawn_chance = 1
    count = 0
    max_count = 1
    image = pygame.image.load("assets/cupta.png")
    cupta_health_lost_until_death = 600

    HEAD = get_sprite(0, 3)
    BODY_STRAIGHT = get_sprite(1, 2)
    TAIL = get_sprite(2, 3)


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs,
                         radius=8,
                         attack=2,
                         hitpoints=600,
                         color=(0, 255, 0),
                         speed=pygame.Vector2(0, -random.randint(6, 12)),
                         )

        Cupta.count += 1
        print('CUPTA HAS ARRIVED')
        self.position.y = 2000
        pos = random_display_position(0)
        self.x = pos.x
        self.cupta_snake_parts = [self.HEAD]
        for _ in range(random.randint(3, 20)):
            self.cupta_snake_parts.append(self.BODY_STRAIGHT)

        self.cupta_snake_parts.append(self.TAIL)

    def __del__(self):
        Cupta.count -= 1
        globals.player.token_count += 5

    def step(self):
        super().step()
        self.position.x = self.x
        cupta_snake_rectangle_collision_shape_box = pygame.Rect(
            self.position.x,
            self.position.y,
            SPRITE_WIDTH,
            SPRITE_HEIGHT * len(self.cupta_snake_parts)
        )
        player_pos = globals.player.get_position()
        player_rectangle_collision_shape_box = pygame.Rect(player_pos.x, player_pos.y, globals.player.radius, globals.player.radius)

        if cupta_snake_rectangle_collision_shape_box.colliderect(player_rectangle_collision_shape_box):
            print('Cupta has begun siphoning your life essence.')
        

    def draw(self, surface: pygame.Surface):
        for i, part in enumerate(self.cupta_snake_parts):
            dst = self.position.copy()
            dst.y += i * SPRITE_HEIGHT
            surface.blit(Cupta.image, dst, part)

    def collide_display_border(self):
        if self.position.y + SPRITE_HEIGHT * len(self.cupta_snake_parts) < -30:
            pos = random_display_position(0)
            self.position.y = 2000
            self.position.x = pos.x
            self.x = pos.x
