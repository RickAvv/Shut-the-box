import random
from collections import Counter
import itertools
import numpy as np

table_shut = np.load("table_shut.npy", allow_pickle=True)
table_mean = np.load("table_mean.npy", allow_pickle=True)

box_start = [1, 2, 3, 4, 5, 6, 7, 8, 9]
die = [1, 2, 3, 4, 5, 6]
repetitions = 100000
games_match = 5
win_list = []

all_comb = [seq for i in range(len(box_start), 0, -1) for seq in itertools.combinations(box_start, i)]

def progress(percent=0, width=30):
    left = width * percent // 100
    right = width - left
    print('\r[', '#' * left, ' ' * right, ']',
          f' {percent:.0f}%',
          sep='', end='', flush=True)

def roll_dice(numdice):
    tot = 0;
    for n in range(numdice):
        tot = tot + random.choice(die)
    return tot;

def flip_tiles(tiles, comb_choice):
    for digit in comb_choice:
        tiles.remove(digit)
    return tiles
    
def calculate_score(box):
    score = 0
    idx = range(len(box)-1, -1, -1)
    for i in range(len(box)-1, -1, -1):        
        score = score + box[idx[i]]*10**i
    return score   
    

    
for rep in range(0, repetitions):    
    progress(round(rep*100/repetitions))
    
    p1_score = 0
    p2_score = 0
    
    for game in range(0, games_match):
        box1 = box_start[:]
        box2 = box_start[:]        
        o1 = True
        o2 = True
        
        while o1:          
            if sum(box1) > 6:
                dice_result = roll_dice(2)
            else:
                dice_result = roll_dice(1)

            comb_choice = table_shut[all_comb.index(tuple(box1))][dice_result]

            if comb_choice:
                box1 = flip_tiles(box1, comb_choice)
            if not comb_choice or not box1:
                round_score = calculate_score(box1)
                if round_score > 0:
                    p1_score = p1_score + round_score
                else:
                    p1_score = 0
                o1 = False
                

        while o2:
            if sum(box2) > 6:
                dice_result = roll_dice(2)
            else:
                dice_result = roll_dice(1)

            comb_choice = table_mean[all_comb.index(tuple(box2))][dice_result]

            if comb_choice:
                box2 = flip_tiles(box2, comb_choice)
            if not comb_choice or not box2:
                round_score = calculate_score(box2)
                if round_score > 0:
                    p2_score = p2_score + round_score
                else:
                    p2_score = 0
                o2 = False

    if p1_score < p2_score:
        win_list.append(1)
    elif p1_score > p2_score:
        win_list.append(2)
    else:
        win_list.append(0)

p1_win = win_list.count(1)
p1_winrate = p1_win*100/len(win_list)
p2_win = win_list.count(2)
p2_winrate = p2_win*100/len(win_list)
ties = win_list.count(0)
tie_rate = ties*100/len(win_list)
print("Player 1 wins %.2f percent of the time" % p1_winrate)
print("Player 2 wins %.2f percent of the time" % p2_winrate)
print("Players tie %.2f percent of the time" % tie_rate)