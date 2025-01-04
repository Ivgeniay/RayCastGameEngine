import pygame as pg
from lib.conf.settings import *
from lib.entitis.player import Player


class Sprites:
    def __init__(self):
        self.sprite_type = {
            "barrel": pg.image.load('resources/sprites/barrel/0.png').convert_alpha(),
            "pedestal": pg.image.load('resources/sprites/pedestal/0.png').convert_alpha(),
            "devil": [pg.image.load(f'resources/sprites/devil/{i}.png').convert_alpha() for i in range(8)]
        }
        self.list_of_objects = [
            SpriteObject(self.sprite_type["barrel"],
                         True, (7.1, 2.1), 1.2, 0.8),
            SpriteObject(self.sprite_type["barrel"],
                         True, (5.9, 2.1), 1.2, 0.8),
            SpriteObject(self.sprite_type["pedestal"],
                         True, (6.5, 2.5), 1.2, 0.8),
            SpriteObject(self.sprite_type["devil"],
                         False, (8.5, 2.5), 0.0, 1),
        ]


class SpriteObject:
    """" Класс для создания спрайтов

      :param object: объект спрайта выраженный изображении с alpha каналом
      :param static: статичный ли спрайт
      :param pos: позиция спрайта выраженная в виде кортежа (x, y) в упращенных координатах карты (каждая клетка 1х1 в дальнейшем умножается на TILE)
      :param shift: смещение спрайта по высоте
      :param scale: масштаб спрайта
    """

    def __init__(self, object, is_static: bool, pos: tuple[float, float], shift: float, scale: float):
        self.object = object
        self.is_static = is_static
        self.pos = self.x, self.y = pos[0] * TILE, pos[1] * TILE
        self.shift = shift
        self.scale = scale

        if not is_static:
            self.sprite_angles = [frozenset(range(i, i + 45))
                                  for i in range(0, 360, 45)]
            self.sprite_positions = {}
            for angle, pos in zip(self.sprite_angles, self.object):
                self.sprite_positions[angle] = pos

    def object_locate(self, player: Player, walls: list):
        fake_walls0 = [walls[0] for i in range(FAKE_RAYS)]
        fake_walls1 = [walls[-1] for i in range(FAKE_RAYS)]
        fake_walls = fake_walls0 + walls + fake_walls1

        dx, dy = self.x - player.x, self.y - player.y
        distance_to_sprite = math.sqrt(dx ** 2 + dy ** 2)

        theta = math.atan2(dy, dx)
        gamma = theta - player.angle
        if dx > 0 and 180 <= math.degrees(player.angle) <= 360 or dx < 0 and dy < 0:
            gamma += DOUBLE_PI

        delta_rays = int(gamma / DELTA_ANGLE)
        current_ray = CENTER_RAY + delta_rays
        distance_to_sprite *= math.cos(HALF_FOV - current_ray * DELTA_ANGLE)

        fake_ray = current_ray + FAKE_RAYS
        if 0 <= fake_ray <= NUM_RAYS - 1 + 2 * FAKE_RAYS and distance_to_sprite < fake_walls[fake_ray][0]:
            # min(int(PROJ_COEFF / distance_to_sprite), HEIGHT)
            proj_height = int(PROJ_COEFF / distance_to_sprite * self.scale)
            half_proj_height = proj_height // 2
            shift = half_proj_height * self.shift

            if not self.is_static:
                if theta < 0:
                    theta += DOUBLE_PI
                theta = 360 - int(math.degrees(theta))

                for angles in self.sprite_angles:
                    if theta in angles:
                        self.object = self.sprite_positions[angles]
                        break

            sprite_shift = HALF_HEIGHT - half_proj_height + shift
            sprite_pos = (current_ray * SCALE - half_proj_height, sprite_shift)
            sprite_width = proj_height / self.scale
            sprite = pg.transform.scale(
                self.object, (int(sprite_width), proj_height))
            return (distance_to_sprite, sprite, sprite_pos)
        else:
            return (False,)
