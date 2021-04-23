'''
Pierre-Charles Dussault
November 3, 2020

Exercise 14-2 in Python Crash Course.

Normally, all the classed would be in their own module, but to avoid having
hundreds of files in the directory after finishing the book, I keep the
classes used for small chapter exercises in the same file as the main program.
'''
import pygame
import sys
import random
from time import sleep


class TargetPractice():
    '''Class for the game instance.'''

    def __init__(self):
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width,
                                               self.settings.screen_height))
        pygame.display.set_caption('Target Practice')
        self.stats = GameStats(self)
        self.avatar = Avatar(self)
        self.projectiles = pygame.sprite.Group()
        self.target = Target(self)
        self.play_button = Button(self, 'Play!')

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_button_clicked(mouse_pos)

    def _check_keydown_events(self, event):
        if event.key == pygame.K_ESCAPE:
            sys.exit()
        elif event.key == pygame.K_UP:
            self.avatar.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.avatar.moving_down = True
        elif event.key == pygame.K_SPACE:
            if self.stats.game_active:
                self._fire_projectile()
        elif event.key == pygame.K_p:
            if not self.stats.game_active:
                self._restart_level()
                pygame.mouse.set_visible(False)

    def _check_keyup_events(self, event):
        if event.key == pygame.K_UP:
            self.avatar.moving_up = False
        if event.key == pygame.K_DOWN:
            self.avatar.moving_down = False

    def _fire_projectile(self):
        new_projectile = Projectile(self)
        self.projectiles.add(new_projectile)

    def _manage_projectiles(self):
        self.projectiles.update()
        for projectile in self.projectiles.copy():
            if projectile.rect.x > self.settings.screen_width:
                self.projectiles.remove(projectile)
                self._missed_target()

    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)
        self.avatar.blitme()
        for projectile in self.projectiles.sprites():
            projectile.draw_projectile()
        self.target.draw_target()
        if not self.stats.game_active:
            self.play_button.draw_button()
        pygame.display.flip()

    def _check_target_edges(self):
        if self.target.check_edges():
            self.settings.target_direction *= -1

    def _missed_target(self):
        if self.stats.player_lives > 0:
            self.stats.player_lives -= 1
            self._update_screen()
            self.projectiles.empty()
            self.target.center_target()
            self.avatar.center_avatar()
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _check_projectile_collisions(self):
        for projectile in self.projectiles.sprites():
            if projectile.rect.colliderect(self.target.rect):
                self.settings.increase_speed()
                self.projectiles.remove(projectile)

    def _check_button_clicked(self, m_pos):
        if self.play_button.rect.collidepoint(m_pos):
            if not self.stats.game_active:
                self._restart_level()
                pygame.mouse.set_visible(False)

    def _restart_level(self):
        self.stats.reset_stats()
        self.avatar.center_avatar()
        self.target.center_target()
        self.settings.initialize_dynamic_settings()
        self.stats.game_active = True

    def run_game(self):
        while True:
            dt = self.settings.clock.tick(self.settings.fps)
            if self.stats.game_active:
                self.avatar.update()
                self._manage_projectiles()
                self._check_projectile_collisions()
                self._check_target_edges()
                self.target.update()
            self._check_events()
            self._update_screen()

###############################################################################


class Settings():

    def __init__(self):
        self.screen_width = 1600
        self.screen_height = 900
        self.bg_color = (200, 100, 100)

        # Framerate cap / movement speed multiplier cap
        self.fps = 30
        self.clock = pygame.time.Clock()
        self.ms_multiplier = 60/self.fps
        self.player_lives = 2
        self.projectile_color = (0, 0, 200)
        self.projectile_width = 15
        self.projectile_height = 3
        self.speedup_scale = 1.05
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        # A direction of 1 is going down, a direction of -1 is going up.
        self.target_direction = 1
        self.target_speed = 2.0 * self.ms_multiplier
        self.projectile_speed = 12.0 * self.ms_multiplier
        self.avatar_speed = 6.0 * self.ms_multiplier

    def increase_speed(self):
        self.target_speed *= self.speedup_scale
        self.avatar_speed *= self.speedup_scale
        self.projectile_speed *= self.speedup_scale
        self.projectile_speed *= self.speedup_scale

