import numpy as np
import sys
from itertools import permutations

#plan = np.array([[40, 30, 35],[90, 110, 95],[395, 385, 270],[440, 470, 630],[620, 740, 630],[850, 800, 920],[1000, 1170, 980],[1080, 1150, 1040]])


data = []
for line in sys.stdin:
    data.append(line)
tot_inv = 7
plan = []
for i in range(len(data)):
    plan.append(data[i].split('\t'))
corp = len(plan[0])
years_of_inv = len(plan)


sum_plan = np.zeros((years_of_inv, corp))
investments = np.empty((years_of_inv, corp), dtype='object')

for j in range(sum_plan.shape[1]):
    for i in range(sum_plan.shape[0]):
        plan[i][j] = int(plan[i][j])


for j in range(sum_plan.shape[1]):
    for i in range(min(tot_inv+1, years_of_inv)):
        lst = [1 if idx < i else 0 for idx in range(years_of_inv-1)]
        combs = set(permutations(lst))
        max = 0
        for comb in combs:
            sum = 0
            num_inv = 0
            for idx in range(years_of_inv-1):
                sum += plan[num_inv][j]
                if comb[idx] == 1:
                    num_inv += 1
            sum += plan[num_inv][j]
            if max < sum:
                max = sum
                comb_new = comb
        comb_new = ''.join([str(num) for num in comb_new])
        sum_plan[i, j] = max
        investments[i, j] = comb_new


dict_sum = {i: [0, ''] for i in range(tot_inv+1)}


for step in range(sum_plan.shape[1]):
    add_dict = {}
    for key in dict_sum.keys():
        for inv in range(sum_plan.shape[0]):
            new_key = key + inv
            if new_key > tot_inv:
                continue
            new_value = dict_sum[key][0] + sum_plan[inv, step]
            if (new_key not in add_dict.keys() or new_value > add_dict[new_key][0]) and new_value > dict_sum[new_key][0]:
                new_str = dict_sum[key][1] + investments[inv, step]
                add_dict.update({new_key: [new_value, new_str]})
    dict_sum.update(add_dict)


investments = [[int(sym) for sym in dict_sum[tot_inv][1][i:i+(len(dict_sum[tot_inv][1])//corp)]] for i in range(0, len(dict_sum[tot_inv][1]), len(dict_sum[tot_inv][1])//corp)]


with open('output.txt', 'w') as file:
    file.write('{0}\n'.format(dict_sum[tot_inv][0]))
    for j in range(len(investments[0])):
        for i in range(len(investments)):
            file.write('{0}\t'.format(investments[i][j]))
        file.write('\n')

