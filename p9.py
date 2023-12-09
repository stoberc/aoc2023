import re

FNAME = "in9.txt"
    
def parse_line(line):
    return [int(i) for i in re.findall('-?\d+', line)] # grab all the ints
data = [parse_line(line) for line in open(FNAME).read().splitlines()]

def extrapolate(sequence):
    # could have base case one layer shallower when all values are ==, but :shrug:
    if all(i == 0 for i in sequence):
        return 0
    diffsequence = []
    for i in range(1, len(sequence)):
        diffsequence.append(sequence[i] - sequence[i - 1])
    d = extrapolate(diffsequence)
    return sequence[-1] + d

print("Part 1:", sum(extrapolate(s) for s in data))

def extrapolate(sequence):
    # could have base case one layer shallower when all values are ==, but :shrug:
    if all(i == 0 for i in sequence):
        return 0
    diffsequence = []
    for i in range(1, len(sequence)):
        diffsequence.append(sequence[i] - sequence[i - 1])
    d = extrapolate(diffsequence)
    return sequence[0] - d        

print("Part 2:", sum(extrapolate(s) for s in data))
