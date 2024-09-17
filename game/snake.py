import random
import curses
import time

class SnakeGame:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        curses.curs_set(0)
        self.sh, self.sw = stdscr.getmaxyx()
        self.w = curses.newwin(self.sh, self.sw, 0, 0)
        self.w.keypad(1)
        self.speed = 150  # Game speed in milliseconds
        self.w.timeout(self.speed)
        self.current_direction = curses.KEY_RIGHT
        self.previous_direction = curses.KEY_RIGHT
        self.game_over = False
        self.main_menu()

    def main_menu(self):
        self.w.clear()
        self.w.addstr(self.sh//2 - 2, self.sw//2 - 5, "SNAKE GAME", curses.A_BOLD)
        self.w.addstr(self.sh//2, self.sw//2 - 5, "1. Start Game")
        self.w.addstr(self.sh//2 + 1, self.sw//2 - 5, "2. Exit")
        self.w.refresh()
        
        while True:
            key = self.w.getch()
            if key == ord('1'):
                self.start_game()
                break
            elif key == ord('2'):
                curses.endwin()
                quit()

    def start_game(self):
        self.snake = [[self.sh//2, self.sw//2]]
        self.food = [self.sh//4, self.sw//4]
        self.score = 0
        self.game_over = False
        self.setup_game()

    def setup_game(self):
        try:
            self.w.clear()
            self.w.addch(self.food[0], self.food[1], curses.ACS_PI)
            self.main_loop()
        except Exception as e:
            curses.endwin()
            print(f"Error: {e}")
            quit()

    def main_loop(self):
        while not self.game_over:
            next_key = self.w.getch()
            if next_key in [curses.KEY_DOWN, curses.KEY_UP, curses.KEY_LEFT, curses.KEY_RIGHT]:
                self.update_direction(next_key)
            self.move_snake()
            self.check_collisions()
            self.update_display()
            self.handle_game_over()

        self.end_game()

    def update_direction(self, key):
        # Prevent snake from reversing direction
        if (key == curses.KEY_DOWN and self.current_direction != curses.KEY_UP) or \
           (key == curses.KEY_UP and self.current_direction != curses.KEY_DOWN) or \
           (key == curses.KEY_LEFT and self.current_direction != curses.KEY_RIGHT) or \
           (key == curses.KEY_RIGHT and self.current_direction != curses.KEY_LEFT):
            self.previous_direction = self.current_direction
            self.current_direction = key

    def move_snake(self):
        head = self.snake[0]
        new_head = [head[0], head[1]]

        if self.current_direction == curses.KEY_DOWN:
            new_head[0] += 1
        if self.current_direction == curses.KEY_UP:
            new_head[0] -= 1
        if self.current_direction == curses.KEY_LEFT:
            new_head[1] -= 1
        if self.current_direction == curses.KEY_RIGHT:
            new_head[1] += 1

        self.snake.insert(0, new_head)

        if self.snake[0] == self.food:
            self.score += 1
            self.spawn_food()
        else:
            tail = self.snake.pop()
            self.w.addch(int(tail[0]), int(tail[1]), ' ')

    def check_collisions(self):
        head = self.snake[0]

        if (head[0] in [0, self.sh] or
            head[1] in [0, self.sw] or
            head in self.snake[1:]):
            self.game_over = True

    def update_display(self):
        self.w.addch(int(self.snake[0][0]), int(self.snake[0][1]), curses.ACS_CKBOARD)
        self.w.addstr(0, 2, f'Score: {self.score} ', curses.color_pair(1))

    def spawn_food(self):
        while True:
            new_food = [
                random.randint(1, self.sh - 1),
                random.randint(1, self.sw - 1)
            ]
            if new_food not in self.snake:
                self.food = new_food
                self.w.addch(self.food[0], self.food[1], curses.ACS_PI)
                break

    def handle_game_over(self):
        if self.game_over:
            self.w.addstr(self.sh//2, self.sw//2 - 8, "Game Over!", curses.color_pair(2))
            self.w.addstr(self.sh//2 + 1, self.sw//2 - 8, f"Final Score: {self.score}", curses.color_pair(2))
            self.w.addstr(self.sh//2 + 3, self.sw//2 - 8, "Press 'r' to Restart or 'q' to Quit", curses.color_pair(2))
            self.w.refresh()

    def end_game(self):
        while True:
            key = self.w.getch()
            if key == ord('r'):
                self.start_game()
                break
            elif key == ord('q'):
                curses.endwin()
                quit()

if __name__ == "__main__":
    curses.wrapper(SnakeGame)

