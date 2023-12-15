FNAME = "in15.txt"
    
initialization = open(FNAME).read().strip().split(',')
# test case from problem description
# result s/b 145 for Part 2
#initialization = "rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7".split(',')

def hash(s):
    current_value = 0
    for i in s:
        current_value += ord(i)
        current_value *= 17
        current_value %= 256
    return current_value
    
print("Part 1:", sum(hash(i) for i in initialization))

boxes = [[] for _ in range(256)]
for instruction in initialization:
    
    if '=' in instruction:
        label, focal_length = instruction.split('=')
        focal_length = int(focal_length)
    else:
        label = instruction[:-1]    
    boxno = hash(label)
    
    if '-' in instruction:
        for i in boxes[boxno]:
            if i[0] == label:
                boxes[boxno].remove(i)
                break
    else:
        replacement = False
        for lens_index in range(len(boxes[boxno])):
            if boxes[boxno][lens_index][0] == label:
                boxes[boxno][lens_index][1] = focal_length
                replacement = True
                break
        if not replacement:
            boxes[boxno].append([label, focal_length])

total_focusing_power = 0
for boxno in range(len(boxes)):
    for lens_index in range(len(boxes[boxno])):
        slotno = 1 + lens_index
        _, focal_length = boxes[boxno][lens_index]
        focusing_power = (1 + boxno) * slotno * focal_length
        total_focusing_power += focusing_power
print("Part 2:", total_focusing_power)
