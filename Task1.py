import os
import sys

import pygame

FPS = 50
WIDTH = 550
HEIGHT = 550


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ["Перемещение Героя", "",
                  "Камера"]

    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


def load_level(filename):
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)


def generate_level(level):
    new_player, x, y = None, None, None
    x1, y1 = None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                x1, y1 = x, y
    print(x, y)
    # вернем игрока, а также размер поля в клетках
    return Player(x1, y1), x, y


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Перемещение Героя')
    screen = pygame.display.set_mode((550, 550))

    # основной персонаж
    player = None

    tile_images = {
        'wall': load_image('box.png'),
        'empty': load_image('grass.png')
    }
    player_image = load_image('mar.png')

    tile_width = tile_height = 50

    # группы спрайтов
    all_sprites = pygame.sprite.Group()
    tiles_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()

    player, level_x, level_y = generate_level(load_level('map2.txt'))

    running = True
    clock = pygame.time.Clock()
    fps = 50
    start_screen()

    size = width, height = (level_x + 1) * 50, (level_y + 1) * 50
    screen = pygame.display.set_mode(size)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    player.rect.y = max(player.rect.y - 50, 5)
                elif event.key == pygame.K_DOWN:
                    player.rect.y = min(player.rect.y + 50, height - 45)
                elif event.key == pygame.K_LEFT:
                    player.rect.x = max(player.rect.x - 50, 15)
                elif event.key == pygame.K_RIGHT:
                    player.rect.x = min(player.rect.x + 50, width - 35)

                for i in all_sprites:
                    if i.image == tile_images['wall'] and i.rect.colliderect(player.rect):
                        if event.key == pygame.K_UP:
                            player.rect.y += 50
                        elif event.key == pygame.K_DOWN:
                            player.rect.y -= 50
                        elif event.key == pygame.K_LEFT:
                            player.rect.x += 50
                        elif event.key == pygame.K_RIGHT:
                            player.rect.x -= 50
        screen.fill((0, 0, 0))

        all_sprites.draw(screen)
        clock.tick(fps)
        pygame.display.flip()
    pygame.quit()