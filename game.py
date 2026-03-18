# game.py
import pygame
import sys
from settings import *
from level import Level
from ui import UI
from enemy import CorporateDrone, RiotPolice, CEO
from tower import NeonLaser, PlasmaBlaster, CyberEMP
from projectile import Projectile

class Game:
    def __init__(self):
        # Setup the display
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Vaporwave Terminal Defense: Late Stage Capitalism")
        
        self.clock = pygame.time.Clock()
        
        # Game states: START_MENU, PLAYING, GAME_OVER
        self.state = "START_MENU"
        
        # Game systems initialization
        self.health = STARTING_HEALTH
        self.credits = STARTING_CREDITS
        self.wave = 0
        self.level = Level()
        self.ui = UI()
        
        self.enemies = pygame.sprite.Group()
        self.towers = pygame.sprite.Group()
        self.projectiles = pygame.sprite.Group()
        
        self.enemies_to_spawn = []
        self.spawn_timer = 0
        self.selected_tower = 1 # 1: Laser, 2: Plasma, 3: EMP
        
        self.running = True

    def run(self):
        """Main game loop managing events, updates, and rendering."""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()

    def handle_events(self):
        """Handle user input events based on the current game state."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            if self.state == "START_MENU":
                # Start game on any key press or mouse click
                if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    self.reset_game()
                    self.state = "PLAYING"
            
            elif self.state == "PLAYING":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        self.selected_tower = 1
                    elif event.key == pygame.K_2:
                        self.selected_tower = 2
                    elif event.key == pygame.K_3:
                        self.selected_tower = 3
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1: # Left click
                        self.place_tower(event.pos)
            
            elif self.state == "GAME_OVER":
                # Press 'R' to restart
                if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    self.reset_game()
                    self.state = "PLAYING"

    def update(self):
        """Update game logic based on the current state."""
        if self.state == "PLAYING":
            if self.health <= 0:
                self.state = "GAME_OVER"
                return
                
            self.spawn_timer -= 1
            if self.spawn_timer <= 0:
                if self.enemies_to_spawn:
                    enemy_class = self.enemies_to_spawn.pop(0)
                    enemy_class(self.level.get_path_pixel_points(), [self.enemies])
                    self.spawn_timer = FPS # 1 second between spawns
                elif len(self.enemies) == 0:
                    self.start_next_wave()
                    
            self.enemies.update()
            self.towers.update(self.enemies, self.create_projectile)
            self.projectiles.update()
            
            for enemy in self.enemies.sprites():
                if getattr(enemy, 'reached_end', False):
                    self.health -= enemy.damage_to_player
                    enemy.kill()
                elif enemy.health <= 0:
                    self.credits += enemy.reward
                    enemy.kill()

    def draw(self):
        """Render to the screen based on the current game state."""
        if self.state == "START_MENU":
            self.screen.fill(MENU_BLUE)
            self.draw_text("VAPORWAVE DEFENSE", 74, NEON_PINK, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3)
            self.draw_text("LATE STAGE CAPITALISM", 48, CYAN, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30)
            self.draw_text("Press Any Key To Interface", 36, NEON_GREEN, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
            
        elif self.state == "PLAYING":
            self.screen.fill(DARK_PURPLE)
            self.draw_grid()
            self.level.draw(self.screen)
            
            self.enemies.draw(self.screen)
            for enemy in self.enemies.sprites():
                enemy.draw_health_bar(self.screen)
                
            self.towers.draw(self.screen)
            self.projectiles.draw(self.screen)
            
            # --- Draw Placement Hologram ---
            mx, my = pygame.mouse.get_pos()
            if 50 < my < SCREEN_HEIGHT - 50:
                grid_x = (mx // TILE_SIZE) * TILE_SIZE + TILE_SIZE // 2
                grid_y = (my // TILE_SIZE) * TILE_SIZE + TILE_SIZE // 2
                
                tower_classes = {1: NeonLaser, 2: PlasmaBlaster, 3: CyberEMP}
                selected_class = tower_classes[self.selected_tower]
                dummy = selected_class((grid_x, grid_y), [])
                
                ghost_img = dummy.image.copy()
                ghost_img.set_alpha(150)
                self.screen.blit(ghost_img, dummy.rect)
                
                # Draw range indicator (red if invalid placement or poor funds)
                snap_rect = pygame.Rect(grid_x - TILE_SIZE//2, grid_y - TILE_SIZE//2, TILE_SIZE, TILE_SIZE)
                invalid = False
                for path_rect in self.level.path_rects:
                    if snap_rect.colliderect(path_rect): invalid = True
                for tower in self.towers.sprites():
                    if tower.rect.collidepoint((grid_x, grid_y)): invalid = True
                if self.credits < dummy.cost: invalid = True
                
                pygame.draw.circle(self.screen, RED if invalid else CYAN, (grid_x, grid_y), dummy.range, 1)
            # -------------------------------
            
            self.ui.draw(self.screen, self.health, self.credits, self.wave, self.selected_tower)
            
        elif self.state == "GAME_OVER":
            self.screen.fill(GRID_COLOR)
            self.draw_text("BANKRUPT", 80, RED, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3)
            self.draw_text("THE CORPORATION COLLECTS", 40, CYAN, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            self.draw_text("Press 'R' to Refinance (Restart)", 32, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60)

        pygame.display.flip()

    def draw_text(self, text, size, color, x, y):
        """Helper to draw text on the screen."""
        try:
            # Try to use a default clear font or generic 'Arial'
            font = pygame.font.Font(None, size)
        except:
            font = pygame.font.SysFont('Arial', size)
            
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(x, y))
        self.screen.blit(text_surface, text_rect)

    def draw_grid(self):
        """Draw aesthetic retro vaporwave grid."""
        for x in range(0, SCREEN_WIDTH, TILE_SIZE):
            pygame.draw.line(self.screen, GRID_COLOR, (x, 0), (x, SCREEN_HEIGHT))
        for y in range(0, SCREEN_HEIGHT, TILE_SIZE):
            pygame.draw.line(self.screen, GRID_COLOR, (0, y), (SCREEN_WIDTH, y))

    def reset_game(self):
        """Reset the game state to start a new run."""
        self.health = STARTING_HEALTH
        self.credits = STARTING_CREDITS
        self.wave = 0
        self.enemies.empty()
        self.towers.empty()
        self.projectiles.empty()
        self.enemies_to_spawn = []
        self.spawn_timer = 0
        self.start_next_wave()
        
    def start_next_wave(self):
        self.wave += 1
        # Simple progression logic: more drones, then riot police, then CEOs
        num_drones = 5 + self.wave * 2
        num_riot = self.wave // 2
        num_ceo = 1 if self.wave % 5 == 0 else 0
        
        self.enemies_to_spawn = [CorporateDrone] * num_drones + [RiotPolice] * num_riot + [CEO] * num_ceo
        self.spawn_timer = 60
        
    def place_tower(self, pos):
        # Prevent placing on UI
        if pos[1] < 50 or pos[1] > SCREEN_HEIGHT - 50:
            return
            
        # Snap to grid center
        grid_x = (pos[0] // TILE_SIZE) * TILE_SIZE + TILE_SIZE // 2
        grid_y = (pos[1] // TILE_SIZE) * TILE_SIZE + TILE_SIZE // 2
        snap_pos = (grid_x, grid_y)
        
        # Check path collision
        snap_rect = pygame.Rect(grid_x - TILE_SIZE//2, grid_y - TILE_SIZE//2, TILE_SIZE, TILE_SIZE)
        for path_rect in self.level.path_rects:
            if snap_rect.colliderect(path_rect):
                return # Cannot place on path
                
        # Check existing towers
        for tower in self.towers.sprites():
            if tower.rect.collidepoint(snap_pos):
                return
                
        tower_classes = {1: NeonLaser, 2: PlasmaBlaster, 3: CyberEMP}
        selected_class = tower_classes[self.selected_tower]
        
        # We need a dummy instance just to check cost, or map consts
        dummy = selected_class((0,0), [])
        cost = dummy.cost
        
        if self.credits >= cost:
            self.credits -= cost
            selected_class(snap_pos, [self.towers])
            
    def create_projectile(self, pos, target, damage):
        Projectile(pos, target, damage, [self.projectiles])
