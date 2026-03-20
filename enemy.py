import pygame
from entity import Entity
from settings import *

class Enemy(Entity):
    def __init__(self, path_points, groups):
        super().__init__(path_points[0], groups)
        self.path_points = path_points
        self.target_waypoint_idx = 1
        
        self.speed = 1.0
        self.max_health = 10
        self.health = self.max_health
        self.reward = 10
        self.damage_to_player = 5
        self.reached_end = False
        self.slow_factor = 1.0
        self.slow_timer = 0
        
        self.image = pygame.Surface((30, 30))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(center=self.pos)
        
    def move(self):
        # Decrement slow timer
        if self.slow_timer > 0:
            self.slow_timer -= 1
            if self.slow_timer <= 0:
                self.slow_factor = 1.0

        if self.target_waypoint_idx < len(self.path_points):
            target = self.path_points[self.target_waypoint_idx]
            direction = target - self.pos
            distance = direction.length()
            effective_speed = self.speed * self.slow_factor

            if distance < effective_speed:
                self.pos = target
                self.target_waypoint_idx += 1
            else:
                direction = direction.normalize()
                self.pos += direction * effective_speed
                
            self.rect.center = self.pos
        else:
            self.reached_end = True
            self.kill()

    def draw_health_bar(self, surface):
        if self.health < self.max_health:
            ratio = max(0, self.health / self.max_health)
            bar_rect = pygame.Rect(self.rect.left, self.rect.top - 8, self.rect.width, 4)
            health_rect = pygame.Rect(self.rect.left, self.rect.top - 8, self.rect.width * ratio, 4)
            pygame.draw.rect(surface, RED, bar_rect)
            pygame.draw.rect(surface, NEON_GREEN, health_rect)

    def update(self):
        self.move()

class CorporateDrone(Enemy):
    def __init__(self, path_points, groups):
        super().__init__(path_points, groups)
        self.speed = 1.5
        self.max_health = 20
        self.health = self.max_health
        self.reward = 5
        self.damage_to_player = 2
        
        img = load_sprite("drone.png", (TILE_SIZE, TILE_SIZE))
        if img:
            self.image = img
        else:
            self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
            self.image.fill(WHITE)
            pygame.draw.rect(self.image, CYAN, (12, 10, 6, 15)) # Small tie
        self.rect = self.image.get_rect(center=self.pos)

class RiotPolice(Enemy):
    def __init__(self, path_points, groups):
        super().__init__(path_points, groups)
        self.speed = 0.8
        self.max_health = 60
        self.health = self.max_health
        self.reward = 15
        self.damage_to_player = 5
        
        img = load_sprite("riot.png", (TILE_SIZE, TILE_SIZE))
        if img:
            self.image = img
        else:
            self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
            self.image.fill((50, 50, 200)) # Blueprint/Shield color
            pygame.draw.rect(self.image, (30, 30, 30), (0, 0, 8, TILE_SIZE)) # Shield
        self.rect = self.image.get_rect(center=self.pos)

class CEO(Enemy):
    def __init__(self, path_points, groups):
        super().__init__(path_points, groups)
        self.speed = 0.5
        self.max_health = 250
        self.health = self.max_health
        self.reward = 100
        self.damage_to_player = 20
        
        img = load_sprite("ceo.png", (TILE_SIZE, TILE_SIZE))
        if img:
            self.image = img
        else:
            self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
            self.image.fill((150, 0, 50)) # Red power suit
            pygame.draw.circle(self.image, YELLOW, (TILE_SIZE//2, TILE_SIZE//2), 8) # Gold monocle/watch
        self.rect = self.image.get_rect(center=self.pos)
