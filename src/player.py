import pygame

import src.globals as globals
from src.unit import Unit
from src.token import Token
from src.bullet import Bullet

class Player(Unit):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, color=(200, 200, 200), radius=20, line_width=6)
        width, height = globals.display.get_size()
        middle = pygame.Vector2(width/2, height/2)
        self.direction = (middle - self.position).normalize()
        self.token_count = 0
        self.last_shot_time = 0

    def handle_keys(self, keys):
        acceleration = 0.5
        rotate_speed = 4  # degrees per frame
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.direction.rotate_ip(-rotate_speed)
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.direction.rotate_ip(rotate_speed)
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.speed += self.direction * acceleration
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.speed -= (self.direction/2) * acceleration
        if keys[pygame.K_SPACE] or keys[pygame.K_RETURN]:
            self.shoot()

    def shoot(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time < 100:  # ms between shots
            return  # too soon to shoot again
        bullet_speed = 12
        bullet_position = self.get_position() + self.direction * (self.radius * 1.5)  # spawn bullet just outside the player
        bullet_speed = self.direction * bullet_speed
        globals.units.append(Bullet(position=bullet_position, speed=bullet_speed))
        self.last_shot_time = pygame.time.get_ticks()  # update last shot time

    def step(self):
        super().step()      # normal step behavior super class Unit
        self.speed *= 0.94  # apply friction to slow down the player over time

    def draw(self, surface):
        super().draw(surface)  # normal draw behavior super class Unit
        end_pos = self.position + self.direction * (self.radius * 1.5)
        pygame.draw.line(surface, (255, 255, 255), self.position, end_pos, self.line_width)

    def collision(self, other):
        if isinstance(other, Token):  # special collision behavior for Token
            self.token_count += 1
            other.hitpoints = -1  # destroy the token
            print('token_count:', self.token_count)
        else:
            super().collision(other)  # normal collision behavior super class Unit
            print('hitpoints:', self.hitpoints)
            