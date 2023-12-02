from math import prod

FNAME = "in2.txt"

# parse a draw string like "6 green, 2 red, 5 blue" into rgb values (2, 6, 5) 
def parse_draw(draw):
    components = draw.split(',')

    result = [0, 0, 0] #rgb
    for c in components:
        value = int(c.split()[0])
        if 'red' in c:
            result[0] += value
        elif 'green' in c:
            result[1] += value
        elif 'blue' in c:
            result[2] += value
        else:
            raise ValueError("Invalid draw component:", c);
    return tuple(result)
    
# break a line apart, returning game number and draw list
def parse_line(line):
    a, b = line.split(": ")
    gameno = int(a.split()[1])
    draws = [parse_draw(draw) for draw in b.split("; ")]
    return gameno, draws
    
# checks if a draw is valid per the rules of Part 1
def valid(draw):
    return draw[0] <= 12 and draw[1] <= 13 and draw[2] <= 14

data = [parse_line(line) for line in open(FNAME).read().splitlines()]

# loop through the data set, summing any valid game
result = sum(gameno for gameno, draws in data if all(valid(draw) for draw in draws))
        
print("Part 1:", result)

# find the minimum number of each color necessary for a particular game
# i.e. the max amount of each color
def mincubes(draws):
    return [max(i) for i in zip(*draws)]

def power(draw):
    return prod(draw)
    
result = sum(power(mincubes(draws)) for _, draws in data)
print("Part 2:", result)
