import pdb

FNAME = "in10.txt"

# load the map from file
map = [list(line) for line in open(FNAME).read().splitlines()]
for i in range(len(map)):
    map[i] = list(map[i])
height = len(map)
width = len(map[0])
    
# find the starting coordinates
for y in range(len(map)):
    if 'S' in map[y]:
        break
x = map[y].index('S')
map_start = (x, y)

# figure out what pipe type is hidden by the S
# precondition: only two adjacent tiles conceivably connect to S
x, y = map_start
top, bottom, left, right = False, False, False, False
if x > 0 and map[y][x - 1] in "-LF":
    left = True
if x < width - 1 and map[y][x + 1] in "-7J":
    right = True
if y > 0 and map[y - 1][x] in "|7F":
    top = True
if y < height - 1 and map[y + 1][x] in "|JL":
    bottom = True
assert [top, bottom, left, right].count(True) == 2
if top and bottom:
    map[y][x] = "|"
elif left and right:
    map[y][x] = "-"
elif top and right:
    map[y][x] = "L"
elif top and left:
    map[y][x] = "J"
elif bottom and left:
    map[y][x] = "7"
elif bottom and right:
    map[y][x] = "F"
else:
    raise ValueError("WTF")

# keep track of how far nodes are from the start moving in each direction
# I think we could actually just keep track of the total distance and solve Part 1,
# but this turns out to be a useful data structure for simply checking loop membership in Part 2
distances = {map_start: 0}

# don't want to have to keep writing these vectors
UP = (0, -1)
DOWN = (0, 1)
LEFT = (1, 0)
RIGHT = (-1, 0)

# keep track of the direction from which each node was entered
vectors = {}

# figure out the two nodes to visit (adjacent to start), 
# and the direction from which they were entered
if map[y][x] == "|":
    nextA = (x, y - 1)
    vectors[nextA] = UP
    nextB = (x, y + 1)
    vectors[nextB] = DOWN
elif map[y][x] == "-":
    nextA = (x - 1, y)
    vectors[nextA] = LEFT
    nextB = (x + 1, y)
    vectors[nextB] = RIGHT
elif map[y][x] == "7":
    nextA = (x - 1, y)
    vectors[nextA] = LEFT
    nextB = (x, y + 1)
    vectors[nextB] = DOWN
elif map[y][x] == "F":
    nextA = (x + 1, y)
    vectors[nextA] = RIGHT
    nextB = (x, y + 1)
    vectors[nextB] = DOWN
elif map[y][x] == "L":
    nextA = (x + 1, y)
    vectors[nextA] = RIGHT
    nextB = (x, y - 1)
    vectors[nextB] = UP
elif map[y][x] == "J":
    nextA = (x - 1, y)
    vectors[nextA] = LEFT
    nextB = (x, y - 1)
    vectors[nextB] = UP    
distances[nextA] = 1
distances[nextB] = 1
current_distance = 1 # could just used above data structure instead

# expand one node in the loop search
# basically take that node, advance it in the appropriate direction
# and log the direction from which that node was entered
# could also log distance here
def advance(coord):
    x, y = coord
    dist = distances[coord]
    direction = vectors[coord]
    if map[y][x] == '|':
        if direction == UP:
            nextcoord = (x, y - 1)
            vectors[nextcoord] = UP
        else:
            assert direction == DOWN
            nextcoord = (x, y + 1)
            vectors[nextcoord] = DOWN
    elif map[y][x] == '-':
        if direction == LEFT:
            nextcoord = (x - 1, y)
            vectors[nextcoord] = LEFT
        else:
            assert direction == RIGHT
            nextcoord = (x + 1, y)
            vectors[nextcoord] = RIGHT
    elif map[y][x] == '7':
        if direction == RIGHT:
            nextcoord = (x, y + 1)
            vectors[nextcoord] = DOWN
        else:
            assert direction == UP
            nextcoord = (x - 1, y)
            vectors[nextcoord] = LEFT
    elif map[y][x] == 'F':
        if direction == LEFT:
            nextcoord = (x, y + 1)
            vectors[nextcoord] = DOWN
        else:
            assert direction == UP
            nextcoord = (x + 1, y)
            vectors[nextcoord] = RIGHT
    elif map[y][x] == 'L':
        if direction == LEFT:
            nextcoord = (x, y - 1)
            vectors[nextcoord] = UP
        else:
            assert direction == DOWN
            nextcoord = (x + 1, y)
            vectors[nextcoord] = RIGHT
    elif map[y][x] == 'J':
        if direction == RIGHT:
            nextcoord = (x, y - 1)
            vectors[nextcoord] = UP
        else:
            assert direction == DOWN
            nextcoord = (x - 1, y)
            vectors[nextcoord] = LEFT
    else:
        raise ValueError("How did we get here?!?")
    distances[nextcoord] = dist + 1
    return nextcoord
           
