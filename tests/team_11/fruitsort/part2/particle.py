import pygame
import pymunk
import numpy as np
from config import config, CollisionTypes


# 用 pymunk 模擬粒子碰撞
class Particle(pymunk.Circle):

    # 把 config.yaml 的 physics 數據透過 config 類搬過來
    def __init__(self, pos, n, space):
        self.n = n % 11
        super().__init__(
            body = pymunk.Body(body_type=pymunk.Body.DYNAMIC),
            radius = config[self.n, "radius"],
        ) 
        self.body.position = tuple(pos)
        self.density = config.physics.density
        self.elasticity = config.physics.elasticity
        self.collision_type = CollisionTypes.PARTICLE
        self.friction = config.physics.fruit_friction
        self.has_collided = False
        self.alive = True
        space.add(self.body, self)

    # 只要水果還存在,就繪製在screen上
    def draw(self, screen):
        if self.alive:
            sprite = pygame.transform.rotate(
                config[self.n, "blit"].copy(),
                -self.body.angle * 180/np.pi,
            )
            screen.blit(sprite, self.sprite_pos(sprite))
    
    # 碰撞合成新水果後,殺掉舊水果
    def kill(self, space):
        space.remove(self.body, self)
        self.alive = False

    @property
    def pos(self):
        return np.array(self.body.position)

    # 計算水果在 screen 上的位置
    def sprite_pos(self, sprite):
        x, y = self.body.position
        w, h = sprite.get_size()             # 旋轉中的水果的寬與高
        a, b = self.sprite_offset            # 旋轉中的水果的偏移量
        return x - w / 2 + a, y - h / 2 + b  # 對齊（x,y)和 w & h 的圖片中心,並加上偏移量 a, b

    @property
    def sprite_offset(self):
        ang = self.body.angle                     # 旋轉角度
        mat = np.array([                          # 旋轉矩陣
            [np.cos(ang), -np.sin(ang)],
            [np.sin(ang), np.cos(ang)],
        ])
        arr = np.array(config[self.n, "offset"])  # 把初始 offset 轉換程 np.array 
        return mat @ arr                          # 回傳矩陣乘法
