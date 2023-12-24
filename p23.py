# this problem is NP-complete?!?
import pdb
from collections import deque
from aoc_utils import *

FNAME = "in23.txt"
    
grid = [list(line) for line in open(FNAME).read().splitlines()]
height = len(grid)
width = len(grid[0])

start_location = startx, starty = (grid[0].index('.'), 0)
goal_location = goalx, goaly = (grid[-1].index('.'), height - 1)

# find all locations where there's a fork in the path
# since inefficient to consider boring intermediate locations
fork_locations = []
for y in range(height):
    for x in range(width):
        if grid[y][x] != "#":
            clear_neighbor_count = 0
            for dx, dy in DIRECTIONS4:
                nx, ny = x + dx, y + dy
                if 0 <= nx < width and 0 <= ny < height and grid[ny][nx] != "#":
                    clear_neighbor_count += 1
            if clear_neighbor_count >= 3:
                fork_locations.append((x, y))
                
interesting_locations = fork_locations + [start_location, goal_location]


# figure out which interesting locations are adjacent to this one, and how far way they are
# returns a list of (x, y, d) triplets    
def get_neighbors_and_distances(x, y):
    
    results = []
    for dir in DIRECTIONS4:
        dx, dy = dir
        nx, ny = x + dx, y + dy
        if 0 <= nx < width and 0 <= ny < height and grid[ny][nx] != "#":
            results.append(push(nx, ny, dir, 1))
            
    return results
    
# starting at this location and entering in the given direction,
# figure out what interesting location we eventually get to,
# and how far away it is
# precondition: no dead ends
opposites = {UP:DOWN, DOWN:UP, RIGHT:LEFT, LEFT:RIGHT}
def push(x, y, enter_dir, bonus_dist = 0):
    
    if (x, y) in interesting_locations:
        return x, y, 0
        
    assert grid[y][x] != "#"
    
    for dir in DIRECTIONS4:
        if dir == opposites[enter_dir]:
            continue
        dx, dy = dir
        nx, ny = x + dx, y + dy
        if 0 <= nx < width and 0 <= ny < height and grid[ny][nx] != "#":
            destx, desty, d = push(nx, ny, dir)
            return destx, desty, 1 + d + bonus_dist
    
    raise ValueError("I thought there were no dead ends...")
    
# create adjacency list graph
neighbors = {}
for point in interesting_locations:
    neighbors[point] = []
    for result in get_neighbors_and_distances(*point):
        neighbors[point].append(result)

# every time we find a path to the end, we'll log its distance
distances_to_end = []

nodecount = 0 # for measuring progress/speed

class Node:
    
    # storing a set of ancestors for every node has the potential to have a huge impact on memory
    # I'm hoping the speedup from O(1) lookup of ancestors (vs. O(n) recursive parental lookup)
    # will make it worth it, but maybe not
    def __init__(self, x, y, distance_from_start, parent):

        self.parent = parent
        
        # for measuring progress/speed
        global nodecount
        if nodecount % 100000 == 0:
            print("Node", nodecount,"created w/", len(self.ancestors()), "ancestors")
        nodecount += 1

        self.x = x
        self.y = y
        self.dist = distance_from_start
        self.symbol = grid[y][x]
        
        
        if (x, y) == (goalx, goaly):
            distances_to_end.append(self.dist)
    
    # expand this node in the graph to include its children
    # instead we push them onto a queue
    # we don't evaluate the children recursively, as we'd quickly hit recursion limits
    def expand(self):
    
        self.children = []
        for x, y, d in neighbors[(self.x, self.y)]:
            if (x, y) not in self.ancestors():
                self.children.append(Node(x, y, self.dist + d, self))
        
        global nodeq
        for child in self.children:
            nodeq.append(child)

            
    def ancestors(self):
        outlist = []
        
        node = self
        while node.parent:
            node = node.parent
            outlist.append((node.x, node.y))
        return outlist
                    
                
                
    
start_node = Node(startx, starty, 0, None)
nodeq = deque()
nodeq.append(start_node)

while nodeq:
    next_node = nodeq.popleft()
    next_node.expand()

print("Part 1:", max(distances_to_end))
pdb.set_trace()






distances_to_end = []

nodecount = 0
class Node:
    
    def __init__(self, x, y, distance_from_start, ancestor_set):
        global nodecount
        if nodecount % 1000 == 0:
            print("Node", nodecount,"created")
        nodecount += 1
        self.x = x
        self.y = y
        self.dist = distance_from_start
        self.ancestors = ancestor_set
        self.symbol = grid[y][x]
        
        if (x, y) == (goalx, goaly):
            distances_to_end.append(self.dist)

    def expand(self):
        self.children = []
        ancestors = self.ancestors.copy()
        ancestors.add((self.x, self.y))
        for x, y in self.descendant_locations():
            self.children.append(Node(x, y, self.dist + 1, ancestors))
        
        global nodeq
        for child in self.children:
            nodeq.append(child)
        
    # find neighbors that haven't been visited,
    # and are either open or downhill
    def descendant_locations(self):
        
        locations = []
        
        directions = DIRECTIONS4

        for dir in directions:
            dx, dy = dir
            nextx, nexty = self.x + dx, self.y + dy
            if (0 <= nextx < width and
                0 <= nexty < height and
                grid[nexty][nextx] != "#" and 
                (nextx, nexty) not in self.ancestors):
                
                locations.append((nextx, nexty))
                
        return locations
                
                
                
        
start_node = Node(startx, starty, 0, set())
nodeq = [start_node]

while nodeq:
    next_node = nodeq.pop(0)
    next_node.expand()

print("Part 1:", max(distances_to_end))


pdb.set_trace()
