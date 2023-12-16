FNAME = "in16.txt"
    
grid = [list(line) for line in open(FNAME).read().splitlines()]
height = len(grid)
width = len(grid[0])

UP = (0, -1)
DOWN = (0, 1)
RIGHT = (1, 0)
LEFT = (-1, 0)

# checks if coordinates are in bounds
# optionally taking an ignored direction so that an entire (x, y, dir) state can be fed in
def inbounds(x, y, direction=None):
    return 0 <= x < width and 0 <= y < height

# given a starting state (e.g. (0, 0, RIGHT)), count how many cells will be energized
def count_energized(start_state):
    
    beamq = [start_state]
    explored_states = set() # (x, y, dir)
    explored_coords = set() # (x, y) sort of lazy to use double space, but easier
    
    while beamq:
        x, y, dir = beamq.pop(0)
        explored_states.add((x, y, dir))
        explored_coords.add((x, y))
        current_cell = grid[y][x]
        
        # figure out what direction(s) we head from here
        dirB = None # always one next state, maybe two
        if current_cell == "-" and dir in [UP, DOWN]:
            dirA = LEFT
            dirB = RIGHT
        elif current_cell == "|" and dir in [LEFT, RIGHT]:
            dirA = UP
            dirB = DOWN
        elif current_cell == "/":
            if dir == LEFT:
                dirA = DOWN
            elif dir == RIGHT:
                dirA = UP
            elif dir == DOWN:
                dirA = LEFT
            elif dir == UP:
                dirA = RIGHT
        elif current_cell == "\\":
            if dir == LEFT:
                dirA = UP
            elif dir == RIGHT:
                dirA = DOWN
            elif dir == DOWN:
                dirA = RIGHT
            elif dir == UP:
                dirA = LEFT
        else:
            dirA = dir
        
        # turn the direction(s) into next state
        dxA, dyA = dirA
        next_pointA = (x + dxA, y + dyA, dirA)
        next_pointB = None
        if dirB:
            dxB, dyB = dirB
            next_pointB = (x + dxB, y + dyB, dirB)
            
        # add next state(s) to q
        if inbounds(*next_pointA) and next_pointA not in explored_states:
                beamq.append(next_pointA)
        if next_pointB and inbounds(*next_pointB) and next_pointB not in explored_states:
                beamq.append(next_pointB)
    
    return len(explored_coords)
            
print("Part 1:", count_energized((0, 0, RIGHT)))

start_states = []
for x in range(width):
    start_states.append((x, 0, DOWN))
    start_states.append((x, height - 1, UP))
for y in range(height):
    start_states.append((0, y, RIGHT))
    start_states.append((width - 1, y, LEFT))
print("Part 2:", max(count_energized(state) for state in start_states)) # not 8315
