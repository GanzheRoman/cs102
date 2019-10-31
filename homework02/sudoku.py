def read_sudoku(filename):
    """ Прочитать Судоку из указанного файла """
    digits = [c for c in open('puzzle1.txt').read() if c in '123456789.']
    grid = group(digits, 9)
    return grid


def display(grid):
    """ Вывод Судоку """
    width = 2
    line = '+'.join(['-' * (width * 3)] * 3)
    for row in range(9):
        print(''.join(grid[row][col].center(width) + ('|' if str(col) in '25' else '') for col in range(9)))
        if str(row) in '25':
            print(line)
    print()


def group(values, n):
    """
    Сгруппировать значения values в список, состоящий из списков по n элементов
    >>> group([1,2,3,4], 2)
    [[1, 2], [3, 4]]
    >>> group([1,2,3,4,5,6,7,8,9], 3)
    [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    """
    s = 0
    matrix = []
    while len(values) > s:
        l = [i for i in values[s:s + n]]
        matrix.append(l)
        s += n
    return matrix


def get_row(grid,pos):
    """ Возвращает все значения для номера строки, указанной в pos
    >>> get_row([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '2', '.']
    >>> get_row([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (1, 0))
    ['4', '.', '6']
    >>> get_row([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (2, 0))
    ['.', '8', '9']
    """
    row, col = pos
    return grid[row]


def get_col(grid,pos):
    """ Возвращает все значения для номера столбца, указанного в pos
    >>> get_col([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '4', '7']
    >>> get_col([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (0, 1))
    ['2', '.', '8']
    >>> get_col([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (0, 2))
    ['3', '6', '9']
    """
    row, col = pos
    l = []
    for i in grid:
        l.append(i[col])
    return l


def get_block(grid,pos):
    """ Возвращает все значения из квадрата, в который попадает позиция pos
    >>> grid = read_sudoku('puzzle1.txt')
    >>> get_block(grid, (0, 1))
    ['5', '3', '.', '6', '.', '.', '.', '9', '8']
    >>> get_block(grid, (4, 7))
    ['.', '.', '3', '.', '.', '1', '.', '.', '6']
    >>> get_block(grid, (8, 8))
    ['2', '8', '.', '.', '.', '5', '.', '7', '9']
    """
    row, col = pos
    block = []
    frow = 0
    lrow = 0
    fcol = 0
    lcol = 0
    if 0 <= row <= 2:
        frow = 0
        lrow = 3
    if 3 <= row <= 5:
        frow = 3
        lrow = 6
    if 6 <= row <= 8:
        frow = 6
        lrow = 9
    if 0 <= col <= 2:
        fcol = 0
        lcol = 3
    if 3 <= col <= 5:
        fcol = 3
        lcol = 6
    if 6 <= col <= 8:
        fcol = 6
        lcol = 9

    for i in grid[frow:lrow]:
        for m in i[fcol:lcol]:
            block.append(m)
    return block


def find_empty_positions(grid):
    """ Найти первую свободную позицию в пазле
    >>> find_empty_positions([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']])
    (0, 2)
    >>> find_empty_positions([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']])
    (1, 1)
    >>> find_empty_positions([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']])
    (2, 0)
    """
    row = 0
    empty_positions = []
    for i in grid:
        col = 0
        for z in i:
            if z == ".":
                empty_positions.append([row, col])
            col += 1
        row += 1
    empty = (empty_positions[0][0], empty_positions[0][1])
    return empty


def find_possible_values(grid,pos):
    """ Вернуть множество возможных значения для указанной позиции
    >>> grid = read_sudoku('puzzle1.txt')
    >>> values = find_possible_values(grid, (0,2))
    >>> values == {'1', '2', '4'}
    True
    >>> values = find_possible_values(grid, (4,7))
    >>> values == {'2', '5', '9'}
    True
    """
    all_values = get_row(grid, pos) + get_col(grid, pos) + get_block(grid, pos)
    possible_values = {str(i) for i in range(1, 10)}
    for i in all_values:
        if i != '.':
            possible_values.discard(i)
    return possible_values


