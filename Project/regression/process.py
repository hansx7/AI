import csv
import string
import numpy as np
import math
import random

def is_number(s):
	try:
		float(s)
		return True
	except Exception as e:
		return False

def is_equal(p, q):
	if math.fabs(p - q) <= 0.0001:
		return True
	else:
		return False

def number_of_the_day(y, m, d):
	days_in_a_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
	days = 0
	if y == 2012:
		days += 365
		days_in_a_month[1] = 29
	for mm in range(0, m-1):
		days += days_in_a_month[mm]
	days += d
	return days

train_set = csv.reader(open('train.csv'))
ts = np.array([0 for i in range(0, 9)])
trow = 0
one_month = np.array([0 for i in range(0, 9)])
miss = []
last_month = 0
this_month = 0
label = np.array([])

for i in train_set:
	if is_number(i[0]) == False:
		continue
	if string.atoi(i[0]) == 0:
		days = this_month - last_month - 1
		for j in miss:
			ts[j[0]][j[1]] = one_month[j[1]] * 1.0 / days
		one_month = [0 for o in range(0, 9)]
		last_month = this_month
		miss = []
		continue

	temp = np.array([])
	s = i[1].split('/')
	year = string.atoi(s[0])
	month = string.atoi(s[1])
	day = string.atoi(s[2])
	if year == 2011 or year == 2012:
		temp = np.hstack((temp, [year-2011]))
	else:
		continue
	if month >= 1 and month <= 12:
		temp = np.hstack((temp, [month]))
	else:
		continue
	if day >= 1 and day <= 31:
		temp = np.hstack((temp, [day]))
	else:
		continue

	for j in range(3, 9):
		if is_number(i[j-1]) == True:
			t = string.atof(i[j-1])
			temp = np.hstack((temp, [t]))
		else:
			miss.append([trow+1, j])
			temp = np.hstack((temp, [0]))
	label = np.hstack((label, string.atoi(i[8])))
	ts = np.row_stack((ts, temp))
	one_month = one_month + temp
	trow += 1
	this_month += 1
