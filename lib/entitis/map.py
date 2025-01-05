from lib.conf.settings import *
import pygame as pg
from numba.core import types
from numba.typed import Dict
from numba import int32, types

_ = False
matrix_map = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, _, _, _, 2, _, _, _, _, 1],
    [1, _, _, _, _, 3, _, _, _, _, _, 1],
    [1, _, 4, 4, 3, _, _, _, _, _, _, 1],
    [1, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, _, _, _, _, _, _, _, _, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

map_resolutions = (len(matrix_map[0]), len(matrix_map))
WORLD_WIDTH = map_resolutions[0] * TILE
WORLD_HEIGHT = map_resolutions[1] * TILE

world_map = Dict.empty(key_type=types.UniTuple(int32, 2), value_type=int32)
mini_map = set()
collision_walls = []
for j, row in enumerate(matrix_map):
    for i, texture_index in enumerate(row):
        if texture_index:
            collision_walls.append(pg.Rect(i * TILE, j * TILE, TILE, TILE))
            mini_map.add((i * MAP_TILE, j * MAP_TILE))
            if texture_index == 1:
                world_map[(i * TILE, j * TILE)] = 1
            elif texture_index == 2:
                world_map[(i * TILE, j * TILE)] = 2
            elif texture_index == 3:
                world_map[(i * TILE, j * TILE)] = 3
            elif texture_index == 4:
                world_map[(i * TILE, j * TILE)] = 4

default_texture_index = 1
