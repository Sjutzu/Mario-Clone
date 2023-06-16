import pygame
from csv import reader
from settings import tile_size
from os import walk

#creating list which will show, which elements are on specific places
def import_csv_layout(path):
    map = []
    with open(path) as submap:
        level = reader(submap, delimiter = ',')
        for row in level:
            map.append(list(row))
        return map

#cutting tiles to make them blend with the background
def import_cut_graphic(path):
    surface = pygame.image.load(path).convert_alpha()
    tile_x = int(surface.get_size()[0] / tile_size)
    tile_y = int(surface.get_size()[1] / tile_size)

    cut_tiles = []
    for row in range(tile_y):
        for col in range(tile_x):
            x = col * tile_size
            y = row * tile_size
            new_surf = pygame.Surface((tile_size, tile_size), flags = pygame.SRCALPHA)
            new_surf.blit(surface, (0, 0), pygame.Rect(x, y, tile_size, tile_size))
            cut_tiles.append(new_surf)

    return cut_tiles

#important for tiles animation
def import_dir(path):
    list = []
    for _, __, files in walk(path):
        for file in files:
            full_path = path + '/' + file
            image = pygame.image.load(full_path).convert_alpha()
            list.append(image)

    return list