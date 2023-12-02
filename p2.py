import pdb

FNAME = "in2.txt"

def parse_draw(draw):
    result = [0, 0, 0] #rgb
    for d in draw:
        if 'red' in d:
            result[0] += int(d.split()[0])
        elif 'green' in d:
            result[1] += int(d.split()[0])
        elif 'blue' in d:
            result[2] += int(d.split()[0])
        else:
            raise ValueError("Invalid draw:", d);
    return tuple(result)
    
def parse_line(line):
    gameno = int(line.split()[1][:-1])
    a, b = line.split(": ")
    draws = b.split("; ")
    draws = [draw.split(",") for draw in draws]
    draws = [parse_draw(draw) for draw in draws]
    return gameno, draws
    
def valid1(draw):
    return draw[0] <= 12 and draw[1] <= 13 and draw[2] <= 14

data = [parse_line(line) for line in open(FNAME).read().splitlines()] # in chunks[0]]

result = 0
for gameno, draws in data:
    if all(valid1(draw) for draw in draws):
        result += gameno
        
print("Part 1:", result)

def mincubes(draws):
    return [max(i) for i in zip(*draws)]

def power(draw):
    return draw[0] * draw[1] * draw[2]
    
print("Part 2:", sum(power(mincubes(draws)) for _, draws in data))

#pdb.set_trace()
