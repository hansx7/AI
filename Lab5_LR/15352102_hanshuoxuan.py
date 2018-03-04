import numpy as np
import csv
import string
import math

train_set = csv.reader(open('train.csv'))
col = 40
ts = np.array([[0 for i in range(0, col+1)]])
label = np.array([-1])
for i in train_set:
	temp = [1]
	for j in range(0, col):
		temp.append(string.atof(i[j]))
	label = np.row_stack((label, [string.atoi(i[col])]))
	ts = np.row_stack((ts, temp))
ts = np.delete(ts, 0, axis = 0)
label = np.delete(label, 0, axis = 0)
row = len(ts)
col += 1

w = np.random.rand(1, col)[0] #初始化w
eta = 0.01                  #初始化eta
l = 0
for iteration in range(0, 1000):
	s = np.zeros(col, dtype = np.float)  #训练集的梯度
	l_old = l
	l = 0                                #代价函数的和
	for i in range(0, row - 1000):
		z = np.dot(ts[i], w)           #每个文本和w点乘
		if z > 700:
			p = 1                      #防止超出乘方上限
		else:                        #不超上限就算logit函数
			p = math.pow(math.e, z) / (1 + math.pow(math.e, z))
		t = p - label[i]
		s += eta * t * ts[i]                 #累加梯度，下一行是累加代价函数
		if (p == 0) or (p == 1):
			l += 0
		else:           
			l += (-math.log(p, math.e)*label[i]-math.log(1-p, math.e)*(1-label[i]))
	if (max(s) == 0) and (min(s) == 0): #梯度为0，跳出循环
		break;
	w -= s  #更新w
	if abs(l - l_old) < 0.05:     #代价函数下降缓慢，表示接近最优值了，减小学习率
		eta = 0.001

nt = 0
for i in range(row - 1000, row):
	z = np.dot(ts[i], w)
	if z > 700:
		t = 1
	else:
		t = math.pow(math.e, z) / (1 + math.pow(math.e, z))
	if t > 0.5:
		if label[i] == 1:
			nt += 1
	else:
		if label[i] == 0:
			nt += 1
print nt*1.0/1000

test_set = csv.reader(open('test.csv'))
res = file('res.csv','wb')
writer = csv.writer(res)
for i in test_set:
	temp = [1]
	for j in i:
		if j == '?':
			break
		temp.append(string.atof(j))
	r = np.dot(w, temp)
	if r > 0.5:
		writer.writerow([1])
	else:
		writer.writerow([0])
