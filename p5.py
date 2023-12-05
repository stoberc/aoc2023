#Part 1: 218513636
#Part 2: 81956384

import pdb

FNAME = "in5.txt"

# break into chunks
chunks = [chunk.splitlines() for chunk in open(FNAME).read().split('\n\n')]

# first chunk is seed values
seeds = [int(i) for i in chunks[0][0].split()[1:]]

# render each rule as an immutable sequence of values, for now
# though later learning makes it clear that converting to boundary values eases reasoning
def parse_rule(line):
    return tuple([int(i) for i in line.split()])
    
# throw out the name and then parse the rest (the rules) 
def parse_ruleset(lines):
    name = lines[0]
    rest = lines[1:]
    return [parse_rule(line) for line in rest]

# rest of chunnks are rulesets
rulesets = chunks[1:]
rulesets = [parse_ruleset(r) for r in rulesets]

# Part 1: map each seed through the lattice to a final location
def get_location(seed):
    current_value = seed
    for ruleset in rulesets:
        for destination_range_start, source_range_start, range_length in ruleset:
            if source_range_start <= current_value < source_range_start + range_length:
                current_value = destination_range_start + current_value - source_range_start
                break
    return current_value

print("Part 1:", min(get_location(seed) for seed in seeds))

# adjacent values are actually pairs in Part 2
seeds = [tuple(i) for i in zip(seeds[0::2], seeds[1::2])]

# way easier to reason with boundary values (inclusive) instead of length
seeds2 = []
for start, length in seeds:
    seeds2.append((start, start + length - 1))
seeds = seeds2

# remap the rulesets in the same fashion, each one will be (source_start, source_end, shift)
def convert(ruleset):
    outrules = []
    for destination_range_start, source_range_start, range_length in ruleset:
        source_end = source_range_start + range_length - 1
        shift = destination_range_start - source_range_start
        outrules.append((source_range_start, source_end, shift))
    return outrules
rulesets = [convert(ruleset) for ruleset in rulesets]

# abandoned first attempt that wasted an insane amount of time
# I think the approach fundamentally works the same as what I ended up doing,
# but I got lost in the nuances of the arithmetic for each case.
# could probably be reworked, but finally had to burn it to the ground and start over using boundary values
# would like to poke around in here and figure out where I went wrong at some point
# which proved much easier to reason with
"""
# takes in a range then returns a list of resultant ranges when passed through the rule set
def apply_ruleset(seed_range, ruleset):
    pause = False
    print("Call to apply_ruleset w/ args:", seed_range, ruleset)
    remaining_ranges = [seed_range]
    output_ranges = []
    for destination_range_start, source_range_start, range_length in ruleset:
        remove_list = []
        add_list = []
        for seed_range in remaining_ranges:
            print("Processing seed_range", seed_range, "vs.", destination_range_start, source_range_start, range_length)
            start, length = seed_range
            end = start + length - 1
            if end < source_range_start:
                print(" end < source_range_start") 
                continue
            elif start > source_range_start + range_length:
                print(" start > source_range_start + range_length")
                continue
            elif start >= source_range_start and end < source_range_start + range_length:
                print(" start >= source_range_start and end < source_range_start + range_length")
                remove_list.append(seed_range)
                start = destination_range_start + start - source_range_start
                end = destination_range_start + end - source_range_start
                output_ranges.append((start, length))
            elif start < source_range_start and end >= source_range_start + range_length:
                print(" start < source_range_start and end >= source_range_start + range_length")
                remove_list.append(seed_range)
                add_list.append((start, source_range_start - start))
                add_list.append((source_range_start + range_length, end - (source_range_start + range_length + 1)))
                output_ranges.append((destination_range_start, range_length))
            elif start < source_range_start:
                print(" start < source_range_start")
                remove_list.append(seed_range)
                add_list.append((start, source_range_start - start))
                output_ranges.append((destination_range_start, end - source_range_start + 1))
            elif end >= source_range_start + range_length:
                print(" end >= source_range_start + range_length")
                remove_list.append(seed_range)
                add_list.append((source_range_start + range_length, end - (source_range_start + range_length)))
                output_ranges.append((destination_range_start + (start - source_range_start), source_range_start + range_length - start + 1)) # CHECK
                #pause = True
            else:
                raise ValueError("I'm confused:", seed_range, destination_range_start, source_range_start, range_length)
            
            print("remove_list:", remove_list)
            print("add_list:", add_list)
            print("output_ranges:", output_ranges)
            if pause:
                pdb.set_trace()
            for r in remove_list:
                remaining_ranges.remove(r)
            for r in add_list:
                remaining_ranges.append(r)
    
    for r in remaining_ranges:
        output_ranges.append(r)
    return output_ranges
"""

# returns two lists:
# first - transformed seed ranges that were affected by the rule
# second - untransformed seed ranges that may still be affected by subsequent rules
def apply_rule(seed_range, rule):
    transformed = []
    untransformed = []
    seed_low, seed_high = seed_range
    rule_low, rule_high, shift = rule
    # if there's nov overlap, then this rule does not affect the seed range
    if seed_high < rule_low or seed_low > rule_high:
        untransformed.append(seed_range)
    # if the rule completely encompasses the seed range,the whole thing is transformed
    elif seed_low >= rule_low and seed_high <= rule_high:
        transformed.append((seed_low + shift, seed_high + shift))
    # if the rule is in the interior of the seed range, a central chunk os transformed
    # and two ends are untransformed
    elif seed_low < rule_low and seed_high > rule_high:
        a = (seed_low, rule_low - 1)
        b = (rule_low + shift, rule_high + shift)
        c = (rule_high + 1, seed_high)
        transformed.append(b)
        untransformed.append(a)
        untransformed.append(c)
    # if the rule affects the upper end of the seed range...
    elif rule_low <= seed_high <= rule_high:
        a = (seed_low, rule_low - 1)
        b = (rule_low + shift, seed_high + shift)
        transformed.append(b)
        untransformed.append(a)
    # if the rule affects the lower end of the seed range...
    elif rule_low <= seed_low <= rule_high:
        b = (seed_low + shift, rule_high + shift)
        c = (rule_high + 1, seed_high)
        transformed.append(b)
        untransformed.append(c)
    else:
        raise ValueError("WTF") # I don't think there are any other possibilities
    return transformed, untransformed
    
# same idea, except apply ALL rules in a ruleset
def apply_ruleset(seed_range, ruleset):
    queue = [seed_range]
    result = []
    while queue:
        seed_range = queue.pop(0)
        rule_applied = False
        for rule in ruleset:
            transformed, untransformed = apply_rule(seed_range, rule)
            if transformed:
                result += transformed
                queue += untransformed
                rule_applied = True
                break
        if not rule_applied:       
            result.append(seed_range)
    return result

# transform all seeds through one ruleset at a time
for ruleset in rulesets:
    next_wave_seeds = []
    for seed_range in seeds:
        next_wave_seeds += apply_ruleset(seed_range, ruleset)
    seeds = next_wave_seeds
    
print("Part 2:", min(i for i, _ in seeds))

#pdb.set_trace()
