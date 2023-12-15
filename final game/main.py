# This file was created by: carlos gomez and Louis Brailey 
# Mr.cozart showed us how to add floor
#Chatgpt helped us instantiate new background image

# import libraries and modules
import pygame as pg
from pygame.sprite import Sprite
import random
from random import randint
import os
from settings import *
from sprites import *
import math

vec = pg.math.Vector2

# setup asset folders here - images sounds etc.
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'images')
snd_folder = os.path.join(game_folder, 'sounds')

# initiate pygame
pg.init()

# set the background image up
screen = pg.display.set_mode((WIDTH, HEIGHT))
background = pg.image.load(os.path.join(img_folder, 'BG.png')).convert()

# Main class
class Game:
    def __init__(self):
        # init pygame and create a window
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption("Bellarun")
        self.clock = pg.time.Clock()
        self.running = True
        self.all_sprites = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.player = Player(self)
        self.all_sprites.add(self.player)    
        self.all_sprites.add(self.mobs)
        self.score = 0
        
        self.background = Background('BG.png')

        self.all_sprites.add(self.background)

        # self.finish_line_passed = False  # Flag to check if the finish line is passed
    def new(self): 
        # create a group for all sprites
        self.score = 0
        self.all_sprites = pg.sprite.Group()
        self.all_platforms = pg.sprite.Group()
        self.all_mobs = pg.sprite.Group()
        # instantiate classes
        self.player = Player(self)
        # add instances to groups
        self.all_sprites.add(self.player)
        self.ground = Fplatform(0, HEIGHT-100, WIDTH, 40, 'nothing')
        self.all_sprites.add(self.ground)

        for p in PLATFORM_LIST:
            # instantiation of the Platform class
            plat = Platform(*p)
            self.all_sprites.add(plat)
            self.all_platforms.add(plat)
        # create mobs...
        for m in range(0,10):
            m = Mob(randint(0, WIDTH), randint(0, math.floor(HEIGHT/2)), 20, 20, 'moving')
            self.all_sprites.add(m)
            self.all_mobs.add(m)

        self.run()
    
    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        self.all_sprites.update()
         # this prevents the player from jumping up through a platform
        hits = pg.sprite.spritecollide(self.player, self.all_platforms, False)
        ghits = pg.sprite.collide_rect(self.player, self.ground)
        if hits or ghits:
            if self.player.vel.y < 0:
                self.player.vel.y = -self.player.vel.y
            # this is what prevents the player from falling through the platform when falling down...
            elif self.player.vel.y > 0:
                if hits:
                    self.player.pos.y = hits[0].rect.top
                    self.player.vel.y = 0
                    self.player.vel.x = hits[0].speed*1.5
                if ghits:
                    self.player.pos.y = self.ground.rect.top
                    self.player.vel.y = 0
        self.background.update(self.player.vel)

        

    def events(self):
        for event in pg.event.get():
        # check for closed window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
                
    def draw(self):
        ############ Draw ################
        # draw the background screen
        self.screen.fill(BLACK)
        self.screen.blit(background, (0, 0))

    # Draw all sprites
        self.all_sprites.draw(self.screen)
        self.draw_text("Health: " + str(self.player.hitpoints), 22, WHITE, WIDTH/2, HEIGHT/10)
        self.background.rect.x -= self.player.vel.x
        # If the background goes off the screen, reset its position
        if self.background.rect.right < WIDTH:
            self.background.rect.x = 0
 
        # Draw the finish line
    
    # After drawing everything, flip the display
        pg.display.flip()

 
    
    def draw_text(self, text, size, color, x, y):
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x,y)
        self.screen.blit(text_surface, text_rect)

    def show_start_screen(self):
        pass
    def show_go_screen(self):
        pass

class Background(pg.sprite.Sprite):
    def __init__(self, image_path):
        super().__init__()

        # Load the background image
        self.image = pg.image.load(os.path.join(img_folder, image_path))
        self.rect = self.image.get_rect()

        # Set the initial position of the background
        self.rect.topleft = (0, 0)

    def update(self, player_velocity):
        # You can add any update logic here if needed
        self.rect.x -= player_velocity.x

        # If the background goes off the screen, reset its position
        if self.rect.right < WIDTH:
            self.rect.x = 0

g = Game()
while g.running:
    g.new()


pg.quit()