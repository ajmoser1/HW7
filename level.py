import pygame
from settings import *

class Level:
    def __init__(self):
        # Define a snaking path for enemies using grid coordinates (col, row)
        self.path = [
            (-1, 2), (3, 2), (3, 6), (8, 6), (8, 3), (12, 3), (12, 8), (16, 8)
        ]
        self.path_rects = []
        self._build_path_rects()

    def _build_path_rects(self):
        """Convert grid path into pixel rects for drawing the track."""
        self.path_rects = []
        for i in range(len(self.path) - 1):
            p1 = self.path[i]
            p2 = self.path[i+1]
            
            x1, y1 = p1[0] * TILE_SIZE, p1[1] * TILE_SIZE
            x2, y2 = p2[0] * TILE_SIZE, p2[1] * TILE_SIZE
            
            if x1 == x2: # Vertical line
                rect = pygame.Rect(x1, min(y1, y2), TILE_SIZE, abs(y2 - y1) + TILE_SIZE)
            else: # Horizontal line
                rect = pygame.Rect(min(x1, x2), y1, abs(x2 - x1) + TILE_SIZE, TILE_SIZE)
            self.path_rects.append(rect)

    def draw(self, surface):
        """Draw the vaporwave-style ground/path."""
        # Draw the neon border (outline layer) first
        for rect in self.path_rects:
            # Inflate gives a larger rect by 4 pixels in width and height (2px on each side)
            outline_rect = rect.inflate(4, 4)
            pygame.draw.rect(surface, NEON_PINK, outline_rect)
            
        # Draw the path itself on top, covering up any overlapping inner outlines
        for rect in self.path_rects:
            pygame.draw.rect(surface, (30, 0, 50), rect)

    def get_path_pixel_points(self):
        """Return exact pixel coordinates for enemy centers to traverse."""
        points = []
        for p in self.path:
            # Center of the tile
            points.append(pygame.math.Vector2(p[0] * TILE_SIZE + TILE_SIZE // 2, p[1] * TILE_SIZE + TILE_SIZE // 2))
        return points
