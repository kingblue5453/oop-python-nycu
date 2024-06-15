import sys
import pygame
import pymunk
import random
from cloud import Cloud
from collision import collide
from config import config, CollisionTypes
from particle import Particle
from text import score, gameover
from wall import Wall
from wheel import Wheel

# 初始化 Pygame 與遊戲窗口
pygame.init()
screen = pygame.display.set_mode((config.screen.width, config.screen.height))
pygame.display.set_caption("Sushi Merge!")
clock = pygame.time.Clock()

# 開始畫面
def show_start_screen(screen, start_image, start_button_image, start_button_pos):
    screen.blit(start_image, (0, 0))
    button_rect = start_button_image.get_rect(topleft=start_button_pos)
    screen.blit(start_button_image, button_rect.topleft)
    pygame.display.update()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    waiting = False

# 結束畫面
def show_game_over_screen(screen, game_over_image, again_button_image, again_button_pos):
    screen.blit(game_over_image, (0, 0))
    button_rect = again_button_image.get_rect(topleft=again_button_pos)
    screen.blit(again_button_image, button_rect.topleft)
    pygame.display.update()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    waiting = False

# 初始化物理空間和各種圖片
def initialize_game():
    space = pymunk.Space()
    space.gravity = (0, config.physics.gravity)
    space.damping = config.physics.damping
    space.collision_bias = config.physics.bias

    left = Wall(config.top_left, config.bot_left, space)
    bottom = Wall(config.bot_left, config.bot_right, space)
    right = Wall(config.bot_right, config.top_right, space)
    walls = [left, bottom, right]

    cloud = Cloud()
    wheel = Wheel()

    return space, cloud, wheel

# 主循環
def main_game_loop(screen):
    space, cloud, wheel = initialize_game()
    game_over = False
    spin_active = False
    wait_for_next = 0
    handler = space.add_collision_handler(CollisionTypes.PARTICLE, CollisionTypes.PARTICLE)
    handler.begin = collide
    handler.data["score"] = 0
    GAME_OVER_HEIGHT = config.pad.killy
    fruit_names = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten"]
    next_fruit = random.choice(fruit_names)

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                cloud.release(space)
                wait_for_next = config.screen.delay
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if spin_active:
                        wheel.stop_spin()
                    else:
                        wheel.start_spin()
                    spin_active = not spin_active

        if wait_for_next > 1:
            wait_for_next -= 1
        if wait_for_next == 1:
            cloud.step()
            wait_for_next -= 1

        cloud.curr.set_x(pygame.mouse.get_pos()[0])

        screen.blit(config.background_blit, (0, 0))
        cloud.draw(screen, wait_for_next)
        wheel.update()
        wheel.draw(screen)

        # 死亡之線
        pygame.draw.line(screen, (205, 133, 63), (355, GAME_OVER_HEIGHT), (config.screen.width, GAME_OVER_HEIGHT), 5)

        for p in space.shapes:
            if isinstance(p, Particle):
                p.draw(screen)
                if p.pos[1] < config.pad.killy and p.has_collided:
                    gameover(screen)
                    game_over = True

        score(handler.data['score'], screen)

        space.step(1 / config.screen.fps)
        pygame.display.update()
        clock.tick(config.screen.fps)

    return game_over

# 起床重睡,遊戲重玩
def start_game(screen):
    show_start_screen(screen, config.start_image, config.start_button_image, config.start_button_pos)
    while True:
        game_over = main_game_loop(screen)
        if game_over:
            show_game_over_screen(screen, config.game_over_image, config.again_button_image, config.again_button_pos)
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            mouse_pos = pygame.mouse.get_pos()
                            button_rect = config.again_button_image.get_rect(topleft=config.again_button_pos)
                            if button_rect.collidepoint(mouse_pos):
                                return True

# 主程序入口
if __name__ == "__main__":
    while True:
        if not start_game(screen):
            break
