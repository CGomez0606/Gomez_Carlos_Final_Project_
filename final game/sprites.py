# This file was created by Carlos Gomez

import pygame as pg
from pygame.sprite import Sprite
import random
from random import randint
from pygame.math import Vector2 as vec
import os
from settings import *

# setup asset folders here - images sounds etc.
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'images')
snd_folder = os.path.join(game_folder, 'sounds')
#  Defines the bell that we see runnning in the game and controls his jump
class Bell(pg.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.image = pg.Surface((25, 25))
        self.image = pg.image.load(os.path.join(img_folder, 'theBigBell.png')).convert()
        self.rect = self.image.get_rect()
        self.rect.midbottom = (WIDTH // 4, HEIGHT)
        self.vel = vec(0, 0)
        self.acc = vec(0, PLAYER_GRAV)  
        self.jumping = False

    def jump(self):
        if not self.jumping:
            self.vel.y = -20
            self.jumping = True

    def update(self):
        self.acc = vec(0, PLAYER_GRAV)
        keys = pg.key.get_pressed()
        if keys[pg.K_SPACE]:
            self.jump()

        self.vel += self.acc
        self.rect.y += self.vel.y

        # Keep the player on the screen
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
            self.jumping = False

#This class is dedicated to the mobs or obstacles
class Obstacle(pg.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.image = pg.Surface((5 , 10))
        self.image = pg.image.load(os.path.join(img_folder, 'JUG.png')).convert()
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH
        self.rect.y = HEIGHT - self.rect.height
        self.speed = -5

 
    def update(self):
        pass