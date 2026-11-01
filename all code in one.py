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
    pygame.display.up








import random
from pygame.locals import *
import pygame

font = pygame.font.Font

SCREEN_WIDTH = 960
SCREEN_HEIGHT = 540
WHITE = (255, 255, 255)

displaysurface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
score_value = 0





class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        # Inherit from the pygame.sprite.Sprite superclass
        super().__init__()
        self.image = pygame.image.load("2_enemies_idle_001.png")  # Find image for enemy
        self.rect = self.image.get_rect()
        xPos = random.randint(0, 1)
        if xPos == 0:
            xPos = 0
        else:
            xPos = SCREEN_WIDTH
        yPos = random.randint(100, SCREEN_HEIGHT - 100)

        self.rect.center = (xPos, yPos)

        # Combat
        self.attacking = False
        self.attack_frame = 0

        # Set the default variables
        self.health = 5
        self.direction = "RIGHT"

        # Set up animation variables
        # self.running = False
        self.move_frame = 0
        self.xpos = (0, 0)
        self.ypos = (0, 0)

    def update(self):
        # Return to base frame if at end of movement sequence
        if self.move_frame > 6:
            self.move_frame = 0
            return

    def move(self, playerCoords):
        playerX = playerCoords[0]
        playerY = playerCoords[1]
        enemyX = self.rect.center[0]
        enemyY = self.rect.center[1]

        if self.rect.left > 0:
            if enemyX > playerX:
                # self.image = run_ani_L[self.move_frame]
                self.rect.move_ip(-1, 0)
                self.direction = "LEFT"
        if self.rect.right < SCREEN_WIDTH:
            if enemyX < playerX:
                # self.image = run_ani_R[self.move_frame]
                self.rect.move_ip(1, 0)
                self.direction = "RIGHT"
        if self.rect.top > 40:
            if enemyY > playerY:
                self.rect.move_ip(0, -1)
                # self.direction = "UP"
        if self.rect.bottom < 485:
            if enemyY < playerY:
                self.rect.move_ip(0, 1)
                # self.direction = "DOWN"

    def attack(self):
        # If attack frame has reached end of sequence, return to base frame
        if self.attack_frame > 10:
            self.attack_frame = 0
            self.attacking = False

        # Check direction for correct animation to display
        if self.direction == "RIGHT":
            self.image = attack_ani_R[self.attack_frame]
        elif self.direction == "LEFT":
            self.image = attack_ani_L[self.attack_frame]
        # Update the current attack frame
        self.attack_frame += 1

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def correction(self):
        # Function is used to correct an error
        # with character position on left attack frames
        if self.attack_frame == 1:
            self.xpos -= 20
        if self.attack_frame == 10:
            self.ypos += 20

    def enemy_hit(self,player):
        if pygame.sprite.collide_rect(player,self):
            print("enemy hit")

            self.kill()








import pygame
import sys
from pygame.locals import *
SCREEN_WIDTH = 960
SCREEN_HEIGHT = 540

displaysurface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# Set player animations
run_ani_R = [pygame.image.load("player/Movement_Animations/Player_Sprite_R.png"),
             pygame.image.load("player/Movement_Animations/Player_Sprite2_R.png"),
             pygame.image.load("player/Movement_Animations/Player_Sprite3_R.png"),
             pygame.image.load("player/Movement_Animations/Player_Sprite4_R.png"),
             pygame.image.load("player/Movement_Animations/Player_Sprite5_R.png"),
             pygame.image.load("player/Movement_Animations/Player_Sprite6_R.png"),
             pygame.image.load("player/Movement_Animations/Player_Sprite_R.png")]

run_ani_L = [pygame.image.load("player/Movement_Animations/Player_Sprite_L.png"),
             pygame.image.load("player/Movement_Animations/Player_Sprite2_L.png"),
             pygame.image.load("player/Movement_Animations/Player_Sprite3_L.png"),
             pygame.image.load("player/Movement_Animations/Player_Sprite4_L.png"),
             pygame.image.load("player/Movement_Animations/Player_Sprite5_L.png"),
             pygame.image.load("player/Movement_Animations/Player_Sprite6_L.png"),
             pygame.image.load("player/Movement_Animations/Player_Sprite_L.png")]

# Attack animation for the RIGHT
attack_ani_R = [pygame.image.load("player/Attack_Animations/Player_Attack_R.png"), pygame.image.load("player/Attack_Animations/Player_Attack_R.png"),
                pygame.image.load("player/Attack_Animations/Player_Attack2_R.png"), pygame.image.load("player/Attack_Animations/Player_Attack2_R.png"),
                pygame.image.load("player/Attack_Animations/Player_Attack3_R.png"), pygame.image.load("player/Attack_Animations/Player_Attack3_R.png"),
                pygame.image.load("player/Attack_Animations/Player_Attack4_R.png"), pygame.image.load("player/Attack_Animations/Player_Attack4_R.png"),
                pygame.image.load("player/Attack_Animations/Player_Attack5_R.png"), pygame.image.load("player/Attack_Animations/Player_Attack5_R.png"),
                pygame.image.load("player/Attack_Animations/Player_Attack_R.png")]

