# maze generator using hunt and kill algorithm

import numpy


class Maze:
#    size = 0
#    grid = []
#    visit_map = []
    directions = {'N': (-2,0),
                  'W': (0,-2),
                  'S':  (2,0),
                  'E':  (0,2),
                  }

    def __init__(self, size=9):
        if size % 2 == 0:
            self.size = size + 1
        else:
            self.size = size
        self.grid = self.generate_grid()
        self.visit_map = numpy.copy(self.grid)
        #self.visit_map = self.grid.copy()

    def generate_grid(self):
        grid = numpy.ones(shape=(self.size, self.size))
        for i in range(1,grid.shape[0], 2):
            for j in range(1,grid.shape[1], 2):
                grid[i,j] = 0
        return numpy.array(grid)

    def get_starting_position(self):
        zeroes = numpy.argwhere(self.grid == 0)
        return tuple(zeroes[numpy.random.choice(len(zeroes))])

    # visited - can be 0 or 1 - determines if looking for unvisited(0) or visited cells(1)
    def check_directions(self, point, state=0):
        available_directions = []
        for dir in self.directions:
            neighbour = numpy.add(point,self.directions[dir])
#            print('NEIGHBOUR: ', neighbour)
            #print("VISIT MAP IN CHECK_DIRECTIONS:")
            #color_print_map(self.visit_map)
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
#            self.carve_passage(point, neighbour)
#        available_directions = []
#        for direction in self.directions:
#            new_dir = tuple(numpy.add(self.directions[direction], list(point)))
#            try:
#                if self.visit_map[new_dir] == 0:
#                    available_directions.append(new_dir)
#                else:
#                    raise ValueError('Visited cell', new_dir)
#            except (IndexError,ValueError) as e:
#                print(e)
#                continue
#        return available_directions

    def carve_passage(self, start, end):
#        print("DIR: ", end)
        passage = tuple((numpy.add(start, end)/2).astype(int))
#        print("PASS: ", passage)
        self.visit_map[end] = 1
        #self.visit_map[start] = 1
        self.grid[passage] = 0

    def kill(self, start):
#        start = self.get_starting_position()i
#        print("START TYPE: ", type(start))
        start = tuple(start)
#        print("START: ", start)
#        tmp = numpy.copy(self.visit_map)
#        print("VISIT MAP BEFORE:")
#        color_print_map(self.visit_map)
        self.visit_map[start] = 1
#        print("VISIT MAP DIFF:")
#        color_print_map(numpy.subtract(self.visit_map,tmp))
#        print("VISIT MAP AFTER:")
#        color_print_map(self.visit_map)
#        self.grid[start] = 2
        while True:
            directions = self.check_directions(start)
#            print("DIRECTIONS: ", directions)
            if not directions: break
            direction = tuple(directions[numpy.random.choice(len(directions))])
            self.carve_passage(start, direction)
#            print("DIR: ", direction)
#            passage = tuple((numpy.add(start, direction)/2).astype(int))
#            print("PASS: ", passage)
#            self.visit_map[direction] = 1
#            self.grid[passage] = 0
            start = direction
#            print('NEW START: ', start)

    def hunt(self):
        unvisited = numpy.argwhere(self.visit_map == 0)
#        print('UNVISITED: ', unvisited)
        for point in unvisited:
#            print('POINT: ', point)
            available_directions = self.check_directions(point,1)
#            print('AVAILABLE DIRECTIONS: ', available_directions)
            if available_directions:
                direction = tuple(available_directions[numpy.random.choice(len(available_directions))])
#                print('CARVING DIRECTION: ', direction)
                self.carve_passage(point, direction)
#                print('NEW START POINT: ', point)
                #print('NEW START POINT: ', direction)
                return point
                #return direction
        return None

    def hunt_n_kill(self):
        start = self.get_starting_position()
        while True:
#            print('start: ', start)
#            print('KILLING')
            self.kill(start)
#            print('GRID:')
#            color_print_map(self.grid)
#            print('VISIT MAP:')
#            color_print_map(self.visit_map)
#            input("continue...1")
#            print("==========")
#            print("HUNTING")
            start = self.hunt()
#            print('GRID:')
#            color_print_map(self.grid)
#            print('VISIT MAP:')
#            color_print_map(self.visit_map)
#            print("==========")
#            input("continue...2")
            if start is None: break


# debugging purposes
def color_print_map(arr, color='OKBLUE'):
    BLUE = '\x1b[1;34m'
    RED = '\x1b[1;31m'
    ENDC = '\x1b[0m'
    for i in range(len(arr)):
        for j in range(len(arr)):
            if arr[i,j] == 0:
                print(RED + str(int(arr[i,j])) + ENDC, end=' ')
            else:
                print(str(int(arr[i,j])), end=' ')

        print()

maze = Maze(11)

#color_print_map(maze.grid)
print()
maze.hunt_n_kill()
#maze.kill(maze.get_starting_position())
print('==============')
color_print_map(maze.grid)
print('==============')
#color_print_map(maze.visit_map)

#print(maze.hunt())