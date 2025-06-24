import sys

import random
import tkinter as tk
from tkinter import messagebox

from matrix import SquareMatrix


class Game2048:

    def __init__(self, field_size: int = 4):
        self.field_size = field_size
        self.cells = SquareMatrix(4)
        for _ in range(self.field_size // 2):
            self.add_random_2()

    def index_free_cells(self) -> list[tuple[int, int]]:
        return self.cells.search(0)

    def add_random_2(self):
        free_cells = self.index_free_cells()
        row, col = random.choice(free_cells)
        self.cells[row][col] = 2

    def shake(self, cells: SquareMatrix):
        """Moves the cells to the left and merges them if there's enough cells"""
        def merge(row: list[int]):
            j = 0
            while True:
                if j >= len(row) - 1:
                    break
                if row[j] == row[j + 1]:
                    row[j] *= 2
                    row.pop(j + 1)
                j += 1

        for i in range(self.field_size):
            cells[i] = [cell for cell in cells[i] if cell]
            if len(cells[i]) >= 2:
                merge(cells[i])
            cells[i] += [0] * (self.field_size - len(cells[i]))

    def are_moves_left(self):
        if self.index_free_cells():
            return True
        else:
            for direction in (0, 1, 2, 3):
                cells_clone = self.cells.clone()
                self.shake_towards(cells_clone, direction)
                if not(cells_clone == self.cells):
                    return True
        return False

    def shake_towards(self, cells: SquareMatrix, direction: int):
        """Shakes towards one of 4 directions:\n
        0 - left\n
        1 - up\n
        2 - right\n
        3 - down"""
        cells.rotate(turns=direction)
        self.shake(cells)
        cells.unrotate()

    def make_turn(self, direction: int) -> bool:
        """Makes a turn and responds whether the game is over"""
        self.shake_towards(self.cells, direction)
        if self.index_free_cells():
            self.add_random_2()
        return True if not self.are_moves_left() else False


class Game2048UI:

    CELL_SIZE = 100
    COLORS = {
        2: '#eee4da',
        4: '#eee4da',
        8: '#f2b179',
        16: '#f59563',
        32: '#f67c60',
        64: '#f65e3b',
        128: '#edcf73',
        256: '#edcc62',
        512: '#edc850',
        1024: '#edc53f',
        2048: '#edc22d'
    }
    KEYCODES = {    # (left, down, right, up)
        'win32': (37, 40, 39, 38),
        'linux': (113, 111, 114, 116)
    }

    def __init__(self, game: Game2048):
        self.game = game
        self.root = tk.Tk()
        window_size = self.game.field_size * self.CELL_SIZE
        self.canvas = tk.Canvas(self.root, width=window_size, height=window_size, bg='#776e65')
        self.canvas.pack()

    def key_pressed(self, event):
        keycode = event.keycode
        directions = dict(zip(self.KEYCODES[sys.platform], (0, 1, 2, 3)))   # bind keycodes to turns based on os
        endgame_status = self.game.make_turn(directions[keycode])
        self.draw()
        if endgame_status:
            messagebox.showwarning('', 'Game is over!')

    def draw_grid(self):
        for i in range(1, self.CELL_SIZE + 1):
            x1, y1 = 0, i * self.CELL_SIZE
            x2, y2 = self.CELL_SIZE * self.game.field_size, i * self.CELL_SIZE
            self.canvas.create_line(x1, y1, x2, y2)
            self.canvas.create_line(y1, x1, y2, x2)

    def draw_cells(self):
        for i in range(self.game.field_size):
            for j in range(self.game.field_size):
                if cell := self.game.cells[i][j]:
                    color = self.COLORS[cell]
                    x, y = j * self.CELL_SIZE + self.CELL_SIZE / 2, i * self.CELL_SIZE + self.CELL_SIZE / 2
                    self.canvas.create_text(x, y, text=str(cell), font=30, fill=color)

    def draw(self):
        self.canvas.delete('all')
        self.draw_grid()
        self.draw_cells()

    def load(self):
        self.draw()
        self.root.bind('<Key>', self.key_pressed)
        self.root.mainloop()


game2048 = Game2048()
ui = Game2048UI(game2048)
ui.load()
