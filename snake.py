import tkinter as tk
import random
import os

CELL_SIZE = 20
GRID_WIDTH = 30
GRID_HEIGHT = 20
WIDTH = CELL_SIZE * GRID_WIDTH
HEIGHT = CELL_SIZE * GRID_HEIGHT
SPEED = 150  # milliseconds between moves

BG_COLOR = "#1a1a2e"
SNAKE_COLOR = "#4ecca3"
SNAKE_HEAD_COLOR = "#00ff88"
FOOD_COLOR = "#e94560"
TEXT_COLOR = "#ffffff"


class SnakeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Snake Game")
        self.root.resizable(False, False)

        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg=BG_COLOR, highlightthickness=0)
        self.canvas.pack()

        self.score_label = tk.Label(root, text="Score: 0", font=("Arial", 14, "bold"),
                                    bg="#0f0f1a", fg=TEXT_COLOR)
        self.score_label.pack(fill=tk.X)

        self.root.configure(bg="#0f0f1a")
        for key in ("<Up>", "<Down>", "<Left>", "<Right>",
                    "<KeyPress-w>", "<KeyPress-W>",
                    "<KeyPress-a>", "<KeyPress-A>",
                    "<KeyPress-s>", "<KeyPress-S>",
                    "<KeyPress-d>", "<KeyPress-D>",
                    "<KeyPress-r>", "<KeyPress-R>"):
            self.root.bind(key, self.on_key_press)

        self.last_score, self.best_score = self.load_stats()
        self.reset_game()

    def load_stats(self):
        last_score, best_score = 0, 0
        if os.path.exists("results.txt"):
            try:
                with open("results.txt", "r") as f:
                    for line in f:
                        key, _, value = line.partition(":")
                        key, value = key.strip(), value.strip()
                        if key == "Last Score":
                            last_score = int(value)
                        elif key == "Best Score":
                            best_score = int(value)
            except (ValueError, IOError):
                pass
        return last_score, best_score

    def save_stats(self):
        with open("results.txt", "w") as f:
            f.write(f"Last Score: {self.score}\n")
            f.write(f"Best Score: {self.best_score}\n")

    def reset_game(self):
        self.canvas.focus_set()
        self.snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = (1, 0)
        self.next_direction = (1, 0)
        self.score = 0
        self.running = True
        self.place_food()
        self.update_score()
        self.run()

    def place_food(self):
        while True:
            pos = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
            if pos not in self.snake:
                self.food = pos
                break

    def on_key_press(self, event):
        key = event.keysym
        if key in ("Up", "w", "W") and self.direction != (0, 1):
            self.next_direction = (0, -1)
        elif key in ("Down", "s", "S") and self.direction != (0, -1):
            self.next_direction = (0, 1)
        elif key in ("Left", "a", "A") and self.direction != (1, 0):
            self.next_direction = (-1, 0)
        elif key in ("Right", "d", "D") and self.direction != (-1, 0):
            self.next_direction = (1, 0)
        elif key == "r" or key == "R":
            if not self.running:
                self.reset_game()
        return "break"

    def move(self):
        self.direction = self.next_direction
        head_x, head_y = self.snake[0]
        dx, dy = self.direction
        new_head = (head_x + dx, head_y + dy)

        # Check wall collision
        if not (0 <= new_head[0] < GRID_WIDTH and 0 <= new_head[1] < GRID_HEIGHT):
            self.game_over()
            return

        # Check self collision
        if new_head in self.snake:
            self.game_over()
            return

        self.snake.insert(0, new_head)

        if new_head == self.food:
            self.score += 10
            self.update_score()
            self.place_food()
        else:
            self.snake.pop()

    def update_score(self):
        self.score_label.config(
            text=f"Score: {self.score}   |   Last: {self.last_score}   |   Best: {self.best_score}"
        )

    def draw(self):
        self.canvas.delete("all")

        # Draw grid lines (subtle)
        for x in range(0, WIDTH, CELL_SIZE):
            self.canvas.create_line(x, 0, x, HEIGHT, fill="#1e1e3a", width=1)
        for y in range(0, HEIGHT, CELL_SIZE):
            self.canvas.create_line(0, y, WIDTH, y, fill="#1e1e3a", width=1)

        # Draw food
        fx, fy = self.food
        self.canvas.create_oval(
            fx * CELL_SIZE + 3, fy * CELL_SIZE + 3,
            fx * CELL_SIZE + CELL_SIZE - 3, fy * CELL_SIZE + CELL_SIZE - 3,
            fill=FOOD_COLOR, outline=""
        )

        # Draw snake
        for i, (x, y) in enumerate(self.snake):
            color = SNAKE_HEAD_COLOR if i == 0 else SNAKE_COLOR
            self.canvas.create_rectangle(
                x * CELL_SIZE + 1, y * CELL_SIZE + 1,
                x * CELL_SIZE + CELL_SIZE - 1, y * CELL_SIZE + CELL_SIZE - 1,
                fill=color, outline=""
            )

    def game_over(self):
        self.running = False
        if self.score > self.best_score:
            self.best_score = self.score
        self.last_score = self.score
        self.save_stats()
        self.update_score()
        self.canvas.create_text(
            WIDTH // 2, HEIGHT // 2 - 20,
            text="GAME OVER", font=("Arial", 32, "bold"), fill=FOOD_COLOR
        )
        self.canvas.create_text(
            WIDTH // 2, HEIGHT // 2 + 20,
            text=f"Score: {self.score}", font=("Arial", 18), fill=TEXT_COLOR
        )
        self.canvas.create_text(
            WIDTH // 2, HEIGHT // 2 + 55,
            text="Press R to restart", font=("Arial", 13), fill="#aaaaaa"
        )

    def run(self):
        if self.running:
            self.move()
            self.draw()
            self.root.after(SPEED, self.run)


def main():
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()


if __name__ == "__main__":
    main()
