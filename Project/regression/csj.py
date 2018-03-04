import csv
import string

target2 = csv.reader(open('answer.csv'))
ans = []
for i in target2:
	ans.append(string.atoi(i[0]))
print ans