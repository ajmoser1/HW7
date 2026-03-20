# Vaporwave/Cyberpunk Tower Defense: Late Stage Capitalism

A Pygame-based tower defense game featuring a vaporwave/cyberpunk aesthetic. Defend against Late-Stage Capitalist Fascists (Corporate Drones, Riot Police, and the CEO!) using Futuristic Weapons.

## Features
- **Vaporwave Aesthetics**: Neon pinks, cyan highlights, deep purple grid lines, retro styling, and transparent pixel-art sprites.
- **Dynamic Wave System**: Aggressively scaling waves with interleaved enemy types — drones, riot police, and CEOs hit you simultaneously.
- **Capitalist Economy**: Earn financial assets by defunding enemies to build and upgrade towers.
- **Tower Arsenals**:
  1. **Neon Laser** ($50) — Fast-firing, balanced DPS. The workhorse.
  2. **Plasma Blaster** ($150) — Slow but devastating single-target damage.
  3. **Cyber EMP** ($125) — Long range, rapid fire, and **slows enemies by 60%** for 3 seconds on hit.
- **Tower Upgrades**: Right-click a placed tower to upgrade it (up to level 3). Each level increases damage, range, and fire rate.
- **Score & High Scores**: Earn points for every enemy killed. High scores persist between sessions.
- **Procedural Synthwave Audio**: All sound effects and background music are generated at runtime — no external audio files needed. Includes placement chimes, shoot zaps, death bursts, wave arpeggios, a doom chord for game over, and a looping synthwave BGM.
- **Pause**: Press P or ESC to pause mid-wave.

## Installation & Running

1. **Install Dependencies**:
   It is recommended to use Pygame Community Edition (`pygame-ce`) for better modern performance.
   ```bash
   pip install -r requirements.txt
   pip install numpy
   ```
   *(numpy is required for the procedural audio system)*

2. **Run the Game**:
   ```bash
   python main.py
   ```

## Controls
| Key | Action |
|-----|--------|
| **Any Key / Click** | Start from the menu |
| **1, 2, 3** | Select tower type (Laser, Plasma, EMP) |
| **Left Click** | Place the selected tower on the grid |
| **Right Click** | Upgrade an existing tower (up to level 3) |
| **P / ESC** | Pause / Unpause |
| **M** | Toggle audio on/off |
| **R** | Restart after Game Over |

## File Structure
- `main.py`: Entry point.
- `settings.py`: Global constants, UI dimensions, Vaporwave color palettes, and sprite loading.
- `game.py`: The `Game` state manager handling the event loop, drawing, wave progression, upgrades, and economy.
- `level.py`: The visual grid and enemy corporate pathway structure.
- `ui.py`: Manages the retro-HUD — integrity, assets, score, wave, and tower selection display.
- `entity.py`: Base sprite component for all game objects.
- `enemy.py`: Includes `CorporateDrone`, `RiotPolice`, and `CEO` fascists, with slow debuff support.
- `tower.py`: Defines the `NeonLaser`, `PlasmaBlaster`, and `CyberEMP` structures, including the upgrade system.
- `projectile.py`: Combat execution component with per-tower-type visuals and EMP slow-on-hit.
- `audio.py`: Procedural synthwave audio manager — generates all sounds and BGM at runtime using numpy.
- `highscore.py`: JSON-based high score persistence.
- `tools/fix_sprites.py`: Utility script used to remove black backgrounds from sprite PNGs.

## License
MIT License
