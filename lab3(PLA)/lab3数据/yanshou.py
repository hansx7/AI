import csv
import string

train_set = csv.reader(open('thur78train.csv'))
ts = [[] for i in range(0,10000)]
label = []
i = 0
for row in train_set:
	ts[i].append(1) 
	for j in range(0,len(row)):
		ts[i].append(string.atof(row[j]))
	i+=1  
	label.append(string.atoi(row[len(row)-1]))
	# print ts[i-1],label[i-1]


w=[]
col=len(ts[0])-1 
num=i
for i in range(0,col):
	w.append(1)

iteration=10000 
i=1
while i<=iteration:
	flag=1
	for j in range(0,num): 
		wsum=0
		for k in range(0,col):
			wsum += w[k]*ts[j][k] 
		if wsum>=0: 
			wsum=1
		else:
			wsum=-1
		if wsum != label[j]:
			flag=0
			for k in range(0,col):
				w[k]=w[k]+label[j]*ts[j][k]
			i+=1 
	if flag == 1:  
		break;    

# val_set = csv.reader(open('val.csv'))
# vs = [[] for i in range(0,10000)]
# label = []
# i=0
# for row in val_set:
# 	vs[i].append(1)
# 	for j in range(0,len(row)):
# 		vs[i].append(string.atof(row[j]))
# 	i+=1
# 	label.append(string.atoi(row[len(row)-1]))
# col=len(vs[0])-1
# num=i
# tp=0 #true positive
# fp=0 #false positive
# tn=0 #true negative
# fn=0 #false negative
# for i in range(0,num):
# 	wsum=0
# 	for j in range(0,col):
# 		wsum+=w[j]*vs[i][j]
# 	if wsum>=0:
# 		wsum=1
# 	else:
# 		wsum=-1
# 	if wsum!=label[i]:
# 		if label[i]==1:
# 			fn+=1
# 		else:
# 			fp+=1
# 	else:
# 		if label[i]==1:
# 			tp+=1
# 		else:
# 			tn+=1
# print tp, tn, fp, fn
# accuracy=(tp+tn)*1.0/(tp+tn+fp+fn)
# recall=tp*1.0/(tp+fn)
# precision=tp*1.0/(tp+fp)
# f1=2*precision*recall/(precision+recall)
# print "accuracy=", accuracy
# print "recall=", recall
# print "precision=", precision
# print "f1=", f1

res1=file('res.csv','wb')
writer=csv.writer(res1)
test_set = csv.reader(open('thur78test.csv'))
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
writer.writerow(w)