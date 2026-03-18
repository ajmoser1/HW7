import pygame
from settings import *

class UI:
    def __init__(self):
        try:
            self.font = pygame.font.Font(None, 36)
        except:
            self.font = pygame.font.SysFont('Arial', 36)

    def draw(self, surface, health, credits, wave, selected_tower_id=1):
        sw = surface.get_width()
        sh = surface.get_height()
        
        # Top HUD bar background
        pygame.draw.rect(surface, MENU_BLUE, (0, 0, sw, 50))
        pygame.draw.line(surface, CYAN, (0, 50), (sw, 50), 3)
        
        # Corporate Integrity (Health)
        health_color = NEON_GREEN if health > 40 else RED
        health_text = self.font.render(f"INTEGRITY: {health}%", True, health_color)
        surface.blit(health_text, (20, 15))
        
        # Financial Assets (Credits)
        credits_text = self.font.render(f"ASSETS: ${credits}M", True, YELLOW)
        credits_rect = credits_text.get_rect(center=(sw // 2, 25))
        surface.blit(credits_text, credits_rect)
        
        # Fiscal Quarter (Wave)
        wave_text = self.font.render(f"Q{wave} TARGET", True, NEON_BLUE)
        wave_rect = wave_text.get_rect(right=sw - 20, centery=25)
        surface.blit(wave_text, wave_rect)
        
        # Bottom HUD for tower selection
        pygame.draw.rect(surface, MENU_BLUE, (0, sh - 50, sw, 50))
        pygame.draw.line(surface, CYAN, (0, sh - 50), (sw, sh - 50), 3)
        
        c1 = NEON_PINK if selected_tower_id == 1 else WHITE
        c2 = NEON_PINK if selected_tower_id == 2 else WHITE
        c3 = NEON_PINK if selected_tower_id == 3 else WHITE
        
        laser_spr = load_sprite("laser.png", (36, 36))
        plasma_spr = load_sprite("plasma.png", (36, 36))
        emp_spr = load_sprite("emp.png", (36, 36))
        
        x_offset = 20
        
        # Tower 1
        t1_num = self.font.render("[1]: ", True, c1)
        surface.blit(t1_num, (x_offset, sh - 35))
        x_offset += t1_num.get_width()
        if laser_spr: surface.blit(laser_spr, (x_offset, sh - 43))
        else: pygame.draw.rect(surface, NEON_PINK, (x_offset, sh - 40, 30, 30))
        x_offset += 42
        t1_cost = self.font.render("$50", True, c1)
        surface.blit(t1_cost, (x_offset, sh - 35))
        x_offset += t1_cost.get_width() + 30
        
        # Tower 2
        t2_num = self.font.render("[2]: ", True, c2)
        surface.blit(t2_num, (x_offset, sh - 35))
        x_offset += t2_num.get_width()
        if plasma_spr: surface.blit(plasma_spr, (x_offset, sh - 43))
        else: pygame.draw.circle(surface, NEON_BLUE, (x_offset+15, sh - 25), 15)
        x_offset += 42
        t2_cost = self.font.render("$150", True, c2)
        surface.blit(t2_cost, (x_offset, sh - 35))
        x_offset += t2_cost.get_width() + 30
        
        # Tower 3
        t3_num = self.font.render("[3]: ", True, c3)
        surface.blit(t3_num, (x_offset, sh - 35))
        x_offset += t3_num.get_width()
        if emp_spr: surface.blit(emp_spr, (x_offset, sh - 43))
        else: pygame.draw.polygon(surface, NEON_GREEN, [(x_offset+15, sh - 40), (x_offset+30, sh - 25), (x_offset+15, sh - 10), (x_offset, sh - 25)])
        x_offset += 42
        t3_cost = self.font.render("$200", True, c3)
        surface.blit(t3_cost, (x_offset, sh - 35))
        
        # Active HUD Item
        act_text = self.font.render("ACTIVE: ", True, NEON_PINK)
        act_rect = act_text.get_rect(right=sw - 70, centery=sh - 25)
        surface.blit(act_text, act_rect)
        
        active_spr = laser_spr if selected_tower_id == 1 else plasma_spr if selected_tower_id == 2 else emp_spr
        if active_spr:
            surface.blit(active_spr, (sw - 60, sh - 43))
        else:
            pygame.draw.rect(surface, NEON_PINK, (sw - 60, sh - 40, 30, 30))
