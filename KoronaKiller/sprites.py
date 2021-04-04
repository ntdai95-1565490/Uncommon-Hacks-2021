import random
import pygame as pg
from os import path

class Player(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.image.load(path.join(path.join(path.dirname(__file__), "Images/character"), "Idle (1).png")).convert_alpha()
        self.image = pg.transform.scale(self.image, (300, 300))
        self.mask = pg.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = 500
        self.player_x_change = 0
        self.player_y_change = 0
        self.player_life_point = 5
        self.player_move_horizontal = None
        self.player_move_vertical = None
        self.player_score = 0 

    def update(self):
        if self.player_move_horizontal == None:
            self.player_x_change = 0
        elif self.player_move_horizontal == "LEFT"and self.rect.y == 500:
            self.player_x_change = -15
        elif self.player_move_horizontal == "RIGHT"and self.rect.y == 500:
            self.player_x_change = 15

        if self.rect.x <= -50:
            self.rect.x = -50
        elif self.rect.x >= 1200:
            self.rect.x = 1200
        self.rect.x += self.player_x_change

        if self.player_move_vertical == "UP" and self.rect.y == 500:
            self.player_y_change = -15
        elif self.rect.y <= 100:
            self.player_y_change = 15
        elif self.rect.y >= 500:
            self.player_y_change = 0
        self.rect.y += self.player_y_change

class Vaccine(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.image.load(path.join(path.join(path.dirname(__file__), "Images"), "vaccine.png")).convert_alpha()
        self.image = pg.transform.scale(self.image, (150, 150))
        self.mask = pg.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = -1000
        self.rect.y = -1000
        self.vaccine_x_change = 25
        self.vaccine_is_on = False

    def update(self):
        if self.vaccine_is_on:
            self.rect.x += self.vaccine_x_change
            if self.rect.x >= 1500:
                self.vaccine_is_on = False
        else:
            self.rect.x = -1000
            self.rect.y = -1000 

class Virus(pg.sprite.Sprite):
    def __init__(self, i):
        super().__init__()
        if i % 3 == 0:
            self.image = pg.image.load(path.join(path.join(path.dirname(__file__), "Images/enemy"), "angry_virus.png")).convert_alpha()
        elif i % 3 == 1:
            self.image = pg.image.load(path.join(path.join(path.dirname(__file__), "Images/enemy"), "happy_virus.png")).convert_alpha()
        else:
            self.image = pg.image.load(path.join(path.join(path.dirname(__file__), "Images/enemy"), "pirate_virus.png")).convert_alpha()
        self.image = pg.transform.scale(self.image, (200, 200))
        self.mask = pg.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(1500, 1800)
        self.rect.y = random.randint(100, 550)
        self.speed = -10

    def update(self):
        if self.rect.x < 0:
            self.rect.x = 1500
            self.rect.y = random.randint(100, 550)
        else:
            self.rect.x += self.speed 


class Mask(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.image.load(path.join(path.join(path.dirname(__file__), "Images"), "mask.png")).convert_alpha()
        self.image = pg.transform.scale(self.image, (100, 100))
        self.mask = pg.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(1500, 1800)
        self.rect.y = random.randint(100, 550)
        self.speed = -10
        self.appear = False

    def update(self):
        if self.appear and self.rect.x == -1000:
            self.rect.x = random.randint(1500, 1800)
            self.rect.y = random.randint(100, 550)
        elif self.appear and self.rect.x >= 0:
            self.rect.x += self.speed 
        else:
            self.appear = False
            self.rect.x = -1000
            self.rect.y = -1000