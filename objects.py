import pygame
from math import ceil

all_sprites = pygame.sprite.Group()
objects_of_game = []


class Object(pygame.sprite.Sprite):
    def __init__(self, x=100, y=100, w=100, h=100):
        super().__init__(all_sprites)
        objects_of_game.append(self)
        self.image = pygame.Surface((w, h))
        self.image.fill('gray')
        self.rect = pygame.Rect(x, y, w, h)

        self.speed = 1
        self.health = 100
        self.experience = 0
        self.dx = 0
        self.dy = 0


class Character(Object):
    def __init__(self, *args):
        super().__init__(*args)
        self.image.fill('green')
        self.items = {}

    def update(self):
        self.rect.move_ip(self.dx * self.speed, self.dy * self.speed)

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

    def add_item(self, item):
        if item in self.items.keys():
            self.items[item]['level'] += 1
        else:
            self.items[item] = {'level': 1, 'time': 0}


class Enemy(Object):
    def __init__(self, *args):
        super().__init__(*args)
        self.image.fill('red')
        self.way = []

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