# Attack animation for the LEFT
attack_ani_L = [pygame.image.load("player/Attack_Animations/Player_Attack_L.png"), pygame.image.load("player/Attack_Animations/Player_Attack_L.png"),
                pygame.image.load("player/Attack_Animations/Player_Attack2_L.png"), pygame.image.load("player/Attack_Animations/Player_Attack2_L.png"),
                pygame.image.load("player/Attack_Animations/Player_Attack3_L.png"), pygame.image.load("player/Attack_Animations/Player_Attack3_L.png"),
                pygame.image.load("player/Attack_Animations/Player_Attack4_L.png"), pygame.image.load("player/Attack_Animations/Player_Attack4_L.png"),
                pygame.image.load("player/Attack_Animations/Player_Attack5_L.png"), pygame.image.load("player/Attack_Animations/Player_Attack5_L.png"),
                pygame.image.load("player/Attack_Animations/Player_Attack_L.png")]

health_ani = [pygame.image.load("health/heart0.png"), pygame.image.load("health/heart.png"),
              pygame.image.load("health/heart2.png"), pygame.image.load("health/heart3.png"),
              pygame.image.load("health/heart4.png"), pygame.image.load("health/heart5.png")]



class Player(pygame.sprite.Sprite):
    def __init__(self):
        # Inherit from the pygame.sprite.Sprite superclass
        super().__init__()
        self.image = run_ani_R[0]
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        # Combat

        self.attacking = False
        self.cooldown = False
        self.attack_frame = 0
        # Set the default variables
        self.health = 5
        self.score = 0
        self.direction = "RIGHT"

        # Set up animation variables
        # self.running = False
        self.move_frame = 0
        self.xpos = (0,0)
        self.ypos = (0,0)
    def update(self):
        # Return to base frame if at end of movement sequence
        if self.move_frame > 6:
            self.move_frame = 0
            return
    def move(self):
        # Change condition values to fit in the background image setting boundary for the player to move
        pressed_keys = pygame.key.get_pressed()
        if self.rect.left > 0:
            if pressed_keys[K_a]:
                self.image = run_ani_L[self.move_frame]
                self.rect.move_ip(-5, 0)
                self.direction = "LEFT"
        if self.rect.right < SCREEN_WIDTH:
            if pressed_keys[K_d]:
                self.image = run_ani_R[self.move_frame]
                self.rect.move_ip(5, 0)
                self.direction = "RIGHT"
        if self.rect.top > 40:
            if pressed_keys[K_w]:
                self.rect.move_ip(0, -5)
                self.direction = "UP"
        if self.rect.bottom < 485:
            if pressed_keys[K_s]:
                self.rect.move_ip(0, 5)
                self.direction = "DOWN"

        if pressed_keys[K_s] == False and pressed_keys[K_w] == False and pressed_keys[K_d] == False and pressed_keys[
            K_a] == False:
            self.move_frame = 0
            if self.direction == "LEFT":
                self.image = run_ani_L[self.move_frame]
            else:
                self.image = run_ani_R[self.move_frame]
        else:
            self.move_frame += 1

    def attack(self):
        # If attack frame has reached end of sequence, return to base frame
        if self.attack_frame > 10:
            self.attack_frame = 0
            self.attacking = False

        # Check direction for correct animation to display
        if self.direction == "RIGHT":
            self.image = attack_ani_R[self.attack_frame]
        elif self.direction == "LEFT":

            self.image = attack_ani_L[self.attack_frame]
     # Update the current attack frame
        self.attack_frame += 1

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def correction(self):
        # Function is used to correct an error
        # with character position on left attack frames
        if self.attack_frame == 1:
            self.xpos -= 20
        if self.attack_frame == 10:
            self.ypos += 20

    def player_hit(self,hit_cooldown,Health):
        if self.cooldown == False:
            self.cooldown = True  # Enable the cooldown
            pygame.time.set_timer(hit_cooldown, 1000)  # Resets cooldown in 1 second

            print("hit")
            self.health -= 1
            Health.image = health_ani[self.health]
    def reset_health(self,Health):
        self.health = 5
        Health.image = health_ani[self.health]

class button:
    def __init__(self, x, y, width, height, fg, bg, content, fontsize):
        self.font = pygame.font.Font("square.ttf", fontsize)
        self.content = content

        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.fg = fg
        self.bg = bg

        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.bg)
        self.rect = self.image.get_rect()

        self.rect.x = self.x
        self.rect.y = self.y
        self.text = self.font.render(self.content, True, self.fg)
        self.text_rect = self.text.get_rect(center=(self.width / 2, self.height / 2))
        self.image.blit(self.text, self.text_rect)

    def is_pressed(self, pos, pressed):
        if self.rect.collidepoint(pos):
            if pressed[0]:
                return True
            return False
        return False


class HealthBar(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("health/heart5.png")

    def render(self):
        displaysurface.blit(self.image, (10, 10))



