import pygame
import sys
from pygame.locals import*
import player
import enemy
from player import button, Player

pygame.init()

FPS = 60
FPS_CLOCK = pygame.time.Clock()
font = pygame.font.Font("square.ttf",32)
# Global variables
SCREEN_WIDTH = 960
SCREEN_HEIGHT = 540

# Setting up color objects
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

displaysurface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))




class Background(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.bgimage = pygame.image.load("game_background_1.png")
        self.bgY = 0
        self.bgX = 0

    def render(self):
        displaysurface.blit(self.bgimage, (self.bgX, self.bgY))


background = Background()
class game:
    def __init__(self):
        self.running = True
        self.font = pygame.font.Font("square.ttf", 32)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.intro_background = pygame.image.load("battleground.png")


    def intro_screen(self):
        intro = True
        title = self.font.render("PYTHON GAME", True, WHITE)
        title_rect = title.get_rect(x=10,y=10)
        play_button = button(10,50,100,50,WHITE,BLUE,"play",32)
        quit_button = button(10,110,100,50,WHITE,BLUE,"quit",32)
        while intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    intro = False
                    self.running = False

            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()
            if play_button.is_pressed(mouse_pos,mouse_pressed):
                intro = False

            self.screen.blit(self.intro_background,(0,0))
            self.screen.blit(title,title_rect)
            self.screen.blit(play_button.image,play_button.rect)
            self.screen.blit(quit_button.image,quit_button.rect)
            pygame.display.update()
gameMenu = game()
gameMenu.intro_screen()
hit_cooldown = pygame.USEREVENT + 1


player2 = Player()
Playergroup = pygame.sprite.Group()
Playergroup.add(player2)

player = player.Player()
enemy1 = enemy.Enemy()

enemy.Enemy.update()
enemy.Enemy.move()
enemy.Enemy.draw()
# Player related functions
player.update()
if player.attacking == True:
      player.attack()
player.update()
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
    for event in pygame.event.get():
        if event.type == hit_cooldown:
            player.cooldown = False
            pygame.time.set_timer(hit_cooldown, 0)

    background.render()
    enemy1.update()
    enemy1.move(player.rect.center)
    enemy1.draw(displaysurface)
    # Move player
    player.update()
    player.draw(displaysurface)
    pygame.display.update()
    FPS_CLOCK.tick(FPS)
    player.update()
    if player.attacking == True:
        player.attack()
    else:
        player.move()

    


