UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
DIRECTIONS4 = (UP, DOWN, LEFT, RIGHT)
DIRECTIONS8 = DIRECTIONS4 + ((1, 1), (-1, -1), (1, -1), (-1, 1))

DIGITS = '0123456789'

# take a collection of points and render them as '#' with non rendered-points as '.'
# useful for e.g. aoc2021/p13 when a set of points represents a visual message
def render(points):
    minx = min(x for x, y in points)
    maxx = max(x for x, y in points)
    miny = min(y for x, y in points)
    maxy = max(y for x, y in points)
    for y in range(miny, maxy + 1):
        for x in range(minx, maxx + 1):
            if (x, y) in points:
                print('#', end='')
            else:
                print('.', end='')
        print()

# return a reversed copy of a string
def reverse_string(s):
    return ''.join(reversed(s))

# transpose a 2D list
def transpose(grid):
    return [list(i) for i in zip(*grid)]

# returns a 2D list representation of input split into single characters
# input block should be lines separated by newlines
def read_grid(block):
    return [list(line) for line in block.splitlines()]

# rotate a 2D list
# TODO: optimize
def rotate_clockwise(block):
    block = transpose(block)
    return [list(reversed(line)) for line in block]

# handy functions to remember:
# rfind to find the rightmost (index) of a substring
# math.prod to find the product of an iterable
