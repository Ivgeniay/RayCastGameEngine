import pygame as pg
from lib.conf.settings import *
from lib.entitis.map import world_map, default_texture_index, WORLD_WIDTH, WORLD_HEIGHT
from lib.entitis.player import Player
from numba import njit


# NOTE: функция для привязки координат к сетке
@njit(fastmath=True)
def mapping(a, b):
    return (a // TILE) * TILE, (b // TILE) * TILE


@njit(fastmath=True)
def ray_cast(player_position, player_angle, world_map):
    casted_walls = []

    cur_angle = player_angle - HALF_FOV
    xo, yo = player_position
    xm, ym = mapping(xo, yo)
    texture_h, texture_v = default_texture_index, default_texture_index
    # NOTE: нахождение переечения с сеткой
    for ray in range(NUM_RAYS):
        sin_a = math.sin(cur_angle)
        cos_a = math.cos(cur_angle)

        # NOTE: с вертикальной линией сетки вертикали
        x, dx = (xm + TILE, 1) if cos_a >= 0 else (xm, -1)
        for i in range(0, WORLD_WIDTH, TILE):
            depth_v = (x - xo) / cos_a
            yv = yo + depth_v * sin_a
            tile_v = mapping(x + dx, yv)
            if tile_v in world_map:
                texture_v = world_map[tile_v]
                break
            x += dx * TILE

        # NOTE: с горизонтальной линией сетки горизонтали
        y, dy = (ym + TILE, 1) if sin_a >= 0 else (ym, -1)
        for i in range(0, WORLD_HEIGHT, TILE):
            depth_h = (y - yo) / sin_a
            xh = xo + depth_h * cos_a
            tile_h = mapping(xh, y + dy)
            if tile_h in world_map:
                texture_h = world_map[tile_h]
                break
            y += dy * TILE

        # NOTE: выбор ближайшего столкновения с стеной и отрисовка
        depth, offset, texture = (depth_v, yv, texture_v) if depth_v < depth_h else (
            depth_h, xh, texture_h)
        offset = int(offset) % TILE
        depth *= math.cos(player_angle - cur_angle)
        depth = max(depth, 0.00001)

        proj_height = min(int(PROJ_COEFF / depth), PENTA_HEIGHT)

        if texture is None:
            texture = default_texture_index

        casted_walls.append((depth, offset, proj_height, texture))
        cur_angle += DELTA_ANGLE

    return casted_walls


def ray_casting_wall(player: Player, textures):
    casted_wall = ray_cast(player.position, player.angle, world_map)
    walls = []

    for ray, casted in enumerate(casted_wall):
        depth, offset, proj_height, texture = casted

        wall_column = textures[texture].subsurface(
            offset * TEXTURE_SCALE, 0, TEXTURE_SCALE, TEXTURE_HEIGHT)
        wall_column = pg.transform.scale(wall_column, (SCALE, proj_height))
        wall_pos = (ray * SCALE, HALF_HEIGHT - proj_height // 2)
        walls.append((depth, wall_column, wall_pos))
    return walls


# NOTE: алгоритм Брезенхема. На вход принимает координаты игрока, угол направления взгляда и возвращает
# глубину проникновения луча в стену и координаты точки столкновения с ней
def ray(x, y, angle):
    """ Функция принимает координаты игрока, угол направления взгляда и возвращает глубину проникновения 
    луча в стену и координаты точки столкновения"""
    sin_a = math.sin(angle)
    cos_a = math.cos(angle)
    for depth in range(MAX_DEPTH):
        _x = x + depth * cos_a
        _y = y + depth * sin_a
        if (_x // TILE * TILE, _y // TILE * TILE) in world_map:
            return (depth, _x, _y)
    return MAX_DEPTH
