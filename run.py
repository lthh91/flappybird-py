from bird import Bird
from pipe import PipeSystem
from screen import GameScreen
import sys, pygame
import random

GAP = 150
VELOCITY = 2
DISTANCE = 150
GRAVITY = 1
BIRD_JUMP_ACC = 20


pygame.init()

# Load images
background = pygame.image.load("images/background-day.png")
base = pygame.image.load("images/base.png")
bird_upflap = pygame.image.load("images/redbird-upflap.png")
bird_midflap = pygame.image.load("images/redbird-midflap.png")
bird_downflap = pygame.image.load("images/redbird-downflap.png")
bird_images = [bird_upflap, bird_midflap, bird_downflap]
bird_die = pygame.transform.rotate(bird_downflap, -90)


gameover_sign = pygame.image.load("images/gameover.png")

botpipe = pygame.image.load("images/pipe-green.png")
toppipe = pygame.transform.rotate(botpipe, 180)

digits = {str(num): pygame.image.load(f"images/{num}.png") for num in range(10)}

# Load sounds
point_sound = pygame.mixer.Sound("audio/point.wav")
swoosh_sound = pygame.mixer.Sound("audio/swoosh.wav")
hit_sound = pygame.mixer.Sound("audio/hit.wav")
die_sound = pygame.mixer.Sound("audio/die.wav")

bg_height = background.get_height()

# initialize objects
screen = GameScreen(background=background,
                    base=base,
                    gameover_sign=gameover_sign,
                    digits=digits)

bird = Bird(screen=screen.screen,
            bg_height=bg_height,
            jump_acc=BIRD_JUMP_ACC,
            bird_images=bird_images,
            bird_die_image=bird_die,
            swoosh_sound = swoosh_sound,
            score_sound = point_sound,
            hit_sound = hit_sound,
            die_sound = die_sound,
            gravity=GRAVITY)

pipe_system = PipeSystem(bird=bird,
                         n_pipes=2,
                         screen=screen.screen,
                         s_height=bg_height,
                         toppipe=toppipe,
                         botpipe=botpipe,
                         gap=GAP,
                         distance=DISTANCE)

clock = pygame.time.Clock()

def game_over():
    bird.draw()
    pipe_system.draw()
    screen.game_over()


def game_on():
    pipe_system.move()
    bird.flap()
    bird.draw()

def reset():
    bird.reset()
    pipe_system.reset()


while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        if event.type == pygame.KEYDOWN:
            if bird.alive:
                bird.jump()
            else:
                reset()

    screen.draw_screen(bird, pipe_system)
    if bird.hit_pipe_system(pipe_system):
        bird.die()
    if bird.alive:
        game_on()
    else:
        game_over()
    pygame.display.flip()
    clock.tick(30)
