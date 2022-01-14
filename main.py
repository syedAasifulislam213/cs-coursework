import pygame
import sys
from pygame.locals import *

import enemy
import player

from player import button, Player, HealthBar

pygame.init()

FPS = 60
FPS_CLOCK = pygame.time.Clock()
font = pygame.font.Font("square.ttf", 32)
# Global variables
SCREEN_WIDTH = 960
SCREEN_HEIGHT = 540

# Setting up color objects
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Set up pygame display object
displaysurface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

score_value = 0
textX = 800
textY = 10

def show_score(x, y):
    score = font.render("score :" + str(score_value), True , WHITE)
    displaysurface.blit(score,(x,y))

class Background(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.bgimage = pygame.image.load("game_background_1.png")
        self.bgY = 0
        self.bgX = 0

    def render(self):
        displaysurface.blit(self.bgimage, (self.bgX, self.bgY))

# Initialise background and health objects
background = Background()
Health = HealthBar()

class game:
    def __init__(self):
        self.running = True
        self.font = pygame.font.Font("square.ttf", 32)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.intro_background = pygame.image.load("battleground.png")

    def intro_screen(self):
        # display variable controls the menu game loop
        display = True
        title = self.font.render("PYTHON GAME", True, WHITE)
        title_rect = title.get_rect(x=10, y=10)
        play_button = button(10, 50, 100, 50, WHITE, BLUE, "play", 32)
        quit_button = button(10, 110, 100, 50, WHITE, BLUE, "quit", 32)
        while display:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    display = False
                    self.running = False

            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()
            if play_button.is_pressed(mouse_pos, mouse_pressed):
                # Close the menu object and start the game
                display = False
            if quit_button.is_pressed(mouse_pos, mouse_pressed):
                pygame.quit()
                sys.exit()

            self.screen.blit(self.intro_background, (0, 0))
            self.screen.blit(title, title_rect)
            self.screen.blit(play_button.image, play_button.rect)
            self.screen.blit(quit_button.image, quit_button.rect)
            pygame.display.update()

    def game_over_screen(self, player, Health):
        global score_value
        # display variable controls the menu game loop
        display = True
        title = self.font.render("GAME OVER", True, WHITE)
        title_rect = title.get_rect(x=10, y=10)
        play_button = button(10, 50, 100, 50, WHITE, BLUE, "play", 32)
        quit_button = button(10, 110, 100, 50, WHITE, BLUE, "quit", 32)
        score = self.font.render("Score:" + str(score_value), True, WHITE)
        score_rect = score.get_rect(x=200, y=60)
        while display:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    display = False
                    self.running = False

            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()
            if play_button.is_pressed(mouse_pos, mouse_pressed):
                # Reset all key game variables
                score_value = 0
                player.reset_health(Health)
                display = False
            if quit_button.is_pressed(mouse_pos, mouse_pressed):
                pygame.quit()
                sys.exit()

            self.screen.blit(self.intro_background, (0, 0))
            self.screen.blit(title, title_rect)
            self.screen.blit(play_button.image, play_button.rect)
            self.screen.blit(quit_button.image, quit_button.rect)
            self.screen.blit(score, score_rect)
            pygame.display.update()

gameMenu = game()
gameMenu.intro_screen()
hit_cooldown = pygame.USEREVENT + 1

player = player.Player()

enemyGroup = pygame.sprite.Group()


ENEMY_SPAWN = pygame.USEREVENT + 2
pygame.time.set_timer(ENEMY_SPAWN, 5000)


# Game loop
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
             if player.attacking == False:
                 player.attack()
                 player.attacking = True
        if event.type == hit_cooldown:
            player.cooldown = False
            pygame.time.set_timer(hit_cooldown, 0)
        if event.type == ENEMY_SPAWN:

            enemyGroup.add(enemy.Enemy())

    background.render()

    # Move enemies
    for enemySprite in enemyGroup:
        enemySprite.update()
        enemySprite.move(player.rect.center)
        enemySprite.draw(displaysurface)

    # Move player
    player.update()
    if player.attacking == True:
        player.attack()
    else:
        player.move()
    player.draw(displaysurface)

    # Player and enemy collision behaviour
    if pygame.sprite.spritecollideany(player, enemyGroup):
        if player.attacking == True:
            print("attack")

            for enemySprite in enemyGroup:
                enemySprite.enemy_hit(player)
                score_value += 1
        else:
            player.player_hit(hit_cooldown,Health)
            if player.health == 0:
                gameMenu.game_over_screen(player, Health)
        if player.health > 0:
            displaysurface.blit(player.image, player.rect)
    Health.render()


    FPS_CLOCK.tick(FPS)
    show_score(textX, textY)
    pygame.display.update()
