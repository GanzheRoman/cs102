import pygame
import random

from pygame.locals import *
from typing import List, Tuple
from pprint import pprint as pp

Cell = Tuple[int, int]
Cells = List[int]
Grid = List[Cells]


class GameOfLife:

    def __init__(self, width: int=640, height: int=480, cell_size: int=20, speed: int=1) -> None:
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.screen_size = width, height
        self.screen = pygame.display.set_mode(self.screen_size)
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size
        self.speed = speed

    def draw_lines(self) -> None:
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                    (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                    (0, y), (self.width, y))


    def run(self) -> None:
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption('Game of Life')
        self.screen.fill(pygame.Color('white'))

        self.create_grid(True)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
            self.draw_lines()

            self.draw_grid()
            self.get_next_generation()

            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()


    def create_grid(self, randomize: bool=False) -> Grid:
        self.grid = [[0] * self.cell_width for _ in range(self.cell_height)]

        if randomize == False:
            return self.grid
        else:
            row = 0
            for i in self.grid:
                col = 0
                for _ in i:
                    self.grid[row][col] = random.randint(0, 1)
                    col += 1
                row += 1
            return self.grid


    def draw_grid(self) -> None:
        y = 0
        grid = self.grid

        for i in grid:
            x = 0
            for v in i:
                color = 'white' if v == 0 else 'green'
                pygame.draw.rect(self.screen, pygame.Color(color),
                                    pygame.Rect(x, y, self.cell_size, self.cell_size))
                x += self.cell_size
            y += self.cell_size


    def get_neighbours(self, cell: Cell) -> Cells:
        grid = self.grid
        relative_neighbours = [[-1, -1], [0, -1], [1, -1], [1, 0], [1, 1], [0, 1], [-1, 1], [-1, 0]]
        list_of_neighbors = []

        for i in relative_neighbours:
            i[0] += cell[0]
            i[1] += cell[1]

        for i in relative_neighbours:
            row, col = i
            try:
                if row >= 0 and col >= 0:
                    list_of_neighbors.append(grid[row][col])
                else:
                    continue
            except IndexError:
                continue

        return list_of_neighbors


    def get_next_generation(self) -> Grid:
        grid = self.grid
        new_matrix = [[0] * self.cell_width for _ in range(self.cell_height)]
        total = {}

        y = 0
        for i in grid:
            x = 0
            for _ in i:
                neighbours = self.get_neighbours((y, x))
                score = 0
                for m in neighbours:
                    score += 1 if m == 1 else 0
                total[(y, x)] = score
                x += 1
            y += 1

        for i in total:
            row, col = i
            if total[(row, col)] == 3:
                new_matrix[row][col] = 1
            elif total[(row, col)] == 2:
                new_matrix[row][col] = 1 if grid[row][col] == 1 else 0
            else:
                new_matrix[row][col] = 0

        self.grid = new_matrix
        return self.grid