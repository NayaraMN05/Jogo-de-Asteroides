# Asteroids Game

## Overview
This is a classic Asteroids game built with Python and Pygame. The player controls a spaceship that can rotate and move in any direction, shooting at asteroids to score points while avoiding collisions.

## Project Architecture
- **Language**: Python 3.11
- **Framework**: Pygame 2.5.2
- **Type**: Desktop GUI Game (VNC)

## File Structure
```
.
├── main.py                    # Main game file with all game logic
├── AsteroidsImages/           # Game assets folder
│   ├── asteroid100.png        # Medium asteroid sprite
│   ├── asteroid150.png        # Large asteroid sprite
│   ├── asteroid50.png         # Small asteroid sprite
│   ├── spaceRocket.png        # Player spaceship sprite
│   └── starbg.png            # Background starfield
├── requirements.txt           # Python dependencies
└── replit.md                 # Project documentation
```

## Game Features
- **Player Controls**:
  - Arrow Keys (Left/Right): Rotate the spaceship
  - Arrow Key (Up): Move forward
  - Arrow Key (Down): Move backward
  - Spacebar: Shoot projectiles
  
- **Gameplay**:
  - Asteroids spawn randomly from screen edges
  - Three sizes of asteroids (large, medium, small)
  - Shooting large asteroids breaks them into medium ones (10 points)
  - Shooting medium asteroids breaks them into small ones (20 points)
  - Shooting small asteroids destroys them (30 points)
  - Player has 3 lives
  - Press Spacebar after game over to restart

## How to Run
The game runs automatically via the configured workflow. The game displays in a VNC window (graphical desktop environment).

## Recent Changes
- **November 7, 2025**: Initial project setup
  - Installed Python 3.11 and Pygame 2.5.2
  - Configured VNC workflow for graphical display
  - Created project documentation

## Technical Details
- Screen size: 600x600 pixels
- Game runs at 60 FPS
- Player spaceship wraps around screen edges
- Asteroids spawn every 50 frames
- Collision detection between player/asteroids and bullets/asteroids
