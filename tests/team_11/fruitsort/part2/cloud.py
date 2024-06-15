from preparticle import PreParticle
from config import config

class Cloud:
    def __init__(self):
        self.curr = PreParticle()
        self.next = PreParticle()

    def draw(self, screen, wait):
        self.curr.draw(screen, wait)
        next_fruit_position = (config.next_sushi_pos[0], config.next_sushi_pos[1])
        self.next.draw_small(screen, next_fruit_position)

    def release(self, space):
        return self.curr.release(space)

    def step(self):
        self.curr = self.next
        self.next = PreParticle()

    def replace_current_fruit(self, fruit_type):
        for i, fruit_name in enumerate(config.fruit_names):
            if fruit_name == fruit_type:
                self.curr = PreParticle()
                self.curr.n = i
                self.curr.sprite = config[self.curr.n, "blit"]
                self.curr.radius = config[self.curr.n, "radius"]
                break