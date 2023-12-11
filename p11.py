FNAME = "in11.txt"
    
map = open(FNAME).read().splitlines()

# identify rows and columns that are galaxy-free
deadrows = []
for y in range(len(map)):
    if map[y].count("#") == 0:
        deadrows.append(y)
    
deadcols = []    
for x in range(len(map[0])):
    if [row[x] for row in map].count("#") == 0:
        deadcols.append(x)
  
# identify galaxy coordinates  
galaxies = []
for y in range(len(map)):
    for x in range(len(map[0])):
        if map[y][x] == "#":
            galaxies.append((x, y))

# find the distance between two galaxies, adding in extra distance for empty
# e.g. for Part 1, there's 1 extra for each of those (since they're doubled)
# for Part 2, there's 999999 extra for each of those (since they're 1000000x)
def dist(galaxy1, galaxy2, extra):
    x1, y1 = galaxy1
    x2, y2 = galaxy2
    return (abs(x2 - x1) + abs(y2 - y1) + 
        extra * (sum(x1 < x < x2 or x2 < x < x1 for x in deadcols) + 
            sum(y1 < y < y2 or y2 < y < y1 for y in deadrows)))

# find pairwise sum of galactic distances
def get_score(extra):
    result = 0
    for i in range(len(galaxies) - 1):
        for j in range(i + 1, len(galaxies)):
            result += dist(galaxies[i], galaxies[j], extra)
    return result
    
# display results
print("Part 1:", get_score(1))
print("Part 2:", get_score(999999))
