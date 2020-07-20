import pygame

class GameScreen:

    def __init__(self, background, base, gameover_sign, digits):
        self.background = background
        self.base = base
        self.gameover_sign = gameover_sign
        self.screen = self.initialize_screen()
        self.digits = digits

    def draw_in_center(self, surface, y_offset=0):
        bg_width, bg_height = self.background.get_size()
        surface_width, surface_height = surface.get_size()
        surface_location_x = int(bg_width/2 - surface_width/2)
        surface_location_y = int(bg_height/2 - surface_height/2) + y_offset

        self.screen.blit(surface, (surface_location_x, surface_location_y))

    def get_score_surface(self, bird):
        score_str = str(bird.points)
        required_images = [self.digits[digit] for digit in score_str]
        all_widths = [image.get_width() for image in required_images]
        combined_surface = pygame.Surface((sum(all_widths), required_images[0].get_height()))
        current_pos = 0
        for position, image in enumerate(required_images):
            combined_surface.blit(image, (current_pos, 0))
            current_pos += all_widths[position]

        return combined_surface

    def initialize_screen(self):
        bg_width, bg_height = self.background.get_size()
        base_height = self.base.get_height()
        full_height = bg_height + base_height
        size = (bg_width, full_height)
        screen = pygame.display.set_mode(size)
        return screen

    def draw_screen(self, bird, pipe_system):
        score_surface = self.get_score_surface(bird)
        bg_height = self.background.get_height()

        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.base, (0, bg_height))
        self.draw_in_center(score_surface, -40)

    def game_over(self):
        self.draw_in_center(self.gameover_sign)