def solve(grid):
    """ Решение пазла, заданного в grid """
    """ Как решать Судоку?
         1. Найти свободную позицию
         2. Найти все возможные значения, которые могут находиться на этой позиции
         3. Для каждого возможного значения:
             3.1. Поместить это значение на эту позицию
             3.2. Продолжить решать оставшуюся часть пазла
     >>> grid = read_sudoku('puzzle1.txt')
     >>> solve(grid)
    [['5', '3', '4', '6', '7', '8', '9', '1', '2'], ['6', '7', '2', '1', '9', '5', '3', '4', '8'], ['1', '9', '8', '3', '4', '2', '5', '6', '7'], ['8', '5', '9', '7', '6', '1', '4', '2', '3'], ['4', '2', '6', '8', '5', '3', '7', '9', '1'], ['7', '1', '3', '9', '2', '4', '8', '5', '6'], ['9', '6', '1', '5', '3', '7', '2', '8', '4'], ['2', '8', '7', '4', '1', '9', '6', '3', '5'], ['3', '4', '5', '2', '8', '6', '1', '7', '9']]
    """
    try:
        empty_position = find_empty_positions(grid)
    except IndexError:
        return grid

    possible_values = find_possible_values(grid, empty_position)
    for i in possible_values:
        grid[empty_position[0]][empty_position[1]] = i
        maybe = solve(grid)
        if maybe:
            return maybe

    grid[empty_position[0]][empty_position[1]] = '.'
    return None


def check_solution(solution):
    """ Если решение solution верно, то вернуть True, в противном случае False
    >>> a = [['4', '3', '4', '6', '7', '8', '9', '1', '2'], ['6', '7', '2', '1', '9', '5', '3', '4', '8'], ['1', '9', '8', '3', '4', '2', '5', '6', '7'], ['8', '5', '9', '7', '6', '1', '4', '2', '3'], ['4', '2', '6', '8', '5', '3', '7', '9', '1'], ['7', '1', '3', '9', '2', '4', '8', '5', '6'], ['9', '6', '1', '5', '3', '7', '2', '8', '4'], ['2', '8', '7', '4', '1', '9', '6', '3', '5'], ['3', '4', '5', '2', '8', '6', '1', '7', '9']]
    >>> check_solution(a)
    False
    >>> grid = read_sudoku('puzzle1.txt')
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    """
    for i in solution:
        values = [_ for _ in range(1, 10)]
        for m in i:
            try:
                values.remove(int(m))
            except ValueError:
                return False

    col = 0
    while col < 8:
        values = [_ for _ in range(1, 10)]
        cols = get_col(solution, (0, col))
        for i in cols:
            try:
                values.remove(int(i))
            except ValueError:
                return False
        col += 1

    blocks = [(0, 0), (0, 3), (0, 6), (3, 0), (3, 3), (3, 6), (6, 0), (6, 3), (6, 6)]
    for i in blocks:
        values = [_ for _ in range(1, 10)]
        block = get_block(solution, i)
        for v in block:
            try:
                values.remove(int(v))
            except ValueError:
                return False

    return True

import random 

def generate_sudoku(N):
    """ Генерация судоку заполненного на N элементов
    >>> grid = generate_sudoku(40)
    >>> sum(1 for row in grid for e in row if e == '.')
    41
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    >>> grid = generate_sudoku(1000)
    >>> sum(1 for row in grid for e in row if e == '.')
    0
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    >>> grid = generate_sudoku(0)
    >>> sum(1 for row in grid for e in row if e == '.')
    81
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    """
    table = [['1', '2', '3', '4', '5', '6', '7', '8', '9'], ['4', '5', '6', '7', '8', '9', '1', '2', '3'],
             ['7', '8', '9', '1', '2', '3', '4', '5', '6'], ['2', '3', '4', '5', '6', '7', '8', '9', '1'],
             ['5', '6', '7', '8', '9', '1', '2', '3', '4'], ['8', '9', '1', '2', '3', '4', '5', '6', '7'],
             ['3', '4', '5', '6', '7', '8', '9', '1', '2'], ['6', '7', '8', '9', '1', '2', '3', '4', '5'],
             ['9', '1', '2', '3', '4', '5', '6', '7', '8']]
    
    score = 81
    while score > N:
        row = random.randint(0, 8)
        col = random.randint(0, 8)
        if table[row][col] != '.':
            table[row][col] = '.'
            score -= 1
    return table

if __name__ == '__main__':
    for fname in ['puzzle1.txt', 'puzzle2.txt', 'puzzle3.txt']:
        grid = read_sudoku(fname)
        display(grid)
        solution = solve(grid)
        if not solution:
            print(f"Puzzle {fname} can't be solved")
        else:
            display(solution)