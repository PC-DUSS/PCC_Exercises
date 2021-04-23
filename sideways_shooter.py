'''
Pierre-Charles Dussault
November 3, 2020

Sideways shooter game.
'''
import pygame
import sys
import random
import json
from time import sleep


class SidewaysShooter():

    def __init__(self):
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width,
                                               self.settings.screen_height)
                                              )
        pygame.display.set_caption('SidewaysShooter')
        self.stats = GameStats(self)
        self.stats.load_highscore()
        self.scoreboard = Scoreboard(self)
        self.avatar = Avatar(self)
        self.projectiles = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self._populate_enemies()
        self.play_button = Button(self, 'Play!')

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.stats.save_highscore()
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
            self.stats.save_highscore()
            sys.exit()
        elif event.key == pygame.K_UP:
            self.avatar.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.avatar.moving_down = True
        elif event.key == pygame.K_SPACE:
            if self.stats.active_state:
                self._fire_projectile()
        elif event.key == pygame.K_p:
            if not self.stats.active_state:
                self._reset_game()
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

    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)
        self.avatar.blitme()
        for projectile in self.projectiles.sprites():
            projectile.draw_projectile()
        self.enemies.draw(self.screen)
        self.scoreboard.draw_scoreboard()
        if not self.stats.active_state:
            self.play_button.draw_button()
        pygame.display.flip()

    def _populate_enemies(self):
        self.projectiles.empty()
        self.enemies.empty()
        new_enemy = Enemy(self)
        self.player_safe_zone = 5 * new_enemy.rect.width
        available_space_y = self.screen.get_rect().height
        available_space_x = self.screen.get_rect().width \
            - self.player_safe_zone - self.avatar.rect.width

        enemies_that_fit_y = \
            self._how_many_fit(available_space_y,
                               new_enemy.rect.height,
                               new_enemy.spacing_mult,
                               new_enemy.outside_spacing_mult
                               )

        enemies_that_fit_x = \
            self._how_many_fit(available_space_x,
                               new_enemy.rect.width,
                               new_enemy.spacing_mult
                               )

        self._spawn_enemy_group(enemies_that_fit_x, enemies_that_fit_y)

    def _check_enemies_edges(self):
        for enemy in self.enemies.sprites():
            if enemy.check_edges():
                self._drop_enemy_group()
                self.settings.change_enemies_direction()
                break

    def _drop_enemy_group(self):
        for enemy in self.enemies.sprites():
            enemy.rect.x -= self.settings.enemy_drop_speed

    def _how_many_fit(self, available_space, dimension, spacing_coefficient=1,
                      outside_spacing=0):
        '''
        Function to calculate how many instances of an object fit on a
        unidimensional dimension of available space.

        Takes:
        - the dimension of available space,
        - the dimension of the object,
        - the spacing between each object expressed by a coefficient of the base
            dimension,
        - the outside blank spacing, if any is desired, expressed as a
            coefficient of the base dimension.

        Returns:
        - an integer of how many instances of the object fit in the given
            available space.
            '''
        return int((available_space - outside_spacing * 2 * dimension) //
                   (spacing_coefficient * dimension)
                   )

    def _calc_current_position_y(self, dimension, spacing_coefficient=1,
                                 outside_spacing=0, iterator_value=0
                                 ):
        '''
        Calculate the current position on y-axis of the enemy currently
        being placed, starting from the top.

        Takes:
        - the dimension of the enemy,
        - the inter-enemy spacing coefficient,
        - the outside spacing coefficient
        - the current iterator value.

        Returns:
        - an integer of the current position on the y-axis.
        '''
        return dimension * spacing_coefficient * iterator_value \
            + (outside_spacing * dimension)

    def _calc_current_position_x(self, dimension, safe_zone,
                                 spacing_coefficient=1, iterator_value=0
                                 ):
        '''
        Calculate the current position on x-axis of the enemy currently
        being placed, starting from the left.

        Takes:
        - the dimension of the enemy
        - the inter-enemy spacing coefficient
        - the safe zone not to be impeded upon.
        - the current iterator value.

        Returns:
        - an integer of the current position on the x-axis.
        '''
        return dimension * spacing_coefficient * iterator_value + safe_zone

    def _create_enemy(self, iterator1, iterator2):
        new_enemy = Enemy(self)

        new_enemy.x = self._calc_current_position_x(
            new_enemy.rect.width, self.player_safe_zone,
            new_enemy.spacing_mult, iterator1)
        new_enemy.rect.x = new_enemy.x

        new_enemy.y = self._calc_current_position_y(
            new_enemy.rect.height, new_enemy.spacing_mult, 1, iterator2)
        new_enemy.rect.y = new_enemy.y

        self.enemies.add(new_enemy)

    def _update_enemies(self):
        self._check_enemies_edges()
        self.enemies.update()
        self._check_avatar_collisions()
        self._check_reached_scr_edge()

    def _check_avatar_collisions(self):
        if pygame.sprite.spritecollideany(self.avatar, self.enemies):
            self._avatar_hit()

    def _check_reached_scr_edge(self):
        for enemy in self.enemies.sprites():
            if enemy.rect.left <= self.screen.get_rect().left:
                # treat it like if player avatar was hit
                self._avatar_hit()
                break

    def _avatar_hit(self):
        if self.stats.player_lives > 0:
            self.stats.remove_a_life()
            self._update_screen()
            self.scoreboard.prep_lives()
            self.avatar.center_avatar()
            self._populate_enemies()
            sleep(0.5)
        else:
            self.stats.active_state = False
            pygame.mouse.set_visible(True)

    def _check_projectile_collisions(self):
        collisions = pygame.sprite.groupcollide(self.projectiles, self.enemies,
                                                True, True
                                                )
        if collisions:
            for each_bullet in collisions:
                for each_enemy in range(0, len(collisions[each_bullet])):
                    self.stats.increase_score()
                    self.scoreboard.prep_score()
                    self._check_highscore()

    def _check_highscore(self):
        if self.stats.score > self.stats.highscore:
            self.stats.update_highscore()
            self.scoreboard.prep_highscore()

    def _spawn_enemy_group(self, amount_that_fit_x, amount_that_fit_y):
        for i in range(amount_that_fit_x):
            for j in range(amount_that_fit_y):
                if random.randint(0, 2):
                    self._create_enemy(i, j)

    def _check_button_clicked(self, m_pos):
        if self.play_button.rect.collidepoint(m_pos):
            if not self.stats.active_state:
                self._reset_game()
                pygame.mouse.set_visible(False)

    def _reset_game(self):
        self.stats.reset_stats()
        self.scoreboard.prep_varying_elements()
        self.stats.active_state = True
        self.settings.setup_dynamic_settings()
        self.avatar.center_avatar()
        self._populate_enemies()

    def _manage_enemies(self):
        if self.enemies:
            self._update_enemies()
        else:
            self._populate_enemies()
            self.stats.speedup_game()
            self.stats.increase_level()
            self.scoreboard.prep_level()
            sleep(0.5)

    def run_game(self):
        while True:
            self.settings.clock.tick(self.settings.fps)
            self._check_events()
            if self.stats.active_state:
                self.avatar.update()
                self._manage_projectiles()
                self._check_projectile_collisions()
                self._manage_enemies()
            self._update_screen()


