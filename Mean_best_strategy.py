import random
from collections import Counter
import itertools

box_start = [1, 2, 3, 4, 5, 6, 7, 8, 9]
die = [1, 2, 3, 4, 5, 6]
repetitions = 1
score_list = []
    
def roll_dice(numdice):
    tot = 0;
    for n in range(numdice):
        tot = tot + random.choice(die)
    return tot;

def all_results(numdice):
    list2 = []
    if numdice == 1:
        for i in die:
            result = [i]
            list2.append(result)
    else:
        result = []
        list1 = all_results(numdice-1)
        for i in die:
            for partial in list1:
                for j in partial:
                    result.append(i)
                    result.append(j)
                    list2.append(result)
                    result = []
    return list2

def results_prob(numdice):
    results = []
    results_probab=[]
    for result in range(numdice,len(die)*numdice+1):
        results_probab.append([result,0])
    for result in all_results(numdice):
        dice_result = sum(result)
        result_probab = results_probab[dice_result-numdice]
        result_probab[1] = result_probab[1] + 1
    for re_pr in results_probab:
        re_pr[1] = re_pr[1]/(len(die)**numdice)
    return results_probab
        

def flip_tiles(tiles, comb_choice):
    tiles_after = [a for a in tiles]
    for digit in comb_choice:
        tiles_after.remove(digit)
    return tiles_after

def calculate_score(box):
    score = 0
    
    idx = range(len(box)-1, -1, -1)        #"assemble" leftover digits and compose score		
    for i in range(len(box)-1, -1, -1):        
        score = score + box[idx[i]]*10**i
    
    #score = sum(box)	#or sum the leftover digits (different score calculation variant)
    
    return score

def mean_before_roll(tiles):
    if tiles == []:
        return 0
    mean = 0
    cont = 0
    if sum(tiles)>6:
        numdice = 2
    else:
        numdice = 1
    for result_prob in r_p[numdice-1]:
        mean = mean + result_prob[1] * mean_after_roll(tiles,result_prob[0])
        if tiles == box_start:
            cont = cont + 1
            perc = 100/len(r_p[numdice-1])*cont
            print("%.0f%%" % perc)
    return mean

def mean_after_roll(tiles,dice_result):
    mean = calculate_score(tiles)
    if dice_result > sum(tiles):
        return mean
    else:
        combinations = [seq for i in range(len(tiles), 0, -1) for seq in itertools.combinations(tiles, i) if sum(seq) == dice_result]
        if combinations == []:
            return mean
        else:
            for comb_choice in combinations:
                tiles_after = flip_tiles(tiles, comb_choice)
                mean_choice = mean_before_roll(tiles_after)
                if mean_choice < mean:
                    mean = mean_choice
        return mean

def prob_before_roll(tiles):
    if tiles == []:
        return 1
    prob = 0
    cont = 0
    if sum(tiles)>6:
        numdice = 2
    else:
        numdice = 1
    for result_prob in r_p[numdice-1]:
#        if tiles == box_start:
#            cont = cont + 1
#            perc = 100/len(r_p[numdice-1])*cont
#            print("%.0f%%" % perc)
        prob = prob + result_prob[1] * prob_after_roll(tiles,result_prob[0])
    return prob

def prob_after_roll(tiles,dice_result):
    proba = 0
    if dice_result > sum(tiles):
        return 0
    else:
        combinations = [seq for i in range(len(tiles), 0, -1) for seq in itertools.combinations(tiles, i) if sum(seq) == dice_result]
        if combinations == []:
            return 0
        else:
            for comb_choice in combinations:
                tiles_after = flip_tiles(tiles, comb_choice)
                prob_choice = prob_before_roll(tiles_after)
                if prob_choice > proba:
                    proba = prob_choice
            return proba

def greater_than(a,b):
    if a == []:
        return False
    else:
        if b == []:
            return True
    a1 = [i for i in a]
    b1 = [i for i in b]
    ma = max(a1)
    mb = max(b1)
    if ma > mb:
        return True
    if ma == mb:
        a1.remove(ma)
        b1.remove(mb)
        return greater_than(a1,b1)
    else:
        return False
    

