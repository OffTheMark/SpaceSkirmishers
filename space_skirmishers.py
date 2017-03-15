import pygame
import sys
from random import randint


GAME_TITLE = "Space Skirmishers"
PLAYER_1_NAME = "Player 1"
PLAYER_2_NAME = "Player 2"
BULLET_NAME = "Bullet"
OBSTACLE_NAME = "Obstacle"

NEAR_BLACK = (19, 15, 48)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 69, 0)
WHITE = (255, 255, 255)

PLAYER_1_KEY_UP = pygame.K_w
PLAYER_1_KEY_DOWN = pygame.K_s
PLAYER_1_KEY_SHOOT = pygame.K_SPACE
PLAYER_2_KEY_UP = pygame.K_UP
PLAYER_2_KEY_DOWN = pygame.K_DOWN
PLAYER_2_KEY_SHOOT = pygame.K_KP0

COLOR_BACKGROUND = NEAR_BLACK
COLOR_BULLET = RED
COLOR_HP_3 = GREEN
COLOR_HP_2 = YELLOW
COLOR_HP_1 = ORANGE
COLOR_PLAYER_1_BULLET = BLUE
COLOR_PLAYER_2_BULLET = RED
COLOR_OBSTACLE = GREEN

TITLE_TEXT_SIZE = 75
SUBTITLE_TEXT_SIZE = 40
TITLE_SUBTITLE_MARGIN = 10

PLAYER_WIDTH = 20
PLAYER_HEIGHT = 60
PLAYER_SPEED = 30
PLAYER_1_BULLET_VECTOR_X = 1
PLAYER_2_BULLET_VECTOR_X = -1
PLAYER_MAX_BULLETS = 1

BULLET_WIDTH = 10
BULLET_HEIGHT = 5
BULLET_DELAY = 500
BULLET_SPEED = 25

OBSTACLE_HEIGHT = 20
OBSTACLE_WIDTH = 20
OBSTACLE_TYPE_1_ROWS = 6
OBSTACLE_TYPE_1_COLUMNS = 4
OBSTACLE_TYPE_2_ROWS = 4
OBSTACLE_TYPE_2_COLUMNS = 4

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_MARGIN = 15
BOUNDS_MIN_X = SCREEN_MARGIN
BOUNDS_MAX_X = SCREEN_WIDTH - SCREEN_MARGIN
BOUNDS_MIN_Y = SCREEN_MARGIN
BOUNDS_MAX_Y = SCREEN_HEIGHT - SCREEN_MARGIN
BULLET_MARGIN = (PLAYER_WIDTH - BULLET_WIDTH) / 2
OBSTACLE_MARGIN_X = 100
OBSTACLE_MARGIN_Y = 50
OBSTACLE_BOUNDS_MIN_X = BOUNDS_MIN_X + OBSTACLE_MARGIN_X
OBSTACLE_BOUNDS_MAX_X = BOUNDS_MAX_X - OBSTACLE_MARGIN_X
OBSTACLE_BOUNDS_MIN_Y = BOUNDS_MIN_Y + OBSTACLE_MARGIN_Y
OBSTACLE_BOUNDS_MAX_Y = BOUNDS_MAX_Y - OBSTACLE_MARGIN_Y

