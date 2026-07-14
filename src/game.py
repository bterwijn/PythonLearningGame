import pygame
import random

import src.globals as globals
from src.player import Player
from src.token import Token
from src.hazard import Hazard

class Game:
    def __init__(self):
        pygame.init()
        self.running = True
        globals.display = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
        pygame.display.set_caption('PythonLearningGame')
        self.background_colour = (0, 0, 0)
        self.frames_per_second = 60
        globals.player = Player()
        globals.units = [globals.player]
        self.mouse_buttons_down = {}

    def spawn_unit(self, unit_class):
        unit = unit_class()
        globals.units.append(unit)

    def spawn_units(self):
        spawn_types = [Token, Hazard]
        for spawn_type in spawn_types:
            if spawn_type.count < spawn_type.max_count:
                if random.random() < spawn_type.spawn_chance:
                    self.spawn_unit(spawn_type)

    def handle_events(self):
        for event in pygame.event.get():  # handle events
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                button = event.button
                print("MOUSEBUTTONDOWN: ",pos, button)
                self.mouse_buttons_down[button] = True
            elif event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                button = event.button
                print("MOUSEBUTTONUP: ",pos, button)
                self.mouse_buttons_down[button] = False
            elif event.type == pygame.MOUSEMOTION:
                if any(self.mouse_buttons_down.values()):
                    pos = pygame.mouse.get_pos()
                    print("MOUSEMOTION: ",pos)

    def collision(self, unit1, unit2):
        unit1.speed, unit2.speed = unit2.speed, unit1.speed

    def step_units(self):
        for unit in globals.units:
            pos_old = unit.get_position().copy() # when colliding, we will revert to this position
            unit.step()
            for other in globals.units:
                if unit is not other:
                    square_distance = (unit.get_position() - other.get_position()).length_squared()
                    square_radius_sum = (unit.radius + other.radius) ** 2
                    if square_distance < square_radius_sum:
                        unit.set_position(pos_old)
                        self.collision(unit, other)  # Handle collision
                        unit.collision(other)
                        other.collision(unit)
            unit.collide_display_border()

    def kill_dead_units(self):
        if globals.player.hitpoints <= 0:
            self.running = False
            return
        globals.units = [unit for unit in globals.units if unit.is_alive()]

    def draw_units(self):
        for unit in globals.units:
            unit.draw(globals.display)

    def start(self):
        print("Game Started")
        print("- use cursor or WASD keys to move")
        print("- catch green tokens to gain points")
        print("- avoid red hazards to stay alive")
        clock = pygame.time.Clock()
        
        self.running = True
        while self.running:
            globals.display.fill(self.background_colour) # clear display

            self.spawn_units()
            keys = pygame.key.get_pressed()
            globals.player.handle_keys(keys)
            self.handle_events()
            self.step_units()
            self.draw_units()
            self.kill_dead_units()

            pygame.display.flip()  # draw everything to the display
            clock.tick(self.frames_per_second)
        print("Game Over")
