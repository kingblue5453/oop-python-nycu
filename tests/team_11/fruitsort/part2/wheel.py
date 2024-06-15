import pygame
import random
from config import config

class Wheel:
    def __init__(self):
        self.wheel_image = config.wheel_image
        self.pointer_image = config.pointer_image
        self.wheel_pos = config.wheel_pos
        self.fruit_names = config.fruit_names
        self.current_fruit = random.choice(self.fruit_names)
        self.spinning = False
        self.spin_speed = 0
        self.max_spin_speed = 480

    def start_spin(self):
        self.spinning = True
        self.spin_speed = self.max_spin_speed

    def stop_spin(self):
        self.spinning = False

    def update(self):
        if self.spinning:
            self.spin_speed *= 0.95
            if self.spin_speed < 1:
                self.spinning = False
                self.spin_speed = 0
                self.current_fruit = random.choice(self.fruit_names)

    def draw(self, screen):
        screen.blit(self.wheel_image, self.wheel_pos)
        if self.spinning:
            self.update()
        screen.blit(self.pointer_image, self.wheel_pos)

    def get_current_fruit(self):
        return self.current_fruit