ts = np.delete(ts, 0, axis=0)
res = file('processed_train.csv','wb')
writer = csv.writer(res)
# writer.writerow(['yr','mnth','hr','weathersit','temp','atemp','hum','windspeed','season','holiday','weekday','workingday','cnt'])
holiday = np.array([17, 52, 105, 150, 185, 248, 283, 315, 328, 360, 367, 381, 416, 472, 514, 551, 612, 647, 682, 692, 725])
# holiday = np.array([121, 487, 640, 274, 1, 366, 725, 359])
j=0
for i in ts:
	i = np.hstack(([j+1], i))
	# number of the day in 2011 and 2012
	day = number_of_the_day(int(i[1]), int(i[2]), int(i[3]))

	# add season
	if (day >= 1 and day <= 80) or (day >= 357 and day <=446) or (day >= 723):
		i = np.hstack((i, [4]))
	elif (day >= 81 and day <= 173) or (day >= 447 and day <= 539):
		i = np.hstack((i, [1]))
	elif (day >= 174 and day <= 266) or (day >= 540 and day <= 632):
		i = np.hstack((i, [2]))
	elif (day >= 267 and day <= 356) or (day >= 633 and day <= 722):
		i = np.hstack((i, [3]))
	# add holiday
	if day in holiday:
		i = np.hstack((i, [1]))
		# i = np.hstack((i, [0]))
	else:
		i = np.hstack((i, [0]))
		# i = np.hstack((i, [1]))
	# add workingday and weekday
	wd = (day + 4) % 7 + 1
	i = np.hstack((i, [wd]))
	if wd == 6 or wd == 7:
		# i = np.hstack((i, [1]))
		i = np.hstack((i, [0]))
	else:
		# i = np.hstack((i, [0]))
		i = np.hstack((i, [1]))
	temp = np.hstack((i, label[j]))
	temp = np.delete(temp, 3, axis=0)
	temp[5] /= 41.0
	temp[6] /= 50.0
	temp[7] /= 100.0
	temp[8] /= 67.0
	# temp = np.delete(temp, 8, axis=0)
	temp = np.delete(temp, 0, axis=0) #delete 'instant'
	if is_equal(temp[0], 1):
		temp = np.hstack((temp, [1]))
	else:
		temp = np.hstack((temp, [0]))
	temp = np.delete(temp, 0, axis=0) #delete 'year' and append onehot
	# print temp[0]
	if is_equal(temp[0], 1):
		temp = np.hstack((temp, [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]))
	elif is_equal(temp[0], 2):
		temp = np.hstack((temp, [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]))
	elif is_equal(temp[0], 3):
		temp = np.hstack((temp, [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]))
	elif is_equal(temp[0], 4):
		temp = np.hstack((temp, [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0]))
	elif is_equal(temp[0], 5):
		temp = np.hstack((temp, [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0]))
	elif is_equal(temp[0], 6):
		temp = np.hstack((temp, [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0]))
	elif is_equal(temp[0], 7):
		temp = np.hstack((temp, [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0]))
	elif is_equal(temp[0], 8):
		temp = np.hstack((temp, [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0]))
	elif is_equal(temp[0], 9):
		temp = np.hstack((temp, [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0]))
	elif is_equal(temp[0], 10):
		temp = np.hstack((temp, [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0]))
	elif is_equal(temp[0], 11):
		temp = np.hstack((temp, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0]))
	else:
		temp = np.hstack((temp, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]))
	temp = np.delete(temp, 0, axis=0) #delete 'month' and append onehot
	tem = [0 for f in range(0, 23)]
	tem.insert(int(temp[0]), 1)
	temp = np.hstack((temp, tem))
	temp = np.delete(temp, 0, axis=0) #delete 'hour' and append onehot

	if is_equal(temp[0], 1):
		temp = np.hstack((temp, [1, 0, 0, 0]))
	elif is_equal(temp[0], 2):
		temp = np.hstack((temp, [0, 1, 0, 0]))
	elif is_equal(temp[0], 3):
		temp = np.hstack((temp, [0, 0, 1, 0]))
	else:
		temp = np.hstack((temp, [0, 0, 0, 1]))
	temp = np.delete(temp, 0, axis=0) #delete 'weathersit' and append onehot
	if is_equal(temp[4], 1):
		temp = np.hstack((temp, [1, 0, 0, 0]))
	elif is_equal(temp[4], 2):
		temp = np.hstack((temp, [0, 1, 0, 0]))
	elif is_equal(temp[4], 3):
		temp = np.hstack((temp, [0, 0, 1, 0]))
	else:
		temp = np.hstack((temp, [0, 0, 0, 1]))
	temp = np.delete(temp, 4, axis=0) #delete 'season' and append onehot
	tem = [0 for f in range(0, 6)]
	tem.insert(int(temp[5])-1, 1)
	temp = np.hstack((temp, tem))
	temp = np.delete(temp, 5, axis=0) #delete 'weekday' and append onehot
	temp = np.hstack((temp, [temp[6]]))
	temp = np.delete(temp, 6, axis=0) #move target to the end of the list
	writer.writerow(temp)
	j += 1

test_set = csv.reader(open('test.csv'))
tts = np.array([0 for i in range(0, 9)])
ttrow = 0
label = np.array([])

for i in test_set:
	if is_number(i[0]) == False:
		continue

	temp = np.array([])
	s = i[1].split('/')
	year = string.atoi(s[0])
	month = string.atoi(s[1])
	day = string.atoi(s[2])
	if year == 2011 or year == 2012:
		temp = np.hstack((temp, [year-2011]))
	else:
		continue
	if month >= 1 and month <= 12:
		temp = np.hstack((temp, [month]))
	else:
		continue
	if day >= 1 and day <= 31:
		temp = np.hstack((temp, [day]))
	else:
		continue

	for j in range(3, 9):
		t = string.atof(i[j-1])
		temp = np.hstack((temp, [t]))
	tts = np.row_stack((tts, temp))
	ttrow += 1
