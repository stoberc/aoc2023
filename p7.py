import pdb
from math import prod
import functools

FNAME = "in7.txt"
    
def parse_line(line):
    hand, bid = line.split()
    bid = int(bid)
    return hand, bid

# return a sorted tuple with the counts of cards
# for example (1, 2, 2) would be two pairs, (2, 3) would be full house...
def count_profile(hand):
    cards = set(hand)
    counts = [hand.count(card) for card in cards]
    counts.sort()
    return tuple(counts)
    
# return a score 1 to 7 inclusive...
# 7 is the best (five of a kind)
# 1 is the worst (high card)
def classify_hand(hand):
    cp = count_profile(hand)
    if cp == (5,): # five of a kind
        return 7
    elif cp == (1, 4): # four of a kind
        return 6
    elif cp == (2, 3): # # full house
        return 5
    elif cp == (1, 1, 3): # three of a kind
        return 4
    elif cp == (1, 2, 2): # two pair
        return 3
    elif cp == (1, 1, 1, 2): # single pair
        return 2
    else: # high card
        return 1
# save the original to allow the updated version for Part 2 to fall back on this when there are no jokers
classify_hand_classic = classify_hand 
    
# lookup table converts cards into sequencable values, needed for breaking ties
VALUE_LUT = {'A':14, 'K':13, 'Q':12, 'J':11, 'T':10, '9':9, '8':8, '7':7, '6':6, '5':5, '4':4, '3':3, '2':2}
def tie_break(hand1, hand2):
    if len(hand1) == 0: # recursion base case
        return 0 # would input allow for exact same hand? probably not, but dealing with it
    if hand1[0] == hand2[0]: # if there's a tie in this spot, move to the next spot
        return tie_break(hand1[1:], hand2[1:])
    if VALUE_LUT[hand1[0]] > VALUE_LUT[hand2[0]]: # compare the cards in this spot
        return 1
    return -1
    
# compare two hands by classified rank first, tiebreaking if necessary
# easier to have this just take a (hand, bid) pair so that I can keep the
# overall data structure intact during sorting
def compare(hand_bid1, hand_bid2):
    hand1 = hand_bid1[0]
    hand2 = hand_bid2[0]
    rank_score1 = classify_hand(hand1)
    rank_score2 = classify_hand(hand2)
    if rank_score1 > rank_score2:
        return 1
    elif rank_score1 < rank_score2:
        return -1
    else:
        return tie_break(hand1, hand2)

# load the list of hands and sequence it    
data = [parse_line(line) for line in open(FNAME).read().splitlines()]
data.sort(key=functools.cmp_to_key(compare))

# score from (1 to n) * bid
rank = 1
result = 0
for _, bid in data:
    result += rank * bid
    rank += 1
print("Part 1:", result)


# redefine this function for Part 2 to deal with jokers
def classify_hand(hand):
    cp = count_profile(hand)
    if 'J' not in hand: # no jokers
        return classify_hand_classic(hand)
    # any hand w/ at most two distinct cards turns into five-of-a-kind w/ jokers
    elif cp in [(5,), (1, 4), (2, 3)]: 
        return 7
    elif len(set(hand)) == 3: # three distince values...
        if cp == (1, 1, 3) or hand.count('J') == 2: # 3 jokers or two-pair w/ two jokers is four-of-a-kind
            return 6
        else: # two pairs with a lone joker is a full house
            return 5
    elif len(set(hand)) == 4: # four distinct values will always turn into three of a kind
        return 4
    else: # five distinct values will turn into a pair
        return 2

# reset scoring for jack to be low for tie breakers
VALUE_LUT['J'] = 1

# resort and recalculate
data.sort(key=functools.cmp_to_key(compare))

rank = 1
result = 0
for _, bid in data:
    result += rank * bid
    rank += 1
print("Part 2:", result)

#pdb.set_trace()
