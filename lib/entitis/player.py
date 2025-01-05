from lib.entitis.sprite_object import Sprites
from lib.entitis.map import collision_walls
from lib.conf.settings import *
import pygame as pg
import math


class Player:
    def __init__(self, sprites: Sprites):
        self.x, self.y = PLAYER_START_POS
        self.angle = PLAYER_START_ANGLE
        self.sprites = sprites

        # NOTE: параметры коллизии
        self.side = PLAYER_COLLISION_RADIUS
        self.rect = pg.Rect(*self.position, self.side, self.side)
        self.collision_sprites = [pg.Rect(
            *obj.pos, obj.collision_radius, obj.collision_radius) for obj in sprites.list_of_objects if obj.blocked]
        self.collision_list = collision_walls + self.collision_sprites

    @property
    def position(self) -> tuple[int, int]:
        return self.x, self.y

    def detect_collision(self, dx: float, dy: float):
        next_rect = self.rect.copy()
        next_rect.move_ip(dx, dy)
        hit_indexes = next_rect.collidelistall(self.collision_list)

        if len(hit_indexes):
            delta_x, delta_y = 0, 0
            for hit_index in hit_indexes:
                hit_rect = self.collision_list[hit_index]
                if dx > 0:
                    delta_x += next_rect.right - hit_rect.left
                if dx < 0:
                    delta_x += hit_rect.right - next_rect.left
                if dy > 0:
                    delta_y += next_rect.bottom - hit_rect.top
                if dy < 0:
                    delta_y += hit_rect.bottom - next_rect.top
            if abs(delta_x - delta_y) < 10:
                dx, dy = 0, 0
            elif delta_x > delta_y:
                dy = 0
            elif delta_y > delta_x:
                dx = 0

        self.x += dx
        self.y += dy

    def movement(self):
        self.key_control()
        self.mouse_motion()
        self.rect.center = self.position
        self.angle %= DOUBLE_PI

    def mouse_motion(self):
        if pg.mouse.get_focused():
            difference = pg.mouse.get_pos()[0] - HALF_WIDTH
            pg.mouse.set_pos((HALF_WIDTH, HALF_HEIGHT))
            self.angle += difference * MOUSE_SENS

    def key_control(self):
        keys = pg.key.get_pressed()
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)

        if keys[pg.K_ESCAPE]:
            pg.quit()
            exit()

        if keys[pg.K_w]:
            dx = PLAYER_SPEED * cos_a
            dy = PLAYER_SPEED * sin_a
            self.detect_collision(dx, dy)

        if keys[pg.K_s]:
            dx = -PLAYER_SPEED * cos_a
            dy = -PLAYER_SPEED * sin_a
            self.detect_collision(dx, dy)

        if keys[pg.K_a]:
            dx = PLAYER_SPEED * sin_a
            dy = -PLAYER_SPEED * cos_a
            self.detect_collision(dx, dy)

        if keys[pg.K_d]:
            dx = -PLAYER_SPEED * sin_a
            dy = PLAYER_SPEED * cos_a
            self.detect_collision(dx, dy)

        if keys[pg.K_LEFT]:
            self.angle -= PLAYER_ROTATION_SPEED
        if keys[pg.K_RIGHT]:
            self.angle += PLAYER_ROTATION_SPEED
