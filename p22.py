import re

FNAME = "in22.txt"
    
class Brick:

    # it'll be convenient to store minimum values in position 0
    def __init__(self, x0, y0, z0, x1, y1, z1):
        if x0 + y0 + z0 < x1 + y1 + z1:
            self.x0 = x0
            self.y0 = y0
            self.z0 = z0
            self.x1 = x1
            self.y1 = y1
            self.z1 = z1
        else:
            self.x0 = x1
            self.y0 = y1
            self.z0 = z1
            self.x1 = x0
            self.y1 = y0
            self.z1 = z0
           
        # list of bricks that I support
        # will populate as other bricks drop and come to rest on me
        self.bricks_i_support = []
  
    def __repr__(self):
        return f"{self.x0},{self.y0},{self.z0}~{self.x1},{self.y1},{self.z1}"
    
    # returns a list of all cubes contained in this brick
    def allcubes(self):
        outcubes = []
        for x in range(self.x0, self.x1 + 1):
            for y in range(self.y0, self.y1 + 1):
                for z in range(self.z0, self.z1 + 1):
                    outcubes.append((x, y, z))
        return outcubes
    
    # does this brick contain a particular cube coordinate?
    def contains(self, x, y, z):
        return (self.x0 <= x <= self.x1 and
                self.y0 <= y <= self.y1 and 
                self.z0 <= z <= self.z1)
                
    # reduce z until I come to rest on another brick
    def drop(self):
        # find all bricks in the xy projection below this one
        bricks_below = [b for b in bricks if b.overlaps_xy(self.x0, self.x1, self.y0, self.y1) and b.z1 < self.z0]
        
        # if there weren't any, we'll rest on the ground, otherwise we'll rest on the highest of them
        if len(bricks_below) == 0:
            highest_z = 0
        else:
            highest_z = max(b.z1 for b in bricks_below)
            
        # figure out how much we need to drop by, then drop that much
        targetz0 = highest_z + 1
        dz = self.z0 - targetz0
        self.z0 -= dz
        self.z1 -= dz
        
        # log which bricks I'm resting on, and log myself for those bricks
        self.supporting_bricks = [b for b in bricks_below if b.z1 == highest_z]
        for b in self.supporting_bricks:
            b.bricks_i_support.append(self)
    
    # debug for me to realize the provided constraint that all bricks are linear
    def volume(self):
        return (self.x1 - self.x0 + 1) * (self.y1 - self.y0 + 1) * (self.z1 - self.z0 + 1)
        
    # check if this brick overlaps a particular xy projection (in any z)
    def overlaps_xy(self, x0, x1, y0, y1):
        # inefficient, but bricks are all small (length <= 5), so it should be OK
        for x, y, z in self.allcubes():
            if x0 <= x <= x1 and y0 <= y <= y1:
                return True
        return False
        
    # return the number of bricks that will fall if I disintegrate
    def topple_count(self):
        toppled = set([self])
        toppleq = [self]
        
        while toppleq:
            b = toppleq.pop(0)
            
            # check all the bricks directly above the current one
            # if all of that bricks supporting bricks are gone, it topples too
            for brick_above in b.bricks_i_support:
                if all(sub_brick in toppled for sub_brick in brick_above.supporting_bricks):
                    toppled.add(brick_above)
                    toppleq.append(brick_above)
            
        return len(toppled) - 1 # self not included
            
bricks = []
for line in open(FNAME).read().splitlines():
    bricks.append(Brick(*[int(i) for i in re.findall('-?\d+', line)]))

# sort bricks based on distance of bottom from ground
bricks.sort(key=lambda b: b.z0)

# bricks that will cause problems if disintegrated, since they are the only brick propping up some other brick
lone_supporting_bricks = set() 

# loop through the bricks, dropping them until they come to rest on another brick, logging any loners
for b in bricks:
    b.drop()
    if len(b.supporting_bricks) == 1:
        lone_supporting_bricks.add(b.supporting_bricks[0])

# Part 1, we actually want the safe bricks
print("Part 1:", len(bricks) - len(lone_supporting_bricks)) # s/b 375
print("Part 2:", sum(b.topple_count() for b in bricks)) # s/b 72352
