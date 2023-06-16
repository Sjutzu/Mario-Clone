import pygame, sys
from settings import *
from level import Level
from game_data import level_1
from player import Player

class Game:
    def __init__(self):
        self.status = "menu"

licznik = 656576586
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
level = Level(level_1, screen)

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    clock.tick(60)
    level.run()
    pygame.display.update()
    if licznik == 1:
        licznik=454
        level.reset_enemies()
    if level.reset_enemy:
        licznik = 1

