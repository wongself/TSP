import csv
import random
import numpy as np
import math
import matplotlib.pyplot as plt
import time


# distance matrix between two cities
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
    save_distance_matrix_as_csv(distance_matrix)
    return distance_matrix


# save distance matrix as csv
def save_distance_matrix_as_csv(distance_matrix):
    with open('data/distance matrix.csv', 'w', newline='') as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerow(['src/dst'] + list(range(1, city_num + 1)))
        for i in range(city_num):
            writer.writerow([i + 1] + distance_matrix[i])


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
def generate_neighbor_path(path_best):
    path_new = []
    for i in range(neigh_max):
        exchange = random.sample(range(len(path_best)), 2)
        path = path_best.copy()
        path[exchange[0]] = path_best[exchange[1]]
        path[exchange[1]] = path_best[exchange[0]]
        if path not in path_new:
            path_new.append(path)
    return path_new


# Setting
city_num = 48  # total number of cities
city_loc = np.loadtxt('city_location.txt')  # list of city coordinates
neigh_max = 50  # neighbor max number
iter_num = 300  # iteration number
table_len = 200  # tabu table length
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

# Initial Expectation
expect_dist = dist_best
expect_path = path_best
dist_curr = [dist_best]
iter_curr = 0

time_start = time.time()

for iter in range(iter_num):  # 迭代
    path_new = generate_neighbor_path(path_best)  # 寻找全领域新解
    dist_new = calculate_path_distance(distance_matrix, path_new)  # 寻找全领域新解
    dist_best = min(dist_new)  # 最短距离
    path_best = path_new[dist_new.index(dist_best)]  # 对应的最短路径方案
    dist_curr.append(dist_best)
    # 选择路径
    if dist_best < expect_dist:  # 最短的<期望
        expect_dist = dist_best
        expect_path = path_best  # 更新两个期望
        if path_best in tabu_table:
            tabu_table.remove(path_best)
            tabu_table.append(path_best)
        else:
            tabu_table.append(path_best)
        iter_curr = iter + 1
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

time_end = time.time()

print('Time:', time_end - time_start)
print('Initial path:', sequence_init)
print('Shortest distance:', expect_dist)
print('Shortest path:', expect_path)
print('Iter of best path:', iter_curr)

path_location_x = []
path_location_y = []

for i in range(city_num):
    path_location_x.append(city_loc[expect_path[i]][1])
    path_location_y.append(city_loc[expect_path[i]][2])

path_location_x.append(city_loc[expect_path[0]][1])
path_location_y.append(city_loc[expect_path[0]][2])

time_curr = time.strftime('%Y-%m-%d %H.%M.%S')

with open('data/' + time_curr + ' ' + ('%.2f' % expect_dist) + '.txt',
          'w') as f:
    f.write('Time: ' + str(time_end - time_start) + '\nInitial path: ' +
            str(sequence_init) + '\nShortest distance: ' + str(expect_dist) +
            '\nShortest path: ' + str(expect_path) + '\nIter of best path: ' +
            str(iter_curr) + '\n')

plt.figure(figsize=(18, 6))
plot_location = plt.subplot(1, 2, 1)
plt.plot(path_location_x, path_location_y, marker='o', ms=8, mec='r', mfc='r')
plt.title('Path detail')
plt.xlabel('x')
plt.ylabel('y')
plot_iteration = plt.subplot(1, 2, 2)
plt.plot(range(len(dist_curr)), dist_curr)
plt.title('Path cost')
plt.xlabel('iteration')
plt.ylabel('cost')
plt.savefig('data/' + time_curr + ' ' + ('%.2f' % expect_dist) + '.png')
plt.show()
