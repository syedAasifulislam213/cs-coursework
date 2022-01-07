import pygame
import sys
from pygame.locals import*
import player
import enemy
pygame.init()

FPS = 60
FPS_CLOCK = pygame.time.Clock()

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



player = player.Player()
enemy1 = enemy.Enemy()
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

    


