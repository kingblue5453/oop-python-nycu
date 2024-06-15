import sys
import pygame
import pymunk
import random
from collections import deque
from cloud import Cloud
from collision import collide
from config import config, CollisionTypes
from particle import Particle
from text import score, gameover
from wall import Wall

# Initialize Pygame and create game window
pygame.init()
screen = pygame.display.set_mode((config.screen.width, config.screen.height))
pygame.display.set_caption("PySuika")
clock = pygame.time.Clock()

# Function to show the start screen
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

# Function to show the game over screen
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

# Show the start screen
show_start_screen(screen, config.start_image, config.start_button_image, config.start_button_pos)

# Initialize physics
space = pymunk.Space()
space.gravity = (0, config.physics.gravity)
space.damping = config.physics.damping
space.collision_bias = config.physics.bias

# Create walls and cloud
left = Wall(config.top_left, config.bot_left, space)
bottom = Wall(config.bot_left, config.bot_right, space)
right = Wall(config.bot_right, config.top_right, space)
walls = [left, bottom, right]
cloud = Cloud()

# Game state
wait_for_next = 0
game_over = False

# Collision handler
handler = space.add_collision_handler(CollisionTypes.PARTICLE, CollisionTypes.PARTICLE)
handler.begin = collide
handler.data["score"] = 0

# Initialize the sushi queue
sushi_queue = deque()
for _ in range(3):  # Initialize with 3 sushi items
    sushi_index = random.randint(0, len(config.fruit_names) - 1)
    sushi_image = config.config[config.fruit_names[sushi_index]]["blit"]
    sushi_queue.append(sushi_image)

while not game_over:
    # Handle user input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN and wait_for_next == 0:
            cloud.release(space)
            wait_for_next = config.screen.delay
            # Update the sushi queue
            sushi_queue.popleft()
            new_sushi_index = random.randint(0, len(config.fruit_names) - 1)
            new_sushi_image = config.config[config.fruit_names[new_sushi_index]]["blit"]
            sushi_queue.append(new_sushi_image)

    if wait_for_next > 1:
        wait_for_next -= 1
    if wait_for_next == 1:
        cloud.step()
        wait_for_next -= 1

    cloud.curr.set_x(pygame.mouse.get_pos()[0])

    # Draw background and particles
    screen.blit(config.background_blit, (0, 0))
    cloud.draw(screen, wait_for_next)

    for p in space.shapes:
        if isinstance(p, Particle):
            p.draw(screen)
            if p.pos[1] < config.pad.killy and p.has_collided:
                gameover(screen)
                game_over = True

    score(handler.data['score'], screen)

    # Draw the next sushi
    next_sushi_image = sushi_queue[0]
    screen.blit(next_sushi_image, config.next_sushi_pos)

    # Update the game state
    space.step(1 / config.screen.fps)
    pygame.display.update()
    clock.tick(config.screen.fps)

# Show the game over screen
show_game_over_screen(screen, config.game_over_image, config.again_button_image, config.again_button_pos)

# Game over loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
            pygame.quit()
            sys.exit()
