import pygame
from entity import Entity
from settings import *

class Projectile(Entity):
    def __init__(self, pos, target, damage, groups, tower_type="generic"):
        super().__init__(pos, groups)
        self.target = target
        self.damage = damage
        self.speed = 8.0
        self.tower_type = tower_type

        # Visual style per tower type
        self.image = pygame.Surface((10, 10), pygame.SRCALPHA)
        if tower_type == "laser":
            pygame.draw.circle(self.image, NEON_PINK, (5, 5), 5)
        elif tower_type == "plasma":
            pygame.draw.circle(self.image, NEON_BLUE, (5, 5), 5)
        elif tower_type == "emp":
            pygame.draw.circle(self.image, NEON_GREEN, (5, 5), 4)
            pygame.draw.circle(self.image, CYAN, (5, 5), 2)
        else:
            pygame.draw.circle(self.image, YELLOW, (5, 5), 5)
        self.rect = self.image.get_rect(center=self.pos)
        
    def update(self):
        if not self.target.alive():
            self.kill()
            return
            
        direction = self.target.pos - self.pos
        distance = direction.length()
        
        if distance < self.speed:
            self.target.health -= self.damage
            # EMP projectiles slow enemies
            if self.tower_type == "emp":
                self.target.slow_factor = 0.4
                self.target.slow_timer = 180  # 3 seconds at 60 FPS
            # We don't kill the target here directly to let Game loop handle reward
            self.kill()
        else:
            if distance != 0:
                direction = direction.normalize()
            self.pos += direction * self.speed
            self.rect.center = self.pos
