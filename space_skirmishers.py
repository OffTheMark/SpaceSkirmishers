import pygame
import sys


GAME_TITLE = "Space Skirmishers"
PLAYER_1_NAME = "Player 1"
PLAYER_2_NAME = "Player 2"

NEAR_BLACK = (19, 15, 48)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

PLAYER_1_KEY_UP = pygame.K_w
PLAYER_1_KEY_DOWN = pygame.K_s
PLAYER_1_KEY_SHOOT = pygame.K_SPACE
PLAYER_2_KEY_UP = pygame.K_UP
PLAYER_2_KEY_DOWN = pygame.K_DOWN
PLAYER_2_KEY_SHOOT = pygame.K_KP0

COLOR_BACKGROUND = NEAR_BLACK
COLOR_BULLET = RED
COLOR_HP_2 = GREEN
COLOR_HP_1 = YELLOW
COLOR_HP_0 = RED
COLOR_PLAYER_1_BULLET = BLUE
COLOR_PLAYER_2_BULLET = RED

PLAYER_WIDTH = 20
PLAYER_HEIGHT = 60
PLAYER_SPEED = 5
PLAYER_1_BULLET_VECTOR_X = 1
PLAYER_2_BULLET_VECTOR_X = -1
PLAYER_MAX_BULLETS = 1

BULLET_WIDTH = 10
BULLET_HEIGHT = 10
BULLET_DELAY = 500
BULLET_SPEED = 20

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_MARGIN = 10
BOUNDS_MIN_X = SCREEN_MARGIN
BOUNDS_MAX_X = SCREEN_WIDTH - SCREEN_MARGIN
BOUNDS_MIN_Y = SCREEN_MARGIN
BOUNDS_MAX_Y = SCREEN_HEIGHT - SCREEN_MARGIN
BULLET_MARGIN = (PLAYER_WIDTH - BULLET_WIDTH) / 2


class Player(pygame.sprite.Sprite):
    def __init__(self, name, key_move_up, key_move_down):
        pygame.sprite.Sprite.__init__(self)
        self.width = PLAYER_WIDTH
        self.height = PLAYER_HEIGHT
        self.color = COLOR_HP_2
        self.image = pygame.Surface((self.width, self.height))
        self.rect = self.image.get_rect()
        self.speed = PLAYER_SPEED
        self.vectory = 0
        self.name = name
        self.key_move_up = key_move_up
        self.key_move_down = key_move_down
        self.hit_points = 2

    def update(self, keys, *args):
        if keys[self.key_move_up]:
            self.rect.y -= self.speed
        if keys[self.key_move_down]:
            self.rect.y += self.speed

        self.check_bounds()
        self.image.fill(self.color)

    def check_bounds(self):
        if self.rect.top < BOUNDS_MIN_Y:
            self.rect.top = BOUNDS_MIN_Y
            self.vectory = 0
        elif self.rect.bottom > BOUNDS_MAX_Y:
            self.rect.bottom = BOUNDS_MAX_Y
            self.vectory = 0

    def compute_hit(self):
        if self.hit_points > 0:
            self.hit_points -= 1

        if self.hit_points == 1:
            self.color = COLOR_HP_1
        elif self.hit_points == 0:
            self.color = COLOR_HP_0



class Bullet(pygame.sprite.Sprite):
    def __init__(self, rect, color, vectorx, speed):
        pygame.sprite.Sprite.__init__(self)
        self.width = BULLET_WIDTH
        self.height = BULLET_HEIGHT
        self.color = color
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.centery = rect.centery
        self.rect.left = rect.left + BULLET_MARGIN
        self.name = "Bullet"
        self.vectorx = vectorx
        self.speed = speed

    def update(self, *args):
        self.rect.x += self.vectorx * self.speed

        if self.rect.left < BOUNDS_MIN_X or self.rect.right > BOUNDS_MAX_X:
            self.kill()


class Game(object):
    def __init__(self):
        pygame.init()
        self.display_screen, self.display_rect = self.make_screen()
        self.laser_sound = pygame.mixer.Sound('assets/laser.ogg')
        self.game_over = False
        self.game_to_start = True
        self.game_started = False

    def make_screen(self):
        pygame.display.set_caption(GAME_TITLE)
        display_screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        display_rect = display_screen.get_rect()
        display_screen.fill(COLOR_BACKGROUND)
        display_screen.convert()
        return display_screen, display_rect

    def make_players(self):
        player_1 = Player(PLAYER_1_NAME, PLAYER_1_KEY_UP, PLAYER_1_KEY_DOWN)
        player_2 = Player(PLAYER_2_NAME, PLAYER_2_KEY_UP, PLAYER_2_KEY_DOWN)

        player_1.rect.top = BOUNDS_MIN_Y
        player_1.rect.left = BOUNDS_MIN_X

        player_2.rect.bottom = BOUNDS_MAX_Y
        player_2.rect.right = BOUNDS_MAX_X

        return player_1, player_2

    def check_input(self):
        for event in pygame.event.get():
            self.keys = pygame.key.get_pressed()

            if event.type == pygame.QUIT:
                self.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == PLAYER_1_KEY_SHOOT and len(self.player_1_bullets) < PLAYER_MAX_BULLETS:
                    bullet = Bullet(self.player_1.rect, COLOR_PLAYER_1_BULLET, PLAYER_1_BULLET_VECTOR_X, BULLET_SPEED)
                    self.player_1_bullets.add(bullet)
                    self.all_sprites.add(bullet)

                    # Pew pew
                    self.laser_sound.play()
                elif event.key == PLAYER_2_KEY_SHOOT and len(self.player_2_bullets) < PLAYER_MAX_BULLETS:
                    bullet = Bullet(self.player_2.rect, COLOR_PLAYER_2_BULLET, PLAYER_2_BULLET_VECTOR_X, BULLET_SPEED)
                    self.player_2_bullets.add(bullet)
                    self.all_sprites.add(bullet)

                    # Pew pew
                    self.laser_sound.play()

    def check_collisions(self):
        for bullet in self.player_1_bullets:
            if pygame.sprite.collide_rect(bullet, self.player_2):
                self.player_2.compute_hit()
                bullet.kill()
        for bullet in self.player_2_bullets:
            if pygame.sprite.collide_rect(bullet, self.player_1):
                self.player_1.compute_hit()
                bullet.kill()

    def check_game_over(self):
        pass

    def quit(self):
        pygame.quit()
        sys.exit()

    def setup_game(self):
        self.game_to_start = False

        # Setting up sprites
        self.player_1, self.player_2 = self.make_players()
        self.player_1_bullets = pygame.sprite.Group()
        self.player_2_bullets = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group(self.player_1, self.player_2)

        # Setting up timing and inputs
        self.fps = 60
        self.keys = pygame.key.get_pressed()
        self.clock = pygame.time.Clock()

        self.game_started = True

    def main_loop(self):
        while True:
            if self.game_to_start:
                self.setup_game()
                self.game_over = False

                self.display_screen.fill(COLOR_BACKGROUND)
            elif self.game_started:
                current_time = pygame.time.get_ticks()
                self.display_screen.fill(COLOR_BACKGROUND)

                # Handling inputs and updates
                self.check_input()
                self.all_sprites.update(self.keys, current_time)
                self.check_collisions()

                # Drawing game
                self.all_sprites.draw(self.display_screen)
                pygame.display.update()

                self.check_game_over()
                self.clock.tick(self.fps)


if __name__ == "__main__":
    game = Game()
    game.main_loop()
