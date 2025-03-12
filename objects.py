import pygame
from math import ceil
from random import choice
from other import *

all_sprites = pygame.sprite.Group()
attack_sprites = pygame.sprite.Group()


class Object(pygame.sprite.Sprite):
    def __init__(self, x=100, y=100, w=100, h=100):
        super().__init__(all_sprites)
        self.image = pygame.Surface((w, h))
        self.image.fill('gray')
        self.rect = pygame.Rect(x, y, w, h)

        self.cooldown = 0
        self.speed = 1
        self.health = 100
        self.dx = 0
        self.dy = 0
        self.way = []


class Character(Object):
    def __init__(self, *args):
        super().__init__(*args)
        self.add(character_sprites)
        self.image = load_image("hurt.png")
        self.experience = 0
        self.items = {Attack: {'level': 1, 'time': 0}}

    def update(self):
        for item in self.items.keys():
            if self.items[item]['time']:
                self.items[item]['time'] -= 1

            else:
                self.items[item]['time'] = 60
                item(self.rect.x, self.rect.y, )

        if 0 in (self.dx, self.dy):
            self.rect.move_ip(self.dx * self.speed, self.dy * self.speed)

        elif self.way:
            x, y = self.way.pop()
            self.rect.move_ip(x * self.speed, y * self.speed)

        else:
            self.way = [(self.dx, 0), (self.dx, self.dy), (0, self.dy), (self.dx, self.dy)]

        self.cooldown -= 1
        if self.health < 0:
            print('ded')

    def move(self, direction, movement):
        velocity = 1 if movement else -1

        if direction == pygame.K_a:
            self.dx += -velocity
        elif direction == pygame.K_w:
            self.dy += -velocity
        elif direction == pygame.K_d:
            self.dx += velocity
        elif direction == pygame.K_s:
            self.dy += velocity

    # def add_item(self, item):
    #     if item in self.items.keys():
    #         self.items[item]['level'] += 1
    #     else:
    #         self.items[item] = {'level': 1, 'time': 0}


class Enemy(Object):
    def __init__(self, *args):
        super().__init__(*args)
        self.add(enemy_sprites)
        self.image = load_image("enemy.png ")
    def update(self, char_x, char_y):
        enemy_x = self.rect.x + self.rect.w // 2
        enemy_y = self.rect.y + self.rect.h // 2

        if enemy_x == char_x and enemy_y == char_y:
            self.way = [(0, 0)]

        elif not self.way:
            x_vector = -1 if enemy_x > char_x else 1 if enemy_x < char_x else None
            y_vector = -1 if enemy_y > char_y else 1 if enemy_y < char_y else None

            if x_vector is None:
                for i in range(10):
                    self.way.append((0, 1 * y_vector))

            elif y_vector is None:
                for i in range(10):
                    self.way.append((1 * x_vector, 0))

            else:
                x_range = abs(char_x - enemy_x)
                y_range = abs(char_y - enemy_y)

                if 10 < x_range > y_range:
                    y_range = ceil(y_range / (x_range / 10))
                    x_range = ceil(x_range / (x_range / 10))
                elif 10 < y_range > x_range:
                    x_range = ceil(x_range / (y_range / 10))
                    y_range = ceil(y_range / (y_range / 10))

                x_max = x_range
                y_max = y_range

                for i in range(10):
                    if x_range / x_max > y_range / y_max:
                        x_range -= 1
                        self.way.append((1 * x_vector, 0))
                    else:
                        y_range -= 1
                        self.way.append((0, 1 * y_vector))

        self.dx, self.dy = self.way.pop(0)
        self.rect.move_ip(self.dx * self.speed, self.dy * self.speed)

        char = pygame.sprite.spritecollideany(self, character_sprites)
        if char and char.cooldown < 0:
            char.health -= 34
            char.cooldown = 120

        self.cooldown -= 1


class Attack(Object):
    def __init__(self, *args):
        super().__init__(*args)
        self.add(attack_sprites)
        self.image = pygame.Surface((50, 50))
        self.image = load_image("1.png")
        self.rect = pygame.Rect(self.rect.x + 25, self.rect.y + 25, 50, 50)
        self.dx = choice([-1, 0, 1])
        self.dy = choice([-1, 1]) if self.dx == 0 else choice([-1, 0, 1])
        self.way = [(self.dx, 0), (self.dx, self.dy), (0, self.dy), (self.dx, self.dy)]

    def update(self):
        if 0 in (self.dx, self.dy):
            self.rect.move_ip(self.dx * self.speed, self.dy * self.speed)

        elif self.way:
            x, y = self.way.pop()
            self.rect.move_ip(x * self.speed, y * self.speed)

        else:
            self.way = [(self.dx, 0), (self.dx, self.dy), (0, self.dy), (self.dx, self.dy)]

        enemy = pygame.sprite.spritecollideany(self, enemy_sprites)
        if enemy and enemy.cooldown < 0:
            enemy.health -= 34
            enemy.cooldown = 120
