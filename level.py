import sys

import pygame
from support import import_csv_layout, import_cut_graphic
from settings import tile_size, screen_height, screen_width
from tiles import Tile, StaticTile, Chest, Coin, Palm, Enemy, Sky, Water, Clouds
from player import Player
from particles import ParticleEffect

class Level:
    def __init__(self, level_data, surface):
        self.reset_enemy = False
        #coins
        self.player_gold = 0
        self.font = pygame.font.Font("../font/ARCADEPI.TTF",30)
        self.coin = pygame.sprite.GroupSingle()
        self.coin_ammount = 0
        #general setup
        self.display_surface = surface
        self.world_shift = 0
        self.current_x = None
        #player
        player_layout = import_csv_layout(level_data['player'])
        self.player_layout = player_layout
        self.player = pygame.sprite.GroupSingle()
        self.goal = pygame.sprite.GroupSingle()
        self.hearts_of_player = pygame.sprite.Group()
        self.player_setup(player_layout)
        self.distance = 0


        #dust
        self.dust_sprite = pygame.sprite.GroupSingle()
        self.player_on_ground = False
        self.explosion_sprites = pygame.sprite.Group()

        #terrain setup
        terrain_layout = import_csv_layout(level_data['terrain'])
        self.terrain_sprites = self.tile_group(terrain_layout, 'terrain')

        #grass setup
        grass_layout = import_csv_layout(level_data['grass'])
        self.grass_sprites = self.tile_group(grass_layout, 'grass')

        #crates
        chest_layout = import_csv_layout(level_data['chests'])
        self.chest_sprites = self.tile_group(chest_layout, 'chests')

        #coins
        coin_layout = import_csv_layout(level_data['coins'])
        self.coin_layouut =coin_layout
        self.coin_sprites = self.tile_group(coin_layout, 'coins')

        #foreground palms
        fg_palm_layout = import_csv_layout(level_data['fg palms'])
        self.fg_palm_sprites = self.tile_group(fg_palm_layout, 'fg palms')

        #background palms
        bg_palm_layout = import_csv_layout(level_data['bg palms'])
        self.bg_palm_sprites = self.tile_group(fg_palm_layout, 'bg palms')

        #enemy
        enemy_layout = import_csv_layout(level_data['enemies'])
        self.enemy_layouut = enemy_layout
        self.enemy_sprites = self.tile_group(enemy_layout, 'enemies')

        #constraint
        constraint_layout = import_csv_layout(level_data['constraints'])
        self.constraint_sprites = self.tile_group(constraint_layout, 'constraints')

        #decoration
        #sky
        self.sky = Sky(8)

        #water
        level_width = len(terrain_layout[0]) * tile_size
        self.water = Water(screen_height - 20, level_width)

        #clouds
        self.clouds = Clouds(400, level_width, 10)

    def win(self):
        if pygame.sprite.spritecollide(self.player.sprite,self.goal,False):
            pygame.quit()
            sys.exit()

    #picking right tiles with the help of condidiontals
    def tile_group(self, layout, type):
        sprite_group = pygame.sprite.Group()

        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                #val == -1 when there is nothing
                if val != "-1":
                    x = col_index * tile_size
                    y = row_index * tile_size

                    if type == "terrain":
                        terrain_tile_list = import_cut_graphic('../graphics/terrain/terrain_tiles.png')
                        tile_surface = terrain_tile_list[int(val)]
                        sprite = StaticTile(tile_size, x, y, tile_surface)

                    if type == "grass":
                        grass_tile_list = import_cut_graphic("../graphics/decoration/grass/grass.png")
                        tile_surface = grass_tile_list[int(val)]
                        sprite = StaticTile(tile_size, x, y, tile_surface)

                    if type == "chests": sprite = Chest(tile_size, x, y)

                    if type == "coins":
                        if val == "0": sprite = Coin(tile_size, x, y, "../graphics/coins/gold")
                        if val == "1": sprite = Coin(tile_size, x, y, "../graphics/coins/silver")

                    if type == "fg palms":
                        if val == "5":
                            sprite = Palm(tile_size, x, y, "../graphics/terrain/palm_small", 38)
                        if val == "4":
                            sprite = Palm(tile_size, x, y, "../graphics/terrain/palm_large", 64)

                    if type == "bg palms": sprite = Palm(tile_size, x, y, "../graphics/terrain/palm_bg", 64)

                    if type == "enemies": sprite = Enemy(tile_size, x, y)

                    if type == "constraints": sprite = Tile(tile_size, x, y)

                    sprite_group.add(sprite)

        return sprite_group

    def reset_enemies(self):
        if self.reset_enemy:
            self.reset_enemy =False
            self.enemy_sprites = self.tile_group(self.enemy_layouut, 'enemies')
            self.reset_enemy =False
            self.coin_sprites = self.tile_group(self.coin_layouut, 'coins')
    #creating the player
    def player_setup(self, layout):
        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size
                if val == '0':
                    sprite = Player((x, y), self.display_surface, self.create_jump_particles)
                    self.player.add(sprite)
                if val == '1':
                    hat_surface = pygame.image.load("../graphics/character/hat.png").convert_alpha()
                    sprite = StaticTile(tile_size, x, y, hat_surface)
                    self.goal.add(sprite)

    def show_coins(self, ammount):
        gold_coin = pygame.image.load("../graphics/coins/gold/0.png").convert_alpha()
        x = 50
        y = 100
        sprite = StaticTile(64, x, y, gold_coin)
        self.coin.add(sprite)
        coin_ammount_surf = self.font.render(str(self.coin_ammount),False,"#33323d")
        coin_ammount_rect = coin_ammount_surf.get_rect(midleft = (90,115))
        self.display_surface.blit(coin_ammount_surf,coin_ammount_rect)

    def hearts(self):
        heart = pygame.image.load("../graphics/health/full_heart.png").convert_alpha()
        x = 0
        y = 45
        for her in range(self.player.sprite.health):
            x = x+50
            sprite = StaticTile(64, x, y, heart)
            self.hearts_of_player.add(sprite)
    #creating smoke under player when jumping
    def create_jump_particles(self, pos):
        if self.player.sprite.facing_right:
            pos -= pygame.math.Vector2(10, 5)
        else:
            pos += pygame.math.Vector2(10, -5)
        jump_particle_sprite = ParticleEffect(pos, 'jump')
        self.dust_sprite.add(jump_particle_sprite)

    #creating smoke under player when jumping
    def create_landing_dust(self):
        if not self.player_on_ground and self.player.sprite.on_ground and not self.dust_sprite.sprites():
            if self.player.sprite.facing_right:
                offset = pygame.math.Vector2(10, 15)
            else:
                offset = pygame.math.Vector2(-10, 15)
            fall_dust_particle = ParticleEffect(self.player.sprite.rect.midbottom - offset, 'land')
            self.dust_sprite.add(fall_dust_particle)

    def defeat(self):
        player = self.player.sprite
        if player.reset:
            for row_index, row in enumerate(self.player_layout):
                for col_index, val in enumerate(row):
                    x = col_index * tile_size
                    y = row_index * tile_size

                    if val == '0':
                        player.rect.y = y
                        player.rect.x = x
                        self.world_shift = (self.distance)
                        player.reset = False
                        self.player.sprite.health = 3
            self.coin_ammount = 0
            self.distance = 0
            self.reset_enemy = True

    def vertical_movement_collision(self):
        player = self.player.sprite
        player.apply_gravity()

        if player.rect.y >= 600:
            player.reset = True



        for sprite in self.terrain_sprites.sprites() + self.chest_sprites.sprites() + self.fg_palm_sprites.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.on_ground = True
                elif player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0
                    player.on_ceiling = True

        if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
            player.on_ground = False
        if player.on_ceiling and player.direction.y > 0:
            player.on_ceiling = False

    #turning back an enemy
    def enemy_collision_reverse(self):
        for enemy in self.enemy_sprites.sprites():
            if pygame.sprite.spritecollide(enemy, self.constraint_sprites, False):
                enemy.reverse()

    def check_coin_collisions(self):
        coin_collisions = pygame.sprite.spritecollide(self.player.sprite, self.coin_sprites, False)

        if coin_collisions:
            for coin in coin_collisions:
                self.coin_ammount = self.coin_ammount+1
                coin.kill()
    #collisions with enemy
    def check_enemy_collisions(self):
        enemy_collisions = pygame.sprite.spritecollide(self.player.sprite, self.enemy_sprites,False)

        if enemy_collisions:
            for enemy in enemy_collisions:
                enemy_center = enemy.rect.centery
                enemy_top = enemy.rect.top
                player_bottom = self.player.sprite.rect.bottom
                if enemy_top < player_bottom < enemy_center and self.player.sprite.direction.y >= 0:
                    self.player.sprite.direction.y = -15
                    explosion_sprite = ParticleEffect(enemy.rect.center, 'explosion')
                    self.explosion_sprites.add(explosion_sprite)
                    enemy.kill()
                else:
                    if self.player.sprite.health > 0 and self.player.sprite.invincible == False:
                        self.player.sprite.health -= 1
                        self.player.sprite.invincible = True
                        self.player.sprite.damage_taken_timer = pygame.time.get_ticks()
                        print(self.player.sprite.health)
                        self.hearts_of_player.empty()

                    if self.player.sprite.health <= 0:
                        player = self.player.sprite
                        player.reset = True

    #movement_x
    def horizontal_movement_collision(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed

        for sprite in self.terrain_sprites.sprites() + self.chest_sprites.sprites() + self.fg_palm_sprites.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                    player.on_left = True
                    self.current_x = player.rect.left
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left
                    player.on_right = True
                    self.current_x = player.rect.right

        if player.on_left and (player.rect.left < self.current_x or player.direction.x >= 0):
            player.on_left = False
        if player.on_right and (player.rect.right > self.current_x or player.direction.x <= 0):
            player.on_right = False

    #catching when player is on ground


    #moving camera
    def scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x

        if player_x < screen_width / 4 and direction_x < 0:
            self.world_shift = 8
            self.distance -= 8
            player.speed = 0
        elif player_x > screen_width - (screen_width / 4) and direction_x > 0:
            self.world_shift = -8
            self.distance += 8
            player.speed = 0
        else:
            self.world_shift = 0
            player.speed = 8

    def run(self):
        #run level

        #sky
        self.sky.draw(self.display_surface)

        #clouds
        self.clouds.draw(self.display_surface, self.world_shift)

        #background palms
        self.bg_palm_sprites.update(self.world_shift)
        self.bg_palm_sprites.draw(self.display_surface)

        #terrain
        self.terrain_sprites.draw(self.display_surface)
        self.terrain_sprites.update(self.world_shift)

        #enemy
        self.enemy_sprites.update(self.world_shift)
        self.constraint_sprites.update(self.world_shift)
        self.enemy_collision_reverse()
        self.enemy_sprites.draw(self.display_surface)
        self.explosion_sprites.update(self.world_shift)
        self.explosion_sprites.draw(self.display_surface)
        #chests
        self.chest_sprites.update(self.world_shift)
        self.chest_sprites.draw(self.display_surface)

        #grass
        self.grass_sprites.update(self.world_shift)
        self.grass_sprites.draw(self.display_surface)

        #coins
        self.coin_sprites.update(self.world_shift)
        self.coin_sprites.draw(self.display_surface)

        #foreground palms
        self.fg_palm_sprites.update(self.world_shift)
        self.fg_palm_sprites.draw(self.display_surface)

        #dust particles
        self.dust_sprite.update(self.world_shift)
        self.dust_sprite.draw(self.display_surface)

        #player sprite
        self.player.update()
        self.horizontal_movement_collision()


        self.vertical_movement_collision()
        self.create_landing_dust()

        self.scroll_x()
        self.defeat()
        self.player.draw(self.display_surface)
        self.goal.update(self.world_shift)
        self.goal.draw(self.display_surface)
        self.check_enemy_collisions()
        self.check_coin_collisions()

        #water
        self.water.draw(self.display_surface, self.world_shift)

        self.hearts()
        self.hearts_of_player.draw(self.display_surface)

        self.show_coins(self.coin_ammount)
        self.coin.draw(self.display_surface)

        self.win()
