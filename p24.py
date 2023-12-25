# wow, what a mess; ended up with an imprecise and buggy but occasionally correct solution
# basically run it several times, keep track of the results
# any that are integers and show up repeatedly are probably right? lol

import re
import random

FNAME = "in24.txt"
    
def parse_line(line):
    return [int(i) for i in re.findall('-?\d+', line)] # grab all the numbers

hailstones = [parse_line(line) for line in open(FNAME).read().splitlines()]

# find the x/y intersection between two hailstone trajectories
# (totally disregarding z)
def intersection(h1, h2):
    px1, py1, pz1, vx1, vy1, vz1 = h1
    px2, py2, pz2, vx2, vy2, vz2 = h2

    # worked out algebra by hand to solve for intersection point and intersection times
    
    # if determinant is zero, trajectories are parallel and there is no intersection
    if vx1 * vy2 - vy1 * vx2 == 0:
        return None, None, None, None
    
    t2 = (vy1*(px2 - px1) - vx1*(py2 - py1)) / (vx1 * vy2 - vy1 * vx2)
    t1 = (px2 + t2 * vx2 - px1) / vx1
    x = px1 + t1 * vx1
    y = py1 + t1 * vy1
    return x, y, t1, t2
    
count = 0
for i in range(len(hailstones) - 1):
    hailstone1 = hailstones[i]
    for hailstone2 in hailstones[i + 1:]:
        x, y, t1, t2 = intersection(hailstone1, hailstone2)
        if (x and t1 >= 0 and t2 >= 0 and 
            200000000000000 <= x <= 400000000000000 and 
            200000000000000 <= y <= 400000000000000):
            
            count += 1
            
print("Part 1:", count) # s/b 13754


# pick three hailstones with linearly independent velocity vectors
# just going to pick the first three and cross my fingers
# true for my input, anyway
# update: as this doesn't seem to work due to buginess, we'll pick three at random and pray

# idea:
# fix a time1 on the first trajectory to pick point1,
# then fix a time2 on the second trajectory to pick point2 such that
# the line between points 1 and 2 intersects trajectory3 at all, at a point we'll call point3
# figure out if the timing works out (unlikely on first try) to visit all three points in sequence
# then run binary search on time1 aka point1 until the timing DOES work out
# then we can extrapolate backwards to find the starting point for the stone

# should be able to pick any three linearly independent,
# but this allows us to play around with it
def pick_hailstones(i, j, k):
    global px1, py1, pz1, vx1, vy1, vz1
    global px2, py2, pz2, vx2, vy2, vz2
    global px3, py3, pz3, vx3, vy3, vz3

    px1, py1, pz1, vx1, vy1, vz1 = hailstones[i]
    px2, py2, pz2, vx2, vy2, vz2 = hailstones[j]
    px3, py3, pz3, vx3, vy3, vz3 = hailstones[k]
pick_hailstones(0, 1, 4)

def pick_random_hailstones():
    n = len(hailstones)
    i = j = k = random.randint(0, n - 1)
    while i == j:
        j = random.randint(0, n - 1)
    while k == i or k == j:
        k = random.randint(0, n - 1)
    pick_hailstones(i, j, k)
        
# vector operations
def cross_product(a1, a2, a3, b1, b2, b3):
    return (a2 * b3 - a3 * b2, a3 * b1 - a1 * b3, a1 * b2 - a2 * b1)
    
def dot_product(a1, a2, a3, b1, b2, b3):
    return a1 * b1 + a2 * b2 + a3 * b3
    
def magnitude(a1, a2, a3):
    return (a1 ** 2 + a2 ** 2 + a3 ** 2) ** 0.5
    
def add(a1, a2, a3, b1, b2, b3):
    return (a1 + b1, a2 + b2, a3 + b3)
    
def sub(a1, a2, a3, b1, b2, b3):
    return (a1 - b1, a2 - b2, a3 - b3)

# credit for these next two calculations:
# https://math.stackexchange.com/questions/2213165/find-shortest-distance-between-lines-in-3d
# find the distance between two lines / hailstone trajectories    
def distance(px1, py1, pz1, vx1, vy1, vz1, px2, py2, pz2, vx2, vy2, vz2):
    n = cross_product(vx1, vy1, vz1, vx2, vy2, vz2)
    diff = sub(px2, py2, pz2, px1, py1, pz1)
    numerator = dot_product(*n, *diff)
    denominator = magnitude(*n)
    return numerator / denominator
    
# find times of closest crossing for two trajectories
def closest_times(px1, py1, pz1, vx1, vy1, vz1, px2, py2, pz2, vx2, vy2, vz2):
    n = cross_product(vx1, vy1, vz1, vx2, vy2, vz2)
    diff = sub(px1, py1, pz1, px2, py2, pz2)
    numerator = dot_product(*n, *diff)
    denominator = magnitude(*n)
    d = numerator / denominator
    
    diff = sub(px2, py2, pz2, px1, py1, pz1)
    coeff1 = cross_product(vx2, vy2, vz2, *n)
    coeff2 = cross_product(vx1, vy1, vz1, *n)
    denominator = dot_product(*n, *n)
    t1 = dot_product(*coeff1, *diff) / denominator
    t2 = dot_product(*coeff2, *diff) / denominator
    return t1, t2

