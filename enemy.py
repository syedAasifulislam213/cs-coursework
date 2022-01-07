import pygame
from pygame.locals import *
import random

# Global variables
SCREEN_WIDTH = 960
SCREEN_HEIGHT = 540


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