class Settings():

    def __init__(self):
        self.screen_width = 1600
        self.screen_height = 900
        self.bg_color = (200, 100, 100)

        self.highscore_savefile = "sideways_shooter_highscore_file.json"

        # framerate cap / movement speed multiplier cap
        self.fps = 30
        self.clock = pygame.time.Clock()
        self.ms_multiplier = 60/self.fps

        self.projectile_color = (0, 0, 200)
        self.projectile_width = 15
        self.projectile_height = 3
        self.enemy_drop_speed = 300
        self.player_lives = 3
        self.game_speedup_rate = 1.1

    def setup_dynamic_settings(self):
        self.enemy_point_value = 50
        self.avatar_speed = 6.0 * self.ms_multiplier
        self.projectile_speed = 12.0 * self.ms_multiplier
        self.enemy_speed = 1.0 * self.ms_multiplier
        # a direction of 1 is going down, a direction of -1 is going up
        self.enemy_direction = 1

    def change_enemies_direction(self):
        self.enemy_direction *= -1

    def speedup_game(self):
        self.enemy_point_value *= (2 * self.game_speedup_rate - 1)
        self.avatar_speed *= self.game_speedup_rate
        self.projectile_speed *= self.game_speedup_rate
        self.enemy_speed *= self.game_speedup_rate


class Avatar(pygame.sprite.Sprite):

    def __init__(self, game_instance):
        super().__init__()
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


class Projectile(pygame.sprite.Sprite):

    def __init__(self, game_instance):
        super().__init__()
        self.screen = game_instance.screen
        self.settings = game_instance.settings
        self.rect = pygame.Rect(0, 0, self.settings.projectile_width,
                                self.settings.projectile_height
                                )
        self.rect.midright = game_instance.avatar.rect.midright
        self.x = float(self.rect.x)

    def update(self):
        self.x += self.settings.projectile_speed
        self.rect.x = self.x

    def draw_projectile(self):
        pygame.draw.rect(self.screen, self.settings.projectile_color, self.rect)


