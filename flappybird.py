import sys, pygame
import time
pygame.init()

size = width, height = 320, 240
speed = [0, 2]
black = 0, 0, 0

screen = pygame.display.set_mode(size)

bird = pygame.image.load("sprites/bluebird-downflap.png")
birdrect = bird.get_rect()

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    screen.fill(black)
    screen.blit(bird, birdrect)
    pygame.display.flip()
