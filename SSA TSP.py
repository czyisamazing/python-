# -*- coding: utf-8 -*-
"""
Created on Fri Jan 29 21:41:56 2021

@author: asus
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import xlrd
import re

def Dis(x,y):
    d = ((x[1]-y[1])**2+(x[2]-y[2])**2)**0.5
    return d

def dis(x):
    d = 0
    for i in range(0,99):
        d += ((x[i][1]-x[i+1][1])**2+(x[i][2]-x[i+1][2])**2)**0.5
    return d

def swap(x,i,j):
    x[i],x[j] = x[j],x[i]
    return x
#产生新解
def new_solution(x):
    ra = np.random.randint(1,100,2)
    x = swap(x,ra[0],ra[1])
    return x

def SSA_P(x,y,t):
    d = np.exp((x-y)/t)
    return d

#def new_solution()



with open("jwsj.txt","r") as f:
    data = f.read()
data = re.split('\t|\n',data)
x_j = []
y_w = []
data_new=[]

for i in range(0,len(data)-1):
    x_j.append(float(data[i].split(' ')[0]))
    y_w.append(float(data[i].split(' ')[-1]))

x_j = np.array(x_j)
y_w = np.array(y_w)

x_j = x_j-x_j[0]
y_w = y_w-y_w[0]

#plt.scatter(x_j,y_w,marker = 'o')

for i in range(0,x_j.shape[0]):
    data_new.append([i,x_j[i],y_w[i]])

#随机产生初始解
flag = 0
while flag==0:
    rarray = np.random.randint(1,100,2) #产生两个随机整数
    if rarray[0] != rarray[1]:
        flag += 1

#贪心算法找初始解
#开始就是从出发点开始
sum_dis = 0
tudo = [0 for i in range(0,100)]
start_dot = 0
for j in range(0,99):
    min_R = 1000000
    for i in range(0,100):
        record_i = 0
        if Dis(data_new[start_dot],data_new[i]) < min_R:
            if i not in tudo:
                min_R = Dis(data_new[start_dot],data_new[i])
                # print(min_R)
                record_i = i
                #print(record_i)
                tudo[j+1] = record_i
    start_dot = tudo[j+1]
    sum_dis += min_R

print(sum_dis)

data_0 = []
for i in tudo:
    data_0.append(data_new[i])

#初始数据确定
#初始解
data_0 = np.array(data_0)

T_0 = 100 #初始温度
T = T_0

alpha = 0.95 #降温系数

t = pow(10,-3) #最低温度

cell_c = 100 #每层循环100次

record_path = [0 for i in range (0,100)] #记录路径

Min_y = [] #记录最短路径 y 

start_dis = dis(data_0)

print(start_dis)

while T>t:
    min_y=[]
    for i in range(0,cell_c):
        min_y.append(dis(data_0))
        start_dis = dis(data_0)
        ra = np.random.randint(1,100,2)
        data_N = data_0
        data_N[ra[0]],data_N[ra[1]] = data_N[ra[1]],data_N[ra[0]]
        rand = np.random.rand()
        cr_dis = dis(data_N)
        if cr_dis < start_dis:
            data_0 = data_N 
        else:
            if SSA_P(start_dis,cr_dis,T) >= rand:
                data_0 = data_N
    for j in range(0,100):
        record_path[j] = data_0[j][0]
    print(record_path)
    T = alpha*T
    Min_y.append(min(min_y))
print(Min_y)
print(record_path)
#解不稳定，初始解寻找的不好，新解创立的不好