LEVELS = [
    [
        {
            "top": OBSTACLE_BOUNDS_MIN_Y,
            "left": OBSTACLE_BOUNDS_MIN_X,
            "rows": OBSTACLE_TYPE_1_ROWS,
            "columns": OBSTACLE_TYPE_1_COLUMNS
        },
        {
            "top": OBSTACLE_BOUNDS_MAX_Y - OBSTACLE_TYPE_1_ROWS * OBSTACLE_HEIGHT,
            "left": OBSTACLE_BOUNDS_MIN_X,
            "rows": OBSTACLE_TYPE_1_ROWS,
            "columns": OBSTACLE_TYPE_1_COLUMNS
        },
        {
            "top": OBSTACLE_BOUNDS_MIN_Y,
            "left": OBSTACLE_BOUNDS_MAX_X - OBSTACLE_TYPE_1_COLUMNS * OBSTACLE_WIDTH,
            "rows": OBSTACLE_TYPE_1_ROWS,
            "columns": OBSTACLE_TYPE_1_COLUMNS
        },
        {
            "top": OBSTACLE_BOUNDS_MAX_Y - OBSTACLE_TYPE_1_ROWS * OBSTACLE_HEIGHT,
            "left": OBSTACLE_BOUNDS_MAX_X - OBSTACLE_TYPE_1_COLUMNS * OBSTACLE_WIDTH,
            "rows": OBSTACLE_TYPE_1_ROWS,
            "columns": OBSTACLE_TYPE_1_COLUMNS
        },
        {
            "top": OBSTACLE_BOUNDS_MIN_Y + 0.5 * (OBSTACLE_BOUNDS_MAX_Y - OBSTACLE_BOUNDS_MIN_Y) - 0.5 * OBSTACLE_TYPE_1_ROWS * OBSTACLE_HEIGHT,
            "left": OBSTACLE_BOUNDS_MIN_X + 0.5 * (OBSTACLE_BOUNDS_MAX_X - OBSTACLE_BOUNDS_MIN_X) - 0.5 * OBSTACLE_TYPE_1_COLUMNS * OBSTACLE_WIDTH,
            "rows": OBSTACLE_TYPE_1_ROWS,
            "columns": OBSTACLE_TYPE_1_COLUMNS
        }
    ],
    [
        {
            "top": OBSTACLE_BOUNDS_MIN_Y + 0.5 * (OBSTACLE_BOUNDS_MAX_Y - OBSTACLE_BOUNDS_MIN_Y) - 0.5 * OBSTACLE_TYPE_2_ROWS * OBSTACLE_HEIGHT,
            "left": OBSTACLE_BOUNDS_MIN_X,
            "rows": OBSTACLE_TYPE_2_ROWS,
            "columns": OBSTACLE_TYPE_2_COLUMNS
        },
        {
            "top": OBSTACLE_BOUNDS_MIN_Y + 0.5 * (OBSTACLE_BOUNDS_MAX_Y - OBSTACLE_BOUNDS_MIN_Y) - 0.5 * OBSTACLE_TYPE_2_ROWS * OBSTACLE_HEIGHT,
            "left": OBSTACLE_BOUNDS_MAX_X - OBSTACLE_TYPE_2_COLUMNS * OBSTACLE_WIDTH,
            "rows": OBSTACLE_TYPE_2_ROWS,
            "columns": OBSTACLE_TYPE_2_COLUMNS
        },
        {
            "top": OBSTACLE_BOUNDS_MIN_Y,
            "left": OBSTACLE_BOUNDS_MIN_X + 0.5 * (OBSTACLE_BOUNDS_MAX_X - OBSTACLE_BOUNDS_MIN_X) - 0.5 * OBSTACLE_TYPE_2_COLUMNS * OBSTACLE_WIDTH,
            "rows": OBSTACLE_TYPE_2_ROWS,
            "columns": OBSTACLE_TYPE_2_COLUMNS
        },
        {
            "top": OBSTACLE_BOUNDS_MAX_Y - OBSTACLE_TYPE_2_ROWS * OBSTACLE_HEIGHT,
            "left": OBSTACLE_BOUNDS_MIN_X + 0.5 * (OBSTACLE_BOUNDS_MAX_X - OBSTACLE_BOUNDS_MIN_X) - 0.5 * OBSTACLE_TYPE_2_COLUMNS * OBSTACLE_WIDTH,
            "rows": OBSTACLE_TYPE_2_ROWS,
            "columns": OBSTACLE_TYPE_2_COLUMNS
        }
    ]
]


