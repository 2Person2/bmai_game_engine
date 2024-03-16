# This file was created by: Brandon Mai
# my first source control edit
# importing libraries

# Goals: completion, enemy, hitpoints

import pygame as pg
import sys
from settings import *
from sprites import *
from random import randint
from os import path
from time import sleep

LEVEL1 = "level1.txt"
LEVEL2 = "level2.txt"

#create game class
class Game:
    # initializing attributes
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        # setting game clock 
        self.clock = pg.time.Clock()
        # self.load_data()
        self.running = True
        self.paused = False
        self.load_data()
    # load save game data
    def load_data(self):
        self.game_folder = path.dirname(__file__)
        self.img_folder = path.join(self.game_folder, 'images')
        self.player_img = pg.image.load(path.join(self.img_folder, 'dragon.png')).convert_alpha()
        self.coin_img = pg.image.load(path.join(self.img_folder, 'coin.png')).convert_alpha()
        self.mob_img = pg.image.load(path.join(self.img_folder, 'bomb.png')).convert_alpha()
        self.map_data = []
        with open(path.join(self.game_folder, 'LEVEL1.txt'), 'rt') as f:
            for line in f:
                self.map_data.append(line)

    def change_level(self, lvl):
        # kill all existing sprites first to save memory
        self.lvl = lvl
        for s in self.all_sprites:
            s.kill()
        # reset criteria for changing level
        self.player.money = 0
        # reset map data list to empty
        self.map_data = []
        # open next level
        with open(path.join(self.game_folder, self.lvl), 'rt') as f:
            for line in f:
                self.map_data.append(line)
        # repopulate the level with stuff
        for row, tiles in enumerate(self.map_data):
            for col, tile in enumerate(tiles):
                if tile == '1':
                    Wall(self, col, row)
                if tile == 'P':
                    self.player = Player(self, col, row)
                if tile == 'C':
                    Coin(self, col, row)
                if tile == 'M':
                    Mob(self, col, row)
                if tile == 'U':
                    PowerUp(self, col, row)

    def new(self):
        # init all variables, setup groups, instantiate classes
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.power_ups = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.coins = pg.sprite.Group()
        for row, tiles in enumerate(self.map_data):
            for col, tile in enumerate(tiles):
                if tile == '1':
                    Wall(self, col, row)
                if tile == 'P':
                    self.player = Player(self, col, row)
                if tile == 'U':
                    PowerUp(self, col, row)
                if tile == 'M':
                    Mob(self, col, row)
                if tile == 'C':
                    Coin(self,col, row)
    #define run method
    def run(self):
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()
    #define quit
    def quit(self):
        pg.quit()
        sys.exit()
    #updating sprites
    def update(self):
        self.all_sprites.update()
        if self.player.lives == 0:
            self.show_death_screen()
        if self.player.money == 10:
            self.change_level(LEVEL2)
        if self.player.money == 11:
            self.show_win_screen


    # drawing background
    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))
    # drawing text
    def draw_text(self, surface, text, size, color, x, y):
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x,y)
        surface.blit(text_surface, text_rect)
    
    # drawing everything
    def draw(self):
        self.screen.fill(BGCOLOR)
        self.draw_grid()
        self.all_sprites.draw(self.screen)
        pg.display.flip()
        self.draw_text(self.screen, "Progress: "+str(self.player.money*10)+"%", 48, BLACK, 1, 1)
        pg.display.flip()
    #events
    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()

    def show_start_screen(self):
        self.screen.fill(BGCOLOR)
        self.draw_text(self.screen, "PRESS ANY KEY TO START", 64, WHITE, 192, HEIGHT/2 - 64)
        pg.display.flip()
        self.wait_for_key()
    
    def show_death_screen(self):
        self.screen.fill(BGCOLOR)
        self.draw_text(self.screen, "YOU DIED", 64, WHITE, WIDTH/2 - 128, HEIGHT/2 - 64)
        pg.display.flip()
        sleep(2)
        level = 1
        self.wait_for_key()

    def show_win_screen(self):
        self.screen.fill(BGCOLOR)
        self.draw_text(self.screen, "YOU WON", 64, WHITE, WIDTH/2 - 128, HEIGHT/2 - 64)
        pg.display.flip()
        sleep(3)
        self.wait_for_key()

    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.quit()
                if event.type == pg.KEYUP:
                    waiting = False
                    self.new()

g = Game()

g.show_start_screen()
while True:
    g.new()
    g.run()
    # g.show_go_screen()

g.run()