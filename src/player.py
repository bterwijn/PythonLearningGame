import pygame
import random

import src.globals as globals
from src.unit import Unit
from src.token import Token
from src.bullet import Bullet
from src.tail import Tail

class Player(Unit):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, color=(200, 200, 200), radius=20, line_width=6)
        width, height = globals.display.get_size()
        middle = pygame.Vector2(width/2, height/2)
        self.direction = (middle - self.position).normalize()
        self.token_count = 0
        self.last_shot_time = 0
        self.last_tail = self

    def handle_keys(self, keys):
        acceleration = 0.5
        rotate_speed = 4  # degrees per frame
        if keys[pygame.K_LEFT] or keys[pygame.K_a] or keys[pygame.K_z]:
            self.direction.rotate_ip(-rotate_speed)
        if keys[pygame.K_RIGHT] or keys[pygame.K_d] or keys[pygame.K_x]:
            self.direction.rotate_ip(rotate_speed)
        if keys[pygame.K_UP] or keys[pygame.K_w] or keys[pygame.K_QUOTE]:
            self.speed += self.direction * acceleration
        if keys[pygame.K_DOWN] or keys[pygame.K_s] or keys[pygame.K_SLASH]:
            self.speed -= (self.direction/2) * acceleration
        if keys[pygame.K_SPACE] or keys[pygame.K_RETURN]:
            self.shoot()

    def shoot(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time < 100:  # ms between shots
            return  # too soon to shoot again
        bullet_speed = 12
        bullet_position = self.get_position() + self.direction * (self.radius * 1.5)  # spawn bullet just outside the player
        gaus = random.gauss(0, 2)  # small random angle for bullet spread
        direction = self.direction.rotate(gaus)
        bullet_speed = direction * bullet_speed
        globals.units.append(Bullet(position=bullet_position, speed=bullet_speed))
        self.last_shot_time = pygame.time.get_ticks()  # update last shot time

    def step(self):
        mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
        self.direction = mouse_pos - self.position
        self.direction.normalize_ip()
        super().step()      # normal step behavior super class Unit
        self.speed *= 0.94  # apply friction to slow down the player over time

    def draw(self, surface):
        super().draw(surface)  # normal draw behavior super class Unit
        end_pos = self.position + self.direction * (self.radius * 1.5)
        pygame.draw.line(surface, (255, 255, 255), self.position, end_pos, self.line_width)

    def add_tail(self):
        prev_tail = self.last_tail
        self.last_tail = Tail(prev=None,
                    next=self.last_tail,
                    direction=self.direction.copy(),
                    position=self.last_tail.position - 
                       self.last_tail.direction * (self.last_tail.radius * 2),
                    speed=self.speed.copy(),
                    )
        if prev_tail is not self:
            prev_tail.prev = self.last_tail 
        globals.units.append(self.last_tail)

    def collision(self, other):
        if isinstance(other, Token):  # special collision behavior for Token
            self.token_count += 1
            other.hitpoints = -1  # destroy the token
            print('token_count:', self.token_count)
            self.add_tail()
        else:
            super().collision(other)  # normal collision behavior super class Unit
            print('hitpoints:', self.hitpoints)
            