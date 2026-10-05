# AWS Student Builder Group - Flappy Bird

A beginner-friendly 2D Flappy Bird clone built with Python and Pygame for the AWS Student Builder Group Technical / Game Development Round 2.

## Requirements implemented

- Bird falls automatically due to gravity.
- Space/Up arrow or mouse click makes the bird flap upward.
- Pipes spawn at regular intervals and move from right to left.
- Pipes disappear after leaving the screen.
- Collision with pipes, ground, or top boundary ends the game.
- Score increases by 1 after passing each pipe pair.
- Three game states:
  - Start Screen
  - Gameplay
  - Game Over Screen
- Press Space, R, or click to restart after game over.
- No built-in physics engine, tilemap, or scene editor is used.

## Setup

Python 3.10+ is recommended.

```bash
python -m pip install pygame
```

## Run

```bash
python main.py
```

## Controls

- Space / Up Arrow: flap
- Mouse click: flap
- R: restart after game over
- Escape: quit

## Project structure

```text
aws_flappy_bird/
├── main.py
├── README.md
└── requirements.txt
```

## Main concepts used

### Gravity

Each frame the bird's vertical velocity increases:

```python
self.velocity += GRAVITY
self.y += self.velocity
```

### Flapping

When the player presses Space/Up or clicks:

```python
self.velocity = FLAP_VELOCITY
```

The negative velocity moves the bird upward.

### Collision detection

The bird and pipes are represented with rectangles. Pygame's `colliderect()` checks whether they overlap.

### Game states

The game uses:

```text
START -> PLAYING -> GAME_OVER
```

This keeps the start screen, active gameplay, and restart screen separate.
