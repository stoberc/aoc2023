import pdb
from collections import defaultdict
from aoc_utils import UP, DOWN, LEFT, RIGHT
import time

FNAME = "in17.txt"
    
grid = [[int(i) for i in line] for line in open(FNAME).read().splitlines()]
height = len(grid)
width = len(grid[0])
goalx, goaly = width - 1, height - 1

distances = defaultdict(lambda: float('inf'))

# state vectors consists of x, y, 
# direction from which cell was entered, and 
# time to live (number of moves left in that particular direction)
# we start at the top left, arbitrarily facing right, with 3 moves left
start_state = (0, 0, RIGHT, 3)
distances[start_state] = 0

# check whether a point is inbounds
# ignorable arguments included so we can feed in a whole state vector if need be
def inbounds(x, y, dir=None, ttl=None):
    return 0 <= x < width and 0 <= y < height

# find the distance from start to goal
def get_distance(goalx, goaly):
    # state vectors consists of x, y, 
    # direction from which cell was entered, and 
    # time to live (number of moves left in that particular direction)
    # we start at the top left, arbitrarily facing right, with 3 moves left
    exploreq = [start_state]

    # essentially running BFS, which leaves lots of room for optimization
    # for example, should really expand least-distant nodes next
    # and shouldn't bother exploring a state that's clearly worse than
    # a previously explored state, e.g. same location, worse distance, worse ttl
    # runtime is bad (~2 minutes), but workable, so I'm going to leave it alone
    while exploreq:
        state = exploreq.pop(0)
        d = distances[state]
        x, y, dir, ttl = state
        
        # figure out up to three directions we can go from here
        # we could turn 90 degrees
        if dir in [UP, DOWN]:
            dirs = [LEFT, RIGHT]
        else:
            dirs = [UP, DOWN]
            
        # we could also go straight if possible
        if ttl > 0:
            dirs.append(dir)
            
        for next_dir in dirs:
            
            dx, dy = next_dir
            nextx, nexty = x + dx, y + dy
            if inbounds(nextx, nexty):
                nextd = d + grid[nexty][nextx]
                
                if next_dir == dir:
                    next_ttl = ttl - 1
                else:
                    next_ttl = 2
                
                next_state = (nextx, nexty, next_dir, next_ttl)
                
                if nextd < distances[next_state]:
                    distances[next_state] = nextd
                    exploreq.append(next_state)
                
    solutions = []
    for state in distances:
        x, y, dir, ttl = state
        if (x, y) == (goalx, goaly):
            solutions.append(distances[state])
    return min(solutions)
    
# get a list of all state vector / distance pairs for a particular coordinate
# mainly for debug    
def get_all_distance(goalx, goaly):
    solutions = []
    for state in distances:
        x, y, dir, ttl = state
        if (x, y) == (goalx, goaly):
            solutions.append((state, distances[state]))
    return solutions    

t0 = time.time()            
print("Part 1:", get_distance(goalx, goaly)) # s/b 797
print("Solved in", time.time() - t0, "seconds")


# Part 2: need two start states since turning right away is otherwise impossible
distances = defaultdict(lambda: float('inf'))
start_state1 = (0, 0, RIGHT, 10)
start_state2 = (0, 0, DOWN, 10)
distances[start_state1] = 0
distances[start_state2] = 0

# find the distance from start to goal
def get_distance(goalx, goaly):
    # state vectors consists of x, y, 
    # direction from which cell was entered, and 
    # time to live (number of moves left in that particular direction)
    # we start at the top left, arbitrarily facing right, with 3 moves left
    exploreq = [start_state1, start_state2]

    # BFS again with similar optimizations avaiable
    # 3.5 minute runtime is workable, though
    while exploreq:
        state = exploreq.pop(0)
        d = distances[state]
        x, y, dir, ttl = state
        
        # figure out up to three directions we can go from here
        # we could turn 90 degrees
        dirs = []
        if ttl > 0:
            dirs.append(dir)
        if ttl <= 6:            
            if dir in [UP, DOWN]:
                dirs.append(LEFT)
                dirs.append(RIGHT)
            else:
                dirs.append(UP)
                dirs.append(DOWN)
                
        for next_dir in dirs:
            
            dx, dy = next_dir
            nextx, nexty = x + dx, y + dy
            if inbounds(nextx, nexty):
                nextd = d + grid[nexty][nextx]
                
                if next_dir == dir:
                    next_ttl = ttl - 1
                else:
                    next_ttl = 9
                    
                next_state = (nextx, nexty, next_dir, next_ttl)
                
                if nextd < distances[next_state]:
                    distances[next_state] = nextd
                    exploreq.append(next_state)
                
    solutions = []
    for state in distances:
        x, y, dir, ttl = state
        if (x, y) == (goalx, goaly) and ttl <= 6:
            solutions.append(distances[state])
    return min(solutions)

t0 = time.time()
print("Part 2:", get_distance(goalx, goaly))
print("Solved in", time.time() - t0, "seconds")
