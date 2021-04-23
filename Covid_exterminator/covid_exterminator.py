"""
Pierre-Charles Dussault
October 28, 2020

Covid Exterminator, a 2D shooting game made while completing
"Python Crash Course" written by Eric Matthes.

Main module.
"""
import pygame
import sys
from time import sleep
import json

from button import Button
from bullet import Bullet
from doctor import Doctor
from game_stats import GameStats
from scoreboard import Scoreboard
from settings import Settings
from virus import Virus


class CovidExterminator():
    """Overall class to manage game assets and behaviour."""

    def __init__(self):
        """Initialize the game, and game resources."""
        # Initial resources for the game.
        pygame.init()
        self.settings = Settings()

        # The screen must be initialized first as it is used in almost all the
        # other objects used in the game instance.
        if not self.settings.fullscreen:
            self.screen = pygame.display.set_mode((self.settings.screen_width,
                                                   self.settings.screen_height))
        else:
            # ...if auto-FULLSCREEN is selected.
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            self.settings.screen_width = self.screen.get_rect().width
            self.settings.screen_height = self.screen.get_rect().height

        pygame.display.set_caption("Covid Exterminator. (press 'ESC' to quit)")
        self.play_button = Button(self, "Play!")

        # The scoreboard must be initialized after the stats because it has
        # dependancies in the stats object and from the
        # 'stats.load_high_score()' method.
        self.stats = GameStats(self)
        self.stats.load_high_score()
        self.scoreboard = Scoreboard(self)

        self.doctor = Doctor(self)
        self.bullets = pygame.sprite.Group()
        self.viruses = pygame.sprite.Group()
        self._create_fleet()

    def _check_events(self):
        """Private method to check for events from mouse and keyboard."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.stats.save_high_score()
                self._print_saved_high_score()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_button_clicked(mouse_pos)

    def _check_keydown_events(self, event):
        """Handle key presses."""
        if event.key == pygame.K_d:
            self.doctor.move_right()
        elif event.key == pygame.K_a:
            self.doctor.move_left()
        elif event.key == pygame.K_SPACE:
            if self.stats.game_active:
                self._fire_bullet()
        elif event.key == pygame.K_ESCAPE:
            self.stats.save_high_score()
            self._print_saved_high_score()
            sys.exit()
        elif event.key == pygame.K_p:
            if not self.stats.game_active:
                self._restart_level()
                pygame.mouse.set_visible(False)

    def _check_keyup_events(self, event):
        """Handle key releases."""
        if event.key == pygame.K_d:
            self.doctor.stop_moving_right()
        elif event.key == pygame.K_a:
            self.doctor.stop_moving_left()

    def _check_button_clicked(self, m_pos):
        """Start a new game when the play clicks 'Play!'."""
        button_clicked = self.play_button.rect.collidepoint(m_pos)
        if not self.stats.game_active:
            if button_clicked:
                # Reset game.
                self._restart_level()
                pygame.mouse.set_visible(False)

    def _fire_bullet(self):
        """Create a new bullet and add it the the bullets group if amount of
        bullets in the bullets group is inferior to allowed limit."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _manage_bullets(self):
        """Handle the general behaviour of bullets."""
        # This calls the defined update() method for each bullet sprite.
        self.bullets.update()

        # Cleanup bullets that have gone off the screen.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_hits()

    def _check_bullet_hits(self):
        """Handle bullet-virus collisions and virus fleet repopulation.
        Handle cheat codes."""
        # This will return a dictionnary, with each key being a sprite in
        # group1, and each value being a list of sprites in group2 that it
        # has collided with.
        # Here, group1 being 'self.bullets', and group2 being 'self.viruses'.
        collisions = \
            pygame.sprite.groupcollide(self.bullets, self.viruses,
                                       not self.settings.INVINCIBLE_BULLET,
                                       not self.settings.INVINCIBLE_VIRUS)

        if collisions:
            for bullet in collisions:
                # Set a variable to hold the list of viruses hit by each bullet.
                aliens_hit_by_this_bullet = len(collisions[bullet])

                # For each virus hit by this bullet.
                for i in range(0, aliens_hit_by_this_bullet):
                    self.stats.increase_score()
                    self.scoreboard.prep_score()
                    self.scoreboard.check_high_score()

        if not self.viruses:
            # If no viruses are left, go to the next level.
            self._next_level()

    def _create_virus(self, virus_number, row_number):
        """Create a virus and places it inside the current row, and then add
        it to the group of viruses."""
        virus = Virus(self)
        virus_width, virus_height = virus.rect.size
        virus.x = virus_width + (2 * virus_width * virus_number)
        virus.y = virus_height + (2 * virus_height * row_number)
        virus.rect.x = virus.x
        virus.rect.y = virus.y
        self.viruses.add(virus)

    def _create_fleet(self):
        """Spawn a fleet of viruses, clearing out any remaining bullets and
        viruses. This is effectively a reset button for the virus fleet."""
        self.bullets.empty()
        self.viruses.empty()
        virus = Virus(self)  # Create a new virus.

        # Set local variables to work with.
        virus_width, virus_height = virus.rect.size
        doctor_height = self.doctor.rect.height

        # Knowing that there is a blank space equal to the width of one virus
        # at the ends of each side of the screen and that the spacing between
        # viruses is equal to the width of one virus, calculate the number of
        # columns of viruses that fit on the screen.
        available_space_x = self.settings.screen_width - (virus_width * 2)
        number_columns = available_space_x // (virus_width * 2)

        # Knowing that the safe zone above the doctor is equal to 2x the height
        # of a virus (the total safe zone height includes the height of the
        # doctor), that there is a blank space equal to one virus height at the
        # top of the screen, and that the spacing between viruses is equal to
        # the height of one virus, calculate the number of rows of viruses that
        # fit on the screen.
        available_space_y = self.settings.screen_height - doctor_height \
            - (3 * virus_height)
        number_rows = available_space_y // (2 * virus_height)

        # Place the viruses on the screen.
        self._place_fleet(number_rows, number_columns)

    def _place_fleet(self, num_of_rows, num_of_viruses):
        '''Handle placing of enemy fleet on the screen surface. '''
        for row_number in range(num_of_rows):
            for virus_number in range(num_of_viruses):
                self._create_virus(virus_number, row_number)

    def _check_fleet_edges(self):
        """Respond appropriately if any viruses have reached an edge."""
        for virus in self.viruses.sprites():
            if virus.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Handle direction change and drop movement for virus fleet."""
        for virus in self.viruses.sprites():
            virus.drop_down()
        self.settings.change_virus_direction()

    def _update_viruses(self):
        """Check if fleet is at an edge, then update the positions of all
        viruses in the fleet. Check for collisions with the doctor. Check if
        any viruses have hit the bottom of the screen."""
        self._check_fleet_edges()

        # This will call the class-defined 'update()' method for each virus.
        self.viruses.update()

        self._check_doctor_infected()
        self._check_viruses_bottom()

    def _check_doctor_infected(self):
        """Check if the doctor gets touched by a virus."""
        if pygame.sprite.spritecollideany(self.doctor, self.viruses):
            self._doctor_infected()

    def _doctor_infected(self):
        """Handle event when doctor is touched by virus."""
        # if the player has any lives left
        if self.stats.doctors_remaining > 0:
            # Decrement number of doctor lives remaining, and update them on
            # the scoreboard.
            self.stats.remove_a_doctor()
            self.scoreboard.prep_doctors()

            # Show the last frame during which the infection happened
            self._update_screen()

            # Reset the virus fleet and re-center the doctor.
            self._create_fleet()
            self.doctor.center_doctor()

            # Pause.
            sleep(0.5)
        else:
            self.stats.deactivate_game()
            pygame.mouse.set_visible(True)

    def _check_viruses_bottom(self):
        """Check if any viruses have hit the bottom of the screen."""
        for virus in self.viruses.sprites():
            if virus.rect.bottom >= self.screen.get_rect().bottom:
                # Treat this the same as if the doctor got infected.
                self._doctor_infected()
                break

    def _restart_level(self):
        self.stats.reset_stats()
        self.settings.initialize_dynamic_settings()
        self.scoreboard.prep_images()
        self.doctor.center_doctor()
        self.stats.activate_game()
        self._create_fleet()

    def _next_level(self):
        """Handle behaviours when going up a level."""
        # Empty bullets and create a new fleet.
        self._create_fleet()  # Emptying of bullets is handled internally.

        # Increase the game speed for the next level.
        self.settings.increase_speed()

        # Increase current level by 1.
        self.stats.increase_level()

        # Prepare the new displayed level image for the next level.
        self.scoreboard.prep_level()

    def _print_saved_high_score(self):
        """A random test to see the workings of 'json.load()'."""
        file_object = self.settings.high_score_savefile
        try:
            with open(file_object, 'r') as f:
                fmted_high_score = "{:,}".format(json.load(f))
                print("\nHigh score saved! " + str(fmted_high_score))
        except FileNotFoundError:
            pass

    def _update_screen(self):
        """Redraw the screen during each pass of the loop"""
        self.screen.fill(self.settings.bg_color)

        # Redraw the doctor at his current position during each pass of
        # the loop, after the screen, so it renders on top.
        self.doctor.blitme()

        # Draw bullets that have been fired.
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        # Draw the viruses on the surface.
        self.viruses.draw(self.screen)

        # Draw the scoreboard.
        self.scoreboard.show_score()

        # Draw the play button if the game is not active.
        if not self.stats.game_active:
            self.play_button.draw_button()

        # Make the most recently drawn screen visible.
        pygame.display.flip()

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            # Set fixed fps with a downtime.
            dt = self.settings.clock.tick(self.settings.fps)

            # Watch for keyboard and mouse events.
            self._check_events()

            # Play the game while it is set to 'active'.
            if self.stats.game_active:
                self.doctor.update()
                self._manage_bullets()
                self._update_viruses()

            self._update_screen()


def main():
    """Make a game instance, and run the game."""
    sample_game_instance = CovidExterminator()
    sample_game_instance.run_game()

    return 0

if __name__ == "__main__":
    main()
