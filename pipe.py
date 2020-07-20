import sys, pygame
import random

GAP = 150
VELOCITY = 2
DISTANCE = 150
GRAVITY = 1
BIRD_JUMP_ACC = 20


class Pipe:
    def __init__(self, screen, s_height, toppipe, botpipe, gap):
        self.screen = screen
        self.s_width = screen.get_width()
        self.s_height = s_height
        self.p_width, self.p_height = toppipe.get_size()
        self.toppipe = toppipe
        self.botpipe = botpipe
        self.gap = gap
        self.longitude = self.s_width + self.p_width
        self.initial_longitude = self.longitude
        self.visible = False
        self.initialize_top_height()

    def initialize_top_height(self):
        self.top_height= random.randint(self.s_height - self.gap - self.p_height, self.p_height)

    def draw(self):
        p_width, p_height = self.toppipe.get_size()
        bot_pipe_top = self.top_height + self.gap
        self.screen.blit(self.toppipe, (self.longitude, 0), (0, self.p_height - self.top_height, self.p_width, self.top_height))
        self.screen.blit(self.botpipe, (self.longitude, bot_pipe_top), (0, 0, self.p_width, self.s_height - bot_pipe_top))


    def pass_bird(self, bird):
        if self.longitude + self.p_width < bird.longitude \
                or not self.visible:
            return True
        return False

    def traveled_distance(self, distance):
        if self.longitude < (self.s_width - distance):
            return True
        return False

    def move(self):
        if self.visible:
            self.draw()
            self.longitude = self.longitude - VELOCITY
        if self.longitude < - self.toppipe.get_width():
            self.reset()

    def reset(self):
        self.initialize_top_height()
        self.longitude = self.initial_longitude
        self.visible = False


class PipeSystem:
    def __init__(self, bird, n_pipes, screen, s_height, toppipe, botpipe, gap, distance):
        self.pipes = [Pipe(screen, s_height, toppipe, botpipe, gap) for i in range(n_pipes)]
        self.screen = screen
        self.releasing_pipe_idx = 0
        self.near_bird_pipe_idx = 0
        self.releasing_pipe().visible = True
        self.bird = bird
        self.distance = distance

    def advance_idx(self, idx):
        return (idx + 1) % (len(self.pipes))

    def releasing_pipe(self):
        return self.pipes[self.releasing_pipe_idx]

    def nearbird_pipe(self):
        return self.pipes[self.near_bird_pipe_idx]

    def move(self):
        for pipe in self.pipes:
            pipe.move()
        if self.releasing_pipe().traveled_distance(self.distance):
            self.releasing_pipe_idx = self.advance_idx(self.releasing_pipe_idx)
            self.releasing_pipe().visible = True
        if self.nearbird_pipe().pass_bird(self.bird):
            self.near_bird_pipe_idx = self.advance_idx(self.near_bird_pipe_idx)
            self.bird.score()

    def draw(self):
        for pipe in self.pipes:
            if pipe.visible:
                pipe.draw()

    def reset(self):
        for pipe in self.pipes:
            pipe.reset()
        self.releasing_pipe_idx = 0
        self.near_bird_pipe_idx = 0
        self.pipes[self.releasing_pipe_idx].visible = True

