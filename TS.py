import random
import numpy as np
import math


def calculate_distance_matrix():
    distance_matrix = []
    for src in range(city_num):
        distance_each = []
        for dst in range(city_num):
            dist = math.sqrt(
                pow(city_loc[src][1] - city_loc[dst][1], 2) +
                pow(city_loc[src][2] - city_loc[dst][2], 2))
            distance_each.append(dist)
        distance_matrix.append(distance_each)
    # print(distance_matrix)
    return distance_matrix


def calculate_path_distance(distance_matrix, path_candidate):
    distance_list = []
    for path in path_candidate:
        dist = 0
        for via in range(city_num - 1):
            dist = distance_matrix[path[via]][path[via + 1]] + dist
        dist = distance_matrix[path[city_num - 1]][path[0]] + dist
        distance_list.append(dist)
    # print(distance_list)
    min_distance_list = min(distance_list)
    print(min_distance_list)
    return min_distance_list, path_candidate[distance_list.index(min_distance_list)]


# 寻找上一个最优路径对应的所有领域解
def find_newpath(path_best):
    path_new = []
    for front in range(0, city_num - 1):
        for end in range(front + 1, city_num):
            path = path_best.copy()
            path[front], path[end] = path[end], path[front]
            path_new.append(path)
    return path_new


# Settings
city_num = 48  # Total number of cities
city_loc = np.loadtxt('city_location.txt')  # List of city coordinates
iter_num = 100  # Iteration number
table_len = 20  # Tabu table length
tabu_table = []

# Path Initialization
distance_matrix = calculate_distance_matrix()
path_init = []
permutation_init = list(range(city_num))
random.shuffle(permutation_init)
path_init.append(permutation_init)

# 加入禁忌表
tabu_table.append(permutation_init)

# 求初始解的路径长度
dis_list = calculate_path_distance(distance_matrix, path_init)
dis_best = min(dis_list)  # 最短距离
path_best = path_init[dis_list.index(dis_best)]  # 对应的最短路径方案
# print(path_best)

# 初始期望
expect_dis = dis_best
expect_best = path_best
for iter in range(iter_num):  # 迭代
    # 寻找全领域新解
    path_new = find_newpath(path_best)
    # print(path_new)

    # 求出所有新解的路径长度
    dis_new = calculate_path_distance(distance_matrix, path_new)
    # print(dis_new)

    # 选择路径
    dis_best = min(dis_new)  # 最短距离
    path_best = path_new[dis_new.index(dis_best)]  # 对应的最短路径方案
    if dis_best < expect_dis:  # 最短的<期望
        expect_dis = dis_best
        expect_best = path_best  # 更新两个期望
        if path_best in tabu_table:
            tabu_table.remove(path_best)
            tabu_table.append(path_best)
        else:
            tabu_table.append(path_best)
    else:  # 最短的还是不能改善期望
        if path_best in tabu_table:  # 在禁忌表里
            dis_new.remove(dis_best)
            path_new.remove(path_best)
            dis_best = min(dis_new)  # 求不在禁忌表中的最短距离
            path_best = path_new[dis_new.index(dis_best)]  # 对应的最短路径方案
            tabu_table.append(path_best)
        else:  # 不在禁忌表
            tabu_table.append(path_best)
    if len(tabu_table) >= table_len:
        del tabu_table[0]

print('Initial path:', permutation_init)
print('Shortest distance:', expect_dis)
print('Shortest path:', expect_best)
