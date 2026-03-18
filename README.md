# Vaporwave/Cyberpunk Tower Defense: Late Stage Capitalism

A Pygame-based tower defense game featuring a vaporwave/cyberpunk aesthetic. Defend against Late-Stage Capitalist Fascists (Corporate Drones, Riot Police, and the CEO!) using Futuristic Weapons.

## Features
- **Vaporwave Aesthetics**: Neon pinks, cyan highlights, deep purple grid lines, and retro styling.
- **Dynamic Wave System**: Progressively harder quarters (waves) of corporate enemies.
- **Capitalist Economy**: Earn financial assets by defunding enemies to build more towers.
- **Tower Arsenals**: 
  1. Neon Laser ($50)
  2. Plasma Blaster ($150)
  3. Cyber EMP ($200)

## Installation & Running

1. **Install Dependencies**:
   It is recommended to use Pygame Community Edition (`pygame-ce`) for better modern performance.
   ```bash
   pip install -r requirements.txt
   ```
   *(Or simply run `pip install pygame-ce`)*

2. **Run the Game**:
   ```bash
   python main.py
   ```

## Controls
- **Any Key** / **Mouse Click**: Interface with the Start Menu.
- **1, 2, 3**: Select tower prototype to deploy (Laser, Plasma, EMP).
- **Left Mouse Click**: Deploy the selected tower onto the grid (cannot be on the path or overlapping other towers).
- **R**: Refinance (Restart the game) after going Bankrupt (Game Over).

## File Structure
- `main.py`: Entry point
- `settings.py`: Global constants, UI dimensions, and Vaporwave color palettes.
- `game.py`: The `Game` state manager handling the event loop, drawing, wave progression, and economy.
- `level.py`: The visual grid and enemy corporate pathway structure.
- `ui.py`: Manages the retro-HUD, currency, integrity tracker, and controls interface.
- `entity.py`: Base sprite component for all game objects.
- `enemy.py`: Includes `CorporateDrone`, `RiotPolice`, and `CEO` fascists.
- `tower.py`: Defines the `NeonLaser`, `PlasmaBlaster`, and `CyberEMP` structures.
- `projectile.py`: Combat execution component.

## License
MIT License
