from random import randint, choice
from typing import Any

import pygame
from pygame import Surface
from pygame.display import set_caption, set_mode
from pygame.image import load
from pygame.sprite import Sprite, Group
from pygame.time import set_timer

# region VARS
pygame.init()
set_timer(pygame.USEREVENT, 1000)  # ball and cards spawn timer
FONT = pygame.font.SysFont("Segoe UI Emoji", 30)
WIDTH, HEIGHT = 800, 600
WINDOW = set_mode((WIDTH, HEIGHT))
set_caption("Football")
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
CLOCK = pygame.time.Clock()
FPS = 60
GAME_SCORE = 0
LIVES = 2


# endregion VARS

# region PLAYER
class Player(Sprite):
    def __init__(self, speed: int, lives: float, filename: str):
        Sprite.__init__(self)
        self.image = load(filename).convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.image.get_width(), self.image.get_height()))
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT - self.image.get_height() // 2))
        self.speed = speed
        self.lives = lives


player = Player(speed=10, lives=float(LIVES), filename='images/footballer.png')


# endregion PLAYER

# region BALLS
class Ball(Sprite):
    def __init__(self, x, speed, group, filename, score):
        Sprite.__init__(self)
        self.image = load(filename).convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.image.get_width() // 45, self.image.get_height() // 45))
        self.rect = self.image.get_rect(center=(x, 0))
        self.speed = speed
        self.add(group)
        self.score = score

    def update(self, *args: Any, **kwargs: Any) -> None:
        if self.rect.y < args[0] - 20:
            self.rect.y += self.speed
        else:
            self.kill()


balls = Group()


def create_ball(group):
    return Ball(
        x=randint(20, WIDTH - 20),
        speed=randint(2, 5),
        group=group,
        filename='images/ball.bmp',
        score=1  # point per 1 ball
    )


def catch_balls():
    global GAME_SCORE
    for ball in balls:
        if player.rect.collidepoint(ball.rect.center):
            GAME_SCORE += ball.score
            ball.kill()


create_ball(group=balls)  # create the first ball before start cycle


# endregion BALLS

# region CARDS
class Card(Sprite):
    def __init__(self, x, speed, group):
        Sprite.__init__(self)
        self.color = choice((YELLOW, RED))
        if self.color == YELLOW:
            self.damage = 0.5
        elif self.color == RED:
            self.damage = 1
        self.image = Surface((20, 30))
        self.image.fill(self.color)
        self.rect = self.image.get_rect(center=(x, 0))
        self.speed = speed
        self.add(group)

    def update(self, *args: Any, **kwargs: Any) -> None:
        if self.rect.y < args[0] - 20:
            self.rect.y += self.speed
        else:
            self.kill()


cards = Group()


def create_card(group):
    return Card(
        x=randint(20, WIDTH - 20),
        speed=randint(2, 5),
        group=group,
    )


def catch_cards():
    for card in cards:
        if player.rect.collidepoint(card.rect.center):
            player.lives -= card.damage
            card.kill()


create_card(group=cards)  # create the first ball before start cycle
# endregion CARDS

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.USEREVENT:
            create_ball(balls)
            create_card(cards)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.rect.x -= player.speed
        if player.rect.x < 0:
            player.rect.x = 0
    elif keys[pygame.K_RIGHT]:
        player.rect.x += player.speed
        if player.rect.x > WIDTH - player.rect.width:
            player.rect.x = WIDTH - player.rect.width

    catch_balls()
    catch_cards()

    # draw background
    WINDOW.fill(BLACK)

    # draw score
    text = FONT.render("Score: " + str(GAME_SCORE), True, WHITE)
    WINDOW.blit(text, (10, 10))

    # draw health bar
    health = "❤️" * int(player.lives)
    if str(player.lives).endswith(".5") and player.lives >= 0:
        health += "💔"
    text = FONT.render("Lives: " + str(health), True, WHITE)
    WINDOW.blit(text, (10, 40))

    if player.lives <= 0:
        text = FONT.render("GAME OVER", True, WHITE)
        WINDOW.blit(text, (WIDTH // 2 - 50, HEIGHT // 2))

    # draw balls
    balls.draw(WINDOW)
    WINDOW.blit(player.image, player.rect)

    # draw cards
    cards.draw(WINDOW)
    WINDOW.blit(player.image, player.rect)

    pygame.display.update()
    CLOCK.tick(FPS)
    balls.update(HEIGHT)
    cards.update(HEIGHT)
