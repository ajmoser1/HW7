import pygame

class Entity(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.pos = pygame.math.Vector2(pos)
        self.image = pygame.Surface((32, 32), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=self.pos)

    def update(self):
        pass
