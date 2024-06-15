import pygame
import numpy as np
from config import config
from particle import Particle

rng = np.random.default_rng()


class PreParticle:

    # 初始生成水果是隨機挑前五個水果中的其中一個
    def __init__(self):
        self.x = config.screen.width // 2
        self.n = rng.integers(0, 5)
        self.radius = config[self.n, "radius"]
        self.sprite = config[self.n, "blit"]

    def draw(self, screen, wait):
        screen.blit(config.cloud_blit, (self.x, 100))
        if not wait:
            pygame.draw.line(
                screen,
                color = config.screen.white,
                start_pos = (self.x, config.pad.line_top),
                end_pos = (self.x, config.pad.line_bot),
                width = 2,
            )
            screen.blit(self.sprite, self.sprite_pos)

    def draw_small(self, screen, position):
        # 绘制缩小版水果
        small_sprite = pygame.transform.scale(self.sprite, (58, 58))
        screen.blit(small_sprite, position)

    @property
    def sprite_pos(self):
        return self._sprite_pos((self.x, config.pad.top))

    def _sprite_pos(self, pos):
        x, y = pos
        w, h = self.sprite.get_size()
        a, b = config[self.n, "offset"]
        return x - w / 2 + a, y - h / 2 + b

    def set_x(self, x):
        left_lim = config.pad.left + self.radius    # 水果移動的左界線
        right_lim = config.pad.right - self.radius  # 水果移動的右界線
        self.x = np.clip(x, left_lim, right_lim)    # 水果移動的範圍

    def release(self, space):
        return Particle((self.x, config.pad.top), self.n, space)
