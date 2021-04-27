import random
import numpy as np
import math

city_num = 48  # Total number of cities
city_loc = np.loadtxt('city_location.txt')  # List of city coordinates
table_len = 15  # 禁忌表长度
taboo_table = []


def calculate_distance_matrix():
    distance_matrix = []
    for src in range(city_num):
        distance_each = []
        for dst in range(city_num):
            dis = math.sqrt(
                pow(city_loc[src][1] - city_loc[dst][1], 2) +
                pow(city_loc[src][2] - city_loc[dst][2], 2))
            distance_each.append(dis)
        distance_matrix.append(distance_each)
    # print(distance_matrix)
    return distance_matrix


# 计算所有路径对应的距离
def calculate_path_distance(distance_matrix, path_new):
    dis_list = []
    for each in path_new:
        dis = 0
        for j in range(city_num - 1):
            dis = distance_matrix[each[j]][each[j + 1]] + dis
        dis = distance_matrix[each[29]][each[0]] + dis  # 回家
        dis_list.append(dis)
    return dis_list


# 寻找上一个最优路径对应的所有领域解
def find_newpath(path_best):
    path_new = []
    for i in range(1, city_num - 1):
        for j in range(i + 1, city_num):
            path = path_best.copy()
            path[i], path[j] = path[j], path[i]
            path_new.append(path)
    return path_new


# ==========================================
# 点对点距离矩阵
distance_matrix = calculate_distance_matrix()

# 设置初始解
path_initial = []
initial = list(range(city_num))
random.shuffle(initial)
path_initial.append(initial)
print(path_initial)

# 加入禁忌表
taboo_table.append(initial)

# 求初始解的路径长度
dis_list = calculate_path_distance(distance_matrix, path_initial)
dis_best = min(dis_list)  # 最短距离
path_best = path_initial[dis_list.index(dis_best)]  # 对应的最短路径方案
# print(path_best)

# 初始期望
expect_dis = dis_best
expect_best = path_best
for iter in range(5000):  # 迭代
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
        if path_best in taboo_table:
            taboo_table.remove(path_best)
            taboo_table.append(path_best)
        else:
            taboo_table.append(path_best)
    else:  # 最短的还是不能改善期望
        if path_best in taboo_table:  # 在禁忌表里
            dis_new.remove(dis_best)
            path_new.remove(path_best)
            dis_best = min(dis_new)  # 求不在禁忌表中的最短距离
            path_best = path_new[dis_new.index(dis_best)]  # 对应的最短路径方案
            taboo_table.append(path_best)
        else:  # 不在禁忌表
            taboo_table.append(path_best)
    if len(taboo_table) >= table_len:
        del taboo_table[0]

print('最短距离', expect_dis)
print('最短路径：', expect_best)
