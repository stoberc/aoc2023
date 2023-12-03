import pdb
from math import prod

FNAME = "in3.txt"
DIGITS = '0123456789'

data = open(FNAME).read().splitlines()

partnos = []

# basically loop through each row until you find a digit
# then advance until you stop finding digits
# then search the surrounding area for symbols
total = 0
for row in range(len(data)):
    line = data[row]
    
    i = 0 # index targeting a digit
    while i < len(line):
        while i < len(line) and line[i] not in DIGITS: # careful not to iterate past the end
            i += 1
        
        if i == len(line): # if we got to the end, break and go to the next line
            break
            
        # now i is the index of the first digit of some number
        j = i + 1 # j targets the index after the final digit
        while j < len(line) and line[j] in DIGITS:
            j += 1
        
        # now i is the start of the number, j is just after the end of the number
        value = int(line[i:j])
        numdigits = j - i
                    
        # want to search adjacent spots, row +/-1 and col +/- 1
        # but need to make sure we don't go out of bounds
        minrow = max(row - 1, 0)
        maxrow = min(row + 1, len(data) - 1)
        mincol = max(i - 1, 0)
        maxcol = min(i + numdigits, len(line) - 1)
        
        # now check all around for a symbol
        symbol_found = False
        for r in range(minrow, maxrow + 1):
            for c in range(mincol, maxcol + 1):
                if data[r][c] not in DIGITS + ".": # ignore numbers and .
                    total += value
                    symbol_found = True
                    break
                if symbol_found:
                    break
        
        i += numdigits # skip past the current number to keep looking
                
print("Part 1:", total)

      
# go to a particular row and column and return the number found there
# this may require expanding the left and/or right from the target
# to see the whole number
# returns None if intial position is not a number      
def grab_number(r, c):
    if data[r][c] not in DIGITS:
        return None
    
    # search for the first digit
    i = c
    while i >= 0 and data[r][i] in DIGITS:
        i -= 1
    i += 1
    
    # search for the last digit (+1)
    j = c
    while j < len(data[r]) and data[r][j] in DIGITS:
        j += 1
        
    return int(data[r][i:j])
  
# now search for gears, then search neighborhood around gear for numbers
# collect all neighboring numbers, then if there are two,
# include product in total  
total = 0
for row in range(len(data)):
    line = data[row]
    for col in range(len(line)):
        if data[row][col] == "*":
            neighbors = []
            # check the row above if it's in bounds
            if row > 0:
                # if there's a digit above,
                # then there's only a single number possible above
                v = grab_number(row - 1, col)
                if v:
                    neighbors.append(v)
                # otherwise, could be two numbers there, left and right
                else:
                    if col > 0:
                        v = grab_number(row - 1, col - 1)
                        if v:
                            neighbors.append(v)
                    if col < len(line) - 1:
                        v = grab_number(row - 1, col + 1)
                        if v:
                            neighbors.append(v)
            # check the row below if it's in bounds
            if row < len(data) - 1:
                v = grab_number(row + 1, col)
                if v:
                    neighbors.append(v)
                else:
                    if col > 0:
                        v = grab_number(row + 1, col - 1)
                        if v:
                            neighbors.append(v)
                    if col < len(line) - 1:
                        v = grab_number(row + 1, col + 1)
                        if v:
                            neighbors.append(v)
            # check to the left of the gear if it's in bounds
            if col > 0:
                v = grab_number(row, col - 1)
                if v:
                    neighbors.append(v)
            # check to the right of the gear if it's in bounds
            if col < len(line) - 1:
                v = grab_number(row, col + 1)
                if v:
                    neighbors.append(v)
            if len(neighbors) == 2:
                total += prod(neighbors)
            
print("Part 2:", total)
        
#pdb.set_trace()
