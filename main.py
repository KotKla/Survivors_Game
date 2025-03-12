import random

from objects import *
from other import *
import sys

pygame.init()
size = width, height = 1080, 720
screen = pygame.display.set_mode(size)


def terminate():
    pygame.quit()
    sys.exit()


def end_screen(count):
    intro_text = [f"счет:{count}"]
    fon = pygame.transform.scale(load_image('end.jpg'), size)
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 80)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 300
        intro_rect.top = text_coord
        intro_rect.x = 500
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()

        pygame.display.flip()


def start_screen():
    fon = pygame.transform.scale(load_image('start.png'), size)
    screen.blit(fon, (0, 0))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                return
        pygame.display.flip()


start_screen()


def main():
    pygame.display.set_caption('Survivors')

    character = Character(540, 360)
    MYEVENTTYPE = pygame.USEREVENT + 1
    pygame.time.set_timer(MYEVENTTYPE, 5000)
    clock = pygame.time.Clock()
    coords = [0, 720]
    count = 0
    running = True
    fon = pygame.transform.scale(load_image('map.jpg'), size)
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN and event.key in (pygame.K_a, pygame.K_w, pygame.K_d, pygame.K_s):
                character.move(event.key, True)

            if event.type == pygame.KEYUP and event.key in (pygame.K_a, pygame.K_w, pygame.K_d, pygame.K_s):
                character.move(event.key, False)
            if event.type == MYEVENTTYPE:
                enemy = Enemy(random.choice(coords), random.choice(coords))
            # if event.type == pygame.KEYDOWN and event.key in (pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4):
            #     if event.key == pygame.K_1:
            #         character.add_item(0)
            #     if event.key == pygame.K_2:
            #             character.add_item(1)
            #     if event.key == pygame.K_3:
            #             character.add_item(2)
            #     if event.key == pygame.K_4:
            #             character.add_item(3)

        for sprite in all_sprites:
            if type(sprite) is Enemy:
                sprite.update(character.rect.x + character.rect.w // 2, character.rect.y + character.rect.h // 2)
            else:
                sprite.update()
        for sprite in enemy_sprites:
            if sprite.health < 0:
                all_sprites.remove(sprite)
                del sprite
                count += 1
        for sprite in character_sprites:
            if sprite.health < 0:
                end_screen(count)
        screen.blit(fon, (0, 0))
        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == '__main__':
    main()
