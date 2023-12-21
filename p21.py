# warning: lots of hard-coded values and assumptions of properties based on observed input

from aoc_utils import DIRECTIONS4

FNAME = "in21.txt"

# read in grid from file    
grid = [list(line) for line in open(FNAME).read().splitlines()]
height = len(grid)
width = len(grid[0])

# identify starting location (turns out to be exact center, important for Part 2)
startx = None
for y in range(height):
    for x in range(width):
        if grid[y][x] == 'S':
            startx, starty = x, y
            break
    if startx:
        break
print("Start:", (startx, starty))
    
# return a list of all neighbors of a point which are in bounds and vacant
def neighbors(point):
    x, y = point
    outlist = []
    for dx, dy in DIRECTIONS4:
        nx, ny = x + dx, y + dy
        if 0 <= nx < width and 0 <= ny < height and grid[ny][nx] != "#":
            outlist.append((nx, ny))
    return outlist
    
# at first, a single point is reachable
reachable = set()
reachable.add((startx, starty))

# one iteration
def step():
    global reachable
    next_reachable = set()
    for node in reachable:
        for n in neighbors(node):
            next_reachable.add(n)
    reachable = next_reachable
 
# fix 64 steps for Part 1 
for _ in range(64):
    step()
    
print("Part 1:", len(reachable)) #  s/b 3637

# debug/exploration on a single iteration
# this revealed that there's a stable alternating pattern in the long run
def render():
    for y in range(height):
        for x in range(width):
            if (x, y) in reachable:
                print('O', end="")
            else:
                print(grid[y][x], end="")
        print()
    print()
         
# since we start at the center with a clear, straight-line path to all corners and edges,
# there are nine different entry points for a particular tile:
# center, n, s, e, w, ne, nw, se, sw
# based on entry point, values should stabilize into alternating sequence after...
# ~130 for center
# ~200 for nsew
# ~275 corners
# based on square tile, 131x131, with center start and clear path to all edge points, no huge cul de sacs
# so all tiles will follow one of those nine patterns, delayed by some lag to be initially reached
# basically for large N, we'll have a whole bunch of saturated tiles in the core after 26501365 steps
# then some frontier of partially iterated sequences
# so lets's find the sequence for each of the nine types,
# then find the quantities and lags for each tile, then sum

# this is so input-specific on the properties and values, that I'll just start hard-coding some
assert (startx, starty) == (65, 65)
assert width == height == 131
direction_names = ["center", "north", "south", "east", "west", "northeast", "northwest", "southeast", "southwest"]
start_locations = {} 
start_locations["center"] = (startx, starty)
start_locations["north"] = (startx, 0)
start_locations["south"] =  (startx, height - 1)
start_locations["east"] = (width - 1, starty)
start_locations["west"] = (0, starty)
start_locations["northeast"] = (width - 1, 0)
start_locations["northwest"] = (0, 0)
start_locations["southeast"] = (width - 1, height - 1)
start_locations["southwest"] = (0, height - 1)

# run 300 steps and log the count which should start at 1,
# proceed through a transient phase,
# then stabilize into an alternating pattern 
def generate_profile(start_point):
    out_sequence = [1]
    reachable = set()
    reachable.add(start_point)
    for _ in range(300):
        next_reachable = set()
        for node in reachable:
            for n in neighbors(node):
                next_reachable.add(n)
        reachable = next_reachable
        out_sequence.append(len(reachable))
    return out_sequence

print("Generating profiles for all nine entry points...")
count_profiles = {}    
for direction_name in direction_names:
    count_profiles[direction_name] = generate_profile(start_locations[direction_name])
    print(len(count_profiles))

# lookup the value of a profile at a particular index
# returning 0 for indices < 0 and extrapolated values for indices > 300
# and shifting the whole sequence by delay steps
def profile_get(profile, index, delay):
    assert len(profile) == 301 # safety check for debugging
    adjusted_index = index - delay
    if adjusted_index < 0:
        return 0
    elif adjusted_index >= len(profile):
        excess_index = adjusted_index - len(profile) + 1
        if excess_index % 2 == 0:
            return profile[-1]
        return profile[-2]
    else:
        return profile[adjusted_index]
    
STEPCOUNT = 26501365 # constant number of steps from part 2

print("Assessing center...")
total_reachable = profile_get(count_profiles['center'], STEPCOUNT, 0)

# inefficient, but I'm a bit too tired for all the math
# basically the first of these get hit after 66 steps,
# and another gets introduced every successive 131 steps
# still runs way faster than profile generation, in any case
print("Assessing nsew...")
for delay in range(66, STEPCOUNT, 131):
    total_reachable += profile_get(count_profiles['north'], STEPCOUNT, delay)
    total_reachable += profile_get(count_profiles['south'], STEPCOUNT, delay)
    total_reachable += profile_get(count_profiles['east'], STEPCOUNT, delay)
    total_reachable += profile_get(count_profiles['west'], STEPCOUNT, delay)

# similar idea, except the first corner is hit at step 132,
# and there are a growing number of such tiles as time passes
print("Assessing ne/nw/se/sw...")
rowcount = 1
for delay in range(132, STEPCOUNT, 131):
    total_reachable += profile_get(count_profiles['northeast'], STEPCOUNT, delay) * rowcount
    total_reachable += profile_get(count_profiles['northwest'], STEPCOUNT, delay) * rowcount
    total_reachable += profile_get(count_profiles['southeast'], STEPCOUNT, delay) * rowcount
    total_reachable += profile_get(count_profiles['southwest'], STEPCOUNT, delay) * rowcount
    rowcount += 1

print("Part 2:", total_reachable) # s/b  601113643448699
