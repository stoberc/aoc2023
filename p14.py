from aoc_utils import transpose, rotate_clockwise

FNAME = "in14.txt"
PART2_TARGET = 1000000000

grid = [list(line) for line in open(FNAME).read().splitlines()]
height = len(grid)
width = len(grid[0])
    
def shift_row_north(x):
    targetY = 0
    for y in range(height):
        if grid[y][x] == "O":
            temp = grid[targetY][x]
            grid[targetY][x] = "O"
            grid[y][x] = temp
            targetY += 1
        elif grid[y][x] == "#":
            targetY = y + 1

def shift_board_north():
    for x in range(width):
        shift_row_north(x)
        
# view map for debugging purposes
def render():
    for line in grid:
        print(''.join(line))
    print()
    
# shift north, then west, then south, east - a complete cycle
def full_cycle():
    global grid
    for _ in range(4):
        shift_board_north()
        grid = rotate_clockwise(grid)

# calculate the score for the current grid
def get_score():
    score = 0
    for x in range(width):
        for y in range(height):
            if grid[y][x] == "O":
                score += height - y
    return score
    
shift_board_north()
print("Part 1:", get_score())

# finish the rest of the first cycle
grid = rotate_clockwise(grid)
for _ in range(3):
    shift_board_north()
    grid = rotate_clockwise(grid)
        
# keep track of scores after each cycle for enough cycles that we can extrapolate based on periodic behavior
# this was implemented a bit manually
# observed that scores stabilize into period ~25 in < 100 cycles, so went to 500 for good measure
print("Generating cycle data...")
scores = [0, get_score()]
for cycle_count in range(2, 501):
    full_cycle()
    scores.append(get_score())

# now find the period starting from 200, again, somewhat caprciously informed by what I saw in the data
# basically we iteratively try periods 2, 3, 4, ... until we find one that models the behavior after 200
print("Searching for period...")
period = 2
while True:
    next_sample_start = 200 + period
    base_sample = scores[200:200+period]
    if any(scores[i:i+period] != base_sample for i in range(next_sample_start, len(scores) - period, period)):
        period += 1
        continue
    break
print("Period acquired:", period)

# find some index in the available data that is in the same place in the cycle as the extrapolation target
print(f"Extrapolating to {PART2_TARGET}...")
period_count = (PART2_TARGET - 500) // period + 1
result = scores[PART2_TARGET - period * period_count]
print("Part 2:", result)
