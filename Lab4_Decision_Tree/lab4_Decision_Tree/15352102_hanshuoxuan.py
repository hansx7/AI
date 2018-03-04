import string
import csv
import math

def id3(ds, choices):
	global col

	hd = 0
	t = 0
	f = 0
	for i in ds:
		if i[col - 1] == 1:
			t += 1
		else:
			f += 1
	if t == 0:
		tt = 0
	else:
		tt = t * 1.0 / len(ds)
		tt = -tt * math.log(tt, 2)
	if f == 0:
		ff = 0
	else:
		ff = f * 1.0 / len(ds)
		ff = -ff * math.log(ff, 2)
	hd = tt + ff

	max_ig = 0
	max_col = -1
	for p in range(0, col - 1):
		if choices[p] == 0:
			continue
		a = set()
		b = {}
		c = {}
		for i in ds:
			a.add(i[p])
		for i in a:
			b[i] = 0
			c[i] = 0
		for i in ds:
			b[i[p]] += 1
			if i[col - 1] == -1:
				c[i[p]] += 1

		ig = 0
		for i in a:
			temp = b[i] * 1.0 / len(ds)
			if c[i] > 0:
				t = c[i] * 1.0 / b[i]
			else:
				t = 0
			if b[i] - c[i] > 0:
				f = (b[i] - c[i]) * 1.0 / b[i]
			else:
				f = 0
			if t > 0:
				tt = -t * math.log(t, 2)
			else:
				tt = 0
			if f > 0:
				ff = -f * math.log(f, 2)
			else:
				ff = 0
			temp *= (tt + ff)
			ig += temp
		gain = hd - ig

		if gain > max_ig:
			max_ig = gain
			max_col = p
	return max_col

def c45(ds, choices):
	global col

	hd = 0
	t = 0
	f = 0
	for i in ds:
		if i[col - 1] == 1:
			t += 1
		else:
			f += 1
	if t == 0:
		tt = 0
	else:
		tt = t * 1.0 / len(ds)
		tt = -tt * math.log(tt, 2)
	if f == 0:
		ff = 0
	else:
		ff = f * 1.0 / len(ds)
		ff = -ff * math.log(ff, 2)
	hd = tt + ff

	max_rt = 0
	max_col = -1
	for p in range(0, col - 1):
		if choices[p] == 0:
			continue
		a = set()
		b = {}
		c = {}
		for i in ds:
			a.add(i[p])
		for i in a:
			b[i] = 0
			c[i] = 0
		for i in ds:
			b[i[p]] += 1
			if i[col - 1] == -1:
				c[i[p]] += 1
		
		splitinfo = 0
		for i in b:
			if b[i] == 0:
				continue
			temp = b[i] * 1.0 / len(ds)
			temp = -temp * math.log(temp, 2)
			splitinfo += temp

		ig = 0
		for i in a:
			temp = b[i] * 1.0 / len(ds)
			if c[i] > 0:
				t = c[i] * 1.0 / b[i]
			else:
				t = 0
			if b[i] - c[i] > 0:
				f = (b[i] - c[i]) * 1.0 / b[i]
			else:
				f = 0
			if t > 0:
				tt = -t * math.log(t, 2)
			else:
				tt = 0
			if f > 0:
				ff = -f * math.log(f, 2)
			else:
				ff = 0
			temp *= (tt + ff)
			ig += temp
		gain = hd - ig
		if gain == 0:
			rt = 0
		else:
			rt = gain * 1.0 / splitinfo
		if rt > max_rt:
			max_rt = rt
			max_col = p
	return max_col

def cart(ds, choices):
	global col
	
	min_gini = 100
	min_col = -1
	for i in range(0, col - 1):
		if choices[i] == 0:
			continue
		t = 0
		f = 0
		a = set()
		b = {}
		c = {}
		gini = 0
		for j in ds:
			a.add(j[i])
		for j in a:
			b[j] = 0
			c[j] = 0
		for j in ds:
			b[j[i]] += 1
			if j[col - 1] == 1:
				c[j[i]] += 1
		for j in a:
			gini += b[j] * 1.0 / len(ds) * (1 - (c[j]*1.0/b[j]) * (c[j]*1.0/b[j]) - (b[j]-c[j])*1.0/b[j] * (b[j]-c[j])*1.0/b[j])
		if gini < min_gini:
			min_gini = gini
			min_col = i
		# print i, gini
	return min_col

def decision_tree(tree, data_set, choices):
	global col

	flag = 1
	for i in data_set:
		if i[col - 1] != 1:
			flag = 0
			break
	if flag == 1:
		return 1
		flag = -1
	for i in data_set:
		if i[col - 1] != -1:
			flag = 0
			break
	if flag == -1:
		return -1

	if max(choices) == 0:
		t = 0
		f = 0
		for i in data_set:
			if i[col - 1] == 1:
				t += 1
			else:
				f += 1
		if t > f:
			return 1
		else:
			return -1

	for i in range(0, col - 1):
		if choices[i] == 0:
			continue
		t = 0
		f = 0
		for j in data_set:
			if j[col - 1] == 1:
				t += 1
			else:
				f += 1
		if t == 0:
			return -1
		if f == 0:
			return 1
	
	# choice = id3(data_set, choices)
	choice = c45(data_set, choices)
	# choice = cart(data_set, choices)

	tree['col'] = choice
	choices[choice] = 0
	a = set()
	b = {}
	for i in data_set:
		a.add(i[choice])
	for i in a:
		b[i] = []
	for i in data_set:
		b[i[choice]].append(i)
	
	for i in b:
		if len(b[i]) == 0:
			tree[i] = 1
		else:
			tree[i] = decision_tree({}, b[i], choices)

	choices[choice] = 1
	return tree

def calc(tree, data):
	chose = data[tree['col']]
	if tree.has_key(chose):
		val = tree[chose]
	else:
		return 1

	if val == 1:
		return 1
	elif val == -1:
		return -1
	else:
		return calc(val, data)
	return 1

train_set = csv.reader(open('train.csv'))
ts = []
i = 0
for row in train_set:
	ts.append([])
	for j in range(0, len(row)):
		ts[i].append(string.atoi(row[j]))
	i += 1
col = len(row)
t_row = i

start = 250
length = 150
vs = [[] for i in range(0,length)]
for i in range(start, start + length):
	vs[i - start] = ts[i]
for i in range(start, start + length):
	del ts[start]
	t_row -= 1
v_row = len(vs)

remain = [1 for i in range(0, col - 1)]
root = {}
root = decision_tree(root, ts, remain)
for i in root:
	print i, root[i]

r = 0
for i in vs:
	if i[col - 1] == calc(root, i):
		r += 1
print r * 1.0 / len(vs)

test_set = csv.reader(open('test.csv'))
ts2 = []
i = 0
for row in test_set:
	ts2.append([])
	for j in range(0, len(row) - 1):
		ts2[i].append(string.atoi(row[j]))
	i += 1
res = file('res.csv','wb')
writer = csv.writer(res)
for i in ts2:
	v = calc(root, i)
	writer.writerow([v])
