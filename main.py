import pygame as pg
from lib.conf.settings import *
from lib.entitis.player import Player
import math
from lib.entitis.map import map_resolutions
from lib.graphic.ray_casting import ray_casting_wall
from lib.graphic.drawing import Drawing
from lib.entitis.sprite_object import *


pg.init()
sc = pg.display.set_mode((WIDTH, HEIGHT))
pg.mouse.set_visible(False)
sc_map = pg.Surface(  # MINIMAP_RES)
    (MAP_TILE * map_resolutions[0], MAP_TILE * map_resolutions[1]))
sprites = Sprites()
clock = pg.time.Clock()
player = Player(sprites)
drawing = Drawing(sc, sc_map)


while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit()

    player.movement()
    sc.fill(BLACK)

    drawing.background(player.angle)
    walls = ray_casting_wall(player, drawing.textures)
    drawing.world(walls + [obj.object_locate(player)
                  for obj in sprites.list_of_objects])
    drawing.fps(clock)
    drawing.mini_map(player)

    pg.display.flip()
    # clock.tick()
    clock.tick(FPS)
