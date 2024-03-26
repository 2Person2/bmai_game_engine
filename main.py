# This file was created by: Brandon Mai
# Inspiration from: Chris Cozort
# my first source control edit
# importing libraries

# Goals: coins, enemy, levels

import pygame as pg
import sys
from settings import *
from sprites import *
from random import randint
from os import path
from time import sleep

LEVEL1_EASY = "level1_easy.txt"
LEVEL2_EASY = "level2_easy.txt"
LEVEL3_EASY = "level3_easy.txt"
LEVEL1_HARD = "level1_hard.txt"
LEVEL2_HARD = "level2_hard.txt"
LEVEL3_HARD = "level3_hard.txt"

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
        # loading images
        self.img_folder = path.join(self.game_folder, 'images')
        self.player_img = pg.image.load(path.join(self.img_folder, 'dragon.png')).convert_alpha()
        self.coin_img = pg.image.load(path.join(self.img_folder, 'coin.png')).convert_alpha()
        self.mob_img = pg.image.load(path.join(self.img_folder, 'bomb.png')).convert_alpha()
        self.speed_img = pg.image.load(path.join(self.img_folder, 'speed.png')).convert_alpha()
        self.map_data = []
        # loading maps
        with open(path.join(self.game_folder, 'LEVEL1_EASY.txt'), 'rt') as f:
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
        if self.player.money == 10 and self.player.level == 1:
            self.change_level(LEVEL2_EASY)
            self.player.level = 2
        if self.player.money == 10 and self.player.level == 2:
            self.change_level(LEVEL3_EASY)
            self.player.level = 3
        if self.player.money == 10 and self.player.level == 3:
            self.show_win_screen()
        if self.player.money == 10 and self.player.level == 7:
            self.change_level(LEVEL2_HARD)
            self.player.level = 8
        if self.player.money == 10 and self.player.level == 8:
            self.change_level(LEVEL3_HARD)
            self.player.level = 9
        if self.player.money == 10 and self.player.level == 9:
            self.show_win_screen()


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
        self.draw_text(self.screen, "Progress: "+str(round(self.player.money*10))+"%", 48, BLACK, 1, 1)
        pg.display.flip()
    #events
    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()

    # start screen
    # start screen
    def show_start_screen_hard(self):
        self.start_button = pg.Rect(332, 325, 400, 100)  # Define start_button as an attribute of the class
        self.screen.fill(BGCOLOR)
        pg.draw.rect(self.screen, RED, self.start_button)
        # Add text on the button
        self.draw_text(self.screen, "START", 64, WHITE, 450, 340)  # Adjust position based on button size and text size
        pg.display.flip()
        self.wait_for_key()

    def show_start_screen(self):
        self.screen.fill(BGCOLOR)
        self.draw_text(self.screen, "PRESS 1 FOR EASY", 64, WHITE, 265, 250)
        self.draw_text(self.screen, "PRESS 2 FOR MEDIUM", 64, WHITE, 230, 340)
        self.draw_text(self.screen, "PRESS 3 FOR HARD", 64, WHITE, 265, 430)
        pg.display.flip()
        self.wait_for_key()
    
    # death screen
    def show_death_screen(self):
        self.screen.fill(BGCOLOR)
        self.draw_text(self.screen, "YOU DIED", 64, WHITE, WIDTH/2 - 128, HEIGHT/2 - 64)
        pg.display.flip()
        sleep(2)
        self.wait_for_key()

    # win screen
    def show_win_screen(self):
        self.screen.fill(BGCOLOR)
        self.draw_text(self.screen, "YOU WON", 64, WHITE, WIDTH/2 - 128, HEIGHT/2 - 64)
        pg.display.flip()
        sleep(3)
        self.wait_for_key()

    # press key to move on
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
                if event.type == pg.MOUSEBUTTONDOWN:
                    mouse_pos = pg.mouse.get_pos()
                    if self.start_button.collidepoint(mouse_pos):  # Access start_button using self
                        waiting = False
                        self.new()

g = Game()

g.show_start_screen()
while True:
    g.new()
    g.run()
