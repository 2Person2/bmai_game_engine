# This file was created by: Brandon Mai
# my first source control edit
# importing libraries

# Goals: waves of enemies, weapons, currency

import pygame as pg
import sys
from settings import *
from sprites import *
from random import randint
from os import path
from time import sleep

#create game class
class Game:
    # initializing attributes
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)
        self.load_data()
    # load save game data
    def load_data(self):
        game_folder = path.dirname(__file__)
        # added image
        img_folder = path.join(game_folder, 'images')
        self.player_img = pg.image.load(path.join(img_folder, 'dragon.png')).convert_alpha()
        self.map_data = []
        with open(path.join(game_folder, 'map.txt'), 'rt') as f:
            for line in f:
                self.map_data.append(line)
                print(self.map_data)
                print(enumerate(self.map_data))

    def new(self):
        # init all variables, setup groups, instantiate classes
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.power_ups = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        # self.player = Player(self, 10, 10)
        # for x in range(10, 20):
        #     Wall(self, x, 5)
        for row, tiles in enumerate(self.map_data):
            for col, tile in enumerate(tiles):
                # print(col)
                # print(tiles)
                if tile == '1':
                    Wall(self, col, row)
                if tile == 'P':
                    self.player = Player(self, col, row)
                if tile == 'U':
                    PowerUp(self, col, row)
                if tile == 'M':
                    Mob(self, col, row)
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

    # drawing background
    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))
    def draw(self):
        self.screen.fill(BGCOLOR)
        self.draw_grid()
        self.all_sprites.draw(self.screen)
        pg.display.flip()
    #events
    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            # if event.type == pg.KEYDOWN:
            #     if event.key == pg.K_LEFT:
            #         self.player.move(dx=-1)
            #     if event.key == pg.K_RIGHT:
            #         self.player.move(dx=1)
            #     if event.key == pg.K_UP:
            #         self.player.move(dy=-1)
            #     if event.key == pg.K_DOWN:
            #         self.player.move(dy=1)

    def show_start_screen(self):
        pass

    def show_go_screen(self):
        pass

g = Game()
# g.show_start_screen()
while True:
    g.new()
    g.run()
    # g.show_go_screen()

g.run()