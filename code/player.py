import pygame
from support import import_dir
from tiles import StaticTile

class Player(pygame.sprite.Sprite):
    def __init__(self, position, surface, create_particles):
        super().__init__()
        self.import_character_assets()
        self.goal2 = pygame.sprite.GroupSingle()
        self.player_index = 0
        self.animation_speed = 0.15
        self.image = self.animations['idle'][self.player_index]
        self.rect = self.image.get_rect(topleft = position)

        self.import_dust_run_particles()
        self.dust_frame_index = 0
        self.dust_animation_speed = 0.15
        self.display_surface = surface
        self.create_particles = create_particles

        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 8
        self.gravity = 0.8
        self.jump_speed = -16

        self.status = 'idle'
        self.facing_right = True

        self.on_ground = False
        self.on_ceiling = False
        self.on_right = False
        self.on_left = False
        self.reset = False

        self.health = 3
        self.max_health = 5
        self.invincible = False
        self.invincibility_timer = 1000
        self.damage_taken_timer = 0
        self.full_heart = pygame.image.load("../graphics/health/full_heart.png").convert_alpha()

    def invincibility_time(self):
        if self.invincible:
            current_time = pygame.time.get_ticks()
            if current_time - self.damage_taken_timer >= self.invincibility_timer:
                self.invincible = False

    def import_character_assets(self):
        character_path = '../graphics/character/'
        self.animations = {'idle':[], 'run':[], 'jump':[], 'fall':[]}

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_dir(full_path)

    def import_dust_run_particles(self):
        self.dust_run_particles = import_dir('../graphics/character/dust_particles/run')

    def animate(self):
        animation = self.animations[self.status]

        self.player_index += self.animation_speed
        if self.player_index >= len(animation):
            self.player_index = 0

        image = animation[int(self.player_index)]
        if self.facing_right:
            self.image = image
        else:
            flipped_image = pygame.transform.flip(image, True, False)
            self.image = flipped_image

        if self.on_ground and self.on_right:
            self.rect = self.image.get_rect(bottomright = self.rect.bottomright)
        elif self.on_ground and self.on_left:
            self.rect = self.image.get_rect(bottomleft = self.rect.bottomleft)
        elif self.on_ground:
            self.rect = self.image.get_rect(midbottom = self.rect.midbottom)
        elif self.on_ceiling and self.on_left:
            self.rect = self.image.get_rect(topleft = self.rect.topleft)
        elif self.on_ceiling and self.on_right:
            self.rect = self.image.get_rect(topright = self.rect.topright)
        elif self.on_ceiling:
            self.rect = self.image.get_rect(midtop = self.rect.midtop)
        else:
            self.rect = self.image.get_rect(center = self.rect.center)

    def run_dust_animation(self):
        if self.status == 'run' and self.on_ground:
            self.dust_frame_index += self.dust_animation_speed
            if self.dust_frame_index >= len(self.dust_run_particles):
                self.dust_frame_index = 0

            dust_particle = self.dust_run_particles[int(self.dust_frame_index)]

            if self.facing_right:
                pos = self.rect.bottomleft - pygame.math.Vector2(6, 10)
                self.display_surface.blit(dust_particle, pos)
            else:
                pos = self.rect.bottomright - pygame.math.Vector2(6, 10)
                flipped_dust_particle = pygame.transform.flip(dust_particle, True, False)
                self.display_surface.blit(flipped_dust_particle, pos)

    def get_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.facing_right = True
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.facing_right = False
        else:
            self.direction.x = 0

        if keys[pygame.K_SPACE]:
            self.jump()
            self.create_particles(self.rect.midbottom)

    def get_status(self):
        if self.direction.y < 0:
            self.status = 'jump'
        elif self.direction.y >self.gravity:
            self.status = 'fall'
        else:
            if self.direction.x != 0:
                self.status = 'run'
            else:
                self.status = 'idle'

    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def jump(self):
        self.direction.y = self.jump_speed

    def update(self):

        self.get_input()
        self.get_status()
        self.animate()
        self.run_dust_animation()
        self.invincibility_time()