class Player(pygame.sprite.Sprite):
    def __init__(self, name, key_move_up, key_move_down):
        pygame.sprite.Sprite.__init__(self)
        self.width = PLAYER_WIDTH
        self.height = PLAYER_HEIGHT
        self.color = COLOR_HP_3
        self.image = pygame.Surface((self.width, self.height))
        self.rect = self.image.get_rect()
        self.speed = PLAYER_SPEED
        self.vectory = 0
        self.name = name
        self.key_move_up = key_move_up
        self.key_move_down = key_move_down
        self.hit_points = 3

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

        if self.hit_points == 2:
            self.color = COLOR_HP_2
        elif self.hit_points == 1:
            self.color = COLOR_HP_1


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
        self.name = BULLET_NAME
        self.vectorx = vectorx
        self.speed = speed

    def update(self, *args):
        self.rect.x += self.vectorx * self.speed

        if self.rect.left < BOUNDS_MIN_X or self.rect.right > BOUNDS_MAX_X:
            self.kill()


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, left, top, color):
        pygame.sprite.Sprite.__init__(self)
        self.width = OBSTACLE_WIDTH
        self.height = OBSTACLE_HEIGHT
        self.color = color
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.name = OBSTACLE_NAME
        self.rect.top = top
        self.rect.left = left


class Text:
    def __init__(self, font, size, message, color, rect):
        self.font = pygame.font.Font(font, size)
        self.color = color
        self.set_message(message)
        self.rect = self.surface.get_rect()
        self.rect.centerx = rect.centerx
        self.rect.centery = rect.centery

    def draw(self, surface):
        surface.blit(self.surface, self.rect)

    def set_message(self, message):
        self.surface = self.font.render(message, True, self.color)


