from aoc_utils import transpose, read_grid

FNAME = "in13.txt"

chunks = open(FNAME).read().split('\n\n')
chunks = [read_grid(chunk) for chunk in chunks]

# returns a list of horizontal xor vertical symmetry lines for a chunk
# e.g. 3 == vertical line that separates left three columns
# 400 == horizontal line that separates top four rows
# if horizontal == True, searches/scores for horizontal lines, else vertical
def get_reflection_lines(chunk, horizontal):
    
    multiplier = 1
    if horizontal:
        chunk = transpose(chunk)
        multiplier = 100
    
    width = len(chunk[0])
    height = len(chunk)
    
    # otherwise a score like 200 could ambighously refer to a vertical or horizontal line
    # not an issue for my input
    assert width <= 100 
    
    # try putting the mirror in all possible places
    symlines = []
    for left_half_width in range(1, width):
        # find the width of the reflected portion (smaller of left/right half 
        min_half_width = min(left_half_width, width - left_half_width)
        symmetrical = True # assume it's symmetrical until we find counterevidence
        for line in chunk:
            left = line[left_half_width - 1::-1][:min_half_width]
            right = line[left_half_width:][:min_half_width]
            if left != right:
                symmetrical = False
                break
        if symmetrical:
            symlines.append(left_half_width * multiplier)
    return symlines
    
def get_all_reflection_lines(chunk):
    return get_reflection_lines(chunk, False) + get_reflection_lines(chunk, True)
    
total = sum(get_all_reflection_lines(chunk)[0] for chunk in chunks)
print("Part 1:", total)

    
# return the new symmetry line for a chunk that can be achieved by correcting a single smudge
def find_smudge(chunk):
    original_symlines = get_all_reflection_lines(chunk)
    for x in range(len(chunk[0])):
        for y in range(len(chunk)):
        
            # invert the current element, find revised symmetry lines, then invert back
            if chunk[y][x] == '.':
                chunk[y][x] = "#"
            else:
                chunk[y][x] = '.'
            revised_symlines = get_all_reflection_lines(chunk)
            if chunk[y][x] == '.':
                chunk[y][x] = "#"
            else:
                chunk[y][x] = '.'
                
            # identify all symmetry lines that weren't here before
            # returning such a line if found
            new_symlines = [i for i in revised_symlines if i not in original_symlines]
            if new_symlines:
                assert len(new_symlines) == 1 # problem property says there should be just one
                return new_symlines[0]

total = sum(find_smudge(chunk) for chunk in chunks)
print("Part 1:", total)
