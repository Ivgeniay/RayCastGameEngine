from lib.conf.settings import *

text_map = [
    '111111111111',
    '1..........1',
    '1..........1',
    '1..........1',
    '1.....2....1',
    '1.....2....1',
    '1..........1',
    '1..........1',
    '1..........1',
    '1..........1',
    '1..........1',
    '111111111111',
]
map_resolutions = (len(text_map[0]), len(text_map))
world_map = {}
mini_map = set()
for j, row in enumerate(text_map):
    for i, char in enumerate(row):
        if char != '.':
            mini_map.add((i * MAP_TILE, j * MAP_TILE))
            if char == '1':
                world_map[(i * TILE, j * TILE)] = '1'
            elif char == '2':
                world_map[(i * TILE, j * TILE)] = '2'

default_texture_index = "1"
