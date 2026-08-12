import pygame
import random

import src.globals as globals
from src.player import Player
from src.token import Token
from src.hazard import Hazard
from src.seeker import Seeker
from src.troll import Troll
from src.bullet import Bullet
from src.explosion import Explosion
from src.tail import Tail
from src import utils

class Game:
    def __init__(self):
        pygame.init()
        self.running = True
        globals.display = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
        pygame.display.set_caption('PythonLearningGame')
        self.background_colour = (0, 0, 0)
        self.frames_per_second = 60
        globals.player = Player()
        globals.units.append(globals.player)
        for i in range(10):
            globals.player.add_tail()  # start with tail of 10 segments
        self.mouse_buttons_down = {}

    def spawn_unit(self, unit_class):
        position = utils.random_position(away_from=globals.player.get_position())
        if position is not None:  # pnly if valid position found
            unit = unit_class(position=position)
            globals.units.append(unit)

    def spawn_units(self):
        spawn_types = [Token, Hazard, Seeker, Troll]
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

    def does_collide(self, unit1, unit2):
        non_collide_types = {(Tail, Tail), 
                             (Player, Tail), (Tail, Player), 
                             (Bullet, Tail), (Tail, Bullet), 
                             (Tail, Token), (Token, Tail),
                             }
        return  (type(unit1), type(unit2)) not in non_collide_types

    def collision(self, unit1, unit2):
        # Switched to elastic collision response based on https://en.wikipedia.org/wiki/Elastic_collision
        # first compute the normal vector between the two units
        delta = unit1.get_position() - unit2.get_position()
        if delta.length_squared() == 0:  # fix if delta is zero
            relative_speed = unit1.speed - unit2.speed
            if relative_speed.length_squared() == 0:
                return  # no fix, ignore collision
            delta = relative_speed.normalize()
        normal = delta.normalize()
        # compute the relative speed along the normal
        relative_speed = unit1.speed - unit2.speed
        velocity_along_normal = relative_speed.dot(normal)
        mass1 = unit1.radius  # mass proportional to radius looks better than area (radius**2)
        mass2 = unit2.radius
        # compute impulse using the formula for elastic collisions
        impulse_strength = -(2.0 * velocity_along_normal) / ((1.0 / mass1) + (1.0 / mass2))
        impulse = normal * impulse_strength
        # apply impulse to the units' speeds
        unit1.speed += impulse / mass1
        unit2.speed -= impulse / mass2

    def step_units(self):
        for unit in globals.units:
            pos_old = unit.get_position().copy() # when colliding, we will revert to this position
            unit.step()
            for other in globals.units:
                if unit is not other: # don't collide with self
                    square_distance = (unit.get_position() - other.get_position()).length_squared()
                    square_radius_sum = (unit.radius + other.radius) ** 2
                    if square_distance < square_radius_sum:
                        if self.does_collide(unit, other):  # test if units should collide
                            self.collision(unit, other)  # Handle collision
                            unit.set_position(pos_old)
                            unit.collision(other)
                            other.collision(unit)
            unit.collide_display_border()

    def kill_dead_units(self):
        if globals.player.hitpoints <= 0:
            self.running = False
        alive_units = []
        for unit in globals.units:
            if unit.is_alive():
                alive_units.append(unit)
            else:
                unit.dies()
                expl = Explosion(radius = unit.radius, 
                                color = unit.color,
                                position = unit.get_position())
                globals.animations.append(expl)
        globals.units = alive_units

    def draw_units(self):
        for unit in globals.units:
            unit.draw(globals.display)

    def draw_panel(self):
        initial_hitpoints = Player.initial_hitpoints
        hitpoints = globals.player.hitpoints
        token_count = globals.player.token_count
        win_token_count = globals.win_token_count
        width = globals.display.get_width()
        height = 4
        margin = 20
        pygame.draw.rect(globals.display, (255, 0, 0), 
                         (margin, height, (width - 2 * margin) * hitpoints / initial_hitpoints, height)) 
        pygame.draw.rect(globals.display, (0, 255, 0), 
                         (margin, 3*height, (width - 2 * margin) * token_count / win_token_count, height))
        pygame.draw.line(globals.display, (255, 255, 255),
                        (margin, height), (margin, 4*height), 4)
        pygame.draw.line(globals.display, (255, 255, 255),
                        (width - margin, height), (width - margin, 4*height), 4)

    def test_win(self):
        return globals.player.token_count >= globals.win_token_count

    def step_animations(self):
        for animation in globals.animations:
            animation.step()

    def draw_animations(self):
        for animation in globals.animations:
            animation.draw(globals.display)

    def remove_animations(self):
        globals.animations = [animation for animation in globals.animations if animation.is_running()]

    def start(self):
        print("Game Started")
        print("- use cursor or WASD or ZX/' keys to move")
        print("- catch green tokens to gain points")
        print("- avoid red hazards to stay alive")
        print("- avoid blue seekers that chase you")
        print("- press SPACE or RETURN to shoot bullets")
        clock = pygame.time.Clock()
        
        self.running = True
        while self.running:
            globals.display.fill(self.background_colour) # clear display

            self.spawn_units()
            keys = pygame.key.get_pressed()
            globals.player.handle_keys(keys)
            self.handle_events()
            self.step_units()
            self.draw_panel()
            self.draw_units()
            self.step_animations()
            self.draw_animations()
            self.kill_dead_units()
            self.remove_animations()
            if self.test_win():
                print("You Win!")
                self.running = False

            pygame.display.flip()  # draw everything to the display
            clock.tick(self.frames_per_second)
        print("Game Over")
