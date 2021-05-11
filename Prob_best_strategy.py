import os
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
    return results_probab
        

def flip_tiles(tiles, comb_choice):
    tiles_after = [a for a in tiles]
    for digit in comb_choice:
        tiles_after.remove(digit)
    return tiles_after

def prob_before_roll(tiles, numdice):
    if tiles == []:
        return 1
    prob = 0
    cont = 0
    for result_prob in r_p[numdice-1]:
        if tiles == box_start:
            cont = cont + 1
            perc = 100/len(r_p[numdice-1])*cont
            print("%.0f%%" % perc)
        if sum(tiles) - result_prob[0] > 6:
            prob = prob + result_prob[1] * prob_after_roll(tiles,result_prob[0], 2)/(len(die)**numdice)
        else:
            prob = prob + result_prob[1] * prob_after_roll(tiles,result_prob[0], 1)/(len(die)**numdice)
    return prob

def prob_after_roll(tiles,dice_result,num_dice):
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
                prob_choice = prob_before_roll(tiles_after, num_dice)
                if prob_choice > proba:
                    proba = prob_choice
            return proba

r_p = [0,0]
r_p[0] = results_prob(1)
r_p[1] = results_prob(2)
prob_shutting = prob_before_roll(box_start,2)*100
print("Box shut with probability %.2f%%." % prob_shutting)
