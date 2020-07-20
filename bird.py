import pygame

class Bird:
    def __init__(self, screen, bg_height, jump_acc, bird_images, bird_die_image, swoosh_sound, score_sound, hit_sound, die_sound, gravity):

        # Initial Positions
        self.size = bird_images[0].get_size()
        initial_latitude = int(bg_height/2 - self.size[1]/2)
        self.longitude = 0
        self.latitude = initial_latitude
        self.initial_latitude = initial_latitude

        # Movement related paramaters
        self.gravity = gravity
        self.velocity = 0
        self.jump_acc = jump_acc
        self.points = 0

        # Images
        self.images = bird_images
        self.die_image = bird_die_image
        self.image_idx = 0
        self.idx_increment = 1
        self.current_image = bird_images[0]

        # Sounds
        self.swoosh_sound = swoosh_sound
        self.score_sound = score_sound
        self.hit_sound = hit_sound
        self.die_sound = die_sound

        # Others
        self.screen = screen
        self.bg_height = bg_height
        self.alive = True

    def die(self):
        self.hit_sound.play()
        self.current_image = self.die_image
        self.die_sound.play()
        self.alive = False

    def draw(self):
        self.screen.blit(self.current_image, (self.longitude, self.latitude))
        self.drop()

    def drop(self):
        self.latitude += self.velocity
        bird_height = self.size[1]
        if self.latitude >= self.bg_height - bird_height:
            self.latitue = self.bg_height - bird_height
            self.velocity = 0
        else:
            self.velocity += self.gravity

    def flap(self):
        # Determine the current bird image
        self.current_image = self.images[self.image_idx]
        self.image_idx += self.idx_increment

        # Change increment direction if necessary
        if self.image_idx >= 2 or self.image_idx <= 0:
            self.idx_increment = -self.idx_increment

    def jump(self):
        self.velocity -= self.jump_acc
        if self.latitude <= 0:
            self.latitude = 0
            self.velocity = 0
        self.swoosh_sound.play()

    def reset(self):
        self.alive = True
        self.latitude = self.initial_latitude
        self.velocity = 0
        self.points = 0

    def score(self):
        self.points += 1
        self.score_sound.play()

    def hit_pipe(self, pipe):
        if pipe.longitude <= self.longitude + self.size[0] and \
                pipe.longitude + pipe.p_width >= self.longitude:
            if self.latitude <= pipe.top_height or \
                    self.latitude + self.size[1] >= pipe.top_height + pipe.gap:
                return True
        return False

    def hit_pipe_system(self, pipe_system):
        if self.alive:
            return self.hit_pipe(pipe_system.nearbird_pipe())
        return False