def choose_and_flip(tiles, dice_result):
#    return choose_and_flip_best_prob(tiles, dice_result)
    return choose_and_flip_best_mean(tiles, dice_result)

#    last_min = 0
#    last_max = 0
#    last_len = 9
#    comb_choice = []
#    combinations = [seq for i in range(len(tiles), 0, -1) for seq in itertools.combinations(tiles, i) if sum(seq) == dice_result]
#    if combinations == []:
#        return [tiles,[]]
#    for comb in combinations:

#choose combination with highest digit
#        if greater_than(comb,comb_choice):   
#            comb_choice = comb

#choose combination whose lowest digit is higher than all the others' lowest digit
#        if min(comb) >= last_min:  
#            last_min = min(comb)
#            comb_choice = comb

#choose combination that minimizes the number of tiles flipped
#and choose the one with higher numbers
#        if len(comb) <= last_len:
#            if len(comb) < last_len:
#                last_len = len(comb)
#                last_min = min(comb)
#                comb_choice = comb
#            else:
#                if min(comb) >= last_min:  
#                    last_min = min(comb)
#                    comb_choice = comb
                    
#    tiles_after = flip_tiles(tiles,comb_choice)
#    return [tiles_after, comb_choice]

def mean_before_roll_fixed_strat(tiles):
    if tiles == []:
        return 0
    mean_tiles = calculate_score(tiles)
    mean = 0
    cont = 0
    if sum(tiles)>6:
        numdice = 2
    else:
        numdice = 1
    for result_prob in r_p[numdice-1]:
        dice_result = result_prob[0]
        move = choose_and_flip(tiles, dice_result)
        if move[1] != []:
            tiles_after = move[0] 
            mean = mean + result_prob[1] * mean_before_roll_fixed_strat(tiles_after)
        else:
            mean = mean + result_prob[1] * mean_tiles
        if tiles == box_start:
            cont = cont + 1
            perc = 100/len(r_p[numdice-1])*cont
            print("%.0f%%" % perc)
    return mean

def prob_before_roll_fixed_strat(tiles):
    if tiles == []:
        return 1
    prob = 0
    cont = 0
    if sum(tiles)>6:
        numdice = 2
    else:
        numdice = 1
    for result_prob in r_p[numdice-1]:
        dice_result = result_prob[0]
        move = choose_and_flip(tiles, dice_result)
        if move[1] != []:
            tiles_after = move[0] 
            prob = prob + result_prob[1] * prob_before_roll_fixed_strat(tiles_after)
        if tiles == box_start:
            cont = cont + 1
            perc = 100/len(r_p[numdice-1])*cont
            print("%.0f%%" % perc)
    return prob

def choose_and_flip_best_prob(tiles, dice_result):
    combinations = [seq for i in range(len(tiles), 0, -1) for seq in itertools.combinations(tiles, i) if sum(seq) == dice_result]
    if combinations == []:
        return [tiles,[]]
    for comb in combinations:
        tiles_after = flip_tiles(tiles,comb)
        if prob_before_roll(tiles_after) == prob_after_roll(tiles, dice_result):
            comb_choice = comb
            return [tiles_after, comb_choice]

def choose_and_flip_best_mean(tiles, dice_result):
    combinations = [seq for i in range(len(tiles), 0, -1) for seq in itertools.combinations(tiles, i) if sum(seq) == dice_result]
    if combinations == []:
        return [tiles,[]]
    for comb in combinations:
        tiles_after = flip_tiles(tiles,comb)
        if mean_before_roll(tiles_after) == mean_after_roll(tiles, dice_result):
            comb_choice = comb
            return [tiles_after, comb_choice]


r_p = [0,0]
r_p[0] = results_prob(1)
r_p[1] = results_prob(2)

#average = mean_before_roll(box_start)
#print("Minimum average score=", average)
#average_fixed = mean_before_roll_fixed_strat(box_start)
#print("Average score with chosen strategy=", average_fixed)
prob_fixed = prob_before_roll_fixed_strat(box_start)*100
print("Probability of shutting the box using the best strategy for minimum average score: %.2f%%" % prob_fixed)

