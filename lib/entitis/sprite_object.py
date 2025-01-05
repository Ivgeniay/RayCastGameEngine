import pygame as pg
from lib.conf.settings import *
from collections import deque


class Sprites:
    def __init__(self):
        self.sprite_parameters = {
            "sprite_barrel": {
                "sprite": pg.image.load('resources/sprites/barrel/base/0.png').convert_alpha(),
                "viewing_angles": None,
                "shift": 1.0,
                "scale": 0.5,
                "animation": deque(
                    [pg.image.load(f'resources/sprites/barrel/anim/{i}.png').convert_alpha() for i in range(8)]),
                "animation_dist": 800,
                "animation_speed": 10,
                "blocked": True,
                "collision_radius": 41,
            },
            "sprite_pedestal": {
                "sprite": pg.image.load(f"resources/sprites/pedestal/base/0.png").convert_alpha(),
                "viewing_angles": None,
                "shift": 0.6,
                "scale": 0.4,
                "animation": None,
                "animation_dist": None,
                "animation_speed": None,
                "blocked": True,
                "collision_radius": 41,
            },
            "sprite_pin": {
                "sprite": pg.image.load(f"resources/sprites/pin/base/0.png").convert_alpha(),
                "viewing_angles": None,
                "shift": 0.6,
                "scale": 0.4,
                "animation": deque(
                    [pg.image.load(f"resources/sprites/pin/anim/{i}.png").convert_alpha() for i in range(8)]),
                "animation_dist": 800,
                "animation_speed": 10,
                "blocked": True,
                "collision_radius": 41,
            },
            "sprite_devil": {
                "sprite": [pg.image.load(f'resources/sprites/npc/devil/base/{i}.png').convert_alpha() for i in range(8)],
                "viewing_angles": True,
                "shift": -0.2,
                "scale": 1.1,
                "animation": deque(
                    [pg.image.load(f'resources/sprites/npc/devil/anim/{i}.png').convert_alpha() for i in range(8)]),
                "animation_dist": 150,
                "animation_speed": 10,
                "blocked": True,
                "collision_radius": 50,
            },
            "sprite_flame": {
                "sprite": pg.image.load(f'resources/sprites/flame/base/0.png').convert_alpha(),
                "viewing_angles": None,
                "shift": 0.7,
                "scale": 0.6,
                "animation": deque(
                    [pg.image.load(f'resources/sprites/flame/anim/{i}.png').convert_alpha() for i in range(8)]),
                "animation_dist": 800,
                "animation_speed": 5,
                "blocked": False,
                "collision_radius": 0,
            },
        }

        self.list_of_objects = [
            SpriteObject(self.sprite_parameters["sprite_barrel"], (7.1, 2.1)),
            SpriteObject(self.sprite_parameters["sprite_barrel"], (5.9, 2.1)),
            SpriteObject(self.sprite_parameters["sprite_flame"], (6.5, 2.5)),
            SpriteObject(self.sprite_parameters["sprite_devil"], (8.5, 2.5)),
            SpriteObject(self.sprite_parameters["sprite_pin"], (7.5, 2.5)),
            SpriteObject(
                self.sprite_parameters["sprite_pedestal"], (5.5, 3.5)),
        ]


class SpriteObject:
    """" Класс для создания спрайтов

      :param object: объект спрайта выраженный изображении с alpha каналом
      :param static: статичный ли спрайт
      :param pos: позиция спрайта выраженная в виде кортежа (x, y) в упращенных координатах карты (каждая клетка 1х1 в дальнейшем умножается на TILE)
      :param shift: смещение спрайта по высоте
      :param scale: масштаб спрайта
    """

    def __init__(self, parameters, pos: tuple[float, float]):
        self.object = parameters["sprite"]
        self.viewing_angles = parameters["viewing_angles"]
        self.shift = parameters["shift"]
        self.scale = parameters["scale"]
        self.animation = parameters["animation"]
        self.animation_dist = parameters["animation_dist"]
        self.animation_speed = parameters["animation_speed"]
        self.blocked = parameters["blocked"]
        self.collision_radius = parameters["collision_radius"]
        self.animation_count = 0
        self.x, self.y = pos[0] * TILE, pos[1] * TILE
        self.pos = self.x - self.collision_radius // 2, self.y - self.collision_radius // 2

        if self.viewing_angles:
            self.sprite_angles = [frozenset(range(i, i + 45))
                                  for i in range(0, 360, 45)]
            self.sprite_positions = {}
            for angle, pos in zip(self.sprite_angles, self.object):
                self.sprite_positions[angle] = pos

    def object_locate(self, player):

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
        if 0 <= fake_ray <= FAKE_RAYS_RANGE and distance_to_sprite > 30:
            # min(int(PROJ_COEFF / distance_to_sprite), HEIGHT)
            proj_height = min(
                int(PROJ_COEFF / distance_to_sprite * self.scale), DOUBLE_HEIGHT)
            half_proj_height = proj_height // 2
            shift = half_proj_height * self.shift

            # NOTE: выбор спрайта взависимости от угла
            if self.viewing_angles:
                if theta < 0:
                    theta += DOUBLE_PI
                theta = 360 - int(math.degrees(theta))

                for angles in self.sprite_angles:
                    if theta in angles:
                        self.object = self.sprite_positions[angles]
                        break

            # NOTE: анимация спрайта
            sprite_object = self.object
            if (self.animation and self.animation_dist > distance_to_sprite):
                sprite_object = self.animation[0]
                if self.animation_count < self.animation_speed:
                    self.animation_count += 1
                else:
                    self.animation.rotate()
                    self.animation_count = 0

            # NOTE: отрисовка спрайта
            sprite_shift = HALF_HEIGHT - half_proj_height + shift
            sprite_pos = (current_ray * SCALE - half_proj_height, sprite_shift)
            sprite_width = proj_height / self.scale
            sprite = pg.transform.scale(
                sprite_object, (int(proj_height), proj_height))
            return (distance_to_sprite, sprite, sprite_pos)
        else:
            return (False,)
