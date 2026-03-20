import pygame
import math
from entity import Entity
from settings import *

class Tower(Entity):
    def __init__(self, pos, groups):
        super().__init__(pos, groups)
        self.range = 150
        self.damage = 10
        self.cooldown = 60 # wait frames
        self.timer = 0
        self.cost = 100
        self.tower_type = "generic"
        self.tower_level = 1
        self.max_level = 3

    @property
    def upgrade_cost(self):
        return int(self.cost * 0.6 * self.tower_level)

    def can_upgrade(self):
        return self.tower_level < self.max_level

    def upgrade(self):
        if not self.can_upgrade():
            return False
        self.tower_level += 1
        self.damage = int(self.damage * 1.4)
        self.range = int(self.range * 1.15)
        self.cooldown = max(3, int(self.cooldown * 0.85))
        # Tint the sprite to show upgrade level
        if hasattr(self, 'original_image') and self.original_image:
            tint = pygame.Surface(self.original_image.get_size(), pygame.SRCALPHA)
            if self.tower_level == 2:
                tint.fill((255, 255, 100, 40))
            elif self.tower_level == 3:
                tint.fill((255, 180, 0, 60))
            self.original_image.blit(tint, (0, 0))
            self.image = self.original_image.copy()
            self.rect = self.image.get_rect(center=self.pos)
        return True

    def draw_level_indicator(self, surface):
        if self.tower_level > 1:
            for i in range(self.tower_level - 1):
                x = self.rect.left + 4 + i * 8
                y = self.rect.bottom - 6
                pygame.draw.circle(surface, YELLOW, (x, y), 3)

    def draw_range(self, surface):
        circle_surf = pygame.Surface((self.range * 2, self.range * 2), pygame.SRCALPHA)
        pygame.draw.circle(circle_surf, (*CYAN, 50), (self.range, self.range), self.range)
        surface.blit(circle_surf, (self.rect.centerx - self.range, self.rect.centery - self.range))

    def update(self, enemies_group, shoot_callback):
        target = self.find_target(enemies_group)
        if target:
            # Calculate angle towards target
            dx = target.pos.x - self.pos.x
            dy = target.pos.y - self.pos.y
            # Pygame rotates CCW. If the sprite points UP initially, offset by -90 to align 0 degrees with RIGHT
            angle = math.degrees(math.atan2(-dy, dx)) - 90
            
            if hasattr(self, 'original_image') and self.original_image:
                self.image = pygame.transform.rotate(self.original_image, angle)
                self.rect = self.image.get_rect(center=self.pos)
                
            if self.timer <= 0:
                shoot_callback(self.rect.center, target, self.damage, self.tower_type)
                self.timer = self.cooldown
                
        if self.timer > 0:
            self.timer -= 1

    def find_target(self, enemies_group):
        closest_enemy = None
        min_dist = self.range
        for enemy in enemies_group.sprites():
            dist = self.pos.distance_to(enemy.pos)
            if dist <= min_dist:
                min_dist = dist
                closest_enemy = enemy
        return closest_enemy

class NeonLaser(Tower):
    def __init__(self, pos, groups):
        super().__init__(pos, groups)
        self.range = 150
        self.damage = 5
        self.cooldown = 20
        self.cost = 50
        self.name = "Neon Laser"
        self.tower_type = "laser"
        
        img = load_sprite("laser.png", (TILE_SIZE, TILE_SIZE))
        if img:
            self.image = img
        else:
            self.image = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
            pygame.draw.rect(self.image, NEON_PINK, (TILE_SIZE//4, TILE_SIZE//4, TILE_SIZE//2, TILE_SIZE//2))
            pygame.draw.rect(self.image, CYAN, (TILE_SIZE//2 - 5, 0, 10, TILE_SIZE//2)) # Gun barrel towards top
        self.rect = self.image.get_rect(center=self.pos)
        self.original_image = self.image.copy()

class PlasmaBlaster(Tower):
    def __init__(self, pos, groups):
        super().__init__(pos, groups)
        self.range = 100
        self.damage = 35
        self.cooldown = 90
        self.cost = 150
        self.name = "Plasma Blaster"
        self.tower_type = "plasma"
        
        img = load_sprite("plasma.png", (TILE_SIZE, TILE_SIZE))
        if img:
            self.image = img
        else:
            self.image = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
            pygame.draw.circle(self.image, NEON_BLUE, (TILE_SIZE//2, TILE_SIZE//2), TILE_SIZE//3)
            pygame.draw.circle(self.image, WHITE, (TILE_SIZE//2, TILE_SIZE//2), 8)
        self.rect = self.image.get_rect(center=self.pos)
        self.original_image = self.image.copy()

class CyberEMP(Tower):
    def __init__(self, pos, groups):
        super().__init__(pos, groups)
        # EMP slows enemies down with fast low damage + slow debuff
        self.range = 180
        self.damage = 3
        self.cooldown = 10
        self.cost = 125
        self.name = "Cyber EMP"
        self.tower_type = "emp"
        
        img = load_sprite("emp.png", (TILE_SIZE, TILE_SIZE))
        if img:
            self.image = img
        else:
            self.image = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
            pts = [(TILE_SIZE//2, 0), (TILE_SIZE, TILE_SIZE//2), (TILE_SIZE//2, TILE_SIZE), (0, TILE_SIZE//2)]
            pygame.draw.polygon(self.image, NEON_GREEN, pts)
        self.rect = self.image.get_rect(center=self.pos)
        self.original_image = self.image.copy()
