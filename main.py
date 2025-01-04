import pygame as pg
from lib.conf.settings import *
from lib.entitis.player import Player
import math
from lib.entitis.map import map_resolutions
from lib.graphic.ray_casting import ray_cast
from lib.graphic.drawing import Drawing
from lib.entitis.sprite_object import *


pg.init()
sc = pg.display.set_mode((WIDTH, HEIGHT))
sc_map = pg.Surface(
    (MAP_TILE * map_resolutions[0], MAP_TILE * map_resolutions[1]))
# sc_map = pg.Surface((WIDTH // MAP_SCALE, HEIGHT // 2))
sprites = Sprites()
clock = pg.time.Clock()
player = Player()
drawing = Drawing(sc, sc_map)

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit()

    player.movement()
    sc.fill(BLACK)

    drawing.background(player.angle)
    # drawing.world(player.position, player.angle)
    walls = ray_cast(player, drawing.textures)
    drawing.world(walls + [obj.object_locate(player, walls)
                  for obj in sprites.list_of_objects])
    drawing.fps(clock)
    drawing.mini_map(player)

    pg.display.flip()
    # clock.tick()
    clock.tick(FPS)
