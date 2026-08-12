import pygame

import src.globals as globals
from src.unit import Unit

class Tail(Unit):

    spawn_chance = 0.005
    count = 0
    max_count = 3

    def __init__(self, direction, 
                 prev=None, next=None,*args, **kwargs):
        super().__init__(*args, **kwargs,
                         color=(255, 255, 255),
                         radius=10,
                         line_width=2,
                         hitpoints=40,
                         attack=30)
        self.direction = direction
        self.prev = prev
        self.next = next
        Tail.count += 1

    def __del__(self):
        Tail.count -= 1

    def step(self):
        super().step()  # normal step behavior super class Unit
        if self.next:
            self.direction = self.next.get_position() - self.get_position()
            dist = self.direction.length()
            if dist == 0:
                return
            self.direction.normalize_ip()
            sum_radius = self.radius + self.next.radius
            min_dist = sum_radius * 1.1
            accel_dist = sum_radius * 1.3
            max_dist = sum_radius * 1.5
            if dist < min_dist:
                delta = dist - min_dist
                self.position += self.direction * delta
            else:
                if dist > accel_dist:
                    self.speed += self.direction * 0.3
                if dist > max_dist:
                    delta = dist - max_dist
                    self.position += self.direction * delta
        self.speed *= 0.96  # apply friction to slow down the tail over time

    def dies(self):
        if self is globals.player.last_tail:
            globals.player.last_tail = self.next
        if self.prev:
            self.prev.next = self.next
        if self.next is not globals.player:  # only update next.prev if next is not the player
            self.next.prev = self.prev
