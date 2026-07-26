import pygame

import src.globals as globals
from src.unit import Unit
from src.token import Token
from src.bullet import Bullet

class Player(Unit):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, color=(200, 200, 200), radius=20, line_width=6)
        self.token_count = 0
        self.last_shot_time = 0

    def handle_keys(self, keys):
        delta_speed = 0.5
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.speed.x -= delta_speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.speed.x += delta_speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.speed.y -= delta_speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.speed.y += delta_speed
        if keys[pygame.K_SPACE] or keys[pygame.K_RETURN]:
            self.shoot()

    def shoot(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time < 100:  # ms between shots
            return  # too soon to shoot again
        bullet_speed = 12
        direction = pygame.Vector2(1, 0)  # shoot in X-direction
        bullet_position = self.get_position() + direction * (self.radius + 10)  # spawn bullet just outside the player
        bullet_speed = direction.elementwise() * self.speed + direction * bullet_speed
        globals.units.append(Bullet(position=bullet_position, speed=bullet_speed))
        self.last_shot_time = pygame.time.get_ticks()  # update last shot time

    def step(self):
        super().step()      # normal step behavior super class Unit
        self.speed *= 0.94  # apply friction to slow down the player over time

    def collision(self, other):
        if isinstance(other, Token):  # special collision behavior for Token
            self.token_count += 1
            other.hitpoints = -1  # destroy the token
            print('token_count:', self.token_count)
        else:
            super().collision(other)  # normal collision behavior super class Unit
            print('hitpoints:', self.hitpoints)
            