# try time1, and return the error between 
# the time hailstone3 reaches the intersection point and 
# the time the magic rock reaches the intersection point
# assign global goal values while we're at it, 
# since we'll want those after this converges
def get_timing_error(t1):
    global pxr, pyr, pzr, vxr, vyr, vzr
  
    x1 = px1 + t1 * vx1
    y1 = py1 + t1 * vy1
    z1 = pz1 + t1 * vz1
    #print(f"Point 1: ({x1}, {y1}, {z1})")
    
    # find t2 that leads to an intersection for this particular t1
    t2 = binary_search(lambda t2: get_distance_error(x1, y1, z1, t2))
    #print(f"t2:{t2}")
    
    # find point2 associated with that time
    x2 = px2 + t2 * vx2
    y2 = py2 + t2 * vy2
    z2 = pz2 + t2 * vz2
    v0 = (x2 - x1, y2 - y1, z2 - z1)
    
    # figure out the velocity vector that would allow the rock 
    # to be at point1 at time1 and point2 at time2
    dt = t2 - t1
    dx = x2 - x1
    dy = y2 - y1
    dz = z2 - z1
    vxr = dx / dt
    vyr = dy / dt
    vzr = dz / dt
    #print(f"Rock velocity:({vxr}, {vyr}, {vzr})")
    
    # figure out the start position too
    pxr = x2 - t2 * vxr
    pyr = y2 - t2 * vyr
    pzr = z2 - t2 * vzr
    #print(f"Rock start position:({pxr}, {pyr}, {pzr})")
    
    # now find the point3 and time3 where that intersection actually occurs
    tr, t3 = closest_times(pxr, pyr, pzr, vxr, vyr, vzr, px3, py3, pz3, vx3, vy3, vz3)
    #print(f"Rock time: {tr}")
    #print(f"t3:{t3}")
    return t3 - tr
    

# take a point1, a time2, calculate point2, 
# then calculate the distance between 
# the line connecting point1 and point2 and line3
def get_distance_error(x1, y1, z1, t2):
    x2 = px2 + t2 * vx2
    y2 = py2 + t2 * vy2
    z2 = pz2 + t2 * vz2
    v0 = sub(x2, y2, z2, x1, y1, z1)
    return distance(x1, y1, z1, *v0, px3, py3, pz3, vx3, vy3, vz3)

def sign(x):
    if x > 0:
        return 1
    elif x < 0:
        return -1
    else:
        return 0
        
# given a function that takes a single input,
# use binary search to find the input that yields an output of zero
# like all binary search, only works if input f is either nonincreasing or nondecreasing
# unclear if this property holds for my functions, though...
def binary_search(f, debug=False):

    v0 = f(0)
    if v0 == 0:
        return 0
    target_sign = -sign(v0)
    
    # find a value that has the opposite signed output as 0
    # lazily searching in both the positive and negative direction
    a, b = 1, -1
    while sign(f(a)) != target_sign and sign(f(b)) != target_sign:
        a *= 2
        b *= 2
        
    # identify which of the two values is the one with the opposite sign
    if sign(f(a)) == target_sign:
        x1 = a
    else:
        x1 = b
        
    # we are searching inputs between x0 and x1
    x0 = 0
    #y0 = f(x0) # already computed
    v1 = f(x1)
    if debug:
        print("Searching between x0 and x1:", x0, x1)
        pdb.set_trace()
    
    xmiddle = (x0 + x1) / 2
    vm = f(xmiddle)
    while vm != 0:
        if sign(vm) == sign(v0):
            x0 = xmiddle
            v0 = vm
        else:
            assert sign(vm) == sign(v1)
            x1 = xmiddle
            v1 = vm
        xmiddle = (x0 + x1) / 2
        vm = f(xmiddle)
        
        # return rounded answer to nearest hundredth or so if no integer solution is found
        if abs(x0 - x1) < 0.001:
            return xmiddle
            
    return xmiddle

# this method fails for selections of the three hailstones for reasons I cannot ascertain
# solution: pick three random hailstones and run the algo until we get a reasonable looking output:
# program terminates without infinite loop or integer overflow and solution is an integer

# thought of implmenting a voting algo where we basically run many random iterations and search
# for solution which comes up most often, but got lucky and first integer solution I found was correct

# I think the main reason this fails sometimes is due to numerical precision issues, but need to debug

pick_random_hailstones()
t1 = binary_search(get_timing_error)
#print(t1, pxr, pyr, pzr, vxr, vyr, vzr)
print("Part 2:", pxr + pyr + pzr) # s/b 711031616315001
