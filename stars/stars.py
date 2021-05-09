import sys
import pygame
import random


class Canvas():

    def __init__(self, random_number):
        pygame.init()
        self.random_number = random_number
        self.surface_width = 1600
        self.surface_height = 900
        self.surface_color = (255, 255, 255)
        self.surface = pygame.display.set_mode((self.surface_width,
                                                self.surface_height
                                                ))
        self.surface.fill(self.surface_color)
        self.stars = pygame.sprite.Group()
        self._fill_with_stars()

    def _create_star(self, star_number, row_number):
        star = Star(self, self.random_number)
        star_width, star_height = star.rect.size
        star.rect.x = star_width * self.random_number * star_number
        star.rect.y = star_height * self.random_number * row_number
        self.stars.add(star)

    def _fill_with_stars(self):
        star = Star(self, self.random_number)
        star_width, star_height = star.rect.size

        # Calculate how many stars fit on the screen with proper spacing.
        available_space_x = self.surface_width
        num_of_stars = available_space_x // (star_width
                                             * self.random_number)

        # Calculate how many rows fit on the screen with proper spacing.
        available_space_y = self.surface_height
        num_of_rows = available_space_y // (star_height
                                            * self.random_number)

        for row_number in range(num_of_rows):
            for star_number in range(num_of_stars):
                self._create_star(star_number, row_number)

    def _check_if_exit(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()

    def _update_canvas(self):
        self.stars.draw(self.surface)
        pygame.display.flip()

    def display_canvas(self):
        while True:
            self._update_canvas()
            self._check_if_exit()


class Star(pygame.sprite.Sprite):

    def __init__(self, canvas, random_number):
        super().__init__()
        self.random_number = random_number
        self.surface = canvas.surface
        self.image = pygame.image.load("star.png")
        self.rect = self.image.get_rect()
        self.rect.x = self.rect.width * (self.random_number - 1)
        self.rect.y = self.rect.height * (self.random_number - 1)


def main():
    random_number = random.randint(1, 5)
    star_canvas = Canvas(random_number)
    star_canvas.display_canvas()


if __name__ == "__main__":
    main()
