import re

FNAME = "in19.txt"
    
workflows_chunk, parts_chunk = open(FNAME).read().split("\n\n")

# workflows looked up based on name
workflows = {}
def parse_workflow(line):
    name, rest = line[:-1].split("{")
    rules = rest.split(',')
    outrules = []
    for rule in rules[:-1]:
        assert ':' in rule
        cond, result = rule.split(':')
        outrules.append((cond, result))
    assert ':' not in rules[-1]
    # easier to keep the final "else" w/ same structure -> else if True
    outrules.append(("True", rules[-1])) 
    workflows[name] = outrules
       
for line in workflows_chunk.splitlines():
    parse_workflow(line)

# mainly a container for x, m, a, s which can be assigned ad hoc
class Part():
    def score(self):
        return self.x + self.m + self.a + self.s
    
def parse_part(line):
    p = Part()
    p.x, p.m, p.a, p.s = [int(i) for i in re.findall('\d+', line)]
    return p
    
parts = [parse_part(line) for line in parts_chunk.splitlines()]

# check if a part is accepted by a particular workflow
def is_accepted(part, workflow_name):
    x, m, a, s = part.x, part.m, part.a, part.s
    for cond, result in workflows[workflow_name]:
        if eval(cond):
            if result == "A":
                return True
            elif result == "R":
                return False
            else:
                return is_accepted(part, result)

print("Part 1:", sum(part.score() for part in parts if is_accepted(part, "in")))


# a container for bounds on x, m, a, s and related operations
class Interval():

    def __init__(self, xmin, xmax, mmin, mmax, amin, amax, smin, smax):
        self.xmin = xmin
        self.xmax = xmax
        self.mmin = mmin
        self.mmax = mmax
        self.amin = amin
        self.amax = amax
        self.smin = smin
        self.smax = smax
        
    # how many distinct combinations are represented by this interval?
    def size(self):
        return (self.xmax - self.xmin + 1) * (self.mmax - self.mmin + 1) * (self.amax - self.amin + 1) * (self.smax - self.smin + 1)
        
    # split the interval into two intervals based on the condition
    # one of these might be a garbage interval if the condition is always true or always false on the interval
    def split(self, cond):
        true_interval = Interval(self.xmin, self.xmax, self.mmin, self.mmax, self.amin, self.amax, self.smin, self.smax)
        false_interval = Interval(self.xmin, self.xmax, self.mmin, self.mmax, self.amin, self.amax, self.smin, self.smax)
        
        if "<" in cond:
            val = int(cond.split("<")[1])
            if 'x' in cond:
                true_interval.xmax = min(true_interval.xmax, val - 1)
                false_interval.xmin = max(false_interval.xmin, val)
            elif 'm' in cond:
                true_interval.mmax = min(true_interval.mmax, val - 1)
                false_interval.mmin = max(false_interval.mmin, val)            
            elif 'a' in cond:
                true_interval.amax = min(true_interval.amax, val - 1)
                false_interval.amin = max(false_interval.amin, val)
            elif 's' in cond:
                true_interval.smax = min(true_interval.smax, val - 1)
                false_interval.smin = max(false_interval.smin, val)
            else:
                raise ValueError("WTF")
        else:
            assert ">" in cond
            val = int(cond.split(">")[1])
            if 'x' in cond:
                false_interval.xmax = min(true_interval.xmax, val)
                true_interval.xmin = max(false_interval.xmin, val + 1)
            elif 'm' in cond:
                false_interval.mmax = min(true_interval.mmax, val)
                true_interval.mmin = max(false_interval.mmin, val + 1)            
            elif 'a' in cond:
                false_interval.amax = min(true_interval.amax, val)
                true_interval.amin = max(false_interval.amin, val + 1)
            elif 's' in cond:
                false_interval.smax = min(true_interval.smax, val)
                true_interval.smin = max(false_interval.smin, val + 1)
            else:
                raise ValueError("WTF")
        
        return true_interval, false_interval
        
    # count the number of acceptances when applying a particular workflow to this interval
    def count_acceptances(self, workflow_name):
        if self.xmax < self.xmin or self.mmax < self.mmin or self.amax < self.amin or self.mmax < self.mmin or workflow_name == "R":
            return 0
            
        if workflow_name == "A":
            return self.size()
            
        total = 0
        
        for cond, result in workflows[workflow_name]:
            if cond == "True":
                total += self.count_acceptances(result)
            else:
                true_interval, self = self.split(cond)
                total += true_interval.count_acceptances(result)
                
        return total
        
    # debug
    def __repr__(self):
        return f"<x({self.xmin}, {self.xmax}), m({self.mmin}, {self.mmax}),a({self.amin}, {self.amax}),s({self.smin}, {self.smax})>"
      
                    
total = Interval(1, 4000, 1, 4000, 1, 4000, 1, 4000)
print("Part 2:", total.count_acceptances("in"))
