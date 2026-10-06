import pytest
import tkinter as tk
import os
from snake import SnakeGame, GRID_WIDTH, GRID_HEIGHT

from unittest.mock import MagicMock

@pytest.fixture
def game():
    # Mocking tkinter components to avoid TclError in headless environments
    root = MagicMock(spec=tk.Tk)
    
    # Mock Canvas and Label to return MagicMocks
    with MagicMock() as mock_canvas, MagicMock() as mock_label:
        tk.Canvas = MagicMock(return_value=mock_canvas)
        tk.Label = MagicMock(return_value=mock_label)
        
        # Mocking run to prevent the infinite loop and UI blocking during tests
        original_run = SnakeGame.run
        SnakeGame.run = lambda self: None 
        
        # Also mock save_stats to avoid side effects on results.txt during most tests
        original_save = SnakeGame.save_stats
        SnakeGame.save_stats = lambda self: None

        app = SnakeGame(root)
        
        yield app
        
        SnakeGame.run = original_run
        SnakeGame.save_stats = original_save

def test_initial_state(game):
    assert game.score == 0
    assert len(game.snake) == 1
    assert game.snake[0] == (GRID_WIDTH // 2, GRID_HEIGHT // 2)
    assert game.running is True

def test_movement(game):
    initial_head = game.snake[0]
    game.direction = (1, 0) # Moving Right
    game.move()
    assert game.snake[0] == (initial_head[0] + 1, initial_head[1])

def test_eat_food(game):
    # Manually place food in front of the snake
    head_x, head_y = game.snake[0]
    game.food = (head_x + 1, head_y)
    game.direction = (1, 0)
    game.next_direction = (1, 0)
    
    game.move()
    
    assert game.score == 10
    assert len(game.snake) == 2
    assert game.food != (head_x + 1, head_y) # New food placed

def test_wall_collision(game):
    # Teleport snake to edge
    game.snake = [(0, 0)]
    game.direction = (-1, 0) # Move left out of bounds
    game.next_direction = (-1, 0)
    game.move()
    
    assert game.running is False

def test_self_collision(game):
    # Snake with length 5
    game.snake = [(5, 5), (6, 5), (6, 6), (5, 6), (4, 6)]
    game.direction = (0, 1) # Down, should hit (5, 6) which is in snake
    game.next_direction = (0, 1)
    
    game.move()
    
    assert game.running is False

def test_direction_invalidation(game):
    game.direction = (1, 0) # Right
    # Try to move Left (180 degree turn)
    event = tk.Event()
    event.keysym = "Left"
    game.on_key_press(event)
    
    assert game.next_direction == (1, 0) # Should NOT change

def test_valid_direction_change(game):
    game.direction = (1, 0) # Right
    # Try to move Up
    event = tk.Event()
    event.keysym = "Up"
    game.on_key_press(event)
    
    assert game.next_direction == (0, -1)

def test_high_score_update(game):
    game.best_score = 50
    game.score = 60
    
    # Trigger game over to check if best_score updates
    game.game_over()
    
    assert game.best_score == 60
    assert game.last_score == 60

def test_reset_game(game):
    game.score = 100
    game.running = False
    
    # Simulate pressing 'R'
    event = tk.Event()
    event.keysym = "r"
    game.on_key_press(event)
    
    assert game.running is True
    assert game.score == 0
    assert len(game.snake) == 1