class Enemy(pygame.sprite.Sprite):

    def __init__(self, game_instance):
        super().__init__()
        self.image = pygame.image.load('star.png')
        self.screen = game_instance.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = game_instance.settings
        self.rect = self.image.get_rect()
        self.rect.x = self.screen_rect.right - 2 * self.rect.width
        self.x = float(self.rect.x)
        self.rect.y = self.rect.height
        self.y = float(self.rect.y)
        # spacing multiplier between each enemy
        self.spacing_mult = 1.5
        # spacing multiplier on each side of the outsides of the screen
        self.outside_spacing_mult = 1

    def update(self):
        self.y += self.settings.enemy_speed \
            * self.settings.enemy_direction
        self.rect.y = self.y

    def check_edges(self):
        if self.rect.top <= self.screen_rect.top \
                or self.rect.bottom >= self.screen_rect.bottom:
            return True


class GameStats():

    def __init__(self, game_instance):
        self.active_state = False
        self.settings = game_instance.settings
        self.highscore = 0
        self.reset_stats()

    def reset_stats(self):
        self.player_lives = self.settings.player_lives
        self.score = 0
        self.level = 1

    def remove_a_life(self):
        self.player_lives -= 1

    def increase_score(self):
        self.score += self.settings.enemy_point_value

    def increase_level(self):
        self.level += 1

    def update_highscore(self):
        self.highscore = self.score

    def save_highscore(self):
        f_obj = self.settings.highscore_savefile
        with open(f_obj, 'w+') as f:
            json.dump(self.highscore, f)

    def load_highscore(self):
        f_obj = self.settings.highscore_savefile
        try:
            with open(f_obj, 'r') as f:
                self.highscore = json.load(f)
        # If the file does not exist, ignore this command
        except FileNotFoundError:
            pass
        # If the file is empty, ignore this command
        except json.decoder.JSONDecodeError:
            pass


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
                                         self.bg_color
                                         )
        self.text_img_rect = self.text_img.get_rect()
        self.text_img_rect.center = self.rect.center

    def draw_button(self):
        self.screen.fill(self.bg_color, self.rect)
        self.screen.blit(self.text_img, self.text_img_rect)


class Scoreboard():

    def __init__(self, game_instance):
        self.game_instance = game_instance
        self.settings = game_instance.settings
        self.screen = game_instance.screen
        self.screen_rect = self.screen.get_rect()
        self.stats = game_instance.stats
        self.font = pygame.font.SysFont(None, 48)
        self.sb_text_color = (30, 30, 30)
        self.prep_varying_elements()
        self.prep_highscore()

    def prep_score(self):
        self.score_str = "{:,}".format(round(self.stats.score))
        self.score_img = self.font.render(self.score_str, True,
                                          self.sb_text_color,
                                          self.settings.bg_color
                                          )
        self.score_img_rect = self.score_img.get_rect()
        self.score_img_rect.top = 10
        self.score_img_rect.right = self.screen_rect.right - 10

    def prep_level(self):
        self.level_img = self.font.render(str(self.stats.level), True,
                                          self.sb_text_color,
                                          self.settings.bg_color
                                          )
        self.level_img_rect = self.level_img.get_rect()
        self.level_img_rect.top = self.score_img_rect.bottom + 5
        self.level_img_rect.right = self.score_img_rect.right

    def prep_lives(self):
        self.avatars = pygame.sprite.Group()
        for avatar_number in range(0, self.stats.player_lives):
            tmp_avatar = Avatar(self.game_instance)
            tmp_avatar.rect.x = avatar_number * tmp_avatar.rect.width + 5
            tmp_avatar.rect.y = 5
            self.avatars.add(tmp_avatar)

    def prep_varying_elements(self):
        self.prep_score()
        self.prep_level()
        self.prep_lives()

    def prep_highscore(self):
        self.highscore_str = "{:,}".format(round(self.stats.highscore))
        self.highscore_img = self.font.render(self.highscore_str, True,
                                              self.sb_text_color,
                                              self.settings.bg_color
                                              )
        self.highscore_img_rect = self.highscore_img.get_rect()
        self.highscore_img_rect.top = 10
        self.highscore_img_rect.centerx = self.screen_rect.centerx

    def draw_scoreboard(self):
        self.screen.blit(self.score_img, self.score_img_rect)
        self.screen.blit(self.level_img, self.level_img_rect)
        self.avatars.draw(self.screen)
        self.screen.blit(self.highscore_img, self.highscore_img_rect)


def main():
    sample_game = SidewaysShooter()
    sample_game.run_game()


if __name__ == "__main__":
    main()
