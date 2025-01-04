from lib.conf.settings import *
import pygame as pg
import math


class Player:
    def __init__(self):
        self.x, self.y = PLAYER_START_POS
        self.angle = PLAYER_START_ANGLE

    @property
    def position(self) -> tuple[int, int]:
        return self.x, self.y

    def movement(self):
        keys = pg.key.get_pressed()
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)
        if keys[pg.K_w]:
            self.x += PLAYER_SPEED * cos_a
            self.y += PLAYER_SPEED * sin_a
        if keys[pg.K_s]:
            self.x -= PLAYER_SPEED * cos_a
            self.y -= PLAYER_SPEED * sin_a
        if keys[pg.K_a]:
            self.x += PLAYER_SPEED * sin_a
            self.y -= PLAYER_SPEED * cos_a
        if keys[pg.K_d]:
            self.x -= PLAYER_SPEED * sin_a
            self.y += PLAYER_SPEED * cos_a
        if keys[pg.K_LEFT]:
            self.angle -= PLAYER_ROTATION_SPEED
        if keys[pg.K_RIGHT]:
            self.angle += PLAYER_ROTATION_SPEED

        self.angle %= DOUBLE_PI
