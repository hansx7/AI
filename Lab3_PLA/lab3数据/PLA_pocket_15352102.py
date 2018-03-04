import csv
import string

train_set = csv.reader(open('train.csv'))
ts = [[] for i in range(0,10000)]
label = []
i = 0
for row in train_set:
	ts[i].append(1)  #给每一个文本首部插入1
	for j in range(0,len(row)):
		ts[i].append(string.atof(row[j])) #读入是string要转成数字
	i+=1  #文本个数加一
	label.append(string.atoi(row[len(row)-1]))  #记录标签


w=[]
w_best=w
col=len(ts[0])-1
num=i
for i in range(0,col):
	w.append(0)
min_false=num
iteration = 10000
i=1
while i<=iteration:
	for j in range(0,num):
		wsum=0
		for k in range(0,col):
			wsum += w[k]*ts[j][k]
		if wsum>=0:
			wsum=1
		else:
			wsum=-1
		if wsum != label[j]:
			pos=j
			break
	for k in range(0,col):
		w[k]=w[k]+label[pos]*ts[pos][k]
	i+=1
	num_false=0 #统计当前w不能满足的文本个数
	for j in range(0,num): #遍历一遍文本
		wsum=0
		for k in range(0,col): #计算
			wsum+=w[k]*ts[j][k]
		if wsum>=0: #分类
			wsum=1
		else:
			wsum=-1
		if wsum!=label[j]: #如果不满足
			num_false+=1   #就记下来
	if num_false<min_false: #新的w更优
		min_false=num_false
		w_best=w  #更新错误记录和w_best
	if num_false==0: #如果已经全满足
		break  #就必须跳出因为不可能再更新了


val_set = csv.reader(open('val.csv'))
vs = [[] for i in range(0,10000)]
label = []
i=0
for row in val_set:
	vs[i].append(1)
	for j in range(0,len(row)):
		vs[i].append(string.atof(row[j]))
	i+=1
	label.append(string.atoi(row[len(row)-1]))
col=len(vs[0])-1
num=i
tp=0
fp=0
tn=0
fn=0
for i in range(0,num):
	wsum=0
	for j in range(0,col):
		wsum+=w[j]*vs[i][j]
	if wsum>=0:
		wsum=1
	else:
		wsum=-1
	if wsum!=label[i]:
		if label[i]==1:
			fn+=1
		else:
			fp+=1
	else:
		if label[i]==1:
			tp+=1
		else:
			tn+=1
print tp, tn, fp, fn
accuracy=(tp+tn)*1.0/(tp+tn+fp+fn)
recall=tp*1.0/(tp+fn)
precision=tp*1.0/(tp+fp)
f1=2*precision*recall/(precision+recall)
print "accuracy=", accuracy
print "recall=", recall
print "precision=", precision
print "f1=", f1

res2=file('res2.csv','wb')
writer=csv.writer(res2)
test_set = csv.reader(open('test.csv'))
ts = [[] for i in range(0,10000)]
label = []
i=0
for row in test_set:
	ts[i].append(1)
	for j in range(0,len(row)):
		if row[j]=='?':
			break
		ts[i].append(string.atof(row[j]))
	i+=1
col=len(ts[0])
num=i
for i in range(0,num):
	wsum=0
	for j in range(0,col):
		wsum+=w[j]*ts[i][j]
	if wsum>=0:
		wsum=1
	else:
		wsum=-1
	writer.writerow([wsum])