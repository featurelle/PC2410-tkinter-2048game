from __future__ import annotations

import numpy as np
from copy import deepcopy


class SquareMatrix:

    def __init__(self, size: int = 2):
        self.matrix = [[0] * size for _ in range(size)]
        self.rotation = 0

    def __getitem__(self, item: int) -> list[int]:
        return self.matrix[item]

    def __setitem__(self, key: int, value: list[int]):
        self.matrix[key] = value

    def __str__(self) -> str:
        return '\n'.join(' '.join(str(item) for item in row) for row in self.matrix)

    def __eq__(self, other: SquareMatrix) -> bool:
        return np.array_equal(self.matrix, other.matrix)

    def search(self, item: int) -> list[tuple[int, int]]:
        return [(index, row.index(item)) for index, row in enumerate(self.matrix) if item in row]

    def clone(self, rotation: int = 0) -> SquareMatrix:
        matrix_copy = deepcopy(self)
        if rotation:
            matrix_copy.rotate(turns=rotation)
        return matrix_copy

    def rotate(self, turns: int):
        """Returns the copy of the matrix rotated counter-clockwise\n
        Resulting rotation:\n
        turns=1 - 90 degrees\n
        turns=2 - 180 degrees\n
        turns=3 - 270 degrees"""
        self.matrix = np.rot90(self.matrix, k=turns).tolist()
        self.rotation = turns

    def unrotate(self):
        """Turns back once to the previous orientation"""
        if self.rotation:
            turns_to_undo = 4 - self.rotation
            self.rotate(turns=turns_to_undo)
            self.rotation = 0
