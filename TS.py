import random
import numpy as np
import math


# Distance matrix between two cities
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


# Distance corresponding to all paths
def calculate_path_distance(distance_matrix, path_candidate):
    distance_list = []
    for path in path_candidate:
        dist = 0
        for via in range(city_num - 1):
            dist = distance_matrix[path[via]][path[via + 1]] + dist
        dist = distance_matrix[path[city_num - 1]][path[0]] + dist
        distance_list.append(dist)
    print(min(distance_list))
    return distance_list


# All domain solutions corresponding to the current optimal path
def geberate_neighbor_path(path_best):
    path_new = []
    for front in range(0, city_num - 1):
        for end in range(front + 1, city_num):
            path = path_best.copy()
            path[front], path[end] = path[end], path[front]
            path_new.append(path)
    return path_new


# Setting
city_num = 48  # Total number of cities
city_loc = np.loadtxt('city_location.txt')  # List of city coordinates
iter_num = 100  # Iteration number
table_len = 20  # Tabu table length
tabu_table = []

# Path Initialization
distance_matrix = calculate_distance_matrix()
path_init = []
sequence_init = list(range(city_num))
random.shuffle(sequence_init)
path_init.append(sequence_init)
tabu_table.append(sequence_init)

# Initial Path Length
dist_list = calculate_path_distance(distance_matrix, path_init)
dist_best = min(dist_list)  # 最短距离
path_best = path_init[dist_list.index(dist_best)]  # 对应的最短路径方案
print(path_init)

# Initial Expectation
expect_dist = dist_best
expect_best = path_best

for iter in range(iter_num):  # 迭代
    path_new = geberate_neighbor_path(path_best)  # 寻找全领域新解
    dist_new = calculate_path_distance(distance_matrix, path_new)  # 寻找全领域新解
    dist_best = min(dist_new)  # 最短距离
    path_best = path_new[dist_new.index(dist_best)]  # 对应的最短路径方案
    # 选择路径
    if dist_best < expect_dist:  # 最短的<期望
        expect_dist = dist_best
        expect_best = path_best  # 更新两个期望
        if path_best in tabu_table:
            tabu_table.remove(path_best)
            tabu_table.append(path_best)
        else:
            tabu_table.append(path_best)
    else:  # 最短的还是不能改善期望
        if path_best in tabu_table:  # 在禁忌表里
            dist_new.remove(dist_best)
            path_new.remove(path_best)
            dist_best = min(dist_new)  # 求不在禁忌表中的最短距离
            path_best = path_new[dist_new.index(dist_best)]  # 对应的最短路径方案
            tabu_table.append(path_best)
        else:  # 不在禁忌表
            tabu_table.append(path_best)
    if len(tabu_table) >= table_len:
        del tabu_table[0]

print('Initial path:', sequence_init)
print('Shortest distance:', expect_dist)
print('Shortest path:', expect_best)
