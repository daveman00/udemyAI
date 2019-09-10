# maze generator using hunt and kill algorithm
from __future__ import print_function
import numpy
import ast


# Maze class - handles generation of square maze using Hunt'n'Kill algorithm
class Maze:
    # dictionary with direction vectors
    directions = {'N': (-2, 0),
                  'W': (0, -2),
                  'S': (2, 0),
                  'E': (0, 2),
                  }

    # initialize Maze class - size should be an odd number
    def __init__(self, size=9):
        if size % 2 == 0:
            self.size = size + 1
        else:
            self.size = size
        # initialize grid
        self.grid = self.generate_grid()
        # copy grid to visit_map to track the changes in maze generation
        self.visit_map = numpy.copy(self.grid)
        self.reinforcement_grid = []
        # generate maze
        #self.hunt_n_kill()
        #self.reinforcement_grid = self.translate_grid()

    # fill maze grid with empty cells in the following manner:
    #   1 1 1 1 1
    #   1 0 1 0 1
    #   1 1 1 1 1
    #   1 0 1 0 1
    #   1 1 1 1 1
    def generate_grid(self):
        grid = numpy.ones(shape=(self.size, self.size))
        for i in range(1, grid.shape[0], 2):
            for j in range(1, grid.shape[1], 2):
                grid[i, j] = 0
        return numpy.array(grid)

    # return coordinates of random unvisited cell
    def get_starting_position(self):
        zeroes = numpy.argwhere(self.grid == 0)
        return tuple(zeroes[numpy.random.choice(len(zeroes))])

    # check available directions from given point
    # state - can be 0 or 1 - determines if looking for unvisited(0) or visited cells(1) in the neighbourhood
    def check_directions(self, point, state=0):
        available_directions = []
        for dir in self.directions:
            neighbour = numpy.add(point,self.directions[dir])
            try:
                if any(n < 0 for n in neighbour):
                    raise IndexError('Negative index: ', neighbour)
                if self.visit_map[tuple(neighbour)] != state:
                    raise ValueError('Neighbour value: ', self.visit_map[tuple(neighbour)], ' - expected the opposite.')
            except (IndexError,ValueError) as e:
                print(e)
                continue
            else:
                available_directions.append(neighbour)
        return available_directions

    # carve passage from unvisited to previously visited cell
    def carve_passage(self, start, end):
        passage = tuple((numpy.add(start, end)/2).astype(int))
        self.visit_map[end] = 1
        self.grid[passage] = 0

    # function carves continuous passages from start point until dead end is reached
    def kill(self, start):
        start = tuple(start)
        self.visit_map[start] = 1
        while True:
            directions = self.check_directions(start)
            if not directions: break
            direction = tuple(directions[numpy.random.choice(len(directions))])
            self.carve_passage(start, direction)
            start = direction

    # function searches for unvisited cell with visited neighbours to continue carving of the maze in new direction
    # returns unvisited cell coordinates as new starting point
    def hunt(self):
        unvisited = numpy.argwhere(self.visit_map == 0)
        for point in unvisited:
            available_directions = self.check_directions(point,1)
            if available_directions:
                direction = tuple(available_directions[numpy.random.choice(len(available_directions))])
                self.carve_passage(point, direction)
                return point
        return None

    # main loop - kill function carves continuous passages,
    # when reaching dead end hunt function is triggered allowing further carving
    # until all cells have been visited
    def hunt_n_kill(self):
        start = self.get_starting_position()
        while True:
            self.kill(start)
            start = self.hunt()
            if start is None: break
        self.reinforcement_grid = self.translate_grid()

    def get_reinforcement_grid(self):
        return self.reinforcement_grid

    def translate_grid(self):
        grid = numpy.where(self.grid > 0, '#', ' ')
        path = numpy.where(grid == ' ')
        indexS = numpy.random.choice(path[0].size, replace=False)
        index1 = numpy.random.choice(path[0].size, replace=False)
        grid = grid.tolist()
        grid[path[0][indexS]][path[1][indexS]] = 'S'
        grid[path[0][index1]][path[1][index1]] = 1
        return grid

    def read_maze(self, filename='maze.txt'):
        with open(filename) as file:
            data = file.read()
            self.reinforcement_grid = ast.literal_eval(data)

    def save_maze(self, filename='maze.txt'):
        file = open(filename, 'w+')
        file.write(str(self.get_reinforcement_grid()))



# debugging purposes
def color_print_map(arr):
#    BLUE = '\x1b[1;34m'
#    RED = '\x1b[1;31m'
#    ENDC = '\x1b[0m'
    print('[', end='')
    for i in range(len(arr)):
        print('[', end='')
        for j in range(len(arr)):
            if arr[i, j] == 0:
#                print(RED + str(int(arr[i,j])) + ENDC, end=' ')
                print('\' \'', end=',')
            else:
#                print(str(int(arr[i,j])), end=' ')
                print('\'#\'', end=',')

        print('],')
    print(']')


if __name__ == '__main__':
    maze = Maze(11)
#    maze.hunt_n_kill()
    print('==============')
#    color_print_map(maze.grid)
    print(maze.grid)
    result = numpy.where(maze.grid > 0, '#', ' ')
    path = numpy.where(result == ' ')
    print('==============')
    print(result)
    print(path)
    print(path[0].size)
    print(path[1].size)
    index = numpy.random.choice(path[0].size, replace=False)
    print(index)
    i = path[0][index], path[1][index]
    print(i)
    result[i] = 'S'
    print(result)
    index = numpy.random.choice(path[0].size, replace=False)
    print(index)
    i = path[0][index], path[1][index]
    print(i)
    result[i] = +1
    print(result)
