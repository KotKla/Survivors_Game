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
    fon = pygame.transform.scale(load_image('start.jfif'), size)
    intro_text = f"счет:{count}"
    screen.blit(fon, (0, 0))
    x = width / 2
    y = height / 2 - height / 10
    draw_text(x - 2, y - 2, intro_text, "black", 40, screen)
    draw_text(x + 2, y - 2, intro_text, "black", 40, screen)
    draw_text(x - 2, y + 2, intro_text, "black", 40, screen)
    draw_text(x + 2, y + 2, intro_text, "black", 40, screen)
    draw_text(x, y, intro_text, "cyan", 40, screen)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()

        pygame.display.flip()


def start_screen():
    fon = pygame.transform.scale(load_image('start.jfif'), size)
    screen.blit(fon, (0, 0))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()


start_screen()


def main():
    pygame.display.set_caption('Survivors')

    character = Character(200, 200)
    enemy = Enemy(0, 0)

    clock = pygame.time.Clock()
    count = 0
    running = True
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN and event.key in (pygame.K_a, pygame.K_w, pygame.K_d, pygame.K_s):
                character.move(event.key, True)

            if event.type == pygame.KEYUP and event.key in (pygame.K_a, pygame.K_w, pygame.K_d, pygame.K_s):
                character.move(event.key, False)

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
                count += 1
                del sprite
        for sprite in character_sprites:
            if sprite.health < 0:
                end_screen(count)
        screen.fill('black')
        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == '__main__':
    main()
