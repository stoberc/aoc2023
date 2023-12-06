from math import prod, floor, ceil

# original solution for Part 1 actually counted values, which doesn't scale for Part 2
# half way through coding up binary search for Part 2 when I realized we could just use math
# did it in Wolfram Alpha + pen/paper, then coded up sol'n later that works for both parts
# simple sol'n (erased) still good for getting first star quickly, so :shrug:

# puzzle input is small, so just manually entered    
TIMES = [40, 81, 77, 72]
DISTANCES = [219, 1012, 1365, 1089]

TIME = int(''.join(str(i) for i in TIMES))
DISTANCE = int(''.join(str(i) for i in DISTANCES))

# return the lowest and highest (inclusive) record breaking charge times
# just solve x * (time - x) = distance
def solve(time, distance):
    # could just do radical, but then have to consider if T is even or odd
    # and think about rounding, so not worth the trouble
    lower_soln = ceil((time - (time * time - 4 * distance) ** 0.5) / 2)
    upper_soln = floor((time + (time * time - 4 * distance) ** 0.5) / 2)
    return upper_soln - lower_soln + 1

print("Part 1:", prod(solve(t, d) for t, d in zip(TIMES, DISTANCES)))    
print("Part 2:", solve(TIME, DISTANCE))
