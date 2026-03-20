# settings.py

# Screen Settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Vaporwave/Cyberpunk Colors
NEON_PINK = (255, 105, 180)
CYAN = (0, 255, 255)
NEON_BLUE = (0, 240, 255)
DARK_PURPLE = (20, 0, 40)
GRID_COLOR = (50, 10, 80)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 50)
NEON_GREEN = (57, 255, 20)
MENU_BLUE = (10, 10, 60)

# Game Constants
TILE_SIZE = 64
ROWS = SCREEN_HEIGHT // TILE_SIZE
COLS = SCREEN_WIDTH // TILE_SIZE

UI_BAR_HEIGHT = 50

# Starting state
STARTING_HEALTH = 100
STARTING_CREDITS = 500  # Corporate Credits

import os
import pygame

_IMAGE_CACHE = {}

def load_sprite(filename, size):
    cache_key = (filename, size)
    if cache_key in _IMAGE_CACHE:
        return _IMAGE_CACHE[cache_key].copy()
        
    path = os.path.join("assets", filename)
    if os.path.exists(path):
        try:
            img = pygame.image.load(path).convert_alpha()
            scaled = pygame.transform.scale(img, size)
            _IMAGE_CACHE[cache_key] = scaled
            return scaled.copy()
        except pygame.error:
            pass
    return None