###############################################################################


class Avatar():

    def __init__(self, game_instance):
        self.screen = game_instance.screen
        self.settings = game_instance.settings
        self.screen_rect = game_instance.screen.get_rect()
        self.image = pygame.image.load('Covid_exterminator/images/doctor.png')
        self.rect = self.image.get_rect()
        self.rect.midleft = self.screen_rect.midleft
        self.y = float(self.rect.y)
        self.moving_up = False
        self.moving_down = False

    def update(self):
        if self.moving_up:
            if self.y <= 0:
                self.y = 0
            else:
                self.y -= self.settings.avatar_speed
        elif self.moving_down:
            if self.y >= (self.settings.screen_height - self.rect.height):
                self.y = (self.settings.screen_height - self.rect.height)
            else:
                self.y += self.settings.avatar_speed
        self.rect.y = self.y

    def blitme(self):
        self.screen.blit(self.image, self.rect)

    def center_avatar(self):
        self.rect.midleft = self.screen.get_rect().midleft
        self.y = float(self.rect.y)

###############################################################################


class Projectile(pygame.sprite.Sprite):

    def __init__(self, game_instance):
        super().__init__()
        self.screen = game_instance.screen
        self.settings = game_instance.settings
        self.rect = pygame.Rect(0, 0, self.settings.projectile_width,
                                self.settings.projectile_height)
        self.rect.midright = game_instance.avatar.rect.midright
        self.x = float(self.rect.x)

    def update(self):
        self.x += self.settings.projectile_speed
        self.rect.x = self.x

    def draw_projectile(self):
        pygame.draw.rect(self.screen, self.settings.projectile_color,
                         self.rect)

###############################################################################


class Target():

    def __init__(self, game_instance):
        self.screen = game_instance.screen
        self.settings = game_instance.settings
        self.width, self.height = 50, 200
        self.color = (0, 255, 255)  # 8-bit RGB
        self.rect = pygame.Rect((0, 0), (self.width, self.height))
        self.y = float(self.rect.y)
        self.center_target()

    def center_target(self):
        self.rect.midright = self.screen.get_rect().midright
        self.y = self.rect.y

    def check_edges(self):
        if self.rect.top <= 0:
            return True
        elif self.rect.bottom >= self.screen.get_rect().bottom:
            return True

    def update(self):
        self.y += self.settings.target_speed * self.settings.target_direction
        self.rect.y = self.y

    def draw_target(self):
        pygame.draw.rect(self.screen, self.color, self.rect)

###############################################################################


class GameStats():

    def __init__(self, game_instance):
        self.game_active = False
        self.settings = game_instance.settings
        self.reset_stats()

    def reset_stats(self):
        self.player_lives = self.settings.player_lives

###############################################################################


class Button():

    def __init__(self, game_instance, text):
        self.screen = game_instance.screen
        self.text = text
        self.width = 200
        self.height = 50
        self.text_color = (0, 0, 0)
        self.bg_color = (0, 255, 0)
        self.font = pygame.font.SysFont(None, 48)
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen.get_rect().center
        self._prep_text()

    def _prep_text(self):
        self.text_img = self.font.render(self.text, True, self.text_color,
                                         self.bg_color)
        self.text_img_rect = self.text_img.get_rect()
        self.text_img_rect.center = self.rect.center

    def draw_button(self):
        self.screen.fill(self.bg_color, self.rect)
        self.screen.blit(self.text_img, self.text_img_rect)

###############################################################################


def main():
    sample_game = TargetPractice()
    sample_game.run_game()
    return 0


if __name__ == '__main__':
    main()
