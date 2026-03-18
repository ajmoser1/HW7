import pygame
from entity import Entity
from settings import *

class Projectile(Entity):
    def __init__(self, pos, target, damage, groups):
        super().__init__(pos, groups)
        self.target = target
        self.damage = damage
        self.speed = 8.0
        
        self.image = pygame.Surface((10, 10), pygame.SRCALPHA)
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
            # We don't kill the target here directly to let Game loop handle reward
            self.kill()
        else:
            if distance != 0:
                direction = direction.normalize()
            self.pos += direction * self.speed
            self.rect.center = self.pos
