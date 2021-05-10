import random
from collections import Counter
import itertools

box_start = [1, 2, 3, 4, 5, 6, 7, 8, 9]
die = [1, 2, 3, 4, 5, 6]
repetitions = 100000
score_list = []
    
def roll_dice(numdice):
    tot = 0;
    for n in range(numdice):
        tot = tot + random.choice(die)
    return tot;

def flip_tiles(tiles, combinations):
#choose random combination
    #comb_choice = random.choice(combinations)  #choose randomly

    last_max = 0
    last_min = 0
    last_len = 0
    for comb in combinations:
#choose combination with highest digit
        if max(comb) >= last_max:   
            last_max = max(comb)
            comb_choice = comb

#choose combination whose lowest digit is higher than all the others' lowest digit
#        if min(comb) >= last_min:  
#            last_min = min(comb)
#            comb_choice = comb

#choose combination that maximizes number of tiles flipped
#        if len(comb) >= last_len:
#            last_len = len(comb)
#            comb_choice = comb
                 
    for digit in comb_choice:
        tiles.remove(digit)
    return tiles
    
    
def calculate_score(box):
    score = 0
    
    idx = range(len(box)-1, -1, -1)        #"assemble" leftover digits and compose score		
    for i in range(len(box)-1, -1, -1):        
        score = score + box[idx[i]]*10**i
    
    #score = sum(box)	#or sum the leftover digits (different score calculation variant)
    
    return score   
    
for rep in range(0, repetitions):    
    box = box_start[:]
    o = True

    while o:
        if sum(box) > 6:
            dice_result = roll_dice(2)
        else:
            dice_result = roll_dice(1)

        combinations = [seq for i in range(len(box), 0, -1) for seq in itertools.combinations(box, i) if sum(seq) == dice_result]

        if combinations:
            box = flip_tiles(box, combinations)
        else:
            score_list.append(calculate_score(box))
            o = False

prob_shutting = score_list.count(0)*100/len(score_list)
print("Box shut %.2f percent of the time" % prob_shutting)

average_score = sum(score_list)/len(score_list)
print("Average score was %d" % average_score)