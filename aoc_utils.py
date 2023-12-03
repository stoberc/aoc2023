DIRECTIONS4 = ((1, 0), (0, 1), (-1, 0), (0, -1))
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
    
# handy functions to remember:
# rfind to find the rightmost (index) of a substring
# math.prod to find the product of an iterable