# assuming from examples that there is a single node that is most distant from the start
# aka even loop length
# would need to do more complex check above to see if nextcoord had already been visited
# in the case of odd loop length
while nextA != nextB:
    nextA = advance(nextA)
    nextB = advance(nextB)
    
print("Part 1:", distances[nextA]) # s/b 6909

# find the highest row in the map that contains a loop element
# and find the leftmost element in that row
# this is guaranteed to be an F
# if we traverse the loop proceeding out the F to the right,
# the outside will always be to the left of the loop,
# and the inside will always be to the right of the loop
toprowy = min(y for x, y in distances)
leftx = min(x for x, y in distances if y == toprowy)

start_loc = (leftx, toprowy)

# keep track of where we are and which way we're pointing as we traverse the loop
current_loc = start_loc
current_dir = RIGHT

# a list of all interior points
# we'll first find those directly along the loop boundary
# then find those deeper in the interior
interior_points = set()

# advanced one increment forward in the loop, logging any new interior points we find
def advance():
    global current_dir
    global current_loc
    
    # advance to the next position
    x, y = current_loc
    if current_dir == RIGHT:
        x += 1
    elif current_dir == LEFT:
        x -= 1
    elif current_dir == UP:
        y -= 1
    elif current_dir == DOWN:
        y += 1
    else:
        raise ValueError("WTF", current_dir)
    current_loc = (x, y)
    assert (x, y) in distances # make sure we didn't get off the loop somehow

    # determine the new orientation, adding interior points that we've found
    # up to two potential interior points will be found, I'll call them target1 and target2
    target1, target2 = None, None
    if map[y][x] == "|":
        if current_dir == UP:
            target1 = (x + 1, y)
        else:
            assert current_dir == DOWN
            target1 = (x - 1, y)
    elif map[y][x] == "-":
        if current_dir == RIGHT:
            target1 = (x, y + 1)
        else:
            assert current_dir == LEFT
            target1 = (x, y - 1)
    elif map[y][x] == "F":
        if current_dir == UP:
            current_dir = RIGHT
        elif current_dir == LEFT:
            current_dir = DOWN
            target1 = (x, y - 1)
            target2 = (x - 1, y)
        else:
            raise ValueError("WTF")
    elif map[y][x] == "L":
        if current_dir == DOWN:
            current_dir = RIGHT
            target1 = (x, y + 1)
            target2 = (x - 1, y)
        elif current_dir == LEFT:
            current_dir = UP
        else:
            raise ValueError("WTF")
    elif map[y][x] == "J":
        if current_dir == DOWN:
            current_dir = LEFT
        elif current_dir == RIGHT:
            current_dir = UP
            target1 = (x, y - 1)
            target2 = (x + 1, y)
        else:
            raise ValueError("WTF")
    elif map[y][x] == "7":
        if current_dir == UP:
            current_dir = LEFT
            target1 = (x, y - 1)
            target2 = (x + 1, y)
        elif current_dir == RIGHT:
            current_dir = DOWN
        else:
            raise ValueError("WTF")
    else:
        raise ValueError("WTF", current_loc, current_dir, map[y][x])
    # this might add duplicates, 
    # but rather than check if it's already an interior point every time,
    # I'll just eliminate duplicates after we finish traversing
    # alternatively, this could just be a set that we add to
    if target1 and target1 not in distances:
        interior_points.add(target1)
    if target2 and target2 not in distances:
        interior_points.add(target2)
        
# move off the start location then traverse the whole loop
advance() 
while start_loc != current_loc:
    advance()
    
# get the neighbors of a point
# no need to check boundaries since this will only be applied within the loop
def neighbors(coord):
    x, y = coord
    return ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1))
    
# expand the interorior points to includes those not on the boundary of the loop
# needs to be a list here since you can't expand sets during iteration
interior_points_list = list(interior_points)
for point in interior_points_list:
    for neighbor_point in neighbors(point):
        if neighbor_point not in distances and neighbor_point not in interior_points:
            interior_points_list.append(neighbor_point)
            interior_points.add(neighbor_point)
print("Part 2:", len(interior_points)) # s/b 461

# convert location into symbol for rendering based on if it's on loop or interior
def render_point(x, y):
    if (x, y) in distances:
        return "*"
    if (x, y) in interior_points:
        return "X"
    return map[y][x]

# visualize the loop and interior for debug purposes
def render(val = ""):
    fname = "render_map" + val + ".txt"
    ofp = open(fname, "w")
    for y in range(len(map)):
        for x in range(len(map[0])):
            ofp.write(render_point(x, y))
        ofp.write("\n")
    print("Render saved to", fname)
    ofp.close()
#render()

#pdb.set_trace()
