from objects import *


def main():
    pygame.init()
    size = 500, 500
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Survivors')

    character = Character(200, 200)
    enemy = Enemy(0, 0)

    clock = pygame.time.Clock()
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
            if sprite.health < 0:
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
