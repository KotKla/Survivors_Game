import os
import pygame

all_sprites = pygame.sprite.Group()
with open('results.txt') as file:
    results = {}
    for line in file.readlines():
        results[line.strip().split(';')[0]] = int(line.strip().split(';')[1])


def load_image(name, color_key=None):
    fullname = os.path.join('sprites\\other', name)
    try:
        image = pygame.image.load(fullname).convert()
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
            image.set_colorkey(color_key)
        else:
            image = image.convert_alpha()
    return image


def draw_text(window, string, color, x, y, size):
    font = pygame.font.SysFont("Impact", size)
    text = font.render(string, True, color)
    textbox = text.get_rect()
    textbox.center = (x, y)
    window.blit(text, textbox)


def draw_outline_text(window, string, color, x, y, size, outline):
    draw_text(window, string, 'black', x - outline, y - outline, size)
    draw_text(window, string, 'black', x + outline, y + outline, size)
    draw_text(window, string, 'black', x + outline, y - outline, size)
    draw_text(window, string, 'black', x - outline, y + outline, size)

    draw_text(window, string, color, x, y, size)

# class AnimatedSprite(pygame.sprite.Sprite):
#     def __init__(self, sheet, columns, rows, x=100, y=100, w=100, h=100):
#         super().__init__(all_sprites)
#         self.frames = []
#         self.cut_sheet(sheet, columns, rows)
#         self.cur_frame = 0
#         self.image = self.frames[self.cur_frame]
#         self.rect = self.rect.move(x, y)
#
#     def cut_sheet(self, sheet, columns, rows):
#         self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
#                                 sheet.get_height() // rows)
#         for j in range(rows):
#             for i in range(columns):
#                 frame_location = (self.rect.w * i, self.rect.h * j)
#                 self.frames.append(sheet.subsurface(pygame.Rect(
#                     frame_location, self.rect.size)))
#
#     def update(self):
#         self.cur_frame = (self.cur_frame + 1) % len(self.frames)
#         self.image = self.frames[self.cur_frame]
