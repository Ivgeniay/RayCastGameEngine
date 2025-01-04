import pygame as pg
from lib.entitis.player import Player
from lib.conf.settings import *
from lib.graphic.ray_casting import ray_cast
from lib.entitis.map import world_map, mini_map


# TODO: создать пайплайн рендеринга: задник, мир, оружие, UI
class Drawing:
    """Класс для отрисовки игрового мира"""

    def __init__(self, screen: pg.surface, mini_map_screen: pg.surface):
        self.sc = screen
        self.sc_map = mini_map_screen
        self.font = pg.font.SysFont('Arial', 36, bold=True)
        self.textures = {
            "1": pg.image.load('resources/img/wall1.png').convert(),
            "2": pg.image.load('resources/img/wall2.png').convert(),
            "S": pg.image.load('resources/img/sky3.png').convert()
        }

    def background(self, player_angle: float):
        # pg.draw.rect(self.sc, SKYBLUE, (0, 0, WIDTH, HALF_HEIGHT))
        sky_offset = -5 * math.degrees(player_angle) % WIDTH
        self.sc.blit(self.textures["S"], (sky_offset, 0))
        self.sc.blit(self.textures["S"], (sky_offset - WIDTH, 0))
        self.sc.blit(self.textures["S"], (sky_offset + WIDTH, 0))
        pg.draw.rect(self.sc, DARKGRAY, (0, HALF_HEIGHT, WIDTH, HALF_HEIGHT))

    def world(self, world_objects: list):
        for obj in sorted(world_objects, key=lambda n: n[0], reverse=True):
            if obj[0]:
                _, object, obj_pos = obj
                self.sc.blit(object, obj_pos)
        pass

    def fps(self, clock: pg.time.Clock):
        display_fps = str(int(clock.get_fps()))
        self.text('FPS: ' + display_fps, self.font, WIDTH - 160, 5, DARKORANGE)

    def text(self, text: str, font: pg.font.Font, x: int, y: int, color: tuple[int, int, int] = (255, 255, 255)):
        img = font.render(text, True, color)
        self.sc.blit(img, (x, y))

    def mini_map(self, player: Player):
        self.sc_map.fill(BLACK)
        map_x, map_y = player.x // MAP_SCALE, player.y // MAP_SCALE
        pg.draw.line(self.sc_map, GREEN, (int(map_x), int(map_y)), (map_x + MAP_PLAYER_RAY_LENGTH *
                     math.cos(player.angle), map_y + MAP_PLAYER_RAY_LENGTH * math.sin(player.angle)), 1)
        pg.draw.circle(self.sc_map, GREEN, (int(map_x),
                       int(map_y)), MAP_PLAYER_INDICATOR_RADIUS)
        for x, y in mini_map:
            map_wall_rect = pg.Rect(x, y, MAP_TILE, MAP_TILE)
            pg.draw.rect(self.sc_map, DARKBROWN, map_wall_rect)
        self.sc.blit(self.sc_map, MAP_POSITION)
