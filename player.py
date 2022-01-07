import pygame
import sys
from pygame.locals import *
SCREEN_WIDTH = 960
SCREEN_HEIGHT = 540


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

class Player(pygame.sprite.Sprite):
    def __init__(self):
        # Inherit from the pygame.sprite.Sprite superclass
        super().__init__()
        self.image = run_ani_R[0]
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        # Combat
        self.attacking = False
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

