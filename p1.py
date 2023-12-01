#import pdb

FNAME = "in1.txt"
DIGITS = '0123456789'
OPTIONS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']
OPTIONS2 = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'eno', 'owt', 'eerht', 'ruof', 'evif', 'xis', 'neves', 'thgie', 'enin']

def parse_line(line):
    
    # ugh this doesn't work because of unfriendly inputs, for example 'eightwo' replacing the 'two' will destroy the 'eight'
    #line = line.replace('one', '1').replace('two', '2').replace('three', '3').replace('four', '4').replace('five', '5').replace('six', '6').replace('seven', '7').replace('eight', '8').replace('nine', '9')
    # would've been nice!

    i = ""    
    for i in line:
        if i in DIGITS:
            break

    j = ""
    for j in reversed(line):
        if j in DIGITS:
            break
    
    return int(i) * 10 + int(j)
    
    
def parse_line2(line):
    a = [line.find(i) for i in OPTIONS]
    b = min(k for k in a if k >= 0)
    c = a.index(b)
    i = OPTIONS[c]
    i = i.replace('one', '1').replace('two', '2').replace('three', '3').replace('four', '4').replace('five', '5').replace('six', '6').replace('seven', '7').replace('eight', '8').replace('nine', '9')
    i = int(i)
    
    line = ''.join(reversed(line))
    a = [line.find(i) for i in OPTIONS2]
    b = min(k for k in a if k >= 0)
    c = a.index(b)
    j = OPTIONS2[c]
    j = j.replace('eno', '1').replace('owt', '2').replace('eerht', '3').replace('ruof', '4').replace('evif', '5').replace('xis', '6').replace('neves', '7').replace('thgie', '8').replace('enin', '9')
    j = int(j)

    return 10 * i + j

data = [parse_line(line) for line in open(FNAME).read().splitlines()]
print("Part 1:", sum(data))

data = [parse_line2(line) for line in open(FNAME).read().splitlines()]
print("Part 2:", sum(data))

#pdb.set_trace()
