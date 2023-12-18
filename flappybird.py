import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 400, 600
FPS = 60
gravity = 0.25
bird_movement = 0
score = 0
font = pygame.font.Font(None, 36)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Load and resize images
bird_img = pygame.image.load('bird.png')
bird_img = pygame.transform.scale(bird_img, (50, 50))
bird_rect = bird_img.get_rect(center=(50, HEIGHT // 2))

pipe_img = pygame.image.load('pipe.png')
pipe_img = pygame.transform.scale(pipe_img, (50, 300))
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1500)
pipe_height = [200, 300, 400]

# Functions
def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_img.get_rect(midtop=(500, random_pipe_pos))
    top_pipe = pipe_img.get_rect(midbottom=(500, random_pipe_pos - 200))
    return bottom_pipe, top_pipe

def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    visible_pipes = [pipe for pipe in pipes if pipe.right > -50]
    return visible_pipes

def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= HEIGHT:
            screen.blit(pipe_img, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_img, False, True)
            screen.blit(flip_pipe, pipe)

def check_collision(pipes, bird):
    for pipe in pipes:
        if bird.colliderect(pipe):
            return True
    if bird.top <= -100 or bird.bottom >= HEIGHT:
        return True
    return False

# Game loop
running = True
while running:
    # Event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_movement = 0
                bird_movement -= 8

        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())

    # Bird movement
    bird_movement += gravity
    bird_rect.centery += bird_movement

    # Draw background
    screen.fill("LIGHT BLUE")

    # Draw the bird
    screen.blit(bird_img, bird_rect)

    # Update and draw pipes
    pipe_list = move_pipes(pipe_list)
    draw_pipes(pipe_list)

    # Collision detection
    if check_collision(pipe_list, bird_rect):
        running = False

    # Score
    score += 1 / FPS
    score_text = font.render(f'Score: {int(score)}', True, BLACK)
    screen.blit(score_text, (10, 10))

    # Update display
    pygame.display.update()
    pygame.time.Clock().tick(FPS)

# Quit Pygame
pygame.quit()
sys.exit()
