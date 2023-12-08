# It turns out that the input has several special properites that greatly simplify Part 2.
# I'm not crazy about puzzles like this where you have to realize lucky properties of the
# input data in order to code up a general solution, though admittedly, the general solution
# would've been way more work.

# Here were the helpful factors of the input data:
# 1. Each start node led to exactly one end node. In the general case, there's no reason a
#    start node couldn't pass several end nodes, including some over and over again once
#    it enters periodicity.
# 2. It was a bit of a magical discovery that the number of steps it takes to go from a
#    particular start to a particular end is exactly equal to the period. There's no reason,
#    for example, that a start couldn't lead immediately to and end, then wander around a long
#    time before coming back to that end.
# 3. It was also a bit magical that the number of steps it took to enter the periodic cylce
#    was exactly equal to the number of steps AFTER the end node in a periodic cycle, resulting
#    in the property that if the period is T, and the end node is first visited at time T, it
#    will again be visited at times 2T, 3T, etc.
# All of these factors together boiled this down to calculating the period of each input and
# find the LCM.

import re
from math import prod, lcm

FNAME = "in8.txt"

# look up table that takes in a node name and returns a tuple containing the left and right
# nodes from there.
options = {}
def parse_line(line):
    a, b, c = re.findall('\w+', line) # each node name is sequence letters '\w{3}' would work too
    options[a] = (b, c)
   
instructions, nodemap = open(FNAME).read().split('\n\n')
nodemap = nodemap.splitlines()

for line in nodemap:
    parse_line(line)
    
count = 0
current = 'AAA'
i = 0
while current != 'ZZZ':
    if instructions[i] == 'L':
        current = options[current][0]
    else:
        current = options[current][1]
    count += 1
    i = (i + 1) % len(instructions)
    
print("Part 1:", count)


start_nodes = [i for i in options if i[2] == 'A']
end_nodes = [i for i in options if i[2] == 'Z']

# precondition: the input is a start node
# returns the period length which == the time it takes to get to the only ending
# originally intendted to return the following in the generalized case:
# period 
# entry time into period, and 
# times on interval [entry_time, entry_time + period) that an end_note is visited
def characterize_periodicity(node):
    instruction_index = 0
    elapsed_time = 0
    current_node = node
    timestamp = {}
    end_times = []
    
    while (current_node, instruction_index) not in timestamp:
        timestamp[(current_node, instruction_index)] = elapsed_time
        if current_node in end_nodes:
            end_times.append(elapsed_time)
            
        if instructions[instruction_index] == 'L':
            current_node = options[current_node][0]
        else:
            current_node = options[current_node][1]
        
        instruction_index = (instruction_index + 1) % len(instructions)
        elapsed_time += 1
    
    entry_time = timestamp[(current_node, instruction_index)]    
    period = elapsed_time - entry_time
    
    # for reasons I don't at all understand, each path from a start node visits exactly one end node
    # and the elapse time that it arrives, as revealed by this diagnostic
    # this greatly simplifies the problem, because then we only need to find the lcm of each period
    #print("Node:", node)
    #print("Period found: ", period)
    #print("Entry time: ", entry_time)
    #print("End times: ", end_times)
    #print()
    
    return end_times[0] 
    
# Used to run those prints above and learn about the data
#for node in start_nodes:
#    characterize_periodicity(node)

# returns where you will be if you start at node and then iterate steps steps
# useful for debug and exploring the data set
def test(node, steps):
    i = 0
    current = node
    for _ in range(steps):
        if instructions[i] == 'L':
            current = options[current][0]
        else:
            current = options[current][1]
        i = (i + 1) % len(instructions)
    return current
        
print("Part 2:", lcm(*[characterize_periodicity(i) for i in start_nodes]))

