import sys, pygame

class Settings():

    def __init__(self):
        self.screen_width = 1200
        self.screen_height = 800
        self.background_color = (230, 230, 230)
        self.raining_speed = 3

        # Multiplier to determine how many 'x' times each dimension worth of
        # pixels we leave between each raindrop for spacing.
        self.space_between_raindrops_multiplier = 3.0


class Raindrop(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("raindrops.png")
        self.rect = self.image.get_rect()
        self.width = self.rect.width
        self.height = self.rect.height


class Raining():

    def __init__(self):
        # Initialize pygame and the settings for this script.
        pygame.init()
        self.settings = Settings()

        # Create the display screen.
        self.screen = pygame.display.set_mode((self.settings.screen_width,
                                               self.settings.screen_height
                                               ))

        # Fill it with a color.
        self.screen.fill(self.settings.background_color)

        # Create a group to manage all raindrops.
        self.raindrops = pygame.sprite.Group()

        # Create raindrops for calculated amount of columns and rows.
        self.num_of_columns = self._determine_columns()
        self.num_of_rows = self._determine_rows()

        # Fill the screen with rain.
        self._fill_with_rain()

    def _determine_columns(self):
        # Local variables to make calculations.
        raindrop = Raindrop()
        space_mult = self.settings.space_between_raindrops_multiplier

        # Calculate how many raindrops fit on the screen.
        return int(self.settings.screen_width // (raindrop.width * space_mult))

    def _determine_rows(self):
        # Local variable to make calculations.
        raindrop = Raindrop()
        space_mult = self.settings.space_between_raindrops_multiplier

        # Calculate how many raindrops fit on the screen.
        return int(self.settings.screen_height // (raindrop.height \
                                                       * space_mult))

    def _create_raindrop(self, row_num, column_num):
        # Create an new raindrop for calculation purposes.
        raindrop = Raindrop()
        space_mult = self.settings.space_between_raindrops_multiplier

        # Position each new raindrop.
        raindrop.rect.x = int(raindrop.width * space_mult * column_num)
        raindrop.rect.y = int(raindrop.height * space_mult * row_num)

        # Add the raindrop to the group of raindrops.
        self.raindrops.add(raindrop)

    def _fill_with_rain(self):
        for row_num in range(self.num_of_rows):
            for column_num in range(self.num_of_columns):
                self._create_raindrop(row_num, column_num)

    def _cleanup_raindrops(self):
        # Remove raindrops that have gone out of the screen.
        for raindrop in self.raindrops.copy():
            if raindrop.rect.top >= self.settings.screen_height:
                self.raindrops.remove(raindrop)

    def _check_if_empty_row(self):
        # Check if there is an empty row of space to repopulate with raindrops.
        if (len(self.raindrops) / self.num_of_columns) < self.num_of_rows:
            return True

    def _fill_row(self):
        # Fill an empty row with raindrops.
        for column_num in range(self.num_of_columns):
            self._create_raindrop(0, column_num)

    def _update_rain(self):
        # Manage out-of-bounds raindrops.
        self._cleanup_raindrops()

        # Check if a new row of raindrops needs to be added.
        if self._check_if_empty_row():
            self._fill_row()

        # Handle raindrop movement for all raindrops.
        for raindrop in self.raindrops.sprites():
            raindrop.rect.y += self.settings.raining_speed

        # Draw all raindrops.
        self.raindrops.draw(self.screen)

    def _update_screen(self):
        # Update elements of the display screen.
        self.screen.fill(self.settings.background_color)
        self._update_rain()
        pygame.display.flip()

    def _check_if_quit(self):
        # Check if the script should end.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()

    def run(self):
        # Main loop for the script
        while True:
            self._update_screen()
            self._check_if_quit()


def main():
    rain_script = Raining()
    rain_script.run()


if __name__ == "__main__":
    main()
