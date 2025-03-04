from objects import *
from other import *


def show_screen(screen, state):
    if state:
        text = f'Счёт: {results['max_count']}'

    else:
        text = 'ВЫЖИВАНИЕ В КИБЕРПАНКЕ'

    background = pygame.transform.scale(load_image('background.jpg'), screen.get_size())
    screen.blit(background, (0, 0))
    x = screen.get_size()[0] / 2
    y = screen.get_size()[1] / 2 - screen.get_size()[1] / 10
    draw_outline_text(screen, text, 'cyan', x, y, 40, 2)
    pygame.display.flip()


def main():
    pygame.init()
    size = width, height = 1080, 720
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('ВЫЖИВАНИЕ В КИБЕРПАНКЕ')
    show_screen(screen, 0)

    clock = pygame.time.Clock()
    running = True
    state = 0

    while state in (0, 2):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if state == 0:
                    state = 1

                else:
                    state = 0
                    show_screen(screen, state)

    character = Character(200, 200)
    enemy = Enemy(0, 0)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                break

            if event.type == pygame.KEYDOWN and event.key in (pygame.K_a, pygame.K_w, pygame.K_d, pygame.K_s):
                character.move(event.key, True)

            if event.type == pygame.KEYUP and event.key in (pygame.K_a, pygame.K_w, pygame.K_d, pygame.K_s):
                character.move(event.key, False)

        for sprite in all_sprites:
            if type(sprite) is Enemy and sprite.health < 0:
                state = 2
                break

            elif sprite.health < 0:
                all_sprites.remove(sprite)
                del sprite

            elif type(sprite) is Enemy:
                sprite.update(character.rect.x + character.rect.w // 2, character.rect.y + character.rect.h // 2)

            else:
                sprite.update()

        screen.fill('black')
        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == '__main__':
    main()