class Game:
    def __init__(self):
        pygame.init()
        self.display_screen, self.display_rect = self.make_screen()
        self.laser_sound = pygame.mixer.Sound('assets/laser.ogg')
        self.block_kill_sound = pygame.mixer.Sound('assets/block_kill.wav')
        self.player_hit_sounds = [
            pygame.mixer.Sound('assets/player_hit_0_hp.wav'),
            pygame.mixer.Sound('assets/player_hit_1_hp.wav'),
            pygame.mixer.Sound('assets/player_hit_2_hp.wav')
        ]
        self.intro_sound = pygame.mixer.Sound('assets/intro.wav')
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

    def make_obstacles(self):
        obstacle_group = pygame.sprite.Group()

        level = LEVELS[randint(0, 1)]

        for obstacle in level:
            obstacle_group.add(self.make_obstace_group(obstacle["top"], obstacle["left"], obstacle["rows"], obstacle["columns"]))

        return obstacle_group

    def make_obstace_group(self, top, left, rows, columns):
        obstacle_group = pygame.sprite.Group()

        for row in range(rows):
            for column in range(columns):
                x = left + column * OBSTACLE_WIDTH
                y = top + row * OBSTACLE_HEIGHT
                obstacle = Obstacle(x, y, COLOR_OBSTACLE)
                obstacle_group.add(obstacle)

        return obstacle_group

    def check_input(self):
        for event in pygame.event.get():
            self.keys = pygame.key.get_pressed()

            if event.type == pygame.QUIT:
                self.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == PLAYER_1_KEY_SHOOT and len(self.player_1_bullets) < PLAYER_MAX_BULLETS:
                    # Pew pew
                    self.laser_sound.play()

                    bullet = Bullet(self.player_1.rect, COLOR_PLAYER_1_BULLET, PLAYER_1_BULLET_VECTOR_X, BULLET_SPEED)
                    self.player_1_bullets.add(bullet)
                    self.all_bullets.add(bullet)
                    self.all_sprites.add(bullet)
                elif event.key == PLAYER_2_KEY_SHOOT and len(self.player_2_bullets) < PLAYER_MAX_BULLETS:
                    # Pew pew
                    self.laser_sound.play()

                    bullet = Bullet(self.player_2.rect, COLOR_PLAYER_2_BULLET, PLAYER_2_BULLET_VECTOR_X, BULLET_SPEED)
                    self.player_2_bullets.add(bullet)
                    self.all_bullets.add(bullet)
                    self.all_sprites.add(bullet)

    def check_game_over_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
            elif event.type == pygame.KEYUP:
                self.game_to_start = True
                self.game_started = False
                self.game_over = False

    def check_game_to_start_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
            elif event.type == pygame.KEYUP:
                self.game_to_start = False
                self.game_started = True
                self.game_over = False
                self.intro_sound.play()

    def check_collisions(self):
        hits = pygame.sprite.groupcollide(self.all_bullets, self.all_obstacles, True, False)
        if hits:
            self.block_kill_sound.play()
            for obstacles in hits.values():
                obstacles[0].kill()


        for bullet in self.player_1_bullets:
            if pygame.sprite.collide_rect(bullet, self.player_2):
                self.player_2.compute_hit()
                self.player_hit_sounds[self.player_2.hit_points].play()
                bullet.kill()

        for bullet in self.player_2_bullets:
            if pygame.sprite.collide_rect(bullet, self.player_1):
                self.player_1.compute_hit()
                self.player_hit_sounds[self.player_1.hit_points].play()
                bullet.kill()

    def check_game_over(self):
        if self.player_1.hit_points == 0 or self.player_2.hit_points == 0:
            self.game_over = True
            self.game_to_start = False
            self.game_started = False

            self.handle_game_over()

    def handle_game_over(self):
        subtitle = ""
        if self.player_1.hit_points == self.player_2.hit_points:
            subtitle = "Both players lose"
        elif self.player_1.hit_points > 0:
            subtitle = "{} wins".format(self.player_1.name)
        else:
            subtitle = "{} wins".format(self.player_2.name)

        self.game_over_subtitle = Text(
            'assets/arcadeclassic.ttf',
            SUBTITLE_TEXT_SIZE,
            subtitle,
            WHITE,
            self.display_rect
        )
        self.game_over_subtitle.rect.top = self.game_over_title.rect.bottom + TITLE_SUBTITLE_MARGIN

    def quit(self):
        pygame.quit()
        sys.exit()

    def setup_game(self):
        self.intro_title = Text(
            'assets/arcadeclassic.ttf',
            TITLE_TEXT_SIZE,
            'Space Skirmishers',
            WHITE,
            self.display_rect
        )
        self.intro_subtitle = Text(
            'assets/arcadeclassic.ttf',
            SUBTITLE_TEXT_SIZE,
            'Press any key to start game',
            WHITE,
            self.display_rect
        )
        self.intro_subtitle.rect.top = self.intro_title.rect.bottom + TITLE_SUBTITLE_MARGIN
        self.game_over_title = Text(
            'assets/arcadeclassic.ttf',
            TITLE_TEXT_SIZE,
            'Game over',
            WHITE,
            self.display_rect
        )

        # Setting up sprites
        self.player_1, self.player_2 = self.make_players()
        self.player_1_bullets = pygame.sprite.Group()
        self.player_2_bullets = pygame.sprite.Group()
        self.all_bullets = pygame.sprite.Group(self.player_1_bullets, self.player_2_bullets)
        self.obstacle_group_1 = self.make_obstacles()
        self.all_obstacles = pygame.sprite.Group(self.obstacle_group_1)
        self.all_sprites = pygame.sprite.Group(self.player_1, self.player_2, self.all_obstacles, self.all_bullets)

        # Setting up timing and inputs
        self.fps = 30
        self.keys = pygame.key.get_pressed()
        self.clock = pygame.time.Clock()

        self.game_to_start = True
        self.game_started = False
        self.game_over = False

    def main_loop(self):
        while True:
            if self.game_to_start:
                self.setup_game()
                self.game_over = False

                self.display_screen.fill(COLOR_BACKGROUND)

                self.intro_title.draw(self.display_screen)
                self.intro_subtitle.draw(self.display_screen)

                self.check_game_to_start_input()
                pygame.display.update()

            elif self.game_over:
                self.display_screen.fill(COLOR_BACKGROUND)

                self.game_over_title.draw(self.display_screen)
                self.game_over_subtitle.draw(self.display_screen)

                self.check_game_over_input()
                pygame.display.update()

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
