from aoc_utils import UP, DOWN, LEFT, RIGHT

FNAME = "in18.txt"
    
dir_lut = {'R':RIGHT, 'D':DOWN, 'L':LEFT, 'U':UP}
def parse_line(line):
    dir, count, color = line.split()
    count = int(count)
    return dir_lut[dir], count, color

data = [parse_line(line) for line in open(FNAME).read().splitlines()]

boundary_points = []
currentx, currenty = 0, 0

# Part 1: inefficient and probably won't work for Part 2,
# but just list out every single boundary point,
# then grab an interior point and keep adding neighbors until
# all interior points have been listed

# loop around the boundary following the directions
for dir, count, _ in data:
    dx, dy = dir
    for _ in range(count):
        currentx += dx
        currenty += dy
        boundary_points.append((currentx, currenty))

# make sure we closed the loop
assert boundary_points[-1] == (0, 0)

# make sure we didn't cross or end w/ duplicates
# (this seems to be a property of the input)
boundary_points_set = set(boundary_points)
assert len(boundary_points) == len(boundary_points_set)

print(f"{len(boundary_points)} boundary points found")

# redirect output to file to see a map
#render(boundary_points)

# find the interior points
# precondition: the interior consists of one contiguous region
# and never folds on itself (at least at the top left corner)

# find the leftmost point in the top edge(s)
topy = min(y for x, y in boundary_points)   
leftx = min(x for x, y in boundary_points if y == topy)

# checks that fold-in property
assert (leftx + 1, topy + 1) not in boundary_points

# get the neighbors of a point
def neighbors(coord):
    x, y = coord
    return ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1))

interior_points = set()
interior_points.add((leftx + 1, topy + 1))

expandq = [(leftx + 1, topy + 1)]
while expandq:
    cur = expandq.pop(0)
    for n in neighbors(cur):
        if n not in boundary_points_set and n not in interior_points:
            interior_points.add(n)
            expandq.append(n)

print(f"{len(interior_points)} interior points found")

print("Part 1:", len(boundary_points) + len(interior_points))

# Part 2 has much larger numbers, so we can't reasonable individually count points
# instead, we'll find the are of the polygon using mathematical formulae
# then adjust for the fact that we're dealing w/ discrete cells and not 0D points

# read in the new directions into direction/value pairs
dir_lut = {'0':RIGHT, '1':DOWN, '2':LEFT, '3':UP}
def parse_instruction(color):
    val = eval('0x' + color[2:7])
    dir = dir_lut[color[7]]
    return dir, val

instructions = [parse_instruction(color) for _, _, color in data]

# calculate the sequence of vertices of the polygon, 
# starting (not listed) and ending with (0, 0) as reference frame
x, y = (0, 0)
vertices = []
perimeter = 0

for dir, val in instructions:
    dx, dy = dir
    dx *= val
    dy *= val
    x = x + dx
    y = y + dy
    perimeter += abs(dx + dy)
    vertices.append((x, y))   
    
# safety check that we read the input correctly and we ended where we started
assert vertices[-1] == (0, 0) 

# credit for area of a polygon from a list of vertices:
# https://stackoverflow.com/questions/451426/how-do-i-calculate-the-area-of-a-2d-polygon
def area(p):
    return 0.5 * abs(sum(x0*y1 - x1*y0 for ((x0, y0), (x1, y1)) in segments(p)))

def segments(p):
    return zip(p, p[1:] + [p[0]])
    
inner_area = area(vertices)

# adjust for the fact that boundary is actually 1x1 cells
# so basically we end up with an extra 1/2 unit wide band around the outside
# plus one more from a cumulative corner
edge_area = perimeter * 0.5 + 1

print("Part 2:", inner_area + edge_area)