tts = np.delete(tts, 0, axis=0)
res = file('processed_test.csv','wb')
writer = csv.writer(res)
# writer.writerow(['yr','mnth','hr','weathersit','temp','atemp','hum','windspeed','season','holiday','weekday','workingday'])
# holiday = np.array([17, 52, 105, 150, 185, 248, 283, 315, 328, 360, 367, 381, 416, 472, 514, 551, 612, 647, 682, 692, 725])
j=0
for i in tts:
	i = np.hstack(([j+1], i))
	# number of the day in 2011 and 2012
	day = number_of_the_day(int(i[1]), int(i[2]), int(i[3]))

	# add season
	if (day >= 1 and day <= 80) or (day >= 357 and day <=446) or (day >= 723):
		i = np.hstack((i, [4]))
	elif (day >= 81 and day <= 173) or (day >= 447 and day <= 539):
		i = np.hstack((i, [1]))
	elif (day >= 174 and day <= 266) or (day >= 540 and day <= 632):
		i = np.hstack((i, [2]))
	elif (day >= 267 and day <= 356) or (day >= 633 and day <= 722):
		i = np.hstack((i, [3]))
	# add holiday
	if day in holiday:
		i = np.hstack((i, [1]))
		# i = np.hstack((i, [0]))
	else:
		i = np.hstack((i, [0]))
		# i = np.hstack((i, [1]))
	# add workingday and weekday
	wd = (day + 4) % 7 + 1
	i = np.hstack((i, [wd]))
	if wd == 6 or wd == 7:
		# i = np.hstack((i, [1]))
		i = np.hstack((i, [0]))
	else:
		# i = np.hstack((i, [0]))
		i = np.hstack((i, [1]))
	temp = np.delete(i, 3, axis=0)
	temp[5] /= 41.0
	temp[6] /= 50.0
	temp[7] /= 100.0
	temp[8] /= 67
	# temp = np.delete(temp, 8, axis=0)
	temp = np.delete(temp, 0, axis=0)
	if is_equal(temp[0], 1):
		temp = np.hstack((temp, [1]))
	else:
		temp = np.hstack((temp, [0]))
	temp = np.delete(temp, 0, axis=0) #delete 'year' and append onehot
	# print temp[0]
	if is_equal(temp[0], 1):
		temp = np.hstack((temp, [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]))
	elif is_equal(temp[0], 2):
		temp = np.hstack((temp, [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]))
	elif is_equal(temp[0], 3):
		temp = np.hstack((temp, [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]))
	elif is_equal(temp[0], 4):
		temp = np.hstack((temp, [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0]))
	elif is_equal(temp[0], 5):
		temp = np.hstack((temp, [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0]))
	elif is_equal(temp[0], 6):
		temp = np.hstack((temp, [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0]))
	elif is_equal(temp[0], 7):
		temp = np.hstack((temp, [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0]))
	elif is_equal(temp[0], 8):
		temp = np.hstack((temp, [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0]))
	elif is_equal(temp[0], 9):
		temp = np.hstack((temp, [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0]))
	elif is_equal(temp[0], 10):
		temp = np.hstack((temp, [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0]))
	elif is_equal(temp[0], 11):
		temp = np.hstack((temp, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0]))
	else:
		temp = np.hstack((temp, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]))
	temp = np.delete(temp, 0, axis=0) #delete 'month' and append onehot
	tem = [0 for f in range(0, 23)]
	tem.insert(int(temp[0]), 1)
	temp = np.hstack((temp, tem))
	temp = np.delete(temp, 0, axis=0) #delete 'hour' and append onehot

	if is_equal(temp[0], 1):
		temp = np.hstack((temp, [1, 0, 0, 0]))
	elif is_equal(temp[0], 2):
		temp = np.hstack((temp, [0, 1, 0, 0]))
	elif is_equal(temp[0], 3):
		temp = np.hstack((temp, [0, 0, 1, 0]))
	else:
		temp = np.hstack((temp, [0, 0, 0, 1]))
	temp = np.delete(temp, 0, axis=0) #delete 'weathersit' and append onehot
	if is_equal(temp[4], 1):
		temp = np.hstack((temp, [1, 0, 0, 0]))
	elif is_equal(temp[4], 2):
		temp = np.hstack((temp, [0, 1, 0, 0]))
	elif is_equal(temp[4], 3):
		temp = np.hstack((temp, [0, 0, 1, 0]))
	else:
		temp = np.hstack((temp, [0, 0, 0, 1]))
	temp = np.delete(temp, 4, axis=0) #delete 'season' and append onehot
	tem = [0 for f in range(0, 6)]
	tem.insert(int(temp[5])-1, 1)
	temp = np.hstack((temp, tem))
	temp = np.delete(temp, 5, axis=0) #delete 'weekday' and append onehot
	writer.writerow(temp)
	j += 1