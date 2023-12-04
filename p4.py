FNAME = "in4.txt"
    
# find the score for each line
def parse_line(line):
    a, b = line.split(":")[1].split("|")
    a = [int(i) for i in a.split()] # winning numbers
    b = [int(i) for i in b.split()] # present numbers
    
    # count the number of winners
    count = len(set(a).intersection(b))
            
    if count == 0:
        return 0
    return 2 ** (count - 1) # score doubles per winner

data = [parse_line(line) for line in open(FNAME).read().splitlines()]
print("Part 1:", sum(data))

# now we need the card number and number of matches (not score)
def parse_line(line):
    cardno, rest = line.split(":")
    cardno = int(cardno.split()[1])
    a, b = rest.split("|")
    a = [int(i) for i in a.split()]
    b = [int(i) for i in b.split()]
    return cardno, len(set(a).intersection(b))
    
data = [parse_line(line) for line in open(FNAME).read().splitlines()]

# easier to have a 0 card entry == 0 to keep indexing the same
cardcounts = [1] * (len(data) + 1)
cardcounts[0] = 0

for cardno, matches in data:
    n = cardcounts[cardno]
    # end behavior unspecified,
    # so assuming input is configured to avoid need to clamp final value
    for i in range(cardno + 1, cardno + 1 + matches): 
        cardcounts[i] += n
  
print("Part 2:", sum(cardcounts))
