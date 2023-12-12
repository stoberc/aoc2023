FNAME = "in12.txt"
    
def parse_line(line):
    sequence, counts = line.split()
    values = [int(i) for i in counts.split(",")]
    return sequence, tuple(values)

data = [parse_line(line) for line in open(FNAME).read().splitlines()]

# memoization needed for Part 2
memo = {}
def count(sequence, values):
    # don't recompute solved problems
    if (sequence, values) in memo:
        return memo[(sequence, values)]
    
    # base case - no more values left
    if len(values) == 0:
        if sequence.count("#") == 0:
            memo[(sequence, values)] = 1
            return 1 # valid, but nothing left to fill
        else:
            memo[(sequence, values)] = 0
            return 0 # impossible to deal with a gear if no values remain
    
    # base case - out of sequence
    elif len(sequence) == 0: # and len(vals) > 0
        memo[(sequence, values)] = 0
        return 0 # out of string, but unsatisfied values :(
    
    # base case that shortcuts if there's not enough characters left to succeed
    # not needed for correctness but improves runtime
    if len(sequence) < sum(values) + len(values) - 1:
        memo[(sequence, values)] = 0
        return 0
   
    # if the next spot is definitely empty, it's not helpful
    if sequence[0] == ".":
        result = count(sequence[1:], values)
        memo[(sequence, values)] = result
        return result
        
    # if it's a gear, it must be part of the leading value
    if sequence[0] == "#":
        l = values[0]
        # don't need this if we keep the shortcut that already checked
        # for enough charcters
        #if len(sequence) < l:
        #    memo[(sequence, values)] = 0
        #    return 0
        # elif...
        # if there are any empty spots that must be gears, we can't succeed
        if any(i == "." for i in sequence[:l]):
            memo[(sequence, values)] = 0
            return 0
        # if the problem continues after this, but the next spot can't be
        # empty, we can't succeed
        elif len(sequence) > l and sequence[l] == "#":
            memo[(sequence, values)] = 0
            return 0
        # we can satisfy the leading value, so try to satisfy the rest
        # being sure to skip an empty spot
        result = count(sequence[l + 1:], values[1:])
        memo[(sequence, values)] = result    
        return result
        
    # if it's unknown, we'll try it both ways
    assert sequence[0] == "?"
    empty_count = count(sequence[1:], values)
    gear_count = count("#" + sequence[1:], values)
    result = empty_count + gear_count
    memo[(sequence, values)] = result  
    return result
    
print("Part 1:", sum(count(s, v) for s, v in data))
print("Part 2:", sum(count("?".join([s] * 5), v * 5) for s, v in data))
          