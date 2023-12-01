FNAME = "in1.txt"
DIGITS = '0123456789'
NUMBERS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']

# Part 1 - only numeral digits, ignore words
def parse_line(line):

    for i in line:
        if i in DIGITS:
            break

    for j in reversed(line):
        if j in DIGITS:
            return int(i + j)

# convert a written value into a digit, returning original value (presumably digit) if not found
DIGIT_LUT = {'one':'1', 'two':'2', 'three':'3', 'four':'4', 'five':'5', 'six':'6', 'seven':'7', 'eight':'8', 'nine':'9'}
def convert(n):
    try:
        return DIGIT_LUT[n]
    except:
        return n
    
# Part 2 - words and digits
def parse_line2(line):

    # find the indices of every possible value, and keep the lowest one
    a = [line.find(i) for i in NUMBERS]
    b = min(k for k in a if k >= 0) # careful w/ -1 not found
    c = a.index(b)
    i = NUMBERS[c]
    i = convert(i)
    
    # use rfind to find rightmost instance, intead
    a = [line.rfind(i) for i in NUMBERS]
    b = max(a)
    c = a.index(b)
    j = NUMBERS[c]
    j = convert(j)
    
    return int(i + j)

lines = open(FNAME).read().splitlines()

data = [parse_line(line) for line in lines]
print("Part 1:", sum(data))

data = [parse_line2(line) for line in lines]
print("Part 2:", sum(data